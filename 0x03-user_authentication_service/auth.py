#!/usr/bin/env python3
"""
auth module
"""
from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> str:
    """Hash a password

    Args:
        password (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    return hashpw(password.encode(), gensalt())
