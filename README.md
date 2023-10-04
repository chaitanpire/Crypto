For Vigenere cipher:
Run python3 vigenere.py
There will be a prompt, then enter the cipher text

For RSA signature:

Run python signature.py <file_name> to generate the digital signature and get the public key (N, e) and the signature in hex.

Run python RSA_verify.py <file_name> <public_key> <signature_hex> to verify the digital signature. It will print "accept" if the signature is valid and "reject" otherwise.
