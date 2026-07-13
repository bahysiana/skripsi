import re
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


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
# DATA CLEANING
# ==========================================================

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Membersihkan dataset.
    """

    df = df.copy()

    # Hilangkan spasi nama kolom
    df.columns = df.columns.str.strip()

    # Hapus duplikasi
    df = df.drop_duplicates()

    # Hapus baris yang seluruh kolomnya kosong
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

    daftar_menu = [

        item.strip()

        for item in menu.split(",")

        if item.strip()

    ]

    return len(daftar_menu)


# ==========================================================
# KONVERSI ANGKA
# ==========================================================

def convert_number(value):
    """
    Mengubah berbagai format angka menjadi numerik.

    Contoh:

    30000 -> 30000

    30.000 -> 30000

    Rp30.000 -> 30000
    """

    if pd.isna(value):
        return None

    text = str(value).strip()

    if text in [

        "",

        "-",

        "--",

        "None",

        "none",

        "nan"

    ]:

        return None

    # Hilangkan tulisan Rp
    text = text.replace("Rp", "")
    text = text.replace("rp", "")

    # Hilangkan titik ribuan
    text = text.replace(".", "")

    # Ambil angka
    angka = re.findall(r"\d+", text)

    if len(angka) == 0:
        return None

    return int("".join(angka))


# ==========================================================
# KONVERSI MENIT
# ==========================================================

def convert_minutes(value):
    """
    Mengubah

    13 menit -> 13

    8 menit -> 8

    - -> None
    """

    if pd.isna(value):
        return None

    text = str(value).strip().lower()

    if text in [

        "",

        "-",

        "--",

        "none",

        "nan"

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
    Menambahkan variabel penelitian yang
    diperlukan pada proses clustering.
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
        .apply(convert_number)
    )

    # ======================================================
    # JUMLAH PESANAN
    # ======================================================

    df["Jumlah_pesanan"] = (
        df["Jumlah_pesanan"]
        .apply(convert_number)
    )

    # ======================================================
    # WAKTU PERSIAPAN DIBERIKAN
    # ======================================================

    df["waktu_persiapan_yang_diberikan"] = (
        df["waktu_persiapan_yang_diberikan"]
        .apply(convert_minutes)
    )

    # ======================================================
    # WAKTU PERSIAPAN DIGUNAKAN
    # ======================================================

    df["waktu_persiapan_digunakan"] = (
        df["waktu_persiapan_digunakan"]
        .apply(convert_minutes)
    )

    return df


# ==========================================================
# SELECT FEATURE
# ==========================================================

def select_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Mengambil variabel penelitian dan
    membersihkan data yang tidak valid.
    """

    feature_df = df.copy()

    # ======================================================
    # VALIDASI KOLOM
    # ======================================================

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

    # ======================================================
    # AMBIL VARIABEL PENELITIAN
    # ======================================================

    feature_df = feature_df[FEATURE_COLUMNS].copy()

    # ======================================================
    # KONVERSI KE NUMERIK
    # ======================================================

    for col in FEATURE_COLUMNS:

        feature_df[col] = pd.to_numeric(

            feature_df[col],

            errors="coerce"

        )

    # ======================================================
    # HAPUS DATA YANG TIDAK VALID
    # ======================================================

    feature_df = feature_df.dropna()

    return feature_df
    # ==========================================================
# MIN MAX NORMALIZATION
# ==========================================================

def minmax_normalization(feature_df: pd.DataFrame) -> pd.DataFrame:
    """
    Melakukan normalisasi Min-Max terhadap
    variabel penelitian.
    """

    scaler = MinMaxScaler()

    normalized = scaler.fit_transform(feature_df)

    normalized_df = pd.DataFrame(
        normalized,
        columns=feature_df.columns
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

    engineered_df = feature_engineering(cleaned_df)

    # ======================================================
    # VARIABEL PENELITIAN
    # ======================================================

    feature_df = select_features(engineered_df)

    # ======================================================
    # SAMAKAN DATASET
    # ======================================================

    valid_index = feature_df.index

    engineered_df = (
        engineered_df
        .loc[valid_index]
        .copy()
        .reset_index(drop=True)
    )

    feature_df = (
        feature_df
        .reset_index(drop=True)
    )

    # ======================================================
    # MIN MAX NORMALIZATION
    # ======================================================

    normalized_df = minmax_normalization(
        feature_df
    )

    # ======================================================
    # RETURN
    # ======================================================

    return (

        engineered_df,

        feature_df,

        normalized_df

    )
