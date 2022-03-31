"""Hashing algorithm is implemented here"""
import secrets
import string

from argon2 import PasswordHasher

ph = PasswordHasher()


def generate_crypto_safe_password():
    """Generates Crypto safe password"""

    alphabet = string.ascii_letters + string.digits + str("!@#$&")
    password = "".join(secrets.choice(alphabet) for i in range(15))

    return password
