import pandas as pd

from sklearn.preprocessing import MinMaxScaler


# ==========================================================
# CLEAN DATA
# ==========================================================

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Membersihkan dataset.
    """

    df = df.copy()

    # Menghapus spasi pada nama kolom
    df.columns = df.columns.str.strip()

    # Menghapus duplikasi
    df = df.drop_duplicates()

    # Menghapus data kosong
    df = df.dropna()

    return df
  # ==========================================================
# HITUNG JUMLAH JENIS MENU
# ==========================================================

def count_menu_types(menu: str) -> int:
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
# HITUNG JUMLAH ITEM MAKANAN
# ==========================================================

def count_food_items(menu: str) -> int:
    """
    Menghitung jumlah item makanan.
    """

    if pd.isna(menu):
        return 0

    makanan = 0

    keywords_minuman = [

        "es",
        "teh",
        "kopi",
        "jus",
        "susu",
        "nutrisari",
        "cappuccino",
        "americano",
        "latte",
        "mocha",
        "air",
        "mineral"

    ]

    for item in str(menu).split(","):

        nama = item.strip().lower()

        if not any(k in nama for k in keywords_minuman):

            makanan += 1

    return makanan


# ==========================================================
# HITUNG JUMLAH ITEM MINUMAN
# ==========================================================

def count_drink_items(menu: str) -> int:
    """
    Menghitung jumlah item minuman.
    """

    if pd.isna(menu):
        return 0

    minuman = 0

    keywords_minuman = [

        "es",
        "teh",
        "kopi",
        "jus",
        "susu",
        "nutrisari",
        "cappuccino",
        "americano",
        "latte",
        "mocha",
        "air",
        "mineral"

    ]

    for item in str(menu).split(","):

        nama = item.strip().lower()

        if any(k in nama for k in keywords_minuman):

            minuman += 1

    return minuman


# ==========================================================
# FEATURE ENGINEERING
# ==========================================================

def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Menambahkan fitur baru.
    """

    df = df.copy()

    df["Jumlah_jenis_menu"] = df["menu_yang_dibeli"].apply(
        count_menu_types
    )

    df["Jumlah_Item_Makanan"] = df["menu_yang_dibeli"].apply(
        count_food_items
    )

    df["Jumlah_Item_Minuman"] = df["menu_yang_dibeli"].apply(
        count_drink_items
    )

    return df
  # ==========================================================
# VARIABEL PENELITIAN
# ==========================================================

FEATURE_COLUMNS = [

    "Total_harga",

    "Jumlah_pesanan",

    "Jumlah_jenis_menu",

    "Jumlah_Item_Makanan",

    "Jumlah_Item_Minuman",

    "waktu_persiapan_digunakan"

]


# ==========================================================
# SELECT FEATURE
# ==========================================================

def select_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Mengambil variabel penelitian.
    """

    return df[FEATURE_COLUMNS].copy()


# ==========================================================
# MIN MAX NORMALIZATION
# ==========================================================

def minmax_normalization(df: pd.DataFrame):

    """
    Melakukan normalisasi Min-Max.
    """

    scaler = MinMaxScaler()

    normalized = scaler.fit_transform(df)

    normalized_df = pd.DataFrame(

        normalized,

        columns=df.columns,

        index=df.index

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
    original_df : Dataset setelah cleaning & feature engineering
    feature_df : Dataset variabel penelitian
    normalized_df : Dataset hasil normalisasi
    """

    # ======================================================
    # CLEANING
    # ======================================================

    cleaned_df = clean_data(df)

    # ======================================================
    # FEATURE ENGINEERING
    # ======================================================

    feature_engineering_df = feature_engineering(
        cleaned_df
    )

    # ======================================================
    # SELECT FEATURE
    # ======================================================

    feature_df = select_features(
        feature_engineering_df
    )

    # ======================================================
    # NORMALIZATION
    # ======================================================

    normalized_df = minmax_normalization(
        feature_df
    )

    return (
        feature_engineering_df,
        feature_df,
        normalized_df
    )
