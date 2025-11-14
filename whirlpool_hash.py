import whirlpool

def generate_whirlpool_hash(input_string):
    # Create a new Whirlpool hash object
    hash_object = whirlpool.new(input_string.encode('utf-8'))
    
    hash_value = hash_object.hexdigest()
    return hash_value


input_data = "Hello, World!"
hash_value = generate_whirlpool_hash(input_data)
print(f"Whirlpool Hash: {hash_value}")