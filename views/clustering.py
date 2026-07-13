import streamlit as st
import pandas as pd
import plotly.express as px

from utils.clustering import perform_clustering


# ==========================================================
# CLUSTERING
# ==========================================================

def show_clustering():

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
terlebih dahulu.
"""
        )

        return

    normalized_df = st.session_state["normalized_df"]

    # ======================================================
    # BUTTON
    # ======================================================

    col1, col2 = st.columns([1,5])

    with col1:

        mulai = st.button(
            "🚀 Jalankan",
            type="primary",
            use_container_width=True
        )

    with col2:

        st.info(
            "Tekan tombol **Jalankan** untuk melakukan proses K-Means Clustering."
        )

    if not mulai:

        return

    # ======================================================
    # CLUSTERING
    # ======================================================

    with st.spinner("Melakukan proses clustering..."):

        result_df, centroid_df = perform_clustering(

            normalized_df,

            n_clusters=2

        )

    st.success("Clustering berhasil dilakukan.")

    st.session_state["cluster_df"] = result_df
    st.session_state["centroid_df"] = centroid_df

    # ======================================================
    # RINGKASAN
    # ======================================================

    summary = (

        result_df["Cluster"]

        .value_counts()

        .sort_index()

        .reset_index()

    )

    summary.columns = [

        "Cluster",

        "Jumlah"

    ]

    total = len(result_df)

    summary["Persentase"] = (

        summary["Jumlah"]

        / total

        * 100

    ).round(2)

    # ======================================================
    # NAMA CLUSTER
    # ======================================================

    summary["Kategori"] = [

        "Prioritas Tinggi",

        "Prioritas Normal"

    ]

    tinggi = int(summary.iloc[0]["Jumlah"])

    normal = int(summary.iloc[1]["Jumlah"])

    tinggi_pct = float(summary.iloc[0]["Persentase"])

    normal_pct = float(summary.iloc[1]["Persentase"])

    st.divider()

    # ======================================================
    # KPI
    # ======================================================

    st.subheader("📌 Ringkasan Hasil Analisis")

    k1, k2, k3, k4 = st.columns(4)

    with k1:

        st.metric(

            "📦 Total Transaksi",

            total

        )

    with k2:

        st.metric(

            "🟧 Prioritas Tinggi",

            tinggi,

            f"{tinggi_pct}%"

        )

    with k3:

        st.metric(

            "🟩 Prioritas Normal",

            normal,

            f"{normal_pct}%"

        )

    with k4:

        st.metric(

            "🧠 Cluster",

            "2"

        )

    st.divider()

    # ======================================================
    # INFORMASI
    # ======================================================

    st.info(
        f"""
Dari **{total} transaksi** yang dianalisis,
sebanyak **{tinggi} transaksi ({tinggi_pct:.2f}%)**
termasuk kelompok **Prioritas Tinggi**.

Sedangkan **{normal} transaksi ({normal_pct:.2f}%)**
termasuk kelompok **Prioritas Normal**.
"""
    )

    st.divider()

    # ======================================================
    # GRAFIK
    # ======================================================

    left, right = st.columns([1.6,1])

    with left:

        st.subheader("📈 Distribusi Cluster")

        chart = pd.DataFrame({

            "Kategori":[

                "Prioritas Tinggi",

                "Prioritas Normal"

            ],

            "Jumlah":[

                tinggi,

                normal

            ]

        })

        fig = px.bar(

            chart,

            x="Kategori",

            y="Jumlah",

            color="Kategori",

            text="Jumlah",

            color_discrete_map={

                "Prioritas Tinggi":"#ff7a00",

                "Prioritas Normal":"#34a853"

            }

        )

        fig.update_layout(

            height=420,

            showlegend=False,

            plot_bgcolor="white",

            paper_bgcolor="white"

        )

        fig.update_traces(

            textposition="outside"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    with right:

        st.subheader("📋 Ringkasan Cluster")

        ringkasan = pd.DataFrame({

            "Kategori":[

                "Prioritas Tinggi",

                "Prioritas Normal"

            ],

            "Jumlah":[

                tinggi,

                normal

            ],

            "Persentase":[

                f"{tinggi_pct:.2f}%",

                f"{normal_pct:.2f}%"

            ]

        })

        st.dataframe(

            ringkasan,

            hide_index=True,

            use_container_width=True

        )

    st.divider()
    # ======================================================
# DETAIL CENTROID
# ======================================================

with st.expander("📐 Detail Nilai Centroid"):

    st.info(
        """
