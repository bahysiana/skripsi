import pandas as pd
from io import BytesIO
from datetime import datetime
from zoneinfo import ZoneInfo

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
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
# STYLE PDF
# ==========================================================

def get_styles():

    return {

        "title": ParagraphStyle(
            name="Title",
            fontName="Helvetica-Bold",
            fontSize=15,
            alignment=TA_CENTER,
            spaceAfter=8,
        ),

        "subtitle": ParagraphStyle(
            name="Subtitle",
            fontName="Helvetica-Bold",
            fontSize=11,
            alignment=TA_CENTER,
            leading=16,
            spaceAfter=10,
        ),

        "heading": ParagraphStyle(
            name="Heading",
            fontName="Helvetica-Bold",
            fontSize=12,
            spaceAfter=10,
        ),

        "table": ParagraphStyle(
            name="Table",
            fontName="Helvetica",
            fontSize=8,
            leading=10,
        ),

    }

# ==========================================================
# HEADER & FOOTER
# ==========================================================

def add_page_number(canvas, doc):

    canvas.saveState()

    # ==========================
    # HEADER
    # ==========================

    tanggal_cetak = datetime.now(
        ZoneInfo("Asia/Jakarta")
    ).strftime("%d/%m/%Y, %H:%M")

    # Tanggal (Kiri Atas)
    canvas.setFont("Helvetica", 9)

    canvas.drawString(
        2 * cm,
        A4[1] - 1 * cm,
        tanggal_cetak
    )

    # Judul Header (Tengah Atas)
    canvas.setFont(
        "Helvetica-Bold",
        9
    )

    canvas.drawCentredString(
        16.9 * cm,
        A4[1] - 1 * cm,
        "LAPORAN HASIL ANALISIS"
    )

    # ==========================
    # FOOTER
    # ==========================

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

def export_pdf(result_df):

    output = BytesIO()

    doc = SimpleDocTemplate(

        output,

        pagesize=A4,

        leftMargin=2 * cm,

        rightMargin=2 * cm,

        topMargin=2.2 * cm,

        bottomMargin=2 * cm,

    )

    styles = get_styles()

    story = []

    # ==========================================================
    # JUDUL LAPORAN
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

    # ==========================================================
    # GARIS PEMISAH
    # ==========================================================

    garis = Table(

        [[""]],

        colWidths=[16.5 * cm]

    )

    garis.setStyle(

        TableStyle([

            ("LINEBELOW", (0, 0), (-1, 0), 2, colors.black),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),

            ("TOPPADDING", (0, 0), (-1, -1), 0),

        ])

    )

    story.append(garis)

    story.append(Spacer(1, 0.5 * cm))

    # ==========================================================
    # SUB JUDUL
    # ==========================================================

    story.append(

        Paragraph(

            "Hasil Akhir Clustering Produk",

            styles["heading"]

        )

    )

    story.append(

        Spacer(1, 0.2 * cm)

    )

    # ==========================================================
    # MENYIAPKAN DATA
    # ==========================================================

    pdf_df = result_df.copy()

    pdf_df = pdf_df[
        [
            "Produk",
            "Jumlah Item Produk",
            "Total Pendapatan",
            "Hasil Cluster"
        ]
    ]

    pdf_df.columns = [
        "Produk",
        "Jumlah Item",
        "Total Pendapatan",
        "Hasil Cluster"
    ]

    # ==========================================================
    # FORMAT TOTAL PENDAPATAN
    # ==========================================================

    pdf_df["Total Pendapatan"] = (

        pdf_df["Total Pendapatan"]

        .fillna(0)

        .astype(int)

        .map(

            lambda x: f"{x:,}".replace(",", ".")

        )

    )

    # ==========================================================
    # MEMBUAT HEADER TABEL
    # ==========================================================

    table_data = [

        [

            Paragraph("<b>No</b>", styles["table"]),

            Paragraph("<b>Produk</b>", styles["table"]),

            Paragraph("<b>Jumlah Item</b>", styles["table"]),

            Paragraph("<b>Total Pendapatan</b>", styles["table"]),

            Paragraph("<b>Hasil Cluster</b>", styles["table"])

        ]

    ]

    # ==========================================================
    # MENAMBAHKAN DATA KE TABEL
    # ==========================================================

    for index, row in pdf_df.iterrows():

        table_data.append(

            [

                str(index + 1),

                Paragraph(
                    str(row["Produk"]),
                    styles["table"]
                ),

                str(row["Jumlah Item"]),

                str(row["Total Pendapatan"]),

                Paragraph(
                    str(row["Hasil Cluster"]),
                    styles["table"]
                )

            ]

        )

    # ==========================================================
    # MEMBUAT TABEL
    # ==========================================================

    tabel = Table(

        table_data,

        repeatRows=1,

        colWidths=[

            1 * cm,      # No

            6 * cm,      # Produk

            2.5 * cm,    # Jumlah Item

            3.5 * cm,    # Total Pendapatan

            5 * cm       # Hasil Cluster

        ]

    )

    # ==========================================================
    # STYLE TABEL
    # ==========================================================

    tabel.setStyle(

        TableStyle([

            # Header
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EAEAEA")),

            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("FONTSIZE", (0, 0), (-1, 0), 9),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),

            ("TOPPADDING", (0, 0), (-1, 0), 8),

            # Isi tabel
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),

            ("FONTSIZE", (0, 1), (-1, -1), 8),

            ("TOPPADDING", (0, 1), (-1, -1), 6),

            ("BOTTOMPADDING", (0, 1), (-1, -1), 6),

            # Border
            ("GRID", (0, 0), (-1, -1), 0.8, colors.black),

            ("BOX", (0, 0), (-1, -1), 1, colors.black),

            # Alignment
            ("ALIGN", (0, 0), (0, -1), "CENTER"),     # No

            ("ALIGN", (2, 1), (3, -1), "CENTER"),     # Jumlah Item & Pendapatan

            ("ALIGN", (1, 1), (1, -1), "LEFT"),       # Produk

            ("ALIGN", (4, 1), (4, -1), "LEFT"),       # Cluster

            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        ])

    )

    story.append(tabel)

    # ==========================================================
    # SPASI AKHIR
    # ==========================================================

    story.append(

        Spacer(1, 0.3 * cm)

    )

    # ==========================================================
    # MEMBANGUN PDF
    # ==========================================================

    doc.build(

        story,

        onFirstPage=add_page_number,

        onLaterPages=add_page_number

    )

    # ==========================================================
    # KEMBALIKAN FILE PDF
    # ==========================================================

    output.seek(0)

    return output
