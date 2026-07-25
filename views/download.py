import streamlit as st

from utils.report import (
    export_pdf,
    export_excel,
    export_csv
)

from utils.clustering import (
    cluster_summary,
    cluster_profile,
    identify_high_service_cluster,
    cluster_name
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

    final_cluster_df = st.session_state["final_cluster_df"]

    centroid_df = st.session_state["centroid_df"]

    summary_df = cluster_summary(cluster_df)

    profile_df = cluster_profile(cluster_df)

    high_service_cluster = identify_high_service_cluster(
        profile_df
    )

    low_service_cluster = (
        1 if high_service_cluster == 0 else 0
    )

    total_data = len(cluster_df)

    tinggi = int(
        summary_df.loc[
            summary_df["Cluster"] == high_service_cluster,
            "Jumlah"
        ].values[0]
    )

    normal = int(
        summary_df.loc[
            summary_df["Cluster"] == low_service_cluster,
            "Jumlah"
        ].values[0]
    )

    tinggi_pct = float(
        summary_df.loc[
            summary_df["Cluster"] == high_service_cluster,
            "Persentase"
        ].values[0]
    )

    normal_pct = float(
        summary_df.loc[
            summary_df["Cluster"] == low_service_cluster,
            "Persentase"
        ].values[0]
    )

    # ======================================================
    # INFORMASI
    # ======================================================

    st.info(
        """
Seluruh hasil analisis dapat diunduh
sesuai kebutuhan.

• PDF digunakan sebagai laporan hasil analisis.

• Excel digunakan untuk pengolahan data lanjutan.

• CSV digunakan untuk pertukaran data dengan aplikasi lain.
        """
    )

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
        final_cluster_df
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
