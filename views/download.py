import streamlit as st

from utils.report import (
    export_pdf,
    export_excel,
    export_csv
)

from utils.clustering import (
    cluster_summary,
    cluster_profile
)


# ==========================================================
# DOWNLOAD
# ==========================================================

def show_download():

    st.title("📥 Download Hasil Analisis")

    st.caption(
        """
Mengunduh hasil analisis pola transaksi
Shopee Food dalam format PDF, Excel,
dan CSV.
        """
    )

    st.divider()

    # ======================================================
    # CEK HASIL CLUSTERING
    # ======================================================

    if (

        "cluster_df" not in st.session_state

        or

        "centroid_df" not in st.session_state

    ):

        st.warning(
            """
Hasil clustering belum tersedia.

Silakan lakukan proses clustering terlebih dahulu.
            """
        )

        return

    # ======================================================
    # LOAD DATA
    # ======================================================

    cluster_df = st.session_state["cluster_df"]

    centroid_df = st.session_state["centroid_df"]

    summary_df = cluster_summary(cluster_df)

    profile_df = cluster_profile(cluster_df)

    total_data = len(cluster_df)

    tinggi = int(summary_df.iloc[0]["Jumlah"])

    normal = int(summary_df.iloc[1]["Jumlah"])

    tinggi_pct = float(summary_df.iloc[0]["Persentase"])

    normal_pct = float(summary_df.iloc[1]["Persentase"])

    # ======================================================
    # INFORMASI
    # ======================================================

    st.divider()

    # ======================================================
    # DOWNLOAD PDF
    # ======================================================

    st.subheader("📄 Laporan Hasil Analisis (PDF)")

    st.write(
        """
Berisi laporan lengkap hasil analisis
yang disusun dalam bentuk dokumen dan
mudah dipahami oleh pihak
**Buffet The Padang Pasir**.
        """
    )

    pdf = export_pdf(

        summary_df,

        centroid_df,

        profile_df,

        total_data,

        tinggi,

        normal,

        tinggi_pct,

        normal_pct

    )

    st.download_button(

        label="📄 Download Laporan PDF",

        data=pdf,

        file_name="Laporan_Hasil_Analisis_ShopeeFood_Buffet_The_Padang_Pasir.pdf",

        mime="application/pdf",

        use_container_width=True

    )

    st.divider()

    # ======================================================
    # DOWNLOAD EXCEL
    # ======================================================

    st.subheader("📊 Dataset Hasil Clustering (Excel)")

    st.write(
        """
Berisi dataset hasil clustering
beserta label cluster dalam format Excel.
        """
    )

    excel = export_excel(

        cluster_df

    )

    st.download_button(

        label="📊 Download Excel",

        data=excel,

        file_name="Hasil_Clustering_ShopeeFood.xlsx",

        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

        use_container_width=True

    )

    st.divider()

    # ======================================================
    # DOWNLOAD CSV
    # ======================================================

    st.subheader("📋 Dataset Hasil Clustering (CSV)")

    st.write(
        """
Berisi dataset hasil clustering
beserta label cluster dalam format CSV.
        """
    )

    csv = export_csv(

        cluster_df

    )

    st.download_button(

        label="📋 Download CSV",

        data=csv,

        file_name="Hasil_Clustering_ShopeeFood.csv",

        mime="text/csv",

        use_container_width=True

    )

    st.divider()

    st.success(
        """
Seluruh hasil analisis telah siap diunduh.

Silakan pilih format file sesuai kebutuhan.
        """
    )
