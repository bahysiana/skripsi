import pandas as pd

from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


# ==========================================================
# EXPORT CSV
# ==========================================================

def export_csv(df: pd.DataFrame):

    return df.to_csv(
        index=False
    ).encode("utf-8")


# ==========================================================
# EXPORT EXCEL
# ==========================================================

def export_excel(df: pd.DataFrame):

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df.to_excel(

            writer,

            index=False,

            sheet_name="Hasil Clustering"

        )

    output.seek(0)

    return output


# ==========================================================
# EXPORT PDF
# ==========================================================

def export_pdf(

    summary_df,

    centroid_df,

    profile_df,

    total_data,

    tinggi,

    normal,

    tinggi_pct,

    normal_pct

):

    output = BytesIO()

    doc = SimpleDocTemplate(

        output,

        pagesize=A4,

        rightMargin=2 * cm,

        leftMargin=2 * cm,

        topMargin=2 * cm,

        bottomMargin=2 * cm

    )

    styles = getSampleStyleSheet()

    story = []

    # ======================================================
    # STYLE
    # ======================================================

    title = styles["Heading1"]

    title.alignment = TA_CENTER

    title.textColor = colors.HexColor("#EE4D2D")

    heading = styles["Heading2"]

    heading.textColor = colors.HexColor("#EE4D2D")

    normal_style = styles["BodyText"]

    # ======================================================
    # COVER
    # ======================================================

    story.append(

        Paragraph(

            "LAPORAN HASIL ANALISIS",

            title

        )

    )

    story.append(

        Paragraph(

            "POLA TRANSAKSI SHOPEE FOOD",

            title

        )

    )

    story.append(

        Spacer(

            1,

            1 * cm

        )

    )

    story.append(

        Paragraph(

            "<b>Objek Penelitian</b>",

            heading

        )

    )

    story.append(

        Paragraph(

            "Buffet The Padang Pasir",

            normal_style

        )

    )

    story.append(

        Spacer(

            1,

            0.5 * cm

        )

    )

    story.append(

        Paragraph(

            "<b>Metode</b>",

            heading

        )

    )

    story.append(

        Paragraph(

            "K-Means Clustering",

            normal_style

        )

    )

    story.append(

        Spacer(

            1,

            0.5 * cm

        )

    )

    story.append(

        Paragraph(

            "<b>Jumlah Data</b>",

            heading

        )

    )

    story.append(

        Paragraph(

            f"{total_data} Transaksi",

            normal_style

        )

    )

    story.append(

        Spacer(

            1,

            1 * cm

        )

    )

    story.append(

        Paragraph(

            """
Laporan ini merupakan hasil analisis pola transaksi
Shopee Food pada Buffet The Padang Pasir menggunakan
metode K-Means Clustering.

Tujuan analisis ini adalah mengelompokkan transaksi
berdasarkan karakteristiknya sehingga dapat membantu
pihak toko memahami pola transaksi pelanggan serta
menjadi bahan pertimbangan dalam pengambilan keputusan
operasional.
            """,

            normal_style

        )

    )

    story.append(

        Spacer(

            1,

            1 * cm

        )

    )

    # ======================================================
    # RINGKASAN ANALISIS
    # ======================================================

    story.append(

        Paragraph(

            "Ringkasan Hasil Analisis",

            heading

        )

    )

    story.append(

        Spacer(

            1,

            0.4 * cm

        )

    )
        # ======================================================
    # TABEL RINGKASAN
    # ======================================================

    summary_table = [

        [

            "Keterangan",

            "Hasil"

        ],

        [

            "Jumlah Transaksi",

            str(total_data)

        ],

        [

            "Jumlah Cluster",

            "2"

        ],

        [

            "Pola Transaksi dengan Beban Pelayanan Tinggi",

            f"{tinggi} Transaksi ({tinggi_pct:.2f}%)"

        ],

        [

            "Pola Transaksi dengan Beban Pelayanan Rendah",

            f"{normal} Transaksi ({normal_pct:.2f}%)"

        ]

    ]

    table = Table(

        summary_table,

        colWidths=[9 * cm, 6 * cm]

    )

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#EE4D2D")),

            ("TEXTCOLOR", (0,0), (-1,0), colors.white),

            ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),

            ("GRID", (0,0), (-1,-1), 1, colors.grey),

            ("BACKGROUND", (0,1), (-1,-1), colors.whitesmoke),

            ("BOTTOMPADDING", (0,0), (-1,0), 10),

            ("ALIGN", (0,0), (-1,-1), "CENTER"),

            ("VALIGN", (0,0), (-1,-1), "MIDDLE")

        ])

    )

    story.append(table)

    story.append(

        Spacer(

            1,

            0.8 * cm

        )

    )

    # ======================================================
    # PENJELASAN
    # ======================================================

    story.append(

        Paragraph(

            "Makna Hasil Analisis",

            heading

        )

    )

    story.append(

        Paragraph(

            """
Berdasarkan proses K-Means Clustering,
transaksi Shopee Food berhasil dikelompokkan
menjadi dua kelompok transaksi berdasarkan
karakteristik transaksi yang dimiliki.

Kelompok pertama merupakan transaksi dengan
beban pelayanan yang relatif lebih tinggi,
sedangkan kelompok kedua merupakan transaksi
dengan beban pelayanan yang relatif lebih rendah.
            """,

            normal_style

        )

    )

    story.append(

        Spacer(

            1,

            0.8 * cm

        )

    )

    # ======================================================
    # CENTROID
    # ======================================================

    story.append(

        Paragraph(

            "Nilai Centroid",

            heading

        )

    )

    centroid_data = [

        ["Variabel"]

        +

        [

            f"Cluster {i}"

            for i in range(len(centroid_df))

        ]

    ]

    for kolom in centroid_df.columns:

        baris = [

            kolom

        ]

        for i in range(len(centroid_df)):

            baris.append(

                round(

                    float(

                        centroid_df.iloc[i][kolom]

                    ),

                    4

                )

            )

        centroid_data.append(baris)

    centroid_table = Table(

        centroid_data,

        repeatRows=1

    )

    centroid_table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#EE4D2D")),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("GRID",(0,0),(-1,-1),1,colors.grey),

            ("BACKGROUND",(0,1),(-1,-1),colors.beige),

            ("ALIGN",(0,0),(-1,-1),"CENTER"),

            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold")

        ])

    )

    story.append(

        centroid_table

    )

    story.append(

        Spacer(

            1,

            0.8 * cm

        )

    )

    story.append(

        Paragraph(

            """
Nilai centroid merupakan nilai rata-rata
setiap variabel pada masing-masing cluster.

Semakin besar nilai centroid suatu variabel,
maka semakin kuat karakteristik variabel tersebut
pada cluster yang bersangkutan.
            """,

            normal_style

        )

    )

    story.append(

        Spacer(

            1,

            1 * cm

        )

    )

    # ======================================================
    # PROFIL CLUSTER
    # ======================================================

    story.append(

        Paragraph(

            "Profil Rata-rata Setiap Cluster",

            heading

        )

    )

    profile_data = [

        ["Cluster"]

        +

        list(profile_df.columns)

    ]

    for idx in profile_df.index:

        row = [

            f"Cluster {idx}"

        ]

        row.extend(

            [

                round(v,4)

                for v in profile_df.loc[idx]

            ]

        )

        profile_data.append(row)

    profile_table = Table(

        profile_data,

        repeatRows=1

    )

    profile_table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#EE4D2D")),

            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

            ("GRID",(0,0),(-1,-1),1,colors.grey),

            ("BACKGROUND",(0,1),(-1,-1),colors.whitesmoke),

            ("ALIGN",(0,0),(-1,-1),"CENTER"),

            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold")

        ])

    )

    story.append(

        profile_table

    )

    story.append(

        Spacer(

            1,

            1 * cm

        )

    )
        # ======================================================
    # INTERPRETASI CLUSTER
    # ======================================================

    story.append(
        Paragraph(
            "Interpretasi Hasil Clustering",
            heading
        )
    )

    story.append(
        Spacer(1, 0.4 * cm)
    )

    # ======================================================
    # CLUSTER BEBAN PELAYANAN TINGGI
    # ======================================================

    story.append(
        Paragraph(
            "<b>Pola Transaksi dengan Beban Pelayanan Tinggi</b>",
            heading
        )
    )

    story.append(
        Paragraph(
            """
Kelompok ini terdiri dari transaksi yang memiliki nilai transaksi,
jumlah pesanan, variasi menu, dan waktu persiapan yang relatif lebih tinggi
dibandingkan kelompok lainnya.
            """,
            normal_style
        )
    )

    story.append(
        Spacer(1, 0.3 * cm)
    )

    story.append(
        Paragraph(
            "<b>Karakteristik</b>",
            heading
        )
    )

    karakteristik_tinggi = [

        "• Nilai transaksi relatif lebih tinggi.",

        "• Jumlah pesanan lebih banyak.",

        "• Variasi menu yang dipesan lebih beragam.",

        "• Waktu persiapan relatif lebih lama."

    ]

    for item in karakteristik_tinggi:

        story.append(
            Paragraph(
                item,
                normal_style
            )
        )

    story.append(
        Spacer(1, 0.3 * cm)
    )

    story.append(
        Paragraph(
            "<b>Makna Hasil Analisis</b>",
            heading
        )
    )

    story.append(
        Paragraph(
            """
Kelompok transaksi ini menunjukkan pesanan yang membutuhkan
beban pelayanan lebih tinggi dibandingkan kelompok lainnya.
Oleh karena itu, transaksi pada kelompok ini memerlukan perhatian
lebih agar kualitas pelayanan tetap terjaga.
            """,
            normal_style
        )
    )

    story.append(
        Spacer(1, 0.3 * cm)
    )

    story.append(
        Paragraph(
            "<b>Rekomendasi</b>",
            heading
        )
    )

    rekomendasi_tinggi = [

        "• Prioritaskan penanganan transaksi pada kelompok ini agar proses pelayanan tetap optimal.",

        "• Pastikan ketersediaan bahan baku untuk menu yang sering muncul pada kelompok transaksi ini.",

        "• Lakukan pembagian tugas karyawan secara efektif ketika menangani transaksi dengan beban pelayanan tinggi.",

        "• Lakukan pemantauan terhadap waktu persiapan agar tetap sesuai dengan estimasi kepada pelanggan.",

        "• Gunakan hasil analisis sebagai dasar evaluasi operasional toko."

    ]

    for item in rekomendasi_tinggi:

        story.append(
            Paragraph(
                item,
                normal_style
            )
        )

    story.append(
        Spacer(1, 0.7 * cm)
    )

    # ======================================================
    # CLUSTER BEBAN PELAYANAN RENDAH
    # ======================================================

    story.append(
        Paragraph(
            "<b>Pola Transaksi dengan Beban Pelayanan Rendah</b>",
            heading
        )
    )

    story.append(
        Paragraph(
            """
Kelompok ini terdiri dari transaksi yang memiliki nilai transaksi,
jumlah pesanan, variasi menu, dan waktu persiapan yang relatif lebih rendah
dibandingkan kelompok lainnya.
            """,
            normal_style
        )
    )

    story.append(
        Spacer(1, 0.3 * cm)
    )

    story.append(
        Paragraph(
            "<b>Karakteristik</b>",
            heading
        )
    )

    karakteristik_rendah = [

        "• Nilai transaksi relatif lebih rendah.",

        "• Jumlah pesanan lebih sedikit.",

        "• Variasi menu yang dipesan lebih sederhana.",

        "• Waktu persiapan relatif lebih singkat."

    ]

    for item in karakteristik_rendah:

        story.append(
            Paragraph(
                item,
                normal_style
            )
        )

    story.append(
        Spacer(1, 0.3 * cm)
    )

    story.append(
        Paragraph(
            "<b>Makna Hasil Analisis</b>",
            heading
        )
    )

    story.append(
        Paragraph(
            """
Kelompok transaksi ini menunjukkan pesanan yang relatif lebih sederhana
sehingga dapat ditangani menggunakan prosedur operasional yang telah
diterapkan oleh pihak toko.
            """,
            normal_style
        )
    )

    story.append(
        Spacer(1, 0.3 * cm)
    )

    story.append(
        Paragraph(
            "<b>Rekomendasi</b>",
            heading
        )
    )

    rekomendasi_rendah = [

        "• Pertahankan kualitas pelayanan yang telah berjalan.",

        "• Gunakan prosedur operasional secara konsisten.",

        "• Manfaatkan hasil analisis sebagai dasar pengelolaan sumber daya.",

        "• Evaluasi menu yang kurang diminati sebagai bahan pengembangan produk.",

        "• Gunakan kelompok transaksi ini sebagai acuan dalam menjaga efisiensi pelayanan."

    ]

    for item in rekomendasi_rendah:

        story.append(
            Paragraph(
                item,
                normal_style
            )
        )

    story.append(
        Spacer(1, 0.8 * cm)
    )

    # ======================================================
    # PENUTUP
    # ======================================================

    story.append(
        Paragraph(
            "Penutup",
            heading
        )
    )

    story.append(
        Paragraph(
            """
Berdasarkan hasil analisis menggunakan metode K-Means Clustering,
transaksi Shopee Food pada Buffet The Padang Pasir berhasil
dikelompokkan menjadi dua kelompok transaksi, yaitu Pola Transaksi
dengan Beban Pelayanan Tinggi dan Pola Transaksi dengan Beban
Pelayanan Rendah.

Hasil pengelompokan ini diharapkan dapat membantu pihak
Buffet The Padang Pasir dalam memahami karakteristik transaksi
pelanggan sehingga dapat dijadikan sebagai salah satu dasar
dalam mendukung pengambilan keputusan operasional secara lebih
terarah.
            """,
            normal_style
        )
    )

    # ======================================================
    # BUILD PDF
    # ======================================================

    doc.build(story)

    output.seek(0)

    return output
