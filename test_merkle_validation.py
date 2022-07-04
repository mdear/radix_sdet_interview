""" This module tests Merkle tree validation test infrastructure code.  """
from unittest import TestCase
from hashlib import sha256
from radix_merkle_file_server_test import leaf_to_root_path, validate_merkle_proof

class TestMerkleValidation(TestCase):
    """ Test the Merkle file server validation code. """

    def test_leaf_to_root_path(self):
        'Unit test of deriving Merkle leaf to root path'
        self.assertEqual((leaf_to_root_path (num_pieces=18, piece_index=16)),
            [True, True, True, True, False])
        self.assertEqual((leaf_to_root_path (num_pieces=18, piece_index=15)),
            [False, False, False, False, True])
        self.assertEqual((leaf_to_root_path (num_pieces=16, piece_index=10)),
            [True, False, True, False])
        self.assertEqual((leaf_to_root_path (num_pieces=1, piece_index=0)),
            [])

    def test_merkle_valid(self):
        'Unit test validating known valid merkle proof'

        proof = [
            "6a10a0b8c1bd3651cba6e5604b31df595e965be137650d296c05afc1084cfe1f", # sibling hash
            "956bf86d100b2f49a8d057ebafa85b8db89a0f19d5627a1226fea1cb3e23d3f3", # uncle hash
            "04284ddea22b003e6098e7dd1a421a565380d11530a35f2e711a8dd2b9b5e7f8", # uncle's uncle hash
            "c66a821b749e0576e54b89dbac8f71211a508f7916e3d6235900372bed6c6c22", # etc.
            "a8bd48117723dee92524c25730f9e08e5d47e78c87d17edb344d4070389d049e"  # child of root
        ]

        content = ("1wSDXYz+dPEXQP9oAYKE7Tz5ttGgCYkD3ile/OXpP4AAAPTqv+BlsRiHgknDtgQv/orRny7+AhAAgB7a"
            "+tKLxbYEp8bkJiY7bdm/L7n35ek/QN/NOQMAGYi+8c17X7AQLf8MUxOjP83+B+jzn71XLs+ZAgQZiKkxO7QCtffz27kjyYu/"
            "zP0HGAwtQJCJGA36zFtvWIgWSrWF646n/wACAFBzIfnqL7qTZGiXFC/+uvPpZ0Z/AvTfpW4AmL9yedpaQD5iKpDRoO0q/lMc/"
            "an9B2Ag5roBwDpAXuI8wLOnTlqItgSABEd/xsVf97/+xocLMCACAGQoxkkaDdqGz2m8e3YjNXc"
            "+1fsPMCDfLQ0As9YD8vLM735jNGjDpdj7Hxd/Gf0JMDAzSwOAUaCQoWdPn3QeoKHi4i"
            "+jPwGogxYgyPkPgOefK3YYDdpITyfYouXiL4CBe6AFyG3AkKl4ymw0aLPErkyK7T93P/+imL923QcMMDhagIAFMRo0Wk5ohij"
            "+Y1pTam5+OOXDBWgALUBAt9jcaTRoY6Q4oenu+S9d/"
            "AUweHNLA8C09YC8xbjJ7a93LMSARTuWi78AqMP8lcsPBACAYvuvj3VnzzM42xK8"
            "+CtGf9676KgZQFMsBoA5SwGEnSffNhp0QOJehrikLTV6/wEa4cIDAWBxOwAg2k/iUDD9t83oTwD68b/1S/"
            "71VcsBhK0vvZjkGMomi10XF38BUKO5lQKABk3gB8+89Ua3JYX+SPHpf7jj6T9AowMAwA9iNOgOrUACwEaK/08/M/oToDm"
            "+WykATFsXYKkYDRo7AdQr1Yu/tP8ANMrMSgEA4CHbXv2F0aB1B4AER3/euzhb3P/"
            "6Gx8uQHOsuAPgDACwomdPnzQatCYRrmKnJTV3PtX7D9Ak81cur7gD8J2lAVYS7SnPnjppIWqQYu9/"
            "XPxl9CdAc9kBAFYlLqhKdVLNoDz10590R66mRu8/QONcWDEAzF"
            "+5bAcAeKxnfvcbo0F76GkXfwEwAMsPAc9aEuBxYjSo8wAbF2uY4mVrdz//opi/dt0HDNAs00v/j83L/p92AViXexdniv"
            "+z76VsC7mRf/mnYuj557J4v3FgdcdbbxTX3nnPF38DUh39efPDKR8uQPM8UOMPPS4dAE8WTzu/f/NEVu95"
            "+PDLxdZDB3z4G5DieYq757908RdAM808LgDYAYB1iHnnNz86k9V73vn7t7uHWFm7CE8p7hg5/"
            "AvQWHOPCwAmAcE6RetDXH6Ui2hfifMArN22V9Mc/RmtgAA0z/yVy48NAHOWCNbv+jvvdaeg5CJGg25/"
            "veODX4OYohTrlmIABqCRHno6OfS4dACsTfQ/53Y4dvuvj3Vvs2V1thn9CQ==")

        known_root_hash = "9b39e1edb4858f7a3424d5a3d0c4579332640e58e101c29f99314a12329fc60b"
        num_file_pieces = 17
        piece_index = 8

        validate_merkle_proof(
            known_root_hash = known_root_hash,
            num_file_pieces = num_file_pieces,
            piece_index = piece_index,
            piece_contents = content,
            proof = proof)


    def test_merkle_invalid(self):
        'Unit test validating exception raised on known bad valid merkle proof (corrupt sibling hash last hex digit)'

        proof = [
            "6a10a0b8c1bd3651cba6e5604b31df595e965be137650d296c05afc1084cfe1e", # sibling hash
            "956bf86d100b2f49a8d057ebafa85b8db89a0f19d5627a1226fea1cb3e23d3f3", # uncle hash
            "04284ddea22b003e6098e7dd1a421a565380d11530a35f2e711a8dd2b9b5e7f8", # uncle's uncle hash
            "c66a821b749e0576e54b89dbac8f71211a508f7916e3d6235900372bed6c6c22", # etc.
            "a8bd48117723dee92524c25730f9e08e5d47e78c87d17edb344d4070389d049e"  # child of root
        ]

        content = ("1wSDXYz+dPEXQP9oAYKE7Tz5ttGgCYkD3ile/OXpP4AAAPTqv+BlsRiHgknDtgQv/orRny7+AhAAgB7a"
            "+tKLxbYEp8bkJiY7bdm/L7n35ek/QN/NOQMAGYi+8c17X7AQLf8MUxOjP83+B+jzn71XLs+ZAgQZiKkxO7QCtffz27kjyYu/"
            "zP0HGAwtQJCJGA36zFtvWIgWSrWF646n/wACAFBzIfnqL7qTZGiXFC/+uvPpZ0Z/AvTfpW4AmL9yedpaQD5iKpDRoO0q/lMc/"
            "an9B2Ag5roBwDpAXuI8wLOnTlqItgSABEd/xsVf97/+xocLMCACAGQoxkkaDdqGz2m8e3YjNXc"
            "+1fsPMCDfLQ0As9YD8vLM735jNGjDpdj7Hxd/Gf0JMDAzSwOAUaCQoWdPn3QeoKHi4i"
            "+jPwGogxYgyPkPgOefK3YYDdpITyfYouXiL4CBe6AFyG3AkKl4ymw0aLPErkyK7T93P/+imL923QcMMDhagIAFMRo0Wk5ohij"
            "+Y1pTam5+OOXDBWgALUBAt9jcaTRoY6Q4oenu+S9d/"
            "AUweHNLA8C09YC8xbjJ7a93LMSARTuWi78AqMP8lcsPBACAYvuvj3VnzzM42xK8"
            "+CtGf9676KgZQFMsBoA5SwGEnSffNhp0QOJehrikLTV6/wEa4cIDAWBxOwAg2k/iUDD9t83oTwD68b/1S/"
            "71VcsBhK0vvZjkGMomi10XF38BUKO5lQKABk3gB8+89Ua3JYX+SPHpf7jj6T9AowMAwA9iNOgOrUACwEaK/08/M/oToDm"
            "+WykATFsXYKkYDRo7AdQr1Yu/tP8ANMrMSgEA4CHbXv2F0aB1B4AER3/euzhb3P/"
            "6Gx8uQHOsuAPgDACwomdPnzQatCYRrmKnJTV3PtX7D9Ak81cur7gD8J2lAVYS7SnPnjppIWqQYu9/"
            "XPxl9CdAc9kBAFYlLqhKdVLNoDz10590R66mRu8/QONcWDEAzF"
            "+5bAcAeKxnfvcbo0F76GkXfwEwAMsPAc9aEuBxYjSo8wAbF2uY4mVrdz//opi/dt0HDNAs00v/j83L/p92AViXexdniv"
            "+z76VsC7mRf/mnYuj557J4v3FgdcdbbxTX3nnPF38DUh39efPDKR8uQPM8UOMPPS4dAE8WTzu/f/NEVu95"
            "+PDLxdZDB3z4G5DieYq757908RdAM808LgDYAYB1iHnnNz86k9V73vn7t7uHWFm7CE8p7hg5/"
            "AvQWHOPCwAmAcE6RetDXH6Ui2hfifMArN22V9Mc/RmtgAA0z/yVy48NAHOWCNbv+jvvdaeg5CJGg25/"
            "veODX4OYohTrlmIABqCRHno6OfS4dACsTfQ/53Y4dvuvj3Vvs2V1thn9CQ==")

        known_root_hash = "9b39e1edb4858f7a3424d5a3d0c4579332640e58e101c29f99314a12329fc60b"
        num_file_pieces = 17
        piece_index = 8

        expected_assert_text = """Calculated hash 
     fe235ab01968f8cac47ba58e9b60322dccddfa37c5b42e35f193f55fc51ee51c 
does not match expected hash 
     9b39e1edb4858f7a3424d5a3d0c4579332640e58e101c29f99314a12329fc60b"""

        with self.assertRaisesRegex(ValueError, expected_assert_text):
            validate_merkle_proof(
                known_root_hash = known_root_hash,
                num_file_pieces = num_file_pieces,
                piece_index = piece_index,
                piece_contents = content,
                proof = proof)

