import hashlib
import random
import sympy

def sha256_hash(filename):
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as file:
        while True:
            data = file.read(65536)
            if not data:
                break
            sha256.update(data)
    return sha256.digest()

def generate_random_semiprime(bits):
    while True:
        p = sympy.randprime(2**(bits-1), 2**bits)
        q = sympy.randprime(2**(bits-1), 2**bits)
        if p != q:
            return p , q, p*q

def modular_inverse(a, m):
    # Extended Euclidean Algorithm to compute the modular inverse of 'a' mod 'm'
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 if x1 >= 0 else x1 + m0

def sign_file(filename):
    # Step 1: Get SHA-256 hash of the file (as bytes)
    hashed_data = int.from_bytes(sha256_hash(filename), 'big')

    # Step 2: Create random semiprime N to be used in the RSA digital signature
    p, q, N = generate_random_semiprime(2048)  # You can adjust the number of bits as needed

    # Step 3: Sign the hash using RSA digital signature with N and e = 65537
    e = 65537
    d  = pow(e, -1, (p-1)*(q-1))  # Compute the private key 'd'
    d = int(d)
    N = int(N)
    print(p,q,d)
    hashed_data = int(hashed_data)
    signature = pow(hashed_data, d, N)

    return (N, e), hex(signature)[2:]

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python sign.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    key_pair, signature = sign_file(filename)
    N, e = key_pair

    print("N:", N)
    print("e:", e)
    print("Signature:", signature)
