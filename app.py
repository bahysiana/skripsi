import streamlit as st
from streamlit_option_menu import option_menu

# =====================================================
# IMPORT HALAMAN
# =====================================================

from views.home import show_home
from views.kelola_data import show_kelola_data
from views.preprocessing import show_preprocessing
from views.clustering import show_clustering
from views.download import show_download

# =====================================================
# KONFIGURASI APLIKASI
# =====================================================

st.set_page_config(
    page_title="Analisis Pola Transaksi Shopee Food",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# LOAD CSS
# =====================================================

try:

    with open(
        "assets/style.css",
        encoding="utf-8"
    ) as css:

        st.markdown(
            f"<style>{css.read()}</style>",
            unsafe_allow_html=True
        )

except FileNotFoundError:

    pass

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown(
        """
        <div class="sidebar-header">

            <div class="sidebar-logo">
                🍽️
            </div>

            <div class="sidebar-title">
                Buffet The Padang Pasir
            </div>

            <div class="sidebar-subtitle">
                Analisis Pola Transaksi
                Shopee Food
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    selected = option_menu(

        menu_title=None,

        options=[
            "Home",
            "Kelola Data",
            "Preprocessing",
            "Clustering",
            "Download"
        ],

        icons=[
            "house-fill",
            "database-fill",
            "sliders",
            "bar-chart-fill",
            "download"
        ],

        default_index=0

    )

    st.markdown(
        """
        <div class="sidebar-footer">

            Versi 1.0

        </div>
        """,
        unsafe_allow_html=True
    )

# =====================================================
# ROUTING
# =====================================================

if selected == "Home":

    show_home()

elif selected == "Kelola Data":

    show_kelola_data()

elif selected == "Preprocessing":

    show_preprocessing()

elif selected == "Clustering":

    show_clustering()

elif selected == "Download":

    show_download()
