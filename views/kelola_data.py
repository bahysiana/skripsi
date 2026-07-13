import streamlit as st
import pandas as pd

from utils.database import (
    get_all_data,
    replace_all_data,
    delete_all_data,
    is_database_empty
)


# ==========================================================
# KELOLA DATA
# ==========================================================

def show_kelola_data():

    st.title("📂 Kelola Data")

    st.caption(
        "Upload dan kelola dataset transaksi Shopee Food."
    )

    st.divider()

    # ======================================================
    # INFORMASI
    # ======================================================

    st.divider()

    # ======================================================
    # UPLOAD
    # ======================================================

    uploaded_file = st.file_uploader(

        "Upload Dataset",

        type=[

            "csv",

            "xlsx",

            "xls"

        ]

    )

    if uploaded_file is None:

        st.warning(
            "Silakan upload dataset terlebih dahulu."
        )

        return
            # ======================================================
    # MEMBACA DATASET
    # ======================================================

    try:

        if uploaded_file.name.lower().endswith(".csv"):

            try:

                df = pd.read_csv(uploaded_file)

            except Exception:

                uploaded_file.seek(0)

                df = pd.read_csv(
                    uploaded_file,
                    sep=";"
                )

        else:

            df = pd.read_excel(uploaded_file)

    except Exception as e:

        st.error(
            f"Gagal membaca dataset.\n\n{e}"
        )

        return

    # ======================================================
    # INFORMASI DATASET
    # ======================================================

    st.success("Dataset berhasil dibaca.")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(

            label="📦 Jumlah Data",

            value=len(df)

        )

    with col2:

        st.metric(

            label="📑 Jumlah Kolom",

            value=len(df.columns)

        )

    st.divider()

    # ======================================================
    # PREVIEW DATASET
    # ======================================================

    st.subheader("📋 Preview Dataset")

    jumlah_baris = st.selectbox(

        "Jumlah Baris",

        [10, 25, 50, 100],

        index=0

    )

    st.dataframe(

        df.head(jumlah_baris),

        use_container_width=True,

        hide_index=True

    )

    st.divider()
        # ======================================================
    # SIMPAN DATASET
    # ======================================================

    st.subheader("💾 Simpan Dataset")

    if st.button(

        "Simpan Dataset ke Database",

        type="primary",

        use_container_width=True

    ):

        try:

            replace_all_data(df)

            st.success(

                "Dataset berhasil disimpan ke database."

            )

            st.rerun()

        except Exception as e:

            st.error(

                f"Gagal menyimpan dataset.\n\n{e}"

            )

    st.divider()

    # ======================================================
    # DATASET DALAM DATABASE
    # ======================================================

    st.subheader("🗄️ Dataset Dalam Database")

    if is_database_empty():

        st.info(

            "Belum ada dataset yang tersimpan."

        )

        return

    db = get_all_data()

    col1, col2 = st.columns(2)

    with col1:

        st.metric(

            "📦 Jumlah Data",

            len(db)

        )

    with col2:

        st.metric(

            "📑 Jumlah Kolom",

            len(db.columns)

        )

    st.dataframe(

        db,

        use_container_width=True,

        hide_index=True

    )

    st.divider()
        # ======================================================
    # HAPUS DATASET
    # ======================================================

    st.subheader("🗑️ Hapus Dataset")

    st.warning(
        """
Seluruh dataset yang tersimpan pada database akan dihapus.

Proses ini **tidak dapat dibatalkan**.
        """
    )

    konfirmasi = st.checkbox(
        "Saya yakin ingin menghapus seluruh dataset."
    )

    if konfirmasi:

        if st.button(
            "Hapus Dataset",
            type="secondary",
            use_container_width=True
        ):

            try:

                delete_all_data()

                st.success(
                    "Dataset berhasil dihapus dari database."
                )

                st.rerun()

            except Exception as e:

                st.error(
                    f"Gagal menghapus dataset.\n\n{e}"
                )

    st.divider()

    # ======================================================
    # PETUNJUK
    # ======================================================

    st.subheader("📌 Petunjuk")

    st.markdown("""
- Upload dataset transaksi Shopee Food.
- Pastikan dataset sesuai dengan format penelitian.
- Klik **Simpan Dataset ke Database**.
- Dataset yang tersimpan akan digunakan pada menu **Preprocessing**.
- Seluruh proses cleaning, feature engineering, dan normalisasi dilakukan pada menu **Preprocessing**.
""")
