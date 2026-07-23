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
metode K-Means Clustering.
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
    # SESSION
    # ======================================================

    if "cluster_df" not in st.session_state:

        st.session_state["cluster_df"] = None

    if "centroid_df" not in st.session_state:

        st.session_state["centroid_df"] = None

    # ======================================================
    # INFORMASI
    # ======================================================

    st.info(
        """
Klik tombol **Jalankan Clustering**
untuk melakukan proses pengelompokan
data transaksi menggunakan metode
K-Means Clustering.
        """
    )

    # ======================================================
    # BUTTON
    # ======================================================

    col_btn, col_info = st.columns([1, 5])

    with col_btn:

        mulai = st.button(
            "🚀 Jalankan",
            type="primary",
            use_container_width=True
        )

    with col_info:

        st.empty()

    # ======================================================
    # PROSES CLUSTERING
    # ======================================================

    if mulai:

        with st.spinner(
            "Sedang melakukan proses clustering..."
        ):

            result_df, centroid_df = perform_clustering(
                normalized_df,
                n_clusters=2
            )

        st.session_state["cluster_df"] = result_df
        st.session_state["centroid_df"] = centroid_df

        st.success(
            "Proses clustering berhasil dilakukan."
        )

    # ======================================================
    # CEK HASIL
    # ======================================================

    if st.session_state["cluster_df"] is None:

        return

    result_df = st.session_state["cluster_df"]

    centroid_df = st.session_state["centroid_df"]

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
    # KPI
    # ======================================================

    st.subheader("📌 Ringkasan Hasil Clustering")

    k1, k2, k3, k4 = st.columns(4)

    with k1:

        st.metric(
            "📦 Total Transaksi",
            total_data
        )

    with k2:

        st.metric(
            "🟧 Beban Pelayanan Tinggi",
            tinggi,
            f"{tinggi_pct:.2f}%"
        )

    with k3:

        st.metric(
            "🟩 Beban Pelayanan Rendah",
            normal,
            f"{normal_pct:.2f}%"
        )

    with k4:

        st.metric(
            "🧠 Jumlah Cluster",
            "2"
        )

    st.divider()
        # ======================================================
    # RINGKASAN ANALISIS
    # ======================================================

    st.subheader("📖 Ringkasan Analisis")

    st.markdown(
        f"""
Berdasarkan proses **K-Means Clustering** terhadap
**{total_data} transaksi**, diperoleh hasil sebagai berikut.

- **{tinggi} transaksi ({tinggi_pct:.2f}%)**
  termasuk kelompok **Pola Transaksi dengan Beban Pelayanan Tinggi**.

- **{normal} transaksi ({normal_pct:.2f}%)**
  termasuk kelompok **Pola Transaksi dengan Beban Pelayanan Rendah**.

Hasil pengelompokan ini memberikan gambaran karakteristik
transaksi pelanggan yang dapat digunakan sebagai salah satu
dasar dalam mendukung pengambilan keputusan operasional
pada Buffet The Padang Pasir.
        """
    )

    st.divider()

    # ======================================================
    # VISUALISASI HASIL CLUSTERING
    # ======================================================

    st.subheader("📈 Visualisasi Hasil Clustering")

    col_chart, col_table = st.columns([2, 1])

    # ======================================================
    # GRAFIK
    # ======================================================

    with col_chart:

        chart_df = pd.DataFrame({

            "Kategori": [

                "Beban Pelayanan Tinggi",

                "Beban Pelayanan Rendah"

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

            color_discrete_map={

                "Beban Pelayanan Tinggi": "#F57C00",

                "Beban Pelayanan Rendah": "#34A853"

            }

        )

        fig.update_layout(

            height=430,

            showlegend=False,

            plot_bgcolor="white",

            paper_bgcolor="white",

            margin=dict(

                l=20,

                r=20,

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
    # RINGKASAN
    # ======================================================

    with col_table:

        st.subheader("📋 Ringkasan")

        ringkasan_df = pd.DataFrame({

            "Kategori": [

                "Beban Pelayanan Tinggi",

                "Beban Pelayanan Rendah"

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

        st.markdown("### ℹ️ Informasi")

        st.info(
            """
Grafik menunjukkan jumlah transaksi
yang termasuk pada masing-masing
cluster hasil K-Means Clustering.

Semakin tinggi jumlah transaksi,
semakin banyak data yang berada
pada kelompok tersebut.
            """
        )

    st.divider()

    # ======================================================
    # DETAIL NILAI CENTROID
    # ======================================================

    st.subheader("📐 Detail Nilai Centroid")

    with st.expander("Lihat Nilai Centroid"):

        st.markdown(
            """
Centroid merupakan titik pusat
dari setiap cluster yang dihasilkan
oleh algoritma K-Means.

Nilai centroid digunakan sebagai
acuan dalam menentukan karakteristik
masing-masing cluster.
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

    # ======================================================
    # BEBAN PELAYANAN TINGGI
    # ======================================================

    with left:

        with st.container(border=True):

            st.markdown(
                "## 🟧 Pola Transaksi dengan Beban Pelayanan Tinggi"
            )

            st.caption(
                """
Kelompok transaksi dengan nilai transaksi,
jumlah pesanan, variasi menu, dan waktu
persiapan yang relatif lebih tinggi.
                """
            )

            st.divider()

            c1, c2 = st.columns(2)

            with c1:

                st.metric(
                    "Jumlah Transaksi",
                    tinggi
                )

            with c2:

                st.metric(
                    "Persentase",
                    f"{tinggi_pct:.2f}%"
                )

            st.divider()

            st.markdown("### 📌 Karakteristik")

            karakteristik_tinggi = [

                "Nilai transaksi relatif lebih tinggi.",

                "Jumlah pesanan lebih banyak.",

                "Variasi menu lebih beragam.",

                "Waktu persiapan relatif lebih lama."

            ]

            for item in karakteristik_tinggi:

                st.markdown(f"✅ {item}")

            st.divider()

            st.markdown("### 💡 Rekomendasi")

            rekomendasi_tinggi = [

                "Prioritaskan penanganan transaksi pada kelompok ini agar proses pelayanan tetap optimal.",

                "Pastikan ketersediaan bahan baku untuk memenuhi kebutuhan transaksi dengan beban pelayanan tinggi.",

                "Atur pembagian tugas karyawan secara efektif agar proses pelayanan dapat dilakukan secara lebih optimal.",

                "Lakukan pemantauan terhadap waktu persiapan pesanan untuk menjaga ketepatan pelayanan kepada pelanggan.",

                "Gunakan hasil analisis cluster sebagai dasar dalam penyusunan strategi operasional dan peningkatan kualitas pelayanan."

            ]

            for item in rekomendasi_tinggi:

                st.markdown(f"• {item}")

    # ======================================================
    # BEBAN PELAYANAN RENDAH
    # ======================================================

    with right:

        with st.container(border=True):

            st.markdown(
                "## 🟩 Pola Transaksi dengan Beban Pelayanan Rendah"
            )

            st.caption(
                """
Kelompok transaksi dengan nilai transaksi,
jumlah pesanan, variasi menu, dan waktu
persiapan yang relatif lebih rendah.
                """
            )

            st.divider()

            c1, c2 = st.columns(2)

            with c1:

                st.metric(
                    "Jumlah Transaksi",
                    normal
                )

            with c2:

                st.metric(
                    "Persentase",
                    f"{normal_pct:.2f}%"
                )

            st.divider()

            st.markdown("### 📌 Karakteristik")

            karakteristik_rendah = [

                "Nilai transaksi relatif lebih rendah.",

                "Jumlah pesanan lebih sedikit.",

                "Variasi menu lebih sederhana.",

                "Waktu persiapan relatif lebih singkat."

            ]

            for item in karakteristik_rendah:

                st.markdown(f"✅ {item}")

            st.divider()

            st.markdown("### 💡 Rekomendasi")

            rekomendasi_rendah = [

                "Pertahankan kualitas pelayanan yang telah berjalan agar kepuasan pelanggan tetap terjaga.",

                "Laksanakan proses pelayanan sesuai dengan prosedur operasional yang telah diterapkan untuk menjaga konsistensi pelayanan.",

                "Manfaatkan hasil analisis sebagai dasar pengelolaan sumber daya.",

                "Lakukan evaluasi terhadap pola transaksi pada kelompok ini untuk mendukung peningkatan kualitas pelayanan secara berkelanjutan.",

                "Gunakan kelompok transaksi ini sebagai acuan dalam menjaga efisiensi operasional tanpa mengurangi kualitas pelayanan."

            ]

            for item in rekomendasi_rendah:

                st.markdown(f"• {item}")

    st.divider()
    # ======================================================
    # DATA HASIL CLUSTERING
    # ======================================================

    st.subheader("📋 Data Hasil Clustering")

    st.markdown("""
    Tabel berikut menampilkan hasil pengelompokan setiap transaksi
    berdasarkan proses K-Means Clustering.
    """)

    # Salin dataframe hasil clustering
    # ================================
    # DATA HASIL CLUSTERING
    # ================================

    # Mengambil data asli hasil preprocessing
    hasil_cluster = st.session_state["original_df"].copy()

    # Menambahkan label cluster
    hasil_cluster["Cluster"] = result_df["Cluster"]

    cluster_mapping = {
        0: "Pola Transaksi dengan Beban Pelayanan Tinggi",
        1: "Pola Transaksi dengan Beban Pelayanan Rendah"
    }

    hasil_cluster["Hasil Clustering"] = (
    hasil_cluster["Cluster"].map(cluster_mapping)
    )

    st.write(hasil_cluster.columns.tolist())

    # ======================================================
    # Ubah nama kolom agar lebih rapi
    # ======================================================

    hasil_cluster = hasil_cluster.rename(columns={

        "username": "Username",

        "Total_harga": "Total Harga",

        "Jumlah_pesanan": "Jumlah Pesanan",

        "Jumlah_jenis_menu": "Jumlah Jenis Menu",

        "waktu_persiapan_yang_diberikan":
            "Waktu Persiapan Diberikan",

        "waktu_persiapan_digunakan":
            "Waktu Persiapan Digunakan",

        "Hasil Clustering":
            "Hasil Clustering"

    })
    kolom_tampil = [

            "Username",

            "Total Harga",

            "Jumlah Pesanan",

            "Jumlah Jenis Menu",

            "Waktu Persiapan Diberikan",

            "Waktu Persiapan Digunakan",

            "Hasil Clustering"

    ]

hasil_cluster = hasil_cluster[kolom_tampil]

    st.dataframe(

        hasil_cluster,

        hide_index=True,

        use_container_width=True

    )

    st.caption(
        f"Menampilkan {len(hasil_cluster)} transaksi hasil pengelompokan menggunakan metode K-Means Clustering."
    )

    st.divider()
        # ======================================================
    # PROFIL CLUSTER
    # ======================================================

    st.subheader("📊 Profil Rata-rata Setiap Cluster")

    st.markdown(
        """
    Tabel berikut menunjukkan rata-rata nilai setiap variabel
    pada masing-masing cluster hasil proses K-Means Clustering.
        """
    )

    profile_df = cluster_profile(result_df)

    profile_df = profile_df.rename(

        index={

            0: "Pola Transaksi dengan Beban Pelayanan Tinggi",

            1: "Pola Transaksi dengan Beban Pelayanan Rendah"

        }

    )

    st.dataframe(

        profile_df,

        use_container_width=True

    )

    st.divider()

    # ======================================================
    # PENUTUP
    # ======================================================

    st.success(
        """
Analisis pola transaksi berhasil dilakukan menggunakan
metode K-Means Clustering.

Hasil pengelompokan menunjukkan bahwa transaksi Shopee Food
pada Buffet The Padang Pasir dapat dibedakan menjadi dua
kelompok berdasarkan karakteristik transaksi, yaitu
**Pola Transaksi dengan Beban Pelayanan Tinggi**
dan
**Pola Transaksi dengan Beban Pelayanan Rendah**.

Hasil analisis ini diharapkan dapat membantu pihak
Buffet The Padang Pasir dalam memahami karakteristik
transaksi pelanggan sehingga dapat digunakan sebagai
salah satu dasar dalam mendukung pengambilan keputusan
operasional secara lebih terarah.
        """
    )
