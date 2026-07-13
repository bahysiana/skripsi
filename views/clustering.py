import streamlit as st
import pandas as pd

from utils.clustering import (
    run_kmeans,
    cluster_summary,
    cluster_profile
)


# ==========================================================
# CLUSTERING
# ==========================================================

def show_clustering():

    st.title("📊 Clustering")

    st.caption(
        "Analisis Pola Transaksi Menggunakan Metode K-Means Clustering."
    )

    st.divider()

    # ======================================================
    # CEK PREPROCESSING
    # ======================================================

    if "normalized_df" not in st.session_state:

        st.warning(
            """
Dataset hasil preprocessing belum tersedia.

Silakan lakukan preprocessing terlebih dahulu.
            """
        )

        return

    normalized_df = st.session_state["normalized_df"]

    # ======================================================
    # PREVIEW DATA
    # ======================================================

    st.subheader("📂 Dataset Hasil Preprocessing")

    st.dataframe(

        normalized_df,

        use_container_width=True,

        hide_index=True

    )

    st.divider()

    # ======================================================
    # PROSES CLUSTERING
    # ======================================================

    if st.button(

        "🚀 Proses Clustering",

        type="primary",

        use_container_width=True

    ):

        with st.spinner("Sedang menjalankan K-Means..."):

            result_df, centroid_df, model = run_kmeans(

                normalized_df

            )

        summary_df = cluster_summary(result_df)

        profile_df = cluster_profile(result_df)

        st.session_state["cluster_result"] = result_df
        st.session_state["cluster_centroid"] = centroid_df
        st.session_state["cluster_summary"] = summary_df
        st.session_state["cluster_profile"] = profile_df

        st.success(
            "Proses Clustering berhasil dilakukan."
        )

        st.divider()

        # ==================================================
        # HASIL CLUSTER
        # ==================================================

        st.subheader("📋 Hasil Clustering")

        st.dataframe(

            result_df,

            use_container_width=True,

            hide_index=True

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
        # RINGKASAN
        # ==================================================

        st.subheader("📈 Ringkasan Cluster")

        st.dataframe(

            summary_df,

            use_container_width=True,

            hide_index=True

        )

        st.divider()

        # ==================================================
        # PROFIL CLUSTER
        # ==================================================

        st.subheader("📊 Profil Cluster")

        st.dataframe(

            profile_df,

            use_container_width=True

        )

        st.divider()

        st.success(
            """
Proses clustering selesai.

Silakan lanjut melihat interpretasi dan rekomendasi cluster.
            """
        )
