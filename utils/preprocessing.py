import re
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


# ==========================================================
# MEMBERSIHKAN DATA
# ==========================================================

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Membersihkan dataset sebelum preprocessing.
    """

    df = df.copy()

    # Hilangkan spasi nama kolom
    df.columns = df.columns.str.strip()

    # Hapus duplikat
    df = df.drop_duplicates()

    # Hapus baris yang seluruhnya kosong
    df = df.dropna(how="all")

    return df


# ==========================================================
# HITUNG JUMLAH JENIS MENU
# ==========================================================

def count_menu_types(menu):

    if pd.isna(menu):
        return 0

    menu = str(menu).strip()

    if menu == "":
        return 0

    daftar = [
        item.strip()
        for item in menu.split(",")
        if item.strip()
    ]

    return len(daftar)


# ==========================================================
# KONVERSI TOTAL HARGA
# ==========================================================

def convert_total_harga(value):

    if pd.isna(value):
        return None

    text = str(value)

    text = text.replace("Rp", "")
    text = text.replace("rp", "")
    text = text.replace(".", "")
    text = text.replace(",", "")
    text = text.strip()

    angka = re.findall(r"\d+", text)

    if len(angka) == 0:
        return None

    return int("".join(angka))


# ==========================================================
# KONVERSI JUMLAH PESANAN
# ==========================================================

def convert_jumlah_pesanan(value):

    if pd.isna(value):
        return None

    angka = re.findall(r"\d+", str(value))

    if len(angka) == 0:
        return None

    return int(angka[0])


# ==========================================================
# KONVERSI WAKTU
# ==========================================================

def convert_minutes(value):

    if pd.isna(value):
        return None

    text = str(value).strip().lower()

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
# FEATURE ENGINEERING
# ==========================================================

def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Menambahkan variabel yang dibutuhkan
    pada proses clustering.
    """

    df = df.copy()

    # ------------------------------------------------------
    # Jumlah Jenis Menu
    # ------------------------------------------------------

    df["Jumlah_jenis_menu"] = (
        df["menu_yang_dibeli"]
        .apply(count_menu_types)
    )

    # ------------------------------------------------------
    # Total Harga
    # ------------------------------------------------------

    df["Total_harga"] = (
        df["Total_harga"]
        .apply(convert_total_harga)
    )

    # ------------------------------------------------------
    # Jumlah Pesanan
    # ------------------------------------------------------

    df["Jumlah_pesanan"] = (
        df["Jumlah_pesanan"]
        .apply(convert_jumlah_pesanan)
    )

    # ------------------------------------------------------
    # Waktu Persiapan yang Diberikan
    # ------------------------------------------------------

    df["waktu_persiapan_yang_diberikan"] = (
        df["waktu_persiapan_yang_diberikan"]
        .apply(convert_minutes)
    )

    # ------------------------------------------------------
    # Waktu Persiapan yang Digunakan
    # ------------------------------------------------------

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
    Mengambil variabel penelitian dan
    memastikan seluruh data numerik.
    """

    feature_df = df.copy()

    # ------------------------------------------------------
    # Validasi Kolom
    # ------------------------------------------------------

    kolom_hilang = [

        col

        for col in FEATURE_COLUMNS

        if col not in feature_df.columns

    ]

    if len(kolom_hilang) > 0:

        raise ValueError(

            "Kolom berikut tidak ditemukan:\n\n"

            + "\n".join(kolom_hilang)

        )

    # ------------------------------------------------------
    # Ambil Variabel Penelitian
    # ------------------------------------------------------

    feature_df = feature_df[FEATURE_COLUMNS].copy()

    # ------------------------------------------------------
    # Konversi Seluruh Kolom Menjadi Numerik
    # ------------------------------------------------------

    for col in feature_df.columns:

        feature_df[col] = pd.to_numeric(

            feature_df[col],

            errors="coerce"

        )

    # ------------------------------------------------------
    # Hapus Data yang Tidak Valid
    # ------------------------------------------------------

    feature_df = feature_df.dropna()

    # ------------------------------------------------------
    # Reset Index
    # ------------------------------------------------------

    feature_df = feature_df.reset_index(drop=True)

    return feature_df
    # ==========================================================
# MIN MAX NORMALIZATION
# ==========================================================

def minmax_normalization(feature_df: pd.DataFrame) -> pd.DataFrame:
    """
    Melakukan normalisasi menggunakan
    Min-Max Normalization.
    """

    scaler = MinMaxScaler()

    normalized = scaler.fit_transform(
        feature_df
    )

    normalized_df = pd.DataFrame(

        normalized,

        columns=feature_df.columns,

        index=feature_df.index

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
    """

    # ======================================================
    # DATA CLEANING
    # ======================================================

    cleaned_df = clean_data(df)

    # ======================================================
    # FEATURE ENGINEERING
    # ======================================================

    engineered_df = feature_engineering(
        cleaned_df
    )

    # ======================================================
    # VARIABEL PENELITIAN
    # ======================================================

    feature_df = select_features(
        engineered_df
    )

    # ======================================================
    # MENYESUAIKAN DATASET
    # ======================================================

    engineered_df = engineered_df.loc[
        feature_df.index
    ].copy()

    # ======================================================
    # NORMALISASI
    # ======================================================

    normalized_df = minmax_normalization(
        feature_df
    )

    # ======================================================
    # RESET INDEX
    # ======================================================

    engineered_df = engineered_df.reset_index(
        drop=True
    )

    feature_df = feature_df.reset_index(
        drop=True
    )

    normalized_df = normalized_df.reset_index(
        drop=True
    )

    # ======================================================
    # RETURN
    # ======================================================

    return (

        engineered_df,

        feature_df,

        normalized_df

    )
