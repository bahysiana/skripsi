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

    # Hilangkan spasi pada nama kolom
    df.columns = df.columns.str.strip()

    # Hapus data duplikat
    df = df.drop_duplicates()

    # Hapus data kosong
    df = df.dropna()

    return df


# ==========================================================
# HITUNG JUMLAH JENIS MENU
# ==========================================================

def count_menu_types(menu) -> int:
    """
    Menghitung jumlah jenis menu
    berdasarkan menu_yang_dibeli.
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
# FEATURE ENGINEERING
# ==========================================================

def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Menambahkan variabel Jumlah_jenis_menu.
    """

    df = df.copy()

    df["Jumlah_jenis_menu"] = df["menu_yang_dibeli"].apply(
        count_menu_types
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

    # Pastikan semua kolom tersedia

    kolom_tidak_ada = [

        col

        for col in FEATURE_COLUMNS

        if col not in df.columns

    ]

    if len(kolom_tidak_ada) > 0:

        raise ValueError(

            "Kolom berikut tidak ditemukan pada dataset:\n\n"

            + "\n".join(kolom_tidak_ada)

        )

    feature_df = df[FEATURE_COLUMNS].copy()

    return feature_df


# ==========================================================
# MIN MAX NORMALIZATION
# ==========================================================

def minmax_normalization(df: pd.DataFrame) -> pd.DataFrame:
    """
    Melakukan normalisasi Min-Max.
    """

    numeric_df = df.copy()

    # Pastikan seluruh data numerik

    for col in numeric_df.columns:

        numeric_df[col] = pd.to_numeric(

            numeric_df[col],

            errors="coerce"

        )

    # Hapus data yang masih tidak valid

    numeric_df = numeric_df.dropna()

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

    Tahapan:

    1. Cleaning
    2. Feature Engineering
    3. Select Feature
    4. Min-Max Normalization
    """

    # -------------------------
    # Cleaning
    # -------------------------

    cleaned_df = clean_data(df)

    # -------------------------
    # Feature Engineering
    # -------------------------

    engineered_df = feature_engineering(

        cleaned_df

    )

    # -------------------------
    # Variabel Penelitian
    # -------------------------

    feature_df = select_features(

        engineered_df

    )

    # -------------------------
    # Min-Max Normalization
    # -------------------------

    normalized_df = minmax_normalization(

        feature_df

    )

    return (

        engineered_df,

        feature_df,

        normalized_df

    )
