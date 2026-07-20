import pandas as pd

from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import (
    TA_CENTER,
    TA_JUSTIFY,
)

from reportlab.lib.styles import ParagraphStyle

from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# ==========================================================
# REGISTER FONT
# ==========================================================

try:

    pdfmetrics.registerFont(
        TTFont(
            "Times",
            "C:/Windows/Fonts/times.ttf"
        )
    )

    pdfmetrics.registerFont(
        TTFont(
            "Times-Bold",
            "C:/Windows/Fonts/timesbd.ttf"
        )
    )

except:
    pass


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
# STYLE
# ==========================================================

def get_styles():

    return {

        "title": ParagraphStyle(

            name="Title",

            fontName="Times-Bold",

            fontSize=18,

            alignment=TA_CENTER,

            spaceAfter=12

        ),

        "subtitle": ParagraphStyle(

            name="Subtitle",

            fontName="Times-Bold",

            fontSize=13,

            alignment=TA_CENTER,

            spaceAfter=20

        ),

        "heading": ParagraphStyle(

            name="Heading",

            fontName="Times-Bold",

            fontSize=12,

            spaceBefore=10,

            spaceAfter=8

        ),

        "normal": ParagraphStyle(

            name="Normal",

            fontName="Times",

            fontSize=11,

            alignment=TA_JUSTIFY,

            leading=20

        ),

        "table": ParagraphStyle(

            name="Table",

            fontName="Times",

            fontSize=10,

            leading=14

        )

    }


# ==========================================================
# FOOTER
# ==========================================================

