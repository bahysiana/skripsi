import sqlite3
import hashlib

from utils.database import DATABASE_PATH


# ==========================================================
# HASH PASSWORD
# ==========================================================

def hash_password(password: str) -> str:
    """
    Mengubah password menjadi SHA-256.
    """

    return hashlib.sha256(
        password.encode()
    ).hexdigest()
