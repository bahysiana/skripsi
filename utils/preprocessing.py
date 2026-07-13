import re
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


# ==========================================================
# DATA CLEANING
# ==========================================================

def clean_data(df: pd.DataFrame):

    df = df.copy()

    # Hilangkan spasi nama kolom
    df.columns = df.columns.str.strip()

    # Hilangkan duplikat
    df = df.drop_duplicates()

    # Hilangkan data kosong
    df = df.dropna(how="all")

    return df


# ==========================================================
# JUMLAH JENIS MENU
# ==========================================================

def count_menu_types(menu):

    if pd.isna(menu):
        return 0

    menu = str(menu).strip()

    if menu == "":
        return 0

    return len(
        [
            x.strip()
            for x in menu.split(",")
            if x.strip()
        ]
    )


# ==========================================================
# KONVERSI WAKTU
# ==========================================================

def convert_minutes(value):

    if pd.isna(value):
        return None

    value = str(value).lower().strip()

    angka = re.findall(r"\d+", value)

    if len(angka) == 0:
        return None

    return int(angka[0])


# ==========================================================
# KONVERSI ANGKA
# ==========================================================

def convert_numeric(value):

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
# FEATURE ENGINEERING
# ==========================================================

def feature_engineering(df):

    df = df.copy()

    df["Jumlah_jenis_menu"] = (
        df["menu_yang_dibeli"]
        .apply(count_menu_types)
    )

    df["waktu_persiapan_yang_diberikan"] = (
        df["waktu_persiapan_yang_diberikan"]
        .apply(convert_minutes)
    )

    df["waktu_persiapan_digunakan"] = (
        df["waktu_persiapan_digunakan"]
        .apply(convert_minutes)
    )

    df["Total_harga"] = (
        df["Total_harga"]
        .apply(convert_numeric)
    )

    df["Jumlah_pesanan"] = (
        df["Jumlah_pesanan"]
        .apply(convert_numeric)
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

def select_features(df):

    kolom_hilang = [

        col

        for col in FEATURE_COLUMNS

        if col not in df.columns

    ]

    if kolom_hilang:

        raise ValueError(

            "Kolom tidak ditemukan:\n\n"

            + "\n".join(kolom_hilang)

        )

    return df[FEATURE_COLUMNS].copy()


# ==========================================================
# MIN MAX
# ==========================================================

def minmax_normalization(df):

    numeric_df = df.copy()

    # Pastikan numerik

    for col in numeric_df.columns:

        numeric_df[col] = pd.to_numeric(

            numeric_df[col],

            errors="coerce"

        )

    # DEBUG

    if numeric_df.isnull().any().any():

        pesan = ""

        for col in numeric_df.columns:

            if numeric_df[col].isnull().any():

                pesan += f"\nKolom : {col}\n"

                pesan += str(

                    df.loc[

                        numeric_df[col].isnull(),

                        col

                    ].head()

                )

                pesan += "\n"

        raise ValueError(pesan)

    scaler = MinMaxScaler()

    hasil = scaler.fit_transform(
        numeric_df
    )

    return pd.DataFrame(

        hasil,

        columns=numeric_df.columns,

        index=numeric_df.index

    )


# ==========================================================
# PREPROCESS DATASET
# ==========================================================

def preprocess_dataset(df):

    # Cleaning

    cleaned_df = clean_data(df)

    # Feature Engineering

    engineered_df = feature_engineering(
        cleaned_df
    )

    # Variabel

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
