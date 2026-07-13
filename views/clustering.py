import streamlit as st
import pandas as pd
import plotly.express as px

from utils.clustering import (
    perform_clustering,
    cluster_summary,
    cluster_profile
)


# ==========================================================
# HALAMAN CLUSTERING
# ==========================================================

def show_clustering():

    # ======================================================
    # HEADER
    # ======================================================

    st.title("📊 Hasil Clustering")

    st.caption(
        """
Analisis pola transaksi Shopee Food menggunakan
algoritma K-Means Clustering.
        """
    )

    st.divider()

    # ======================================================
    # CEK PREPROCESSING
    # ======================================================

    if "normalized_df" not in st.session_state:

        st.warning(
            """
Silakan lakukan **Preprocessing**
terlebih dahulu sebelum menjalankan
proses clustering.
            """
        )

        return

    normalized_df = st.session_state["normalized_df"]

    # ======================================================
    # INFORMASI
    # ======================================================

    st.info(
        """
Klik tombol **Jalankan Clustering**
untuk mengelompokkan transaksi menjadi
dua kelompok berdasarkan karakteristik transaksi.
        """
    )

    # ======================================================
    # BUTTON
    # ======================================================

    col1, col2 = st.columns([1, 5])

    with col1:

        mulai = st.button(

            "🚀 Jalankan",

            type="primary",

            use_container_width=True

        )

    with col2:

        st.empty()

    if not mulai:

        return

    # ======================================================
    # PROSES KMEANS
    # ======================================================

    with st.spinner("Sedang melakukan proses clustering..."):

        result_df, centroid_df = perform_clustering(

            normalized_df,

            n_clusters=2

        )

    st.success(
        "Proses clustering berhasil dilakukan."
    )

    # ======================================================
    # SIMPAN SESSION
    # ======================================================

    st.session_state["cluster_df"] = result_df

    st.session_state["centroid_df"] = centroid_df

    # ======================================================
    # RINGKASAN
    # ======================================================

    summary = cluster_summary(result_df)

    total_data = len(result_df)

    tinggi = int(summary.iloc[0]["Jumlah"])

    normal = int(summary.iloc[1]["Jumlah"])

    tinggi_pct = float(summary.iloc[0]["Persentase"])

    normal_pct = float(summary.iloc[1]["Persentase"])

    st.divider()
        # ======================================================
    # DASHBOARD KPI
    # ======================================================

    st.subheader("📌 Ringkasan Hasil Clustering")

    st.markdown(
        f"""
        <div class="dashboard-row">

            <div class="dashboard-card">

                <div class="dashboard-icon">📦</div>

                <div class="dashboard-value">
                    {total_data}
                </div>

                <div class="dashboard-label">
                    Total Transaksi
                </div>

            </div>

            <div class="dashboard-card">

                <div class="dashboard-icon orange">
                    🟧
                </div>

                <div class="dashboard-value">
                    {tinggi}
                </div>

                <div class="dashboard-label">
                    Prioritas Tinggi
                </div>

                <div class="dashboard-percent">
                    {tinggi_pct:.2f}%
                </div>

            </div>

            <div class="dashboard-card">

                <div class="dashboard-icon green">
                    🟩
                </div>

                <div class="dashboard-value">
                    {normal}
                </div>

                <div class="dashboard-label">
                    Prioritas Normal
                </div>

                <div class="dashboard-percent">
                    {normal_pct:.2f}%
                </div>

            </div>

            <div class="dashboard-card">

                <div class="dashboard-icon">
                    🧠
                </div>

                <div class="dashboard-value">
                    2
                </div>

                <div class="dashboard-label">
                    Jumlah Cluster
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # ======================================================
    # RINGKASAN ANALISIS
    # ======================================================

    st.subheader("📖 Ringkasan Analisis")

    st.markdown(
        f"""
Berdasarkan hasil proses **K-Means Clustering**, sebanyak
**{total_data} transaksi** berhasil dikelompokkan menjadi
**2 kelompok transaksi**.

- 🟧 **Transaksi Prioritas Tinggi** berjumlah **{tinggi} transaksi**
  atau sekitar **{tinggi_pct:.2f}%** dari seluruh data.

- 🟩 **Transaksi Prioritas Normal** berjumlah **{normal} transaksi**
  atau sekitar **{normal_pct:.2f}%** dari seluruh data.

Informasi ini memberikan gambaran mengenai pola transaksi
yang dapat digunakan sebagai dasar dalam menentukan prioritas
pelayanan dan pengelolaan operasional pada Buffet The Padang Pasir.
        """
    )

    st.divider()
        # ======================================================
    # VISUALISASI CLUSTER
    # ======================================================

    st.subheader("📈 Visualisasi Hasil Clustering")

    col_chart, col_table = st.columns([2, 1])

    # ======================================================
    # GRAFIK BAR
    # ======================================================

    with col_chart:

        chart_df = pd.DataFrame({

            "Kategori": [

                "Prioritas Tinggi",

                "Prioritas Normal"

            ],

            "Jumlah": [

                tinggi,

                normal

            ]

        })

        fig = px.bar(

            chart_df,

            x="Kategori",

            y="Jumlah",

            text="Jumlah",

            color="Kategori",

            color="Kategori",

            color_discrete_map={

                "Prioritas Tinggi": "#F57C00",

                "Prioritas Normal": "#43A047"

            }

        )

        fig.update_layout(

            height=430,

            plot_bgcolor="white",

            paper_bgcolor="white",

            showlegend=False,

            margin=dict(

                l=20,

                r=20,

                t=30,

                b=20

            )

        )

        fig.update_traces(

            textposition="outside",

            marker_line_width=0

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    # ======================================================
    # TABEL RINGKASAN
    # ======================================================

    with col_table:

        st.markdown("### 📋 Ringkasan")

        summary_view = pd.DataFrame({

            "Kategori": [

                "Prioritas Tinggi",

                "Prioritas Normal"

            ],

            "Jumlah": [

                tinggi,

                normal

            ],

            "Persentase": [

                f"{tinggi_pct:.2f}%",

                f"{normal_pct:.2f}%"

            ]

        })

        st.dataframe(

            summary_view,

            hide_index=True,

            use_container_width=True

        )

        st.markdown("---")

        st.markdown("### ℹ️ Informasi")

        st.info(

            """
Grafik menunjukkan distribusi jumlah transaksi
pada masing-masing cluster hasil
K-Means Clustering.

Semakin tinggi batang grafik,
semakin banyak transaksi yang
termasuk pada kelompok tersebut.
            """

        )

    st.divider()
        # ======================================================
    # DETAIL CENTROID
    # ======================================================

    st.subheader("📐 Detail Nilai Centroid")

    with st.expander("Lihat Nilai Centroid"):

        st.markdown(
            """
Nilai centroid merupakan titik pusat setiap cluster hasil
K-Means Clustering.

Semakin besar nilai centroid pada suatu variabel,
maka semakin besar karakteristik variabel tersebut
pada cluster yang bersangkutan.
            """
        )

        st.dataframe(

            centroid_df.round(4),

            hide_index=True,

            use_container_width=True

        )

    st.divider()

    # ======================================================
    # INTERPRETASI
    # ======================================================

    st.subheader("🎯 Interpretasi Hasil Clustering")

    left, right = st.columns(2)
        with left:

        with st.container(border=True):

            st.markdown(
                """
### 🟧 Transaksi Prioritas Tinggi

Kelompok transaksi yang memiliki karakteristik
nilai transaksi, jumlah pesanan,
dan waktu pelayanan yang relatif lebih tinggi.
                """
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(

                    "Jumlah",

                    tinggi

                )

            with col2:

                st.metric(

                    "Persentase",

                    f"{tinggi_pct:.2f}%"

                )

            st.markdown("---")

            st.markdown("#### 📌 Karakteristik")

            st.markdown("""

- Nilai transaksi relatif tinggi

- Jumlah pesanan lebih banyak

- Variasi menu lebih beragam

- Waktu persiapan relatif lebih lama

- Menjadi prioritas ketika jam operasional ramai

""")

            st.markdown("#### 💡 Rekomendasi")

            st.markdown("""

- Prioritaskan transaksi pada kelompok ini.

- Pastikan stok bahan baku tersedia.

- Siapkan bahan sebelum jam ramai.

- Tambahkan tenaga kerja ketika volume meningkat.

- Pantau waktu penyelesaian pesanan.

""")
                # ======================================================
    # CARD PRIORITAS NORMAL
    # ======================================================

    with right:

        with st.container(border=True):

            st.markdown(
                """
### 🟩 Transaksi Prioritas Normal

Kelompok transaksi yang memiliki karakteristik
nilai transaksi, jumlah pesanan,
dan waktu pelayanan yang relatif lebih rendah.
                """
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(

                    "Jumlah",

                    normal

                )

            with col2:

                st.metric(

                    "Persentase",

                    f"{normal_pct:.2f}%"

                )

            st.markdown("---")

            st.markdown("#### 📌 Karakteristik")

            st.markdown("""

- Nilai transaksi relatif lebih rendah

- Jumlah pesanan lebih sedikit

- Variasi menu lebih sederhana

- Waktu persiapan relatif lebih singkat

- Diproses menggunakan alur operasional standar

""")

            st.markdown("#### 💡 Rekomendasi")

            st.markdown("""

- Pertahankan kualitas pelayanan.

- Gunakan SOP yang telah berjalan.

- Siapkan bahan baku sebelum jam operasional.

- Tingkatkan nilai transaksi melalui promosi.

- Evaluasi menu yang kurang diminati pelanggan.

""")

    st.divider()

    # ======================================================
    # PROFIL CLUSTER
    # ======================================================

    st.subheader("📊 Profil Rata-rata Setiap Cluster")

    profile_df = cluster_profile(result_df)

    st.dataframe(

        profile_df,

        use_container_width=True

    )

    st.divider()

    # ======================================================
    # FOOTER
    # ======================================================

    st.success(
        """
Proses clustering berhasil dilakukan.

Hasil pengelompokan ini dapat digunakan sebagai
acuan dalam memahami pola transaksi pelanggan
serta membantu pengambilan keputusan operasional
pada Buffet The Padang Pasir.
        """
    )
