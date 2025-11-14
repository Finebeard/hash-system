def gf_mult(a, b):
    """Multiply two numbers in GF(2^8)."""
    result = 0
    for _ in range(8):
        if b & 1:
            result ^= a
        high_bit = a & 0x80
        a = (a << 1) & 0xFF
        if high_bit:
            a ^= 0x11D  # irreducible polynomial
        b >>= 1
    return result
