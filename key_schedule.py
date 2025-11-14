from constants import ROUND_CONSTANTS, SBOX, MDS_MATRIX
from gfmath import gf_mult


def sub_bytes_key(key: list[int]) -> list[int]:
    """Apply S-box substitution to all 64 bytes of the key."""
    return [SBOX[b] for b in key]


def shift_columns_key(key: list[int]) -> list[int]:
    """Cyclically shift row r left by r positions (8×8 matrix view)."""
    matrix = [key[i * 8:(i + 1) * 8] for i in range(8)]
    for r in range(8):
        matrix[r] = matrix[r][r:] + matrix[r][:r]
    return [b for row in matrix for b in row]


def mix_rows_key(key: list[int]) -> list[int]:
    """Mix rows using Whirlpool’s MDS matrix multiplication in GF(2^8)."""
    matrix = [key[i * 8:(i + 1) * 8] for i in range(8)]
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


def key_schedule(prev_key: list[int], round_idx: int) -> list[int]:
    """
    Whirlpool key schedule.
    Produces the round key for round `round_idx` from `prev_key`.
    """
    # 1. SubBytes
    new_key = sub_bytes_key(prev_key)

    # 2. ShiftColumns
    new_key = shift_columns_key(new_key)

    # 3. MixRows
    new_key = mix_rows_key(new_key)

    # 4. Add round constant (only first byte is nonzero)
    rc = ROUND_CONSTANTS[round_idx] & 0xFF
    round_const = [0] * 64
    round_const[0] = rc
    new_key = [(k ^ c) & 0xFF for k, c in zip(new_key, round_const)]

    return new_key
