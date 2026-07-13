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
    layout="wide",
    page_icon="🍽️",
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
### Buffet The Padang Pasir

Analisis Pola Transaksi Shopee Food
        """
    )

    st.divider()

    selected = option_menu(
        
        menu_title="",
        
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

        menu_icon="list",

        default_index=0,

        styles={

            "container": {
                "padding": "0px",
                "background-color": "#ffffff",
            },

            "icon": {
                "color": "#EE4D2D",
                "font-size": "18px"
            },

            "nav-link": {
                "font-size": "15px",
                "text-align": "left",
                "margin": "5px 0",
                "padding": "10px",
                "border-radius": "10px",
                "--hover-color": "#FFF3F0",
            },

            "nav-link-selected": {
                "background-color": "#EE4D2D",
                "color": "white",
            }

        }

    )

    st.divider()

    st.caption("Buffet The Padang Pasir")

    st.caption("Versi 1.0")

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
