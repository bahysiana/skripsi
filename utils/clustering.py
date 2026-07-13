import pandas as pd

from sklearn.cluster import KMeans


# ==========================================================
# DEFAULT
# ==========================================================

DEFAULT_CLUSTER = 2

RANDOM_STATE = 42


# ==========================================================
# PROSES K-MEANS
# ==========================================================

def perform_clustering(
    df: pd.DataFrame,
    n_clusters: int = DEFAULT_CLUSTER
):
    """
    Melakukan proses K-Means Clustering.

    Parameters
    ----------
    df : DataFrame
        Dataset hasil preprocessing.

    n_clusters : int
        Jumlah cluster.

    Returns
    -------
    result_df : DataFrame
        Dataset beserta label cluster.

    centroid_df : DataFrame
        Nilai centroid.
    """

    model = KMeans(

        n_clusters=n_clusters,

        random_state=RANDOM_STATE,

        n_init=10

    )

    labels = model.fit_predict(df)

    result_df = df.copy()

    result_df["Cluster"] = labels

    centroid_df = pd.DataFrame(

        model.cluster_centers_,

        columns=df.columns

    )

    return result_df, centroid_df


# ==========================================================
# RINGKASAN CLUSTER
# ==========================================================

def cluster_summary(
    cluster_df: pd.DataFrame
):
    """
    Menghasilkan ringkasan jumlah anggota cluster.
    """

    summary = (

        cluster_df["Cluster"]

        .value_counts()

        .sort_index()

        .reset_index()

    )

    summary.columns = [

        "Cluster",

        "Jumlah"

    ]

    summary["Persentase"] = (

        summary["Jumlah"]

        / summary["Jumlah"].sum()

        * 100

    ).round(2)

    return summary


# ==========================================================
# PROFIL CLUSTER
# ==========================================================

def cluster_profile(
    cluster_df: pd.DataFrame
):
    """
    Menghasilkan rata-rata setiap variabel
    pada masing-masing cluster.
    """

    profile = (

        cluster_df

        .groupby("Cluster")

        .mean(numeric_only=True)

        .round(4)

    )

    return profile


# ==========================================================
# NAMA CLUSTER
# ==========================================================

def cluster_name(cluster: int):
    """
    Mengubah nomor cluster menjadi
    nama yang mudah dipahami.
    """

    if cluster == 0:

        return "Transaksi Prioritas Tinggi"

    return "Transaksi Prioritas Normal"
