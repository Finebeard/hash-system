from whirlpool import whirlpool_hash

if __name__ == "__main__":
    msg = b"I AM"
    digest = whirlpool_hash(msg)
    print("Whirlpool digest:", digest.hex())
