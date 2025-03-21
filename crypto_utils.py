import hashlib
from Crypto.Cipher import AES
import base64
import os

# Generate a fixed 256-bit encryption key using SHA-256
password = "SuperSecretPassword"  # Change this for better security
KEY = hashlib.sha256(password.encode()).digest()  # 32-byte AES key

def encrypt_file(file_data):
    """Encrypts file data using AES-256."""
    cipher = AES.new(KEY, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(file_data)
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

def decrypt_file(encrypted_data):
    """Decrypts file data using AES-256."""
    data = base64.b64decode(encrypted_data)
    nonce, tag, ciphertext = data[:16], data[16:32], data[32:]
    cipher = AES.new(KEY, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)
