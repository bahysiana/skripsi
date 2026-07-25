import streamlit as st

from utils.auth import verify_login


# ==========================================================
# CSS
# ==========================================================

st.markdown("""
<style>

/* Jarak halaman */
.block-container{
    padding-top:1.5rem;
    padding-bottom:1rem;
    max-width:1200px;
}

/* Hilangkan menu */
#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

header{
    visibility:hidden;
}

/* Judul */
.login-title{
    text-align:center;
    font-size:36px;
    font-weight:700;
    color:#222;
    margin-bottom:8px;
}

/* Subtitle */
.login-subtitle{
    text-align:center;
    color:#666;
    font-size:16px;
    line-height:1.7;
    margin-bottom:25px;
}

/* Footer */
.footer-login{
    text-align:center;
    color:#888;
    margin-top:25px;
    font-size:13px;
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
    # HEADER
    # ======================================================

    st.markdown(
        """
        <div style="text-align:center;font-size:70px;">
            🍽️
        </div>

        <div class="login-title">
            Buffet The Padang Pasir
        </div>

        <div class="login-subtitle">
            Sistem Analisis Pola Transaksi Shopee Food<br>
            Menggunakan Metode K-Means Clustering
        </div>
        """,
        unsafe_allow_html=True
    )

    # ======================================================
    # CARD LOGIN
    # ======================================================

    left, center, right = st.columns([1.4,1.6,1.4])

    with center:

        with st.container(border=True):

            st.markdown(
                "<h3 style='text-align:center;'>🔐 Login Administrator</h3>",
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
                    "🔓 Login",
                    type="primary",
                    use_container_width=True
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

    # ======================================================
    # FOOTER
    # ======================================================

    st.markdown(
        """
        <div class="footer-login">
            © 2026 Buffet The Padang Pasir
        </div>
        """,
        unsafe_allow_html=True
    )
