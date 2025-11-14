from compression import whirlpool_compress
from constants import STATE_SIZE

def pad_message(message_bytes: bytes) -> bytes:
    
    bit_length = len(message_bytes) * 8
    padded = message_bytes + b'\x80'
    while (len(padded) + 32) % 64 != 0:
        padded += b'\x00'
    padded += bit_length.to_bytes(32, byteorder="big")
    return padded

def whirlpool_hash(message: bytes) -> bytes:
    
    padded = pad_message(message)
    state = [0] * STATE_SIZE

    for i in range(0, len(padded), 64):
        block = list(padded[i:i+64])
        state = whirlpool_compress(state, block)

    return bytes(state)
