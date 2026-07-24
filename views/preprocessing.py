import streamlit as st

from utils.database import (
    get_all_data,
    is_database_empty
)

from utils.preprocessing import (
    preprocess_dataset,
    FEATURE_COLUMNS
)


# ==========================================================
# HALAMAN PREPROCESSING
# ==========================================================

def show_preprocessing():

    # ======================================================
    # HEADER
    # ======================================================

    st.title("🧹 Preprocessing")

    st.caption(
        """
Melakukan proses Data Cleaning,
Agregasi Produk, Feature Selection,
dan Min-Max Normalization
sebelum proses K-Means Clustering.
        """
    )

    st.divider()

    # ======================================================
    # CEK DATABASE
    # ======================================================

    if is_database_empty():

        st.warning(
            """
Belum ada dataset pada database.

Silakan upload dataset terlebih dahulu
melalui menu **Kelola Data**.
            """
        )

        return

    # ======================================================
    # LOAD DATASET
    # ======================================================

    df = get_all_data()

    # ======================================================
    # INFORMASI PREPROCESSING
    # ======================================================

    st.info(
        """
Tahapan preprocessing yang dilakukan:

1. Data Cleaning

2. Agregasi Produk

3. Feature Selection

4. Min-Max Normalization

Dataset hasil preprocessing
akan digunakan pada proses
K-Means Clustering.
        """
    )

    st.divider()

    # ======================================================
    # DATASET AWAL
    # ======================================================

    st.subheader("📂 Dataset Awal")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(

            "Jumlah Transaksi",

            len(df)

        )

    with col2:

        st.metric(

            "Jumlah Kolom",

            len(df.columns)

        )

    st.dataframe(

        df,

        hide_index=True,

        use_container_width=True

    )

    st.divider()

    # ======================================================
    # TOMBOL PREPROCESSING
    # ======================================================

    mulai = st.button(

        "▶ Mulai Preprocessing",

        type="primary",

        use_container_width=True

    )

    if not mulai:

        return

    # ======================================================
    # PROSES PREPROCESSING
    # ======================================================

    with st.spinner("Sedang melakukan preprocessing data..."):

        (
            cleaned_df,
            product_dataset,
            feature_df,
            normalized_df,
            scaler
        ) = preprocess_dataset(df)

    st.success(
        "Preprocessing berhasil dilakukan."
    )

    st.divider()

    # ======================================================
    # HASIL DATA CLEANING
    # ======================================================

    st.subheader("🧹 Hasil Data Cleaning")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Jumlah Data",
            len(cleaned_df)
        )

    with col2:

        st.metric(
            "Jumlah Kolom",
            len(cleaned_df.columns)
        )

    st.markdown(
        """
Tahap ini bertujuan untuk membersihkan dataset
dari data duplikat, data kosong, serta merapikan
struktur data sehingga siap digunakan pada proses
berikutnya.
        """
    )

    st.dataframe(

        cleaned_df,

        hide_index=True,

        use_container_width=True

    )

    st.divider()

    # ======================================================
    # DATASET PRODUK
    # ======================================================

    st.subheader("📦 Dataset Produk")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Jumlah Produk",
            len(product_dataset)
        )

    with col2:

        st.metric(
            "Jumlah Variabel",
            len(product_dataset.columns)
        )

    st.markdown(
        """
Dataset transaksi diubah menjadi dataset
berdasarkan produk melalui proses agregasi.
Setiap produk direpresentasikan berdasarkan
jumlah item yang terjual, frekuensi pembelian,
total pendapatan, serta rata-rata waktu
persiapan pesanan.
        """
    )

    st.dataframe(

        product_dataset,

        hide_index=True,

        use_container_width=True

    )

    st.divider()

    # ======================================================
    # FEATURE SELECTION
    # ======================================================

    st.subheader("📊 Variabel Penelitian")

    st.markdown(
        """
Tahap Feature Selection dilakukan untuk memilih
variabel yang digunakan pada proses
K-Means Clustering sesuai dengan
variabel penelitian.
        """
    )

    st.markdown("### Variabel yang digunakan")

    nama_variabel = {
        "Jumlah_Item_Produk": "• Jumlah Item Produk",
        "Frekuensi_Produk": "• Frekuensi Produk",
        "Total_Pendapatan": "• Total Pendapatan",
        "Rata2_Waktu_Persiapan_Diberikan": "• Rata-rata Waktu Persiapan Diberikan",
        "Rata2_Waktu_Persiapan_Digunakan": "• Rata-rata Waktu Persiapan Digunakan"
    }

    for fitur in FEATURE_COLUMNS:

        st.write(nama_variabel.get(fitur, fitur))

    st.markdown("### Dataset Variabel Penelitian")

    st.dataframe(

        feature_df,

        hide_index=True,

        use_container_width=True

    )

    st.divider()

    # ======================================================
    # MIN-MAX NORMALIZATION
    # ======================================================

    st.subheader("📈 Hasil Min-Max Normalization")

    st.markdown(
        """
Normalisasi dilakukan menggunakan metode
Min-Max Normalization sehingga seluruh
variabel memiliki rentang nilai antara
0 sampai 1.

Normalisasi bertujuan agar seluruh variabel
memiliki skala yang sama sebelum dilakukan
proses clustering menggunakan algoritma
K-Means.
        """
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(

            "Jumlah Data",

            len(normalized_df)

        )

    with col2:

        st.metric(

            "Jumlah Variabel",

            len(normalized_df.columns)

        )

    st.dataframe(

        normalized_df.round(4),

        hide_index=True,

        use_container_width=True

    )

    st.divider()

    # ======================================================
    # SIMPAN KE SESSION STATE
    # ======================================================

    st.session_state["cleaned_df"] = cleaned_df

    st.session_state["product_dataset"] = product_dataset

    st.session_state["feature_df"] = feature_df

    st.session_state["normalized_df"] = normalized_df

    st.session_state["scaler"] = scaler

    # ======================================================
    # RINGKASAN HASIL PREPROCESSING
    # ======================================================

    st.subheader("📋 Ringkasan Hasil Preprocessing")

    ringkasan_df = {
        "Tahapan": [
            "Data Cleaning",
            "Agregasi Produk",
            "Feature Selection",
            "Min-Max Normalization"
        ],
        "Status": [
            "✅ Berhasil",
            "✅ Berhasil",
            "✅ Berhasil",
            "✅ Berhasil"
        ]
    }

    st.dataframe(
        ringkasan_df,
        hide_index=True,
        use_container_width=True
    )

    st.divider()

    # ======================================================
    # INFORMASI DATA
    # ======================================================

    st.subheader("📌 Informasi Dataset")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Jumlah Transaksi Awal",
            len(df)
        )

    with col2:

        st.metric(
            "Jumlah Produk",
            len(product_dataset)
        )

    with col3:

        st.metric(
            "Variabel Clustering",
            len(FEATURE_COLUMNS)
        )

    st.divider()

    # ======================================================
    # PENUTUP
    # ======================================================

    st.success(
        """
Preprocessing data berhasil dilakukan.

Seluruh tahapan preprocessing telah selesai,
meliputi Data Cleaning, Agregasi Produk,
Feature Selection, dan Min-Max Normalization.

Dataset hasil preprocessing telah disimpan
dan siap digunakan pada proses
K-Means Clustering.
        """
    )
