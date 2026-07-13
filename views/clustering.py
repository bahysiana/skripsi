import pandas as pd

from sklearn.cluster import KMeans


# ==========================================================
# KONSTANTA
# ==========================================================

N_CLUSTER = 2

RANDOM_STATE = 42


# ==========================================================
# PROSES K-MEANS
# ==========================================================

def run_kmeans(df: pd.DataFrame):
    """
    Menjalankan proses K-Means Clustering.
    """

    model = KMeans(

        n_clusters=N_CLUSTER,

        random_state=RANDOM_STATE,

        n_init=10

    )

    cluster = model.fit_predict(df)

    result = df.copy()

    result["Cluster"] = cluster

    centroid = pd.DataFrame(

        model.cluster_centers_,

        columns=df.columns

    )

    return result, centroid, model


# ==========================================================
# RINGKASAN CLUSTER
# ==========================================================

def cluster_summary(df: pd.DataFrame):
    """
    Menghitung jumlah anggota setiap cluster.
    """

    summary = (

        df["Cluster"]

        .value_counts()

        .sort_index()

        .reset_index()

    )

    summary.columns = [

        "Cluster",

        "Jumlah_Data"

    ]

    summary["Persentase"] = (

        summary["Jumlah_Data"]

        / summary["Jumlah_Data"].sum()

        * 100

    ).round(2)

    return summary


# ==========================================================
# RATA-RATA SETIAP CLUSTER
# ==========================================================

def cluster_profile(df: pd.DataFrame):
    """
    Menghitung rata-rata setiap variabel
    berdasarkan cluster.
    """

    profile = (

        df

        .groupby("Cluster")

        .mean(numeric_only=True)

        .round(4)

    )

    return profile
