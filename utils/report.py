import pandas as pd
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)

# ==========================================================
# EXPORT CSV
# ==========================================================

def export_csv(df: pd.DataFrame):

    return df.to_csv(index=False).encode("utf-8")


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
# STYLE
# ==========================================================

def get_styles():

    return {

        "title": ParagraphStyle(
            name="Title",
            fontName="Helvetica-Bold",
            fontSize=18,
            alignment=TA_CENTER,
            spaceAfter=14,
        ),

        "subtitle": ParagraphStyle(
            name="Subtitle",
            fontName="Helvetica-Bold",
            fontSize=12,
            alignment=TA_CENTER,
            spaceAfter=20,
        ),

        "heading": ParagraphStyle(
            name="Heading",
            fontName="Helvetica-Bold",
            fontSize=12,
            spaceBefore=10,
            spaceAfter=8,
        ),

        "normal": ParagraphStyle(
            name="Normal",
            fontName="Helvetica",
            fontSize=10,
            alignment=TA_JUSTIFY,
            leading=18,
        ),

        "table": ParagraphStyle(
            name="Table",
            fontName="Helvetica",
            fontSize=9,
            leading=12,
        ),

    }


# ==========================================================
# FOOTER
# ==========================================================

def add_page_number(canvas, doc):

    canvas.saveState()

    canvas.setFont(
        "Helvetica",
        9
    )

    canvas.drawString(
        2 * cm,
        1 * cm,
        "Laporan Hasil Analisis"
    )

    canvas.drawRightString(
        A4[0] - 2 * cm,
        1 * cm,
        f"Halaman {doc.page}"
    )

    canvas.restoreState()


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

    normal_pct,

):

    output = BytesIO()

    doc = SimpleDocTemplate(

        output,

        pagesize=A4,

        leftMargin=2.2 * cm,

        rightMargin=2.2 * cm,

        topMargin=2.5 * cm,

        bottomMargin=2.2 * cm,

    )

    styles = get_styles()

    story = []
        # ==========================================================
    # HALAMAN 1
    # ==========================================================

    story.append(
        Paragraph(
            "LAPORAN HASIL ANALISIS",
            styles["title"]
        )
    )

    story.append(
        Paragraph(
            "Analisis Pola Transaksi Shopee Food Menggunakan "
            "Metode K-Means Clustering Berdasarkan Data Pemesanan "
            "pada Toko Buffet The Padang Pasir",
            styles["subtitle"]
        )
    )

    story.append(Spacer(1, 0.8 * cm))

    # ==========================================================
    # RINGKASAN
    # ==========================================================

    story.append(
        Paragraph(
            "Ringkasan Hasil Analisis",
            styles["heading"]
        )
    )

    data_ringkasan = [

        [

            Paragraph("<b>Nama Cluster</b>", styles["table"]),

            Paragraph("<b>Jumlah</b>", styles["table"]),

            Paragraph("<b>Persentase (%)</b>", styles["table"])

        ],

        [

            Paragraph(
                "Pola Transaksi dengan Beban Pelayanan Tinggi",
                styles["table"]
            ),

            Paragraph(
                str(tinggi),
                styles["table"]
            ),

            Paragraph(
                f"{tinggi_pct:.2f}",
                styles["table"]
            )

        ],

        [

            Paragraph(
                "Pola Transaksi dengan Beban Pelayanan Rendah",
                styles["table"]
            ),

            Paragraph(
                str(normal),
                styles["table"]
            ),

            Paragraph(
                f"{normal_pct:.2f}",
                styles["table"]
            )

        ]

    ]

    tabel_ringkasan = Table(

        data_ringkasan,

        colWidths=[10 * cm, 2.5 * cm, 3 * cm]

    )

    tabel_ringkasan.setStyle(

        TableStyle([

            ("GRID", (0, 0), (-1, -1), 1, colors.black),

            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EAEAEA")),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("ALIGN", (1, 1), (-1, -1), "CENTER"),

            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),

            ("TOPPADDING", (0, 0), (-1, -1), 8),

        ])

    )

    story.append(tabel_ringkasan)

    story.append(Spacer(1, 0.8 * cm))

    # ==========================================================
    # KESIMPULAN
    # ==========================================================

    story.append(

        Paragraph(

            "Kesimpulan",

            styles["heading"]

        )

    )

    story.append(

        Paragraph(

            f"""
            Berdasarkan hasil analisis terhadap <b>{total_data}</b> data
            transaksi Shopee Food menggunakan metode K-Means Clustering,
            diperoleh dua kelompok transaksi.

            Kelompok pertama yaitu
            <b>Pola Transaksi dengan Beban Pelayanan Tinggi</b>
            sebanyak <b>{tinggi}</b> transaksi
            (<b>{tinggi_pct:.2f}%</b>).

            Kelompok kedua yaitu
            <b>Pola Transaksi dengan Beban Pelayanan Rendah</b>
            sebanyak <b>{normal}</b> transaksi
            (<b>{normal_pct:.2f}%</b>).

            Hasil pengelompokan ini dapat dijadikan sebagai dasar
            dalam mendukung pengambilan keputusan operasional,
            pembagian sumber daya, serta peningkatan kualitas
            pelayanan pada Buffet The Padang Pasir.
            """,

            styles["normal"]

        )

    )

    story.append(

        PageBreak()

    )
        # ==========================================================
    # HALAMAN 2
    # ==========================================================

    story.append(

        Paragraph(

            "Interpretasi Hasil Clustering",

            styles["title"]

        )

    )

    story.append(

        Spacer(1, 0.5 * cm)

    )

    story.append(

        Paragraph(

            "Interpretasi hasil clustering digunakan untuk memberikan "
            "gambaran karakteristik dari setiap kelompok transaksi "
            "beserta rekomendasi yang dapat dijadikan dasar dalam "
            "pengambilan keputusan operasional.",

            styles["normal"]

        )

    )

    story.append(

        Spacer(1, 0.5 * cm)

    )

    # ==========================================================
    # TABEL INTERPRETASI
    # ==========================================================

    data_interpretasi = [

        [

            Paragraph("<b>Nama Cluster</b>", styles["table"]),

            Paragraph("<b>Karakteristik</b>", styles["table"]),

            Paragraph("<b>Rekomendasi</b>", styles["table"])

        ],

        [

            Paragraph(

                "Pola Transaksi dengan Beban Pelayanan Tinggi",

                styles["table"]

            ),

            Paragraph(

                """
                • Nilai transaksi relatif tinggi.<br/>
                • Jumlah pesanan lebih banyak.<br/>
                • Variasi menu lebih beragam.<br/>
                • Waktu persiapan relatif lebih lama.
                """,

                styles["table"]

            ),

            Paragraph(

                """
                • Prioritaskan pelayanan transaksi.<br/>
                • Pastikan stok bahan baku tersedia.<br/>
                • Atur pembagian tugas karyawan.<br/>
                • Pantau waktu persiapan pesanan.<br/>
                • Jadikan cluster ini sebagai prioritas operasional.
                """,

                styles["table"]

            )

        ],

        [

            Paragraph(

                "Pola Transaksi dengan Beban Pelayanan Rendah",

                styles["table"]

            ),

            Paragraph(

                """
                • Nilai transaksi relatif rendah.<br/>
                • Jumlah pesanan lebih sedikit.<br/>
                • Variasi menu lebih sederhana.<br/>
                • Waktu persiapan relatif singkat.
                """,

                styles["table"]

            ),

            Paragraph(

                """
                • Pertahankan kualitas pelayanan.<br/>
                • Kelola sumber daya secara efisien.<br/>
                • Lakukan evaluasi berkala.<br/>
                • Pertahankan standar operasional.<br/>
                • Tetap menjaga kepuasan pelanggan.
                """,

                styles["table"]

            )

        ]

    ]

    tabel_interpretasi = Table(

        data_interpretasi,

        colWidths=[5 * cm, 6 * cm, 6 * cm]

    )

    tabel_interpretasi.setStyle(

        TableStyle([

            ("GRID", (0, 0), (-1, -1), 1, colors.black),

            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EAEAEA")),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),

            ("VALIGN", (0, 0), (-1, -1), "TOP"),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),

            ("TOPPADDING", (0, 0), (-1, -1), 8),

            ("LEFTPADDING", (0, 0), (-1, -1), 6),

            ("RIGHTPADDING", (0, 0), (-1, -1), 6),

        ])

    )

    story.append(

        tabel_interpretasi

    )

    story.append(

        Spacer(1, 0.7 * cm)

    )

    # ==========================================================
    # PENUTUP
    # ==========================================================

    story.append(

        Paragraph(

            "Penutup",

            styles["heading"]

        )

    )

    story.append(

        Paragraph(

            """
            Hasil analisis clustering ini diharapkan dapat membantu
            Buffet The Padang Pasir dalam memahami pola transaksi
            pelanggan sehingga dapat digunakan sebagai dasar dalam
            menentukan prioritas pelayanan, pengelolaan stok bahan baku,
            pembagian sumber daya, serta meningkatkan efektivitas
            operasional berdasarkan karakteristik transaksi yang
            telah terbentuk.
            """,

            styles["normal"]

        )

    )

    # ==========================================================
    # MEMBANGUN PDF
    # ==========================================================

    doc.build(

        story,

        onFirstPage=add_page_number,

        onLaterPages=add_page_number

    )

    output.seek(0)

    return output
