import pandas as pd

from utils.clustering import (
    identify_high_service_cluster,
    cluster_name
)


# ==========================================================
# INTERPRETASI CLUSTER
# ==========================================================

def generate_interpretation(profile_df: pd.DataFrame):
    """
    Menghasilkan interpretasi dan rekomendasi
    berdasarkan profil masing-masing cluster.

    Parameters
    ----------
    profile_df : DataFrame
        DataFrame hasil cluster_profile().

    Returns
    -------
    list
        Daftar interpretasi setiap cluster.
    """

    interpretation = []

    # ======================================================
    # IDENTIFIKASI CLUSTER
    # ======================================================

    high_service_cluster = identify_high_service_cluster(
        profile_df
    )

    # ======================================================
    # MEMBUAT INTERPRETASI
    # ======================================================

    for cluster in profile_df.index:

        nama = cluster_name(
            cluster,
            high_service_cluster
        )

        data = profile_df.loc[cluster]

        if cluster == high_service_cluster:

            karakteristik = [

                f"Rata-rata jumlah item produk sebesar {data['Jumlah_Item_Produk']:.4f}.",

                f"Rata-rata frekuensi produk sebesar {data['Frekuensi_Produk']:.4f}.",

                f"Rata-rata total pendapatan sebesar {data['Total_Pendapatan']:.4f}.",

                f"Rata-rata waktu persiapan yang diberikan sebesar {data['Rata2_Waktu_Persiapan_Diberikan']:.4f}.",

                f"Rata-rata waktu persiapan yang digunakan sebesar {data['Rata2_Waktu_Persiapan_Digunakan']:.4f}.",

                "Produk pada cluster ini memiliki tingkat aktivitas yang lebih tinggi dibandingkan cluster lainnya."

            ]

            rekomendasi = [

                "Prioritaskan ketersediaan stok bahan baku untuk produk pada cluster ini.",

                "Pastikan proses persiapan produk dilakukan secara optimal agar pelayanan tetap terjaga.",

                "Jadikan produk pada cluster ini sebagai prioritas dalam operasional harian.",

                "Lakukan pemantauan terhadap waktu persiapan agar pelayanan tetap konsisten.",

                "Manfaatkan hasil clustering sebagai dasar dalam penyusunan strategi operasional dan peningkatan kualitas pelayanan."

            ]

        else:

            karakteristik = [

                f"Rata-rata jumlah item produk sebesar {data['Jumlah_Item_Produk']:.4f}.",

                f"Rata-rata frekuensi produk sebesar {data['Frekuensi_Produk']:.4f}.",

                f"Rata-rata total pendapatan sebesar {data['Total_Pendapatan']:.4f}.",

                f"Rata-rata waktu persiapan yang diberikan sebesar {data['Rata2_Waktu_Persiapan_Diberikan']:.4f}.",

                f"Rata-rata waktu persiapan yang digunakan sebesar {data['Rata2_Waktu_Persiapan_Digunakan']:.4f}.",

                "Produk pada cluster ini memiliki tingkat aktivitas yang relatif lebih rendah dibandingkan cluster prioritas."

            ]

            rekomendasi = [

                "Lakukan promosi terhadap produk pada cluster ini untuk meningkatkan frekuensi pembelian.",

                "Pertimbangkan strategi bundling dengan produk yang memiliki tingkat permintaan tinggi.",

                "Evaluasi strategi pemasaran untuk meningkatkan kontribusi produk terhadap pendapatan.",

                "Lakukan pemantauan terhadap perkembangan permintaan produk secara berkala.",

                "Gunakan hasil clustering sebagai bahan evaluasi dalam penyusunan strategi penjualan."

            ]

        interpretation.append({

            "cluster": int(cluster),

            "nama_cluster": nama,

            "karakteristik": karakteristik,

            "rekomendasi": rekomendasi

        })

    return interpretation


# ==========================================================
# KESIMPULAN
# ==========================================================

def generate_conclusion():
    """
    Menghasilkan kesimpulan umum hasil clustering.
    """

    return (
        "Berdasarkan hasil K-Means Clustering, produk berhasil "
        "dikelompokkan menjadi dua cluster yaitu Pola Transaksi "
        "dengan Beban Pelayanan Tinggi dan Pola Transaksi dengan "
        "Beban Pelayanan Rendah. Hasil pengelompokan ini dapat "
        "digunakan sebagai dasar dalam menentukan prioritas "
        "pelayanan, pengelolaan stok bahan baku, serta penyusunan "
        "strategi operasional pada Buffet The Padang Pasir."
    )
