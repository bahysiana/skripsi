import streamlit as st
import pandas as pd

from utils.database import (
    get_all_data,
    is_database_empty
)

from utils.preprocessing import (
    preprocess_dataset,
    FEATURE_COLUMNS
)


# ==========================================================
# PREPROCESSING
# ==========================================================

def show_preprocessing():

    st.title("🧹 Preprocessing")

    st.caption(
        "Melakukan Data Cleaning, Feature Engineering, dan Min-Max Normalization."
    )

    st.divider()

    # ======================================================
    # DATABASE CHECK
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
    # LOAD DATA
    # ======================================================

    df = get_all_data()

    # ======================================================
    # INFORMASI
    # ======================================================

    st.info(
        """
Tahapan preprocessing yang dilakukan:

1. Data Cleaning

2. Feature Engineering

3. Pemilihan Variabel

4. Min-Max Normalization
        """
    )

    st.divider()

    # ======================================================
    # DATASET AWAL
    # ======================================================

    st.subheader("📂 Dataset Awal")

    st.write(f"Jumlah Data : **{len(df)}**")

    st.write(f"Jumlah Kolom : **{len(df.columns)}**")

    st.dataframe(

        df,

        use_container_width=True,

        hide_index=True

    )

    st.divider()

    # ======================================================
    # PROSES
    # ======================================================

    if st.button(

        "▶ Mulai Preprocessing",

        type="primary",

        use_container_width=True

    ):

        with st.spinner("Sedang melakukan preprocessing..."):

            original_df, feature_df, normalized_df = preprocess_dataset(df)

        st.success(
            "Preprocessing berhasil dilakukan."
        )

        st.divider()

        # ==================================================
        # CLEANING
        # ==================================================

        st.subheader("🧹 Hasil Data Cleaning")

        st.write(f"Jumlah Data : **{len(original_df)}**")

        st.write(f"Jumlah Kolom : **{len(original_df.columns)}**")

        st.dataframe(

            original_df,

            use_container_width=True,

            hide_index=True

        )

        st.divider()

        # ==================================================
        # FEATURE ENGINEERING
        # ==================================================

        st.subheader("⚙️ Feature Engineering")

        st.success(
            """
Kolom baru berhasil ditambahkan:

• Jumlah_jenis_menu

• Jumlah_Item_Makanan

• Jumlah_Item_Minuman
            """
        )

        st.dataframe(

            original_df,

            use_container_width=True,

            hide_index=True

        )

        st.divider()

        # ==================================================
        # VARIABEL PENELITIAN
        # ==================================================

        st.subheader("📊 Variabel Penelitian")

        st.write(FEATURE_COLUMNS)

        st.dataframe(

            feature_df,

            use_container_width=True,

            hide_index=True

        )

        st.divider()

        # ==================================================
        # NORMALISASI
        # ==================================================

        st.subheader("📈 Hasil Min-Max Normalization")

        st.dataframe(

            normalized_df,

            use_container_width=True,

            hide_index=True

        )

        st.divider()

        # ==================================================
        # SESSION
        # ==================================================

        st.session_state["original_df"] = original_df

        st.session_state["feature_df"] = feature_df

        st.session_state["normalized_df"] = normalized_df

        st.success(
            """
Dataset hasil preprocessing berhasil disimpan.

Silakan lanjut ke menu **Clustering**.
            """
        )
