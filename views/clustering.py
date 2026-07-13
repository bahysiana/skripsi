import streamlit as st
import pandas as pd
import plotly.express as px

from utils.clustering import (
    run_kmeans,
    cluster_summary,
    cluster_profile
)

from utils.interpretation import (
    generate_interpretation
)


# ==========================================================
# CLUSTERING
# ==========================================================

def show_clustering():

    st.title("📊 Clustering")

    st.caption(
        "Analisis Pola Transaksi Shopee Food Menggunakan Metode K-Means Clustering (K = 2)"
    )

    st.divider()

    # ======================================================
    # CEK PREPROCESSING
    # ======================================================

    if "normalized_df" not in st.session_state:

        st.warning(
            "Silakan lakukan preprocessing terlebih dahulu."
        )

        return

    normalized_df = st.session_state["normalized_df"]

    st.subheader("📂 Dataset Hasil Preprocessing")

    st.dataframe(
        normalized_df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ======================================================
    # BUTTON
    # ======================================================

    if st.button(
        "🚀 Proses Clustering",
        type="primary",
        use_container_width=True
    ):

        with st.spinner("Sedang melakukan clustering..."):

            result_df, centroid_df, model = run_kmeans(
                normalized_df
            )

            summary_df = cluster_summary(result_df)

            profile_df = cluster_profile(result_df)

            interpretation = generate_interpretation(
                profile_df
            )

        st.session_state["cluster_result"] = result_df
        st.session_state["cluster_centroid"] = centroid_df
        st.session_state["cluster_summary"] = summary_df
        st.session_state["cluster_profile"] = profile_df

        st.success("Clustering berhasil dilakukan.")

        st.divider()

        # ==================================================
        # HASIL
        # ==================================================

        st.subheader("📋 Hasil Clustering")

        st.dataframe(
            result_df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        # ==================================================
        # JUMLAH CLUSTER
        # ==================================================

        st.subheader("📈 Jumlah Anggota Cluster")

        st.dataframe(
            summary_df,
            use_container_width=True,
            hide_index=True
        )

        fig = px.bar(
            summary_df,
            x="Cluster",
            y="Jumlah_Data",
            text="Jumlah_Data"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.divider()

        # ==================================================
        # CENTROID
        # ==================================================

        st.subheader("🎯 Nilai Centroid")

        st.dataframe(
            centroid_df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        # ==================================================
        # PROFIL
        # ==================================================

        st.subheader("📊 Profil Cluster")

        st.dataframe(
            profile_df,
            use_container_width=True
        )

        st.divider()

        # ==================================================
        # INTERPRETASI
        # ==================================================

        st.subheader("📌 Interpretasi Cluster")

        for item in interpretation:

            st.markdown(f"## Cluster {item['cluster']}")

            st.success(item["nama_cluster"])

            st.write("### Karakteristik")

            for k in item["karakteristik"]:

                st.write(f"✔ {k}")

            st.write("### Rekomendasi")

            for r in item["rekomendasi"]:

                st.write(f"• {r}")

            st.divider()

        # ==================================================
        # KESIMPULAN
        # ==================================================

        st.subheader("📝 Kesimpulan")

        st.info(
            """
Hasil K-Means Clustering berhasil mengelompokkan transaksi Shopee Food menjadi dua kelompok berdasarkan karakteristik transaksi.

Cluster dengan beban pelayanan tinggi memerlukan perhatian lebih dalam proses operasional karena memiliki jumlah pesanan, variasi menu, dan waktu persiapan yang lebih besar.

Cluster dengan beban pelayanan rendah memiliki karakteristik transaksi yang lebih sederhana sehingga dapat ditangani menggunakan alur operasional yang telah berjalan.

Hasil clustering ini dapat dimanfaatkan sebagai pendukung pengambilan keputusan operasional pada Toko Buffet The Padang Pasir.
            """
        )
