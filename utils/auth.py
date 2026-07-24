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

# ==========================================================
# CREATE USERS TABLE
# ==========================================================

def create_users_table():
    """
    Membuat tabel users jika belum tersedia.
    """

    conn = sqlite3.connect(DATABASE_PATH)

    try:

        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                username TEXT UNIQUE NOT NULL,

                password TEXT NOT NULL

            )
        """)

        conn.commit()

    finally:

        conn.close()

# ==========================================================
# CREATE DEFAULT ADMIN
# ==========================================================

def create_default_admin():
    """
    Membuat akun admin default jika belum tersedia.
    """

    create_users_table()

    conn = sqlite3.connect(DATABASE_PATH)

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE username = ?
            """,
            ("admin",)
        )

        user = cursor.fetchone()

        if user is None:

            cursor.execute(
                """
                INSERT INTO users
                (username, password)
                VALUES (?, ?)
                """,
                (
                    "admin",
                    hash_password("admin123")
                )
            )

            conn.commit()

    finally:

        conn.close()

# ==========================================================
# VERIFY LOGIN
# ==========================================================

def verify_login(username: str, password: str) -> bool:
    """
    Memverifikasi username dan password admin.
    """

    create_default_admin()

    conn = sqlite3.connect(DATABASE_PATH)

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT password
            FROM users
            WHERE username = ?
            """,
            (username,)
        )

        result = cursor.fetchone()

        if result is None:

            return False

        stored_password = result[0]

        return stored_password == hash_password(password)

    finally:

        conn.close()

# ==========================================================
# INITIALIZE AUTH
# ==========================================================

def initialize_auth():
    """
   Inisialisasi sistem autentikasi.
    """

    create_default_admin()
