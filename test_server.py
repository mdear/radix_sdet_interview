""" Test the supplied Merkle-based file server. """
import logging
import unittest
import requests
from os import environ
from shlex import split
from pathlib import Path
from time import sleep
from base64 import b64decode
from random import randrange
from unittest import TestCase
from multiprocessing import Process
from subprocess import Popen, PIPE,STDOUT
from logging.handlers import RotatingFileHandler

from radix_merkle_file_server_test import validate_merkle_proof


SVR_PATH = Path(environ.get('MERKLE_FILE_SERVER_ROOT',
    '/mnt/c/Users/smdea/wsl/venv/radix_test/files/radix-merkle-file-server-sdet-challenge'))
LOG_DIR = environ.get('MERKLE_FILE_SERVER_LOGS', '/tmp')
LOGFILE_BASE_NAME = 'merkle_server_console'
TARGET_FILE_NAME = str(SVR_PATH / 'icons_rgb_circle.png')
SVR_INVOCATION_CMD = 'java -jar {svr} {tgt}'.format(
    svr = str(SVR_PATH / 'merkle-tree-java.jar'),
    tgt = TARGET_FILE_NAME)
SVR_HOSTNAME = 'localhost'
SVR_PORT = 8080
HASHES_SVR_REST_API_PATH = f'http://{SVR_HOSTNAME}:{SVR_PORT}/hashes'
PIECES_SVR_REST_API_PATH = r'http://{SVR_HOSTNAME}:{SVR_PORT}/piece/{root_hash_id}/{piece_id}'
AFTER_FILE_PAD_VALUE = bytes(chr(0), encoding='utf-8')

class TestMerkleServer(TestCase):
    """ Test the supplied Merkle-based file server. """
    @staticmethod
    def setUpLogging():
        file_num=randrange(0, pow(10,10))
        logging.basicConfig(
            level=logging.DEBUG,
            handlers=[
                RotatingFileHandler(filename=Path(LOG_DIR) / (LOGFILE_BASE_NAME+f'_{file_num}.log'),
                    maxBytes=10*1024, backupCount=10)
            ])

    @classmethod
    def setUpClass(cls):
        cls.server = Popen(args=split(SVR_INVOCATION_CMD), stdin=None, stdout=PIPE, stderr=STDOUT)
        cls.output_logger = Process(target=cls.log_subprocess_output)
        cls.output_logger.start()
        svr_ready = False
        while not svr_ready:
            try:
                requests.get(HASHES_SVR_REST_API_PATH)
                svr_ready = True
            except Exception as e:
                sleep(1)


    @classmethod
    def log_subprocess_output(cls):
        '''  Pull output from the server pipe and redirect to logging file output.
        '''
        cls.setUpLogging()
        for line in iter(cls.server.stdout.readline, b''):
            logging.info(line)

    @classmethod
    def tearDownClass(cls):
        cls.server.terminate()
        cls.output_logger.terminate()

    def test_retrieve_and_validate_one_piece(self):
        '''Retrieve and validate one piece of a single served file.
        Also induce and test validation failure. '''

        hashes_response = requests.get(HASHES_SVR_REST_API_PATH).json()[0]
        root_hash = hashes_response.get('hash')
        num_file_pieces = hashes_response.get('pieces')
        piece_to_get = 8

        piece_response = requests.get(PIECES_SVR_REST_API_PATH.format(
            SVR_HOSTNAME=SVR_HOSTNAME,
            SVR_PORT=SVR_PORT,
            root_hash_id = root_hash,
            piece_id = piece_to_get)).json()
        content = piece_response.get('content')
        proof = piece_response.get('proof')

        validate_merkle_proof(
            known_root_hash = root_hash,
            num_file_pieces = num_file_pieces,
            piece_index = piece_to_get,
            piece_contents = content,
            proof = proof)
        
        proof[0] += 'ff'
        expected_assert_text = """Calculated hash 
     1bb5dc7df2923f8ab9a4bf19dbe47de4434df95cd86c4255d624a90b9d4da106 
does not match expected hash 
     9b39e1edb4858f7a3424d5a3d0c4579332640e58e101c29f99314a12329fc60b"""

        with self.assertRaisesRegex(ValueError, expected_assert_text):
            validate_merkle_proof(
                known_root_hash = root_hash,
                num_file_pieces = num_file_pieces,
                piece_index = piece_to_get,
                piece_contents = content,
                proof = proof)
        

    def test_retrieve_and_validate_all_pieces(self):
        '''Retrieve and validate all pieces of a single served file.
        Also, validate that the final reassembled file is identical to the served file.'''

        hashes_response = requests.get(HASHES_SVR_REST_API_PATH).json()[0]
        root_hash = hashes_response.get('hash')
        num_file_pieces = hashes_response.get('pieces')
        file_contents = b''
        for piece_to_get in range(num_file_pieces):
            piece_response = requests.get(PIECES_SVR_REST_API_PATH.format(
                SVR_HOSTNAME=SVR_HOSTNAME,
                SVR_PORT=SVR_PORT,
                root_hash_id = root_hash,
                piece_id = piece_to_get)).json()
            content = piece_response.get('content')
            proof = piece_response.get('proof')
            file_contents += b64decode(content)

            validate_merkle_proof(
                known_root_hash = root_hash,
                num_file_pieces = num_file_pieces,
                piece_index = piece_to_get,
                piece_contents = content,
                proof = proof)

        file_contents = file_contents.rstrip(AFTER_FILE_PAD_VALUE)
        with open (TARGET_FILE_NAME, 'rb') as target_file:
            target_file_contents = target_file.read()
            with open (TARGET_FILE_NAME+'_reconstituted', 'wb') as reconstituted_file:
                reconstituted_file.write(file_contents)
            self.assertEqual(target_file_contents, file_contents, 
                "original and reconstructed file content unexpectedly differ.")



# This phrase allows the file to be executed directly
# rather than only imported as a module.
if __name__ == "__main__":
   unittest.main() 