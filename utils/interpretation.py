import pandas as pd


# ==========================================================
# INTERPRETASI CLUSTER
# ==========================================================

def generate_interpretation(profile_df: pd.DataFrame):
    """
    Menentukan interpretasi dan rekomendasi
    berdasarkan profil cluster.
    """

    interpretation = []

    # Menentukan cluster dengan beban pelayanan tinggi
    total_harga = profile_df["Total_harga"]

    high_cluster = total_harga.idxmax()
    low_cluster = total_harga.idxmin()

    # ======================================================
    # CLUSTER BEBAN TINGGI
    # ======================================================

    interpretation.append({

        "cluster": int(high_cluster),

        "nama_cluster": "Pola Transaksi dengan Beban Pelayanan Tinggi",

        "karakteristik": [

            "Memiliki nilai total transaksi relatif tinggi.",

            "Jumlah pesanan dalam satu transaksi lebih banyak.",

            "Variasi menu yang dipesan lebih beragam.",

            "Membutuhkan waktu persiapan yang lebih lama."

        ],

        "rekomendasi": [

            "Prioritaskan penanganan transaksi pada cluster ini agar pelayanan tetap optimal.",

            "Pastikan ketersediaan bahan baku untuk memenuhi kebutuhan transaksi dengan beban pelayanan tinggi.",

            "Atur pembagian tugas karyawan secara efektif agar proses pelayanan dapat dilakukan secara lebih optimal.",

            "Lakukan pemantauan terhadap waktu persiapan pesanan untuk menjaga ketepatan pelayanan kepada pelanggan.",

            "Gunakan hasil analisis cluster sebagai dasar dalam penyusunan strategi operasional dan peningkatan kualitas pelayanan."

        ]

    })

    # ======================================================
    # CLUSTER BEBAN RENDAH
    # ======================================================

    interpretation.append({

        "cluster": int(low_cluster),

        "nama_cluster": "Pola Transaksi dengan Beban Pelayanan Rendah",

        "karakteristik": [

            "Nilai transaksi relatif lebih rendah.",

            "Jumlah pesanan lebih sedikit.",

            "Variasi menu lebih sederhana.",

            "Waktu persiapan relatif lebih singkat."

        ],

        "rekomendasi": [

            "Pertahankan kualitas pelayanan yang sudah berjalan dengan baik.",

            "Manfaatkan waktu luang untuk menyiapkan bahan baku.",

            "Dorong pelanggan meningkatkan nilai transaksi melalui paket menu.",

            "Evaluasi menu yang kurang diminati pelanggan.",

            "Pertahankan konsistensi waktu penyajian pesanan.",

            "Gunakan hasil cluster sebagai pendukung evaluasi operasional toko."

        ]

    })

    return interpretation
