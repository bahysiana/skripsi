import re
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


# ==========================================================
# DATA CLEANING
# ==========================================================

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Membersihkan dataset.
    """

    df = df.copy()

    # Menghapus spasi pada nama kolom
    df.columns = df.columns.str.strip()

    # Menghapus data duplikat
    df = df.drop_duplicates()

    # Menghapus data kosong
    df = df.dropna()

    return df


# ==========================================================
# HITUNG JUMLAH JENIS MENU
# ==========================================================

def count_menu_types(menu) -> int:
    """
    Menghitung jumlah jenis menu yang dibeli.
    """

    if pd.isna(menu):
        return 0

    menu_list = [

        item.strip()

        for item in str(menu).split(",")

        if item.strip()

    ]

    return len(menu_list)


# ==========================================================
# KONVERSI WAKTU
# ==========================================================

def convert_minutes(value):
    """
    Mengubah teks:
    '13 menit' -> 13
    """

    if pd.isna(value):
        return None

    angka = re.findall(r"\d+", str(value))

    if len(angka) == 0:
        return None

    return int(angka[0])


# ==========================================================
# FEATURE ENGINEERING
# ==========================================================

def feature_engineering(df: pd.DataFrame):
    """
    Feature engineering.
    """

    df = df.copy()

    # Jumlah jenis menu

    df["Jumlah_jenis_menu"] = df["menu_yang_dibeli"].apply(
        count_menu_types
    )

    # Konversi waktu persiapan

    df["waktu_persiapan_yang_diberikan"] = (
        df["waktu_persiapan_yang_diberikan"]
        .apply(convert_minutes)
    )

    df["waktu_persiapan_digunakan"] = (
        df["waktu_persiapan_digunakan"]
        .apply(convert_minutes)
    )

    return df


# ==========================================================
# VARIABEL PENELITIAN
# ==========================================================

FEATURE_COLUMNS = [

    "Total_harga",

    "Jumlah_pesanan",

    "Jumlah_jenis_menu",

    "waktu_persiapan_yang_diberikan",

    "waktu_persiapan_digunakan"

]


# ==========================================================
# SELECT FEATURE
# ==========================================================

def select_features(df: pd.DataFrame):

    kolom_hilang = [

        col

        for col in FEATURE_COLUMNS

        if col not in df.columns

    ]

    if kolom_hilang:

        raise ValueError(

            "Kolom berikut tidak ditemukan:\n\n"

            + "\n".join(kolom_hilang)

        )

    feature_df = df[FEATURE_COLUMNS].copy()

    return feature_df


# ==========================================================
# MIN MAX NORMALIZATION
# ==========================================================

def minmax_normalization(df: pd.DataFrame):

    numeric_df = df.copy()

    # Pastikan seluruh kolom numerik

    for col in numeric_df.columns:

        numeric_df[col] = pd.to_numeric(

            numeric_df[col],

            errors="coerce"

        )

    # Cek apakah ada nilai kosong

    if numeric_df.isnull().sum().sum() > 0:

        raise ValueError(
            "Masih terdapat data yang bukan numerik pada variabel penelitian."
        )

    scaler = MinMaxScaler()

    normalized = scaler.fit_transform(
        numeric_df
    )

    normalized_df = pd.DataFrame(

        normalized,

        columns=numeric_df.columns,

        index=numeric_df.index

    )

    return normalized_df


# ==========================================================
# PREPROCESS DATASET
# ==========================================================

def preprocess_dataset(df: pd.DataFrame):
    """
    Pipeline preprocessing.

    1. Data Cleaning
    2. Feature Engineering
    3. Select Feature
    4. Min-Max Normalization
    """

    # Cleaning

    cleaned_df = clean_data(df)

    # Feature Engineering

    engineered_df = feature_engineering(
        cleaned_df
    )

    # Variabel Penelitian

    feature_df = select_features(
        engineered_df
    )

    # Normalisasi

    normalized_df = minmax_normalization(
        feature_df
    )

    return (

        engineered_df,

        feature_df,

        normalized_df

    )
