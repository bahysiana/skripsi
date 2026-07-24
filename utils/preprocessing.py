import re
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# ==========================================================
# VARIABEL PENELITIAN
# ==========================================================

FEATURE_COLUMNS = [

    "Jumlah_Item_Produk",

    "Frekuensi_Produk",

    "Total_Pendapatan",

    "Rata2_Waktu_Persiapan_Diberikan",

    "Rata2_Waktu_Persiapan_Digunakan"

]


# ==========================================================
# DATA CLEANING
# ==========================================================

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Membersihkan dataset sebelum diproses.
    """

    df = df.copy()

    # Hilangkan spasi pada nama kolom
    df.columns = df.columns.str.strip()

    # Hapus data duplikat
    df = df.drop_duplicates()

    # Hapus baris yang seluruh kolomnya kosong
    df = df.dropna(how="all")

    return df


# ==========================================================
# KONVERSI ANGKA
# ==========================================================

def convert_number(value):
    """
    Mengubah berbagai format angka menjadi integer.

    Contoh:
    --------
    Rp30.000 -> 30000

    30.000 -> 30000

    30000 -> 30000
    """

    if pd.isna(value):
        return None

    text = str(value).strip()

    if text.lower() in [

        "",

        "-",

        "--",

        "none",

        "nan"

    ]:

        return None

    # Hilangkan tulisan Rp
    text = re.sub(r"rp", "", text, flags=re.IGNORECASE)

    # Hilangkan titik ribuan
    text = text.replace(".", "")

    angka = re.findall(r"\d+", text)

    if not angka:
        return None

    return int("".join(angka))


# ==========================================================
# KONVERSI MENIT
# ==========================================================

def convert_minutes(value):
    """
    Mengubah format waktu menjadi menit.

    Contoh:
    --------
    13 menit -> 13

    8 Menit -> 8
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

    if not angka:
        return None

    return int(angka[0])


# ==========================================================
# EKSTRAK NAMA PRODUK DAN QUANTITY
# ==========================================================

def extract_product_info(menu_name):
    """
    Mengekstrak nama produk dan jumlah item.

    Contoh:
    --------
    Ayam Goreng
        -> ("Ayam Goreng", 1)

    Ayam Goreng (2x)
        -> ("Ayam Goreng", 2)

    Ayam Goreng x2
        -> ("Ayam Goreng", 2)

    2x Ayam Goreng
        -> ("Ayam Goreng", 2)

    x2 Ayam Goreng
        -> ("Ayam Goreng", 2)
    """

    if pd.isna(menu_name):
        return "", 1

    text = str(menu_name).strip()

    qty = 1

    patterns = [

        r"\(\s*(\d+)\s*x\s*\)",

        r"(\d+)\s*x",

        r"x\s*(\d+)"

    ]

    for pattern in patterns:

        match = re.search(

            pattern,

            text,

            flags=re.IGNORECASE

        )

        if match:

            qty = int(match.group(1))

            text = re.sub(

                pattern,

                "",

                text,

                flags=re.IGNORECASE

            )

            break

    # Hapus kurung kosong
    text = re.sub(r"\(\)", "", text)

    # Rapikan spasi
    text = " ".join(text.split())

    return text.strip(), qty

# ==========================================================
# MEMECAH TRANSAKSI MENJADI DATA PRODUK
# ==========================================================

def split_products(df: pd.DataFrame) -> pd.DataFrame:
    """
    Mengubah setiap transaksi menjadi beberapa baris produk.

    Output:
    ----------------------------------------------------------
    Produk
    Qty
    Pendapatan_Produk
    Waktu_Diberikan
    Waktu_Digunakan
    ----------------------------------------------------------

    Fungsi ini sudah menangani dua format harga Shopee Food:

    Format A
    --------
    Menu :
        Bubur Kampiun (2x)

    Harga :
        27000

    Format B
    --------
    Menu :
        Mie Nyemek (2x)

    Harga :
        17500,17500
    """

    rows = []

    for _, row in df.iterrows():

        menu_text = row.get("menu_yang_dibeli", "")
        harga_text = row.get("harga_per_menu", "")

        if pd.isna(menu_text):
            continue

        # --------------------------------------------
        # Pecah daftar menu
        # --------------------------------------------

        menu_list = [

            item.strip()

            for item in str(menu_text).split(",")

            if item.strip()

        ]

        # --------------------------------------------
        # Pecah daftar harga
        # --------------------------------------------

        harga_list = []

        if pd.notna(harga_text):

            harga_list = [

                convert_number(x)

                for x in str(harga_text).split(",")

                if str(x).strip() != ""

            ]

        menu_index = 0
        harga_index = 0

        while menu_index < len(menu_list):

            menu = menu_list[menu_index]

            nama_produk, qty = extract_product_info(menu)

            pendapatan_produk = 0

            # =====================================================
            # TIDAK ADA HARGA
            # =====================================================

            if len(harga_list) == 0:

                pendapatan_produk = None

            # =====================================================
            # FORMAT 1
            # jumlah harga == jumlah menu
            # =====================================================

            elif len(harga_list) == len(menu_list):

                pendapatan_produk = harga_list[menu_index]

            # =====================================================
            # FORMAT 2
            # harga mengikuti quantity
            # =====================================================

            else:

                if harga_index + qty <= len(harga_list):

                    daftar_harga = harga_list[
                        harga_index:
                        harga_index + qty
                    ]

                    pendapatan_produk = sum(

                        h

                        for h in daftar_harga

                        if h is not None

                    )

                    harga_index += qty

                else:

                    if harga_index < len(harga_list):

                        pendapatan_produk = harga_list[harga_index]

                        harga_index += 1

                    else:

                        pendapatan_produk = None

            rows.append({

                "Produk": nama_produk,

                "Qty": qty,

                "Pendapatan_Produk": pendapatan_produk,

                "Waktu_Diberikan": convert_minutes(

                    row.get(
                        "waktu_persiapan_yang_diberikan"
                    )

                ),

                "Waktu_Digunakan": convert_minutes(

                    row.get(
                        "waktu_persiapan_digunakan"
                    )

                )

            })

            menu_index += 1

    product_df = pd.DataFrame(rows)

    return product_df

