import streamlit as st

from utils.report import (
    export_csv,
    export_excel
)


# ==========================================================
# DOWNLOAD
# ==========================================================

def show_download():

    st.title("⬇ Download Hasil")

    st.caption(
        "Mengunduh hasil clustering transaksi Shopee Food."
    )

    st.divider()

    # ======================================================
    # CEK HASIL CLUSTER
    # ======================================================

    if "cluster_result" not in st.session_state:

        st.warning(
            """
Belum ada hasil clustering.

Silakan lakukan proses clustering terlebih dahulu.
            """
        )

        return

    df = st.session_state["cluster_result"]

    summary = st.session_state["cluster_summary"]

    centroid = st.session_state["cluster_centroid"]

    # ======================================================
    # PREVIEW
    # ======================================================

    st.subheader("📋 Preview Hasil Clustering")

    st.dataframe(

        df,

        use_container_width=True,

        hide_index=True

    )

    st.divider()

    # ======================================================
    # RINGKASAN
    # ======================================================

    st.subheader("📊 Ringkasan")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(

            "Jumlah Transaksi",

            len(df)

        )

    with col2:

        st.metric(

            "Jumlah Cluster",

            2

        )

    with col3:

        st.metric(

            "Centroid",

            len(centroid)

        )

    st.divider()

    st.subheader("📈 Ringkasan Cluster")

    st.dataframe(

        summary,

        use_container_width=True,

        hide_index=True

    )

    st.divider()

    # ======================================================
    # DOWNLOAD CSV
    # ======================================================

    csv = export_csv(df)

    st.download_button(

        label="⬇ Download CSV",

        data=csv,

        file_name="hasil_clustering.csv",

        mime="text/csv",

        use_container_width=True

    )

    # ======================================================
    # DOWNLOAD EXCEL
    # ======================================================

    excel = export_excel(df)

    st.download_button(

        label="⬇ Download Excel",

        data=excel,

        file_name="hasil_clustering.xlsx",

        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

        use_container_width=True

    )

    st.divider()

    st.success(
        """
Hasil clustering berhasil dipersiapkan.

Silakan pilih format file yang ingin diunduh.
        """
    )