def add_page_number(canvas, doc):

    canvas.saveState()

    canvas.setFont(
        "Times",
        10
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

    normal_pct

):
        output = BytesIO()

    doc = SimpleDocTemplate(

        output,

        pagesize=A4,

        leftMargin=2.5 * cm,

        rightMargin=2.5 * cm,

        topMargin=2.5 * cm,

        bottomMargin=2.5 * cm

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

            "Analisis Pola Transaksi Shopee Food Menggunakan<br/>"

            "Metode K-Means Clustering Berdasarkan Data Pemesanan<br/>"

            "pada Toko Buffet The Padang Pasir",

            styles["subtitle"]

        )

    )

    story.append(

        Spacer(

            1,

            0.8 * cm

        )

    )

    # ==========================================================
    # RINGKASAN HASIL ANALISIS
    # ==========================================================

    story.append(

        Paragraph(

            "Ringkasan Hasil Analisis",

            styles["heading"]

        )

    )

    summary_table = [

        [

            Paragraph("<b>Nama Cluster</b>", styles["table"]),

            Paragraph("<b>Jumlah</b>", styles["table"]),

            Paragraph("<b>Persentase (%)</b>", styles["table"])

        ]

    ]

    summary_table.append(

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

        ]

    )

    summary_table.append(

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

    )

    table = Table(

        summary_table,

        colWidths=[10 * cm, 2.5 * cm, 3 * cm]

    )

    table.setStyle(

        TableStyle([

            ("GRID", (0, 0), (-1, -1), 1, colors.black),

            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),

            ("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),

            ("ALIGN", (1, 1), (-1, -1), "CENTER"),

            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),

            ("TOPPADDING", (0, 0), (-1, -1), 8)

        ])

    )

    story.append(

        table

    )

    story.append(

        Spacer(

            1,

            0.8 * cm

        )

    )

    # ==========================================================
    # KESIMPULAN
    # ==========================================================

    story.append(

        Paragraph(

            "Kesimpulan Singkat",

            styles["heading"]

        )

    )

    story.append(

        Paragraph(

            f"""

            Berdasarkan hasil analisis terhadap <b>{total_data}</b> data transaksi

            Shopee Food, diperoleh dua kelompok transaksi yaitu

            <b>Pola Transaksi dengan Beban Pelayanan Tinggi</b>

            sebanyak <b>{tinggi}</b> transaksi

            (<b>{tinggi_pct:.2f}%</b>)

            dan

            <b>Pola Transaksi dengan Beban Pelayanan Rendah</b>

            sebanyak <b>{normal}</b> transaksi

            (<b>{normal_pct:.2f}%</b>).

            Hasil pengelompokan ini dapat digunakan sebagai dasar dalam

            mendukung pengambilan keputusan operasional pada

            Buffet The Padang Pasir.

            """,

            styles["normal"]

        )

    )

    # ==========================================================
    # HALAMAN BARU
    # ==========================================================

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

        Spacer(

            1,

            0.5 * cm

        )

    )

    # ==========================================================
    # DATA INTERPRETASI
    # ==========================================================

    karakteristik_tinggi = """
    • Nilai transaksi relatif lebih tinggi.<br/>
    • Jumlah pesanan lebih banyak.<br/>
    • Variasi menu lebih beragam.<br/>
    • Waktu persiapan relatif lebih lama.
    """

    rekomendasi_tinggi = """
    • Prioritaskan penanganan transaksi.<br/>
    • Pastikan ketersediaan bahan baku.<br/>
    • Atur pembagian tugas karyawan.<br/>
    • Pantau waktu persiapan pesanan.<br/>
    • Gunakan hasil analisis sebagai dasar strategi operasional.
    """

    karakteristik_rendah = """
    • Nilai transaksi relatif lebih rendah.<br/>
    • Jumlah pesanan lebih sedikit.<br/>
    • Variasi menu lebih sederhana.<br/>
    • Waktu persiapan relatif lebih singkat.
    """

    rekomendasi_rendah = """
    • Pertahankan kualitas pelayanan.<br/>
    • Jalankan prosedur operasional.<br/>
    • Kelola sumber daya secara optimal.<br/>
    • Lakukan evaluasi berkala.<br/>
    • Jaga efisiensi operasional.
    """

    # ==========================================================
    # TABEL INTERPRETASI
    # ==========================================================

    interpretasi_table = [

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

                karakteristik_tinggi,

                styles["table"]

            ),

            Paragraph(

                rekomendasi_tinggi,

                styles["table"]

            )

        ],

        [

            Paragraph(

                "Pola Transaksi dengan Beban Pelayanan Rendah",

                styles["table"]

            ),

            Paragraph(

                karakteristik_rendah,

                styles["table"]

            ),

            Paragraph(

                rekomendasi_rendah,

                styles["table"]

            )

        ]

    ]

    interpretasi = Table(

        interpretasi_table,

        colWidths=[5 * cm, 5.5 * cm, 6 * cm]

    )

    interpretasi.setStyle(

        TableStyle([

            ("GRID", (0, 0), (-1, -1), 1, colors.black),

            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),

            ("FONTNAME", (0, 0), (-1, 0), "Times-Bold"),

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),

            ("VALIGN", (0, 0), (-1, -1), "TOP"),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),

            ("TOPPADDING", (0, 0), (-1, -1), 8),

            ("LEFTPADDING", (0, 0), (-1, -1), 6),

            ("RIGHTPADDING", (0, 0), (-1, -1), 6)

        ])

    )

    story.append(

        interpretasi

    )

    story.append(

        Spacer(

            1,

            0.7 * cm

        )

    )

    # ==========================================================
    # PENJELASAN
    # ==========================================================

    story.append(

        Paragraph(

            "Keterangan",

            styles["heading"]

        )

    )

    story.append(

        Paragraph(

            """
            Interpretasi hasil clustering memberikan gambaran mengenai
            karakteristik masing-masing kelompok transaksi beserta rekomendasi
            yang dapat digunakan sebagai bahan pertimbangan dalam mendukung
            pengambilan keputusan operasional pada Buffet The Padang Pasir.
            """,

            styles["normal"]

        )

    )
    # ==========================================================
    # MEMBANGUN DOKUMEN PDF
    # ==========================================================

    doc.build(

        story,

        onFirstPage=add_page_number,

        onLaterPages=add_page_number

    )

    output.seek(0)

    return output
