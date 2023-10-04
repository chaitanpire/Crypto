import hashlib

def sha256_hash(filename):
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as file:
        while True:
            data = file.read(65536)
            if not data:
                break
            sha256.update(data)
    return sha256.digest()

def modular_exponentiation(base, exponent, mod):
    result = 1
    base %= mod
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % mod
        exponent //= 2
        base = (base * base) % mod
    return result

def verify_signature(filename, N, e, signature_hex):
    # Step 1: Get SHA-256 hash of the file (as bytes)
    hashed_data = int.from_bytes(sha256_hash(filename), 'big')

    # Step 2: Convert the hexadecimal signature to an integer
    signature = int(signature_hex, 16)

    # Step 3: Verify the signature using RSA verification
    verified_signature = modular_exponentiation(signature, e, N)
    expected_hash = hashed_data

    # Step 4: Return accept if the signature is valid, reject otherwise
    if verified_signature == expected_hash:
        return "accept"
    else:
        return "reject"

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 5:
        print("Usage: python verifier.py <filename> <N> <e> <signature_hex>")
        sys.exit(1)

    filename = sys.argv[1]
    N = int(sys.argv[2])
    e = int(sys.argv[3])
    signature_hex = sys.argv[4]

    result = verify_signature(filename, N, e, signature_hex)
    print(result)