Nilai centroid merupakan titik pusat setiap cluster yang
dihasilkan oleh algoritma K-Means. Informasi ini digunakan
untuk kebutuhan analisis penelitian.
        """
    )

    st.dataframe(
        centroid_df.round(4),
        hide_index=True,
        use_container_width=True
    )

st.divider()

# ======================================================
# HASIL INTERPRETASI
# ======================================================

st.subheader("🎯 Interpretasi Hasil Clustering")

left, right = st.columns(2)

# ======================================================
# PRIORITAS TINGGI
# ======================================================
with left:

    st.markdown(f"""
<div class="cluster-box cluster-high">

<div class="cluster-title">
🟧 Transaksi Prioritas Tinggi
</div>

<div class="cluster-desc">
Kelompok transaksi dengan beban pelayanan tinggi.
</div>

<div class="mini-card">

<div class="mini-number">

{tinggi}

</div>

<div class="mini-title">

Jumlah Transaksi

</div>

</div>

<div class="mini-card">

<div class="mini-number">

{tinggi_pct:.2f}%

</div>

<div class="mini-title">

Persentase

</div>

</div>

<div class="section-title">

Karakteristik

</div>

<div class="check-list">

✅ Nilai transaksi lebih tinggi<br>

✅ Jumlah pesanan lebih banyak<br>

✅ Variasi menu lebih beragam<br>

✅ Waktu persiapan lebih lama<br>

✅ Membutuhkan perhatian lebih saat jam sibuk

</div>

<div class="section-title">

💡 Rekomendasi

</div>

<div class="rekom-card">

• Prioritaskan transaksi ini saat antrean padat.<br>

• Pastikan stok bahan baku tersedia.<br>

• Siapkan bahan sebelum jam operasional ramai.<br>

• Tambahkan tenaga kerja ketika volume meningkat.<br>

• Pantau waktu penyelesaian pesanan.

</div>

</div>
""", unsafe_allow_html=True)
    with right:

    st.markdown(f"""
<div class="cluster-box cluster-normal">

<div class="cluster-title">
🟩 Transaksi Prioritas Normal
</div>

<div class="cluster-desc">
Kelompok transaksi dengan beban pelayanan normal.
</div>

<div class="mini-card">

<div class="mini-number">

{normal}

</div>

<div class="mini-title">

Jumlah Transaksi

</div>

</div>

<div class="mini-card">

<div class="mini-number">

{normal_pct:.2f}%

</div>

<div class="mini-title">

Persentase

</div>

</div>

<div class="section-title">

Karakteristik

</div>

<div class="check-list">

✅ Nilai transaksi relatif rendah<br>

✅ Jumlah pesanan lebih sedikit<br>

✅ Variasi menu lebih sederhana<br>

✅ Waktu persiapan lebih singkat<br>

✅ Dapat diproses menggunakan SOP standar

</div>

<div class="section-title">

💡 Rekomendasi

</div>

<div class="rekom-card-green">

• Pertahankan kualitas pelayanan.<br>

• Gunakan alur operasional standar.<br>

• Siapkan bahan baku saat waktu senggang.<br>

• Tingkatkan nilai transaksi melalui promosi.<br>

• Evaluasi menu yang kurang diminati.

</div>

</div>
""", unsafe_allow_html=True)
