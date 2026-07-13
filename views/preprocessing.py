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
# PREPROCESSING
# ==========================================================

def show_preprocessing():

    st.title("🧹 Preprocessing")

    st.caption(
        "Melakukan Data Cleaning, Feature Engineering, dan Min-Max Normalization."
    )

    st.divider()

    # ======================================================
    # CEK DATABASE
    # ======================================================

    if is_database_empty():

        st.warning(
            """
Belum ada dataset pada database.

Silakan upload dataset terlebih dahulu melalui menu **Kelola Data**.
            """
        )

        return

    # ======================================================
    # LOAD DATA
    # ======================================================

    df = get_all_data()

    # ======================================================
    # DEBUG DATASET
    # ======================================================

    with st.expander("🔍 Debug Dataset"):

        st.write("Nama Kolom")

        st.write(df.columns.tolist())

        st.write("Tipe Data")

        st.write(df.dtypes)

        st.write("5 Data Pertama")

        st.dataframe(
            df.head(),
            use_container_width=True,
            hide_index=True
        )

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

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Jumlah Data",
            len(df)
        )

    with col2:

        st.metric(
            "Jumlah Kolom",
            len(df.columns)
        )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ======================================================
    # BUTTON PREPROCESS
    # ======================================================

    if st.button(
        "▶ Mulai Preprocessing",
        type="primary",
        use_container_width=True
    ):

        try:

            with st.spinner("Sedang melakukan preprocessing..."):

                original_df, feature_df, normalized_df = preprocess_dataset(df)

        except Exception as e:

            st.error("Preprocessing gagal.")

            st.code(str(e))

            return

        st.success(
            "Preprocessing berhasil dilakukan."
        )

        st.divider()

        # ==================================================
        # HASIL CLEANING
        # ==================================================

        st.subheader("🧹 Hasil Data Cleaning")

        st.metric(
            "Jumlah Data",
            len(original_df)
        )

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
        # SIMPAN SESSION
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
