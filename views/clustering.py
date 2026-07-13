import streamlit as st
import pandas as pd

from utils.clustering import perform_clustering


# ==========================================================
# CLUSTERING
# ==========================================================

def show_clustering():

    # ======================================================
    # HEADER
    # ======================================================

    st.title("📊 Hasil Clustering")

    st.caption(
        """
Analisis pola transaksi Shopee Food menggunakan
metode K-Means Clustering dengan jumlah cluster (K = 2).
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
terlebih dahulu melalui menu Preprocessing.
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
untuk melakukan proses pengelompokan transaksi
menggunakan algoritma K-Means.
        """
    )

    # ======================================================
    # BUTTON
    # ======================================================

    if not st.button(

        "🚀 Jalankan Clustering",

        type="primary",

        use_container_width=True

    ):

        return

    # ======================================================
    # PROSES CLUSTERING
    # ======================================================

    with st.spinner("Sedang melakukan clustering..."):

        cluster_df, centroid_df = perform_clustering(

            normalized_df,

            n_clusters=2

        )

    st.success("Clustering berhasil dilakukan.")

    # ======================================================
    # SIMPAN SESSION
    # ======================================================

    st.session_state["cluster_df"] = cluster_df

    st.session_state["centroid_df"] = centroid_df

    # ======================================================
    # RINGKASAN CLUSTER
    # ======================================================

    summary = (

        cluster_df["Cluster"]

        .value_counts()

        .sort_index()

        .reset_index()

    )

    summary.columns = [

        "Cluster",

        "Jumlah"

    ]

    total_data = len(cluster_df)

    summary["Persentase"] = (

        summary["Jumlah"]

        / total_data

        * 100

    ).round(2)

    # ======================================================
    # NAMA CLUSTER
    # ======================================================

    summary["Kategori"] = [

        "Transaksi Prioritas Tinggi",

        "Transaksi Prioritas Normal"

    ]

    tinggi = int(summary.iloc[0]["Jumlah"])

    normal = int(summary.iloc[1]["Jumlah"])

    tinggi_pct = float(summary.iloc[0]["Persentase"])

    normal_pct = float(summary.iloc[1]["Persentase"])

    st.divider()
        # ======================================================
    # RINGKASAN ANALISIS
    # ======================================================

    st.subheader("📌 Ringkasan Hasil Analisis")

    st.info(
        f"""
Dari **{total_data} transaksi** yang dianalisis menggunakan metode
**K-Means Clustering**, diperoleh:

- **{tinggi} transaksi ({tinggi_pct:.2f}%)** termasuk kategori **Transaksi Prioritas Tinggi**.
- **{normal} transaksi ({normal_pct:.2f}%)** termasuk kategori **Transaksi Prioritas Normal**.

Hasil ini dapat digunakan sebagai dasar dalam menentukan prioritas pelayanan
dan pengambilan keputusan operasional pada Buffet The Padang Pasir.
"""
    )

    st.divider()

    # ======================================================
    # KPI CARD
    # ======================================================

    st.subheader("📊 Statistik Clustering")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            label="📦 Total Transaksi",
            value=total_data
        )

    with col2:

        st.metric(
            label="🟧 Prioritas Tinggi",
            value=tinggi,
            delta=f"{tinggi_pct:.2f}%"
        )

    with col3:

        st.metric(
            label="🟩 Prioritas Normal",
            value=normal,
            delta=f"{normal_pct:.2f}%"
        )

    with col4:

        st.metric(
            label="🧠 Jumlah Cluster",
            value="2"
        )

    st.divider()

    # ======================================================
    # GRAFIK DAN TABEL
    # ======================================================

    left, right = st.columns([1.7, 1])

    # ======================================================
    # GRAFIK
    # ======================================================

    with left:

        st.subheader("📈 Distribusi Hasil Clustering")

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

        import plotly.express as px

        fig = px.bar(

            chart_df,

            x="Kategori",

            y="Jumlah",

            text="Jumlah",

            color="Kategori",

            color_discrete_map={

                "Prioritas Tinggi": "#ff7a00",

                "Prioritas Normal": "#34a853"

            }

        )

        fig.update_layout(

            height=420,

            showlegend=False,

            plot_bgcolor="white",

            paper_bgcolor="white",

            title=None

        )

        fig.update_traces(

            textposition="outside"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    # ======================================================
    # RINGKASAN CLUSTER
    # ======================================================

    with right:

        st.subheader("📋 Ringkasan Cluster")

        ringkasan_df = pd.DataFrame({

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

            ringkasan_df,

            hide_index=True,

            use_container_width=True

        )

    st.divider()
        # ======================================================
    # DETAIL CENTROID
    # ======================================================

    st.subheader("📐 Detail Hasil Perhitungan")

    with st.expander("Lihat Nilai Centroid"):

        st.markdown("""
Nilai centroid merupakan titik pusat masing-masing cluster yang
dihasilkan oleh algoritma K-Means. Informasi ini digunakan sebagai
acuan dalam proses pengelompokan transaksi.
        """)

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
        # ======================================================
    # CARD PRIORITAS TINGGI
    # ======================================================

    with left:

        st.markdown(
            """
            <div class="cluster-box cluster-high">
            <div class="cluster-title">
            🟧 Transaksi Prioritas Tinggi
            </div>

            <div class="cluster-desc">
            Kelompok transaksi dengan nilai transaksi, jumlah pesanan,
            variasi menu, dan waktu pelayanan yang relatif lebih tinggi.
            </div>
            """,
            unsafe_allow_html=True
        )

        # -----------------------------
        # KPI
        # -----------------------------

        col_a, col_b = st.columns(2)

        with col_a:

            st.markdown(f"""
            <div class="mini-card">
                <div class="mini-number">{tinggi}</div>
                <div class="mini-title">Jumlah Transaksi</div>
            </div>
            """,
            unsafe_allow_html=True)

        with col_b:

            st.markdown(f"""
            <div class="mini-card">
                <div class="mini-number">{tinggi_pct:.2f}%</div>
                <div class="mini-title">Persentase</div>
            </div>
            """,
            unsafe_allow_html=True)

        st.markdown("### 📌 Karakteristik")

        st.markdown("""
- ✅ Nilai transaksi relatif lebih tinggi.
- ✅ Jumlah pesanan lebih banyak.
- ✅ Variasi menu lebih beragam.
- ✅ Waktu persiapan lebih lama.
- ✅ Memerlukan perhatian lebih ketika jam operasional ramai.
        """)

        st.markdown("### 💡 Rekomendasi")

        st.success("""
1. Prioritaskan transaksi pada kelompok ini ketika antrean meningkat.

2. Pastikan stok bahan baku selalu tersedia.

3. Lakukan persiapan bahan sebelum jam sibuk.

4. Tambahkan tenaga kerja ketika volume transaksi meningkat.

5. Pantau waktu penyelesaian agar sesuai estimasi Shopee Food.
        """)

        st.markdown("</div>", unsafe_allow_html=True)
            # ======================================================
    # CARD PRIORITAS NORMAL
    # ======================================================

    with right:

        st.markdown(
            """
            <div class="cluster-box cluster-normal">
            <div class="cluster-title">
            🟩 Transaksi Prioritas Normal
            </div>

            <div class="cluster-desc">
            Kelompok transaksi dengan nilai transaksi, jumlah pesanan,
            variasi menu, dan waktu pelayanan yang relatif lebih rendah.
            </div>
            """,
            unsafe_allow_html=True
        )

        # -----------------------------
        # KPI
        # -----------------------------

        col_a, col_b = st.columns(2)

        with col_a:

            st.markdown(
                f"""
                <div class="mini-card">
                    <div class="mini-number">
                        {normal}
                    </div>

                    <div class="mini-title">
                        Jumlah Transaksi
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col_b:

            st.markdown(
                f"""
                <div class="mini-card">
                    <div class="mini-number">
                        {normal_pct:.2f}%
                    </div>

                    <div class="mini-title">
                        Persentase
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # -----------------------------
        # KARAKTERISTIK
        # -----------------------------

        st.markdown("### 📌 Karakteristik")

        st.markdown("""
- ✅ Nilai transaksi relatif lebih rendah.
- ✅ Jumlah pesanan lebih sedikit.
- ✅ Variasi menu lebih sederhana.
- ✅ Waktu persiapan relatif lebih singkat.
- ✅ Dapat diproses menggunakan alur operasional standar.
        """)

        # -----------------------------
        # REKOMENDASI
        # -----------------------------

        st.markdown("### 💡 Rekomendasi")

        st.info("""
1. Pertahankan kualitas pelayanan yang sudah berjalan.

2. Gunakan prosedur operasional standar dalam proses pelayanan.

3. Manfaatkan waktu senggang untuk menyiapkan bahan baku.

4. Tingkatkan nilai transaksi melalui paket menu atau promosi.

5. Evaluasi menu yang kurang diminati pelanggan sebagai bahan pengembangan produk.
        """)

        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    # ======================================================
    # FOOTER
    # ======================================================

    st.success(
        """
Analisis clustering telah selesai dilakukan.

Hasil pengelompokan ini dapat digunakan sebagai dasar dalam
menentukan prioritas pelayanan transaksi Shopee Food pada
Buffet The Padang Pasir.
        """
    )
    
