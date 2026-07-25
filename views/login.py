import streamlit as st

from utils.auth import verify_login


# ==========================================================
# CSS
# ==========================================================

st.markdown("""
<style>

/* =========================
   HALAMAN
========================= */

.block-container{
    max-width:1200px;
    padding-top:1.5rem;
    padding-bottom:1rem;
}

/* Hilangkan menu bawaan */

#MainMenu{
    visibility:hidden;
}

header{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

/* =========================
   HEADER
========================= */

.logo{
    text-align:center;
    font-size:60px;
    margin-bottom:-10px;
}

.title{
    text-align:center;
    font-size:34px;
    font-weight:700;
    color:#222;
    margin-bottom:5px;
}

.subtitle{
    text-align:center;
    font-size:17px;
    color:#666;
    line-height:1.8;
    margin-bottom:25px;
}

/* =========================
   LOGIN TITLE
========================= */

.login-title{
    text-align:center;
    font-size:28px;
    font-weight:bold;
    margin-bottom:10px;
}

/* =========================
   FOOTER
========================= */

.footer{
    text-align:center;
    color:#888;
    font-size:13px;
    margin-top:20px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================================
# LOGIN PAGE
# ==========================================================

def show_login():

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # ======================================================
    # LAYOUT
    # ======================================================

    kiri, tengah, kanan = st.columns([1.3, 1.4, 1.3])

    with tengah:

        # ==================================================
        # HEADER
        # ==================================================

        st.markdown(
            """
            <div class="logo">🍽️</div>

            <div class="title">
                Buffet The Padang Pasir
            </div>

            <div class="subtitle">
                Sistem Analisis Pola Transaksi Shopee Food<br>
                Menggunakan Metode K-Means Clustering
            </div>
            """,
            unsafe_allow_html=True
        )

        # ==================================================
        # CARD
        # ==================================================

        with st.container(border=True):

            st.markdown(
                """
                <div class="login-title">
                    🔐 Login Administrator
                </div>
                """,
                unsafe_allow_html=True
            )

            st.write("")

            with st.form("login_form"):

                username = st.text_input(
                    "Username",
                    placeholder="Masukkan Username"
                )

                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Masukkan Password"
                )

                st.write("")

                login = st.form_submit_button(
                    "Masuk",
                    type="primary",
                    use_container_width=True
                )

        st.markdown(
            """
            <div class="footer">
                © 2026 Buffet The Padang Pasir
            </div>
            """,
            unsafe_allow_html=True
        )

    # ======================================================
    # LOGIN
    # ======================================================

    if login:

        if verify_login(username, password):

            st.session_state.logged_in = True

            st.success("Login berhasil.")

            st.rerun()

        else:

            st.error("Username atau Password salah.")
