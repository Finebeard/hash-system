from constants import SBOX, MDS_MATRIX
from gfmath import gf_mult

def sub_bytes(state):
    # Make sure every element is in 0–255 range
    return [SBOX[b & 0xFF] for b in state]

def shift_columns(state):
    matrix = [state[i*8:(i+1)*8] for i in range(8)]
    for r in range(8):
        matrix[r] = matrix[r][r:] + matrix[r][:r]
    return [b for row in matrix for b in row]

def mix_rows(state):
    matrix = [state[i*8:(i+1)*8] for i in range(8)]
    new_matrix = []
    for r in range(8):
        new_row = []
        for c in range(8):
            val = 0
            for k in range(8):
                val ^= gf_mult(MDS_MATRIX[r][k], matrix[k][c]) & 0xFF
            new_row.append(val)
        new_matrix.append(new_row)
    return [b for row in new_matrix for b in row]

def add_round_key(state, round_key):
    return [(s ^ k) & 0xFF for s, k in zip(state, round_key)]
