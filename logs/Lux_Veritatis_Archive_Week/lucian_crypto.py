
# lucian_crypto.py
# 🔐 Lucian Sigil Encryption Utilities (Symmetric)

from cryptography.fernet import Fernet
import base64
import hashlib

def get_cipher(passphrase: str):
    key = hashlib.sha256(passphrase.encode()).digest()
    fernet_key = base64.urlsafe_b64encode(key)
    return Fernet(fernet_key)

def encrypt_sigil(sigil: str, passphrase: str) -> str:
    cipher = get_cipher(passphrase)
    return cipher.encrypt(sigil.encode()).decode()

def decrypt_sigil(token: str, passphrase: str) -> str:
    cipher = get_cipher(passphrase)
    return cipher.decrypt(token.encode()).decode()
