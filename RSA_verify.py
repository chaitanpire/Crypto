import sys
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

def verify_signature(file_name, public_key, signature_hex):
    # Read the content of the file
    with open(file_name, 'rb') as file:
        file_data = file.read()

    # Calculate the SHA-256 hash of the file
    sha256_hash = hashes.Hash(hashes.SHA256())
    sha256_hash.update(file_data)
    hash_digest = sha256_hash.finalize()

    # Deserialize the public key
    public_key_obj = serialization.load_pem_public_key(public_key)

    # Verify the signature
    signature = bytes.fromhex(signature_hex)
    try:
        public_key_obj.verify(
            signature,
            hash_digest,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return "accept"
    except Exception:
        return "reject"

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python verifier.py <file_name> <public_key> <signature_hex>")
        sys.exit(1)

    file_name = sys.argv[1]
    public_key = sys.argv[2]
    signature_hex = sys.argv[3]

    result = verify_signature(file_name, public_key.encode(), signature_hex)
    print(result)
