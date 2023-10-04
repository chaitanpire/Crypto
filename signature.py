import sys
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

def generate_key_and_signature(file_name):
    # Read the content of the file
    with open(file_name, 'rb') as file:
        file_data = file.read()

    # Calculate the SHA-256 hash of the file
    sha256_hash = hashes.Hash(hashes.SHA256())
    sha256_hash.update(file_data)
    hash_digest = sha256_hash.finalize()

    # Generate a random semiprime N for RSA
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()

    # Sign the hash using RSA digital signature
    signature = private_key.sign(
        hash_digest,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # Serialize public key
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return (public_key_pem, signature)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sign.py <file_name>")
        sys.exit(1)

    file_name = sys.argv[1]

    if not os.path.isfile(file_name):
        print(f"File '{file_name}' does not exist.")
        sys.exit(1)

    public_key, signature = generate_key_and_signature(file_name)
    print("Public Key (N, e):")
    print(public_key.decode())
    print("Signature (in hex):")
    print(signature.hex())
