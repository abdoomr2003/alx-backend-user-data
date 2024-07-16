#!/usr/bin/env python3
"""
Auth module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Takes in password string argument
    Returns bytes (salted_hashed)
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())