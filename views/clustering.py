import streamlit as st
import pandas as pd
import plotly.express as px

from utils.clustering import perform_clustering


# ==========================================================
# CLUSTERING
# ==========================================================

def show_clustering():

    st.title("📊 Hasil Clustering Transaksi Shopee Food")

    st.caption(
        "Pengelompokan transaksi berdasarkan lima variabel penelitian menggunakan metode K-Means Clustering (K = 2)."
    )

    st.divider()

    # ======================================================
    # CEK PREPROCESSING
    # ======================================================

    if "normalized_df" not in st.session_state:

        st.warning(
            """
Silakan lakukan **Preprocessing**
terlebih dahulu sebelum menjalankan clustering.
            """
        )

        return

    normalized_df = st.session_state["normalized_df"]

    # ======================================================
    # PROSES CLUSTERING
    # ======================================================

    result_df, centroid_df = perform_clustering(
        normalized_df,
        n_clusters=2
    )

    st.session_state["cluster_df"] = result_df
    st.session_state["centroid_df"] = centroid_df

    # ======================================================
    # HITUNG JUMLAH CLUSTER
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

    tinggi = int(summary.iloc[0]["Jumlah"])
    normal = int(summary.iloc[1]["Jumlah"])

    tinggi_pct = summary.iloc[0]["Persentase"]
    normal_pct = summary.iloc[1]["Persentase"]

    # ======================================================
    # KPI CARD
    # ======================================================

    st.markdown("## 📌 Ringkasan Hasil Analisis")

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(

            label="📦 Total Transaksi",

            value=total,

            delta="Data Dianalisis"

        )

    with c2:

        st.metric(

            label="🟧 Prioritas Tinggi",

            value=tinggi,

            delta=f"{tinggi_pct}%"

        )

    with c3:

        st.metric(

            label="🟩 Prioritas Normal",

            value=normal,

            delta=f"{normal_pct}%"

        )

    with c4:

        st.metric(

            label="🧠 Jumlah Cluster",

            value="2",

            delta="K-Means"

        )

    st.divider()

    # ======================================================
    # GRAFIK + TABEL
    # ======================================================

    left, right = st.columns([1.2, 1])

    # ======================================================
    # GRAFIK
    # ======================================================

    with left:

        st.subheader("📈 Distribusi Transaksi")

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

            x="Jumlah",

            y="Kategori",

            orientation="h",

            text="Jumlah",

            color="Kategori",

            color_discrete_map={

                "Prioritas Tinggi": "#ff7a00",

                "Prioritas Normal": "#28a745"

            }

        )

        fig.update_layout(

            height=380,

            showlegend=False,

            plot_bgcolor="white",

            paper_bgcolor="white",

            margin=dict(

                l=10,

                r=10,

                t=20,

                b=20

            )

        )

        fig.update_traces(

            textposition="outside"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    # ======================================================
    # TABEL RINGKASAN
    # ======================================================

    with right:

        st.subheader("📋 Ringkasan Cluster")

        ringkasan = pd.DataFrame({

            "Kategori": [

                "Prioritas Tinggi",

                "Prioritas Normal"

            ],

            "Jumlah Transaksi": [

                tinggi,

                normal

            ],

            "Persentase": [

                f"{tinggi_pct}%",

                f"{normal_pct}%"

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

with st.expander("📐 Detail Perhitungan K-Means (Nilai Centroid)"):

    st.info(
        """
Nilai centroid merupakan titik pusat masing-masing cluster
hasil proses K-Means. Nilai ini digunakan sebagai dasar
pengelompokan transaksi berdasarkan lima variabel penelitian.
        """
    )

    st.dataframe(
        centroid_df.round(4),
        hide_index=True,
        use_container_width=True
    )

st.divider()

# ======================================================
# INTERPRETASI CLUSTER
# ======================================================

st.subheader("🎯 Interpretasi Hasil Clustering")

left_card, right_card = st.columns(2)

# ======================================================
# CLUSTER PRIORITAS TINGGI
# ======================================================

with left_card:

    st.markdown(
        """
### 🟧 Transaksi Prioritas Tinggi

Transaksi dengan karakteristik beban pelayanan lebih tinggi.
"""
    )

    m1, m2 = st.columns(2)

    with m1:

        st.metric(
            "Jumlah Transaksi",
            tinggi
        )

    with m2:

        st.metric(
            "Persentase",
            f"{tinggi_pct}%"
        )

    st.markdown("### Karakteristik")

    st.success(
        """
✅ Nilai transaksi relatif lebih tinggi

✅ Jumlah pesanan lebih banyak

✅ Variasi menu lebih beragam

✅ Membutuhkan waktu persiapan lebih lama

✅ Memerlukan perhatian lebih saat jam sibuk
"""
    )

    st.markdown("### 💡 Rekomendasi")

    st.info(
        """
• Prioritaskan transaksi pada kelompok ini agar pelayanan tetap optimal.

• Pastikan stok bahan baku selalu tersedia.

• Lakukan persiapan bahan sebelum jam operasional ramai.

• Atur pembagian tugas karyawan ketika volume pesanan meningkat.

• Evaluasi waktu penyelesaian pesanan agar tetap sesuai estimasi Shopee Food.

• Jadikan cluster ini sebagai acuan utama dalam penyusunan strategi operasional toko.
"""
    )

# ======================================================
# CLUSTER PRIORITAS NORMAL
# ======================================================

with right_card:

    st.markdown(
        """
### 🟩 Transaksi Prioritas Normal

Transaksi dengan karakteristik beban pelayanan lebih ringan.
"""
    )

    m3, m4 = st.columns(2)

    with m3:

        st.metric(
            "Jumlah Transaksi",
            normal
        )

    with m4:

        st.metric(
            "Persentase",
            f"{normal_pct}%"
        )

    st.markdown("### Karakteristik")

    st.success(
        """
✅ Nilai transaksi relatif lebih rendah

✅ Jumlah pesanan lebih sedikit

✅ Variasi menu lebih sederhana

✅ Waktu persiapan relatif lebih singkat

✅ Dapat diproses menggunakan alur operasional standar
"""
    )

    st.markdown("### 💡 Rekomendasi")

    st.info(
        """
• Pertahankan kualitas pelayanan yang sudah berjalan.

• Manfaatkan waktu luang untuk persiapan bahan baku.

• Dorong peningkatan nilai transaksi melalui paket menu atau promosi.

• Evaluasi menu yang kurang diminati pelanggan.

• Gunakan cluster ini sebagai dasar penyusunan strategi pelayanan harian.
"""
    )

st.divider()
