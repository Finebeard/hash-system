from whirlpool import whirlpool_hash

def run_tests():
    tests = {
        b"": "19FA61D75522A4669B44E39C1D2E1726... (full hex)",
        b"a": "4E2448A4C6F486BB16B6562C73B4020B... (full hex)",
        b"abc": "4E2448A4C6F486BB16B6562C73B4020B... (full hex)",
    }

    for msg, expected in tests.items():
        digest = whirlpool_hash(msg).hex().upper()
        print(f"Input: {msg} → {digest[:20]}...")
        assert digest.startswith(expected[:20]), "Test failed!"

if __name__ == "__main__":
    run_tests()
