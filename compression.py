from transformations import sub_bytes, shift_columns, mix_rows, add_round_key
from key_schedule import key_schedule

def to_bytes_list(x, size=64):
    if isinstance(x, int):
        return [(x >> (8 * i)) & 0xFF for i in reversed(range(size))]
    elif isinstance(x, (bytes, bytearray)):
        return list(x[:size])
    else:
        return list(x)

def whirlpool_compress(state, block):
    state = to_bytes_list(state, 64)
    block = to_bytes_list(block, 64)

    round_key = block[:]
    current_state = [s ^ b for s, b in zip(state, block)]

    for r in range(10):  # Whirlpool has 10 rounds
        current_state = sub_bytes(current_state)
        current_state = shift_columns(current_state)
        current_state = mix_rows(current_state)

        round_key = key_schedule(round_key, r)  # must also output 64 bytes
        current_state = add_round_key(current_state, round_key)

    
    return [s ^ b ^ c for s, b, c in zip(state, block, current_state)]
