import sqlite3
import pandas as pd
from pathlib import Path


# ==========================================================
# DATABASE CONFIG
# ==========================================================

DATABASE_DIR = Path("database")

DATABASE_DIR.mkdir(
    exist_ok=True
)

DATABASE_PATH = DATABASE_DIR / "shopee_food.db"

TABLE_NAME = "transaksi"


# ==========================================================
# CREATE DATABASE
# ==========================================================

def create_database():
    """
    Membuat database jika belum tersedia.
    """

    conn = sqlite3.connect(
        DATABASE_PATH
    )

    conn.close()
  # ==========================================================
# REPLACE ALL DATA
# ==========================================================

def replace_all_data(df: pd.DataFrame):
    """
    Menghapus seluruh data lama kemudian
    menyimpan dataset baru.
    """

    create_database()

    conn = sqlite3.connect(
        DATABASE_PATH
    )

    try:

        df.to_sql(

            TABLE_NAME,

            conn,

            if_exists="replace",

            index=False

        )

        conn.commit()

    finally:

        conn.close()


# ==========================================================
# GET ALL DATA
# ==========================================================

def get_all_data() -> pd.DataFrame:
    """
    Mengambil seluruh dataset dari database.
    """

    create_database()

    conn = sqlite3.connect(
        DATABASE_PATH
    )

    try:

        cursor = conn.cursor()

        cursor.execute(
            f"""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            AND name='{TABLE_NAME}'
            """
        )

        table_exists = cursor.fetchone()

        if table_exists is None:

            return pd.DataFrame()

        return pd.read_sql(

            f"SELECT * FROM {TABLE_NAME}",

            conn

        )

    finally:

        conn.close()
      # ==========================================================
# DELETE ALL DATA
# ==========================================================

def delete_all_data():
    """
    Menghapus seluruh data pada database.
    """

    create_database()

    conn = sqlite3.connect(
        DATABASE_PATH
    )

    try:

        cursor = conn.cursor()

        cursor.execute(
            f"DROP TABLE IF EXISTS {TABLE_NAME}"
        )

        conn.commit()

    finally:

        conn.close()


# ==========================================================
# GET TOTAL DATA
# ==========================================================

def get_total_data() -> int:
    """
    Mengembalikan jumlah seluruh data.
    """

    df = get_all_data()

    return len(df)


# ==========================================================
# CHECK DATABASE
# ==========================================================

def is_database_empty() -> bool:
    """
    Mengecek apakah database kosong.
    """

    return get_total_data() == 0


# ==========================================================
# GET COLUMNS
# ==========================================================

def get_columns():
    """
    Mengembalikan daftar nama kolom dataset.
    """

    df = get_all_data()

    if df.empty:

        return []

    return list(df.columns)