# ==========================================================
# MEMBANGUN DATASET BERDASARKAN PRODUK
# ==========================================================

def build_product_dataset(product_df: pd.DataFrame) -> pd.DataFrame:
    """
    Mengubah hasil split_products()
    menjadi dataset agregasi per produk.
    """

    if product_df.empty:

        return pd.DataFrame(columns=[

            "Produk",

            "Jumlah_Item_Produk",

            "Frekuensi_Produk",

            "Total_Pendapatan",

            "Rata2_Waktu_Persiapan_Diberikan",

            "Rata2_Waktu_Persiapan_Digunakan"

        ])

    df = product_df.copy()

    # ======================================================
    # Pastikan seluruh kolom numerik
    # ======================================================

    numeric_columns = [

        "Qty",

        "Pendapatan_Produk",

        "Waktu_Diberikan",

        "Waktu_Digunakan"

    ]

    for col in numeric_columns:

        df[col] = pd.to_numeric(

            df[col],

            errors="coerce"

        )

    # ======================================================
    # Hilangkan produk kosong
    # ======================================================

    df = df[

        df["Produk"].notna()

    ]

    df = df[

        df["Produk"].str.strip() != ""

    ]

    # ======================================================
    # GROUP BY PRODUK
    # ======================================================

    result = (

        df

        .groupby(

            "Produk",

            as_index=False

        )

        .agg(

            Jumlah_Item_Produk=(

                "Qty",

                "sum"

            ),

            Frekuensi_Produk=(

                "Produk",

                "count"

            ),

            Total_Pendapatan=(

                "Pendapatan_Produk",

                "sum"

            ),

            Rata2_Waktu_Persiapan_Diberikan=(

                "Waktu_Diberikan",

                "mean"

            ),

            Rata2_Waktu_Persiapan_Digunakan=(

                "Waktu_Digunakan",

                "mean"

            )

        )

    )

    # ======================================================
    # Pembulatan rata-rata
    # ======================================================

    result[

        "Rata2_Waktu_Persiapan_Diberikan"

    ] = (

        result[

            "Rata2_Waktu_Persiapan_Diberikan"

        ]

        .round(2)

    )

    result[

        "Rata2_Waktu_Persiapan_Digunakan"

    ] = (

        result[

            "Rata2_Waktu_Persiapan_Digunakan"

        ]

        .round(2)

    )

    return result

# ==========================================================
# SELECT FEATURE
# ==========================================================

def select_features(product_dataset: pd.DataFrame):
    """
    Mengambil variabel penelitian
    yang akan digunakan pada proses clustering.
    """

    feature_df = product_dataset.copy()

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
    # UBAH MENJADI NUMERIK
    # ======================================================

    for col in FEATURE_COLUMNS:

        feature_df[col] = pd.to_numeric(

            feature_df[col],

            errors="coerce"

        )

    # ======================================================
    # HAPUS DATA TIDAK VALID
    # ======================================================

    feature_df = feature_df.dropna()

    # ======================================================
    # RESET INDEX
    # ======================================================

    feature_df = feature_df.reset_index(drop=True)

    return feature_df

# ==========================================================
# MIN-MAX NORMALIZATION
# ==========================================================

def minmax_normalization(feature_df: pd.DataFrame):
    """
    Melakukan normalisasi menggunakan
    Min-Max Normalization.

    Rumus:

        X' = (X - Xmin) / (Xmax - Xmin)
    """

    if feature_df.empty:

        raise ValueError(

            "Data feature kosong."

        )

    scaler = MinMaxScaler()

    normalized = scaler.fit_transform(

        feature_df

    )

    normalized_df = pd.DataFrame(

        normalized,

        columns=feature_df.columns,

        index=feature_df.index

    )

    return normalized_df, scaler

# ==========================================================
# PREPROCESS DATASET
# ==========================================================

def preprocess_dataset(df: pd.DataFrame):
    """
    Pipeline preprocessing.

    Tahapan:
    --------
    1. Data Cleaning
    2. Split Produk
    3. Agregasi Produk
    4. Feature Selection
    5. Min-Max Normalization
    """

    # ======================================================
    # DATA CLEANING
    # ======================================================

    cleaned_df = clean_data(df)

    # ======================================================
    # SPLIT PRODUK
    # ======================================================

    product_detail_df = split_products(cleaned_df)

    # ======================================================
    # AGREGASI PRODUK
    # ======================================================

    product_dataset = build_product_dataset(
        product_detail_df
    )

    # ======================================================
    # FEATURE SELECTION
    # ======================================================

    feature_df = select_features(
        product_dataset
    )

    # ======================================================
    # SAMAKAN INDEX
    # ======================================================

    valid_index = feature_df.index

    product_dataset = (

        product_dataset

        .loc[valid_index]

        .reset_index(drop=True)

    )

    feature_df = (

        feature_df

        .reset_index(drop=True)

    )

    # ======================================================
    # NORMALISASI
    # ======================================================

    normalized_df, scaler = (

        minmax_normalization(

            feature_df

        )

    )

    normalized_df = (

        normalized_df

        .reset_index(drop=True)

    )

    # ======================================================
    # RETURN
    # ======================================================

    return (

        product_dataset,

        feature_df,

        normalized_df,

        scaler

    )
