import pandas as pd


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

    from io import BytesIO

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
