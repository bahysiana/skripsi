import re
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


# ==========================================================
# DATA CLEANING
# ==========================================================

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Membersihkan dataset transaksi.
    """

    df = df.copy()

    # ------------------------------------------------------
    # Menghapus spasi pada nama kolom
    # ------------------------------------------------------

    df.columns = df.columns.str.strip()

    # ------------------------------------------------------
    # Menghapus duplikat
    # ------------------------------------------------------

    df = df.drop_duplicates()

    # ------------------------------------------------------
    # Menghapus baris yang seluruh isinya kosong
    # ------------------------------------------------------

    df = df.dropna(how="all")

    return df


# ==========================================================
# HITUNG JUMLAH JENIS MENU
# ==========================================================

def count_menu_types(menu) -> int:
    """
    Menghitung jumlah jenis menu berdasarkan
    kolom menu_yang_dibeli.
    """

    if pd.isna(menu):

        return 0

    menu = str(menu).strip()

    if menu == "":

        return 0

    daftar_menu = [

        item.strip()

        for item in menu.split(",")

        if item.strip()

    ]

    return len(daftar_menu)


# ==========================================================
# KONVERSI WAKTU
# ==========================================================

def convert_minutes(value):
    """
    Contoh:

    13 menit -> 13

    8 menit -> 8

    - -> None
    """

    if pd.isna(value):

        return None

    text = str(value).strip().lower()

    # -------------------------------
    # Nilai kosong
    # -------------------------------

    if text in [

        "",

        "-",

        "--",

        "nan",

        "none"

    ]:

        return None

    angka = re.findall(r"\d+", text)

    if len(angka) == 0:

        return None

    return int(angka[0])


# ==========================================================
# KONVERSI ANGKA
# ==========================================================

def convert_numeric(value):
    """
    Mengubah berbagai format angka menjadi integer.

    Contoh:

    Rp30.000 -> 30000

    30.000 -> 30000

    30000 -> 30000
    """

    if pd.isna(value):

        return None

    text = str(value).strip()

    if text in [

        "",

        "-",

        "--",

        "nan",

        "None"

    ]:

        return None

    text = text.replace("Rp", "")

    text = text.replace("rp", "")

    text = text.replace(".", "")

    text = text.replace(",", "")

    text = text.replace(" ", "")

    angka = re.findall(r"\d+", text)

    if len(angka) == 0:

        return None

    return int("".join(angka))
    # ==========================================================
# FEATURE ENGINEERING
# ==========================================================

def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Menambahkan variabel penelitian yang dibutuhkan.
    """

    df = df.copy()

    # ======================================================
    # JUMLAH JENIS MENU
    # ======================================================

    df["Jumlah_jenis_menu"] = (
        df["menu_yang_dibeli"]
        .apply(count_menu_types)
    )

    # ======================================================
    # TOTAL HARGA
    # ======================================================

    df["Total_harga"] = (
        df["Total_harga"]
        .apply(convert_numeric)
    )

    # ======================================================
    # JUMLAH PESANAN
    # ======================================================

    df["Jumlah_pesanan"] = (
        df["Jumlah_pesanan"]
        .apply(convert_numeric)
    )

    # ======================================================
    # WAKTU YANG DIBERIKAN
    # ======================================================

    df["waktu_persiapan_yang_diberikan"] = (
        df["waktu_persiapan_yang_diberikan"]
        .apply(convert_minutes)
    )

    # ======================================================
    # WAKTU DIGUNAKAN
    # ======================================================

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

def select_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Mengambil variabel penelitian.
    """

    df = df.copy()

    # ======================================================
    # VALIDASI KOLOM
    # ======================================================

    kolom_hilang = [

        col

        for col in FEATURE_COLUMNS

        if col not in df.columns

    ]

    if len(kolom_hilang) > 0:

        raise ValueError(

            "Kolom berikut tidak ditemukan:\n\n"

            + "\n".join(kolom_hilang)

        )

    feature_df = df[FEATURE_COLUMNS].copy()

    # ======================================================
    # HAPUS BARIS TIDAK VALID
    # ======================================================

    feature_df = feature_df.dropna()

    # ======================================================
    # RESET INDEX
    # ======================================================

    feature_df = feature_df.reset_index(drop=True)

    return feature_df
    # ==========================================================
# MIN MAX NORMALIZATION
# ==========================================================

def minmax_normalization(df: pd.DataFrame) -> pd.DataFrame:
    """
    Melakukan normalisasi menggunakan
    Min-Max Normalization.
    """

    numeric_df = df.copy()

    # ======================================================
    # PASTIKAN SELURUH DATA NUMERIK
    # ======================================================

    for col in numeric_df.columns:

        numeric_df[col] = pd.to_numeric(

            numeric_df[col],

            errors="coerce"

        )

    # ======================================================
    # HAPUS DATA YANG TIDAK VALID
    # ======================================================

    before_rows = len(numeric_df)

    numeric_df = numeric_df.dropna()

    after_rows = len(numeric_df)

    # ======================================================
    # VALIDASI
    # ======================================================

    if numeric_df.empty:

        raise ValueError(
            "Seluruh data hasil preprocessing kosong. "
            "Periksa kembali dataset yang diupload."
        )

    # ======================================================
    # INFORMASI BARIS YANG DIHAPUS
    # ======================================================

    removed_rows = before_rows - after_rows

    if removed_rows > 0:

        print(
            f"{removed_rows} baris tidak valid dihapus "
            "karena mengandung nilai kosong atau tidak numerik."
        )

    # ======================================================
    # MIN MAX SCALER
    # ======================================================

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
    Pipeline preprocessing lengkap.

    Tahapan:
    1. Data Cleaning
    2. Feature Engineering
    3. Pemilihan Variabel
    4. Min-Max Normalization

    Returns
    -------
    original_df
        Dataset setelah cleaning dan feature engineering.

    feature_df
        Dataset variabel penelitian.

    normalized_df
        Dataset hasil normalisasi Min-Max.
    """

    # ======================================================
    # DATA CLEANING
    # ======================================================

    cleaned_df = clean_data(df)

    # ======================================================
    # FEATURE ENGINEERING
    # ======================================================

    engineered_df = feature_engineering(cleaned_df)

    # ======================================================
    # VARIABEL PENELITIAN
    # ======================================================

    feature_df = select_features(engineered_df)

    # ======================================================
    # NORMALISASI
    # ======================================================

    normalized_df = minmax_normalization(feature_df)

    # ======================================================
    # SAMAKAN INDEX
    # ======================================================

    feature_df = feature_df.loc[
        normalized_df.index
    ].reset_index(drop=True)

    engineered_df = engineered_df.loc[
        normalized_df.index
    ].reset_index(drop=True)

    normalized_df = normalized_df.reset_index(drop=True)

    # ======================================================
    # RETURN
    # ======================================================

    return (
        engineered_df,
        feature_df,
        normalized_df
    )
