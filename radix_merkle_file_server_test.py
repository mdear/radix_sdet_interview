''' Test framework to enable validation of Merkle file server. '''

# To validate hash, we need to know whether we/our parent/parent's parent is
# on a left or right branch of the Merkle tree.
# Parent hash computed by concatenating left/right children hashes.
# Algorithm : must determine by the piece number what the path is back to
# the root, either whether the parent's left or right link is traversed
# when moving up one level.
# I posit this can be calculated deterministically.
#
# NOTE: I could likely just use a library on pypi to do this, but for the
# purposes of the exercise I'll derive it.  This will add a little time to the exercise
# completion time, I'm ok with this if you are.
# Idea : first calculate how many levels deep the tree must be
# Then derive path from root to that particular leaf node

# 0-based piece number, on leaf (bottom) row of tree, increments from l->r with
# 0 being leftmost piece.
# Parent's left link connects to an even numbered child.
# Parent's right link connects to an odd numbered child.

# PLO = 0-based leaf row offset of piece
# PPO = 0-based offset of a parent node in the parent row = PLO/2
# N = Total number of pieces
# LR = 0-based row number of the leaves = ceil(log2(N))
# LN = number of nodes in leaf row = pow(2, LR)

from copy import copy
from hashlib import sha256
from base64 import b64decode
from math import ceil, floor, pow, log2

def leaf_to_root_path (num_pieces, piece_index):
    ''' Get path from Merkle tree leaf node to root.
    Assuming a node can only have at most two children (binary tree)

    Parameters
    ----------
    num_pieces : int
        The number of 1KB pieces in the file

    piece_index : int
        The 0-based offset of the piece in the file represented on the leaf
        row of the Merkle tree.

    Returns
    -------
    A list showing the path from leaf to root.
    True means traversal via the parent's left link.
    False means traversal via the parent's left link.
    '''
    current_row = ceil(log2(num_pieces))
    current_index = piece_index

    root_path_is_left = []
    while current_row > 0:
        root_path_is_left.append(True if (current_index % 2) == 0 else False)
        current_row -= 1

        # Move up to the next row closer to the root
        # and compute the parent's row index
        current_index = floor(current_index/2)
    return root_path_is_left


def validate_merkle_proof(known_root_hash, num_file_pieces, piece_index,
        piece_contents, proof):
    ''' Validate that the proof matches the known root hash.

    Parameters
    ----------
    known_root_hash : 64-character hex string
        Known correct Merkle root hash

    num_file_pieces : int
        1-based number of file pieces

    piece_contents : base64 encoded string
        Contents of a file piece

    proof : List of 64-character hex strings
        List of hashes needed to compute a Merkle root hash.

    Raises
    ------
    ValueError : if the proof does not match the known root hash
    '''

    proof = copy(proof)
    path_to_root = leaf_to_root_path (
        num_pieces=num_file_pieces, piece_index=piece_index)

    current_hash = sha256(b64decode(piece_contents))

    while proof and path_to_root:
        is_left = path_to_root.pop(0)
        popped_proof = proof.pop(0)
        if is_left:
            current_hash = sha256(
                current_hash.digest() + bytes.fromhex(popped_proof))
        else:
            current_hash = sha256(
                bytes.fromhex(popped_proof) + current_hash.digest())


    if current_hash.hexdigest() != known_root_hash:
        raise ValueError(f'Calculated hash \n     {current_hash.hexdigest()} '
        f'\ndoes not match expected hash \n     {known_root_hash}')
