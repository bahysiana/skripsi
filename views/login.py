import streamlit as st

from utils.auth import verify_login


# ==========================================================
# CSS
# ==========================================================

st.markdown("""
<style>

/* Mengurangi ruang atas */
.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

/* Hilangkan menu dan footer bawaan */
#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

/* Judul */
.login-title{
    text-align:center;
    font-size:40px;
    font-weight:bold;
    color:#222222;
    margin-bottom:8px;
}

/* Subtitle */
.login-subtitle{
    text-align:center;
    font-size:18px;
    color:#666666;
    margin-bottom:30px;
}

/* Card */
.login-card{
    background:white;
    padding:35px;
    border-radius:15px;
    border:1px solid #EAEAEA;
    box-shadow:0px 4px 20px rgba(0,0,0,0.08);
}

/* Footer */
.footer-login{
    text-align:center;
    color:#888888;
    font-size:13px;
    margin-top:25px;
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
        <div class="login-title">
            🍽️ Buffet The Padang Pasir
        </div>

        <div class="login-subtitle">
            Sistem Analisis Pola Transaksi Shopee Food<br>
            Menggunakan Metode K-Means Clustering
        </div>
        """,
        unsafe_allow_html=True
    )

    # ======================================================
    # FORM DI TENGAH
    # ======================================================

    left, center, right = st.columns([1.3, 2, 1.3])

    with center:

        st.markdown(
            """
            <div class="login-card">
            <h3 style="text-align:center;margin-bottom:25px;">
                🔐 Login Administrator
            </h3>
            """,
            unsafe_allow_html=True
        )

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

            login = st.form_submit_button(
                "🔓 Login",
                type="primary",
                use_container_width=True
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )

    # ======================================================
    # PROSES LOGIN
    # ======================================================

    if login:

        if verify_login(username, password):

            st.session_state.logged_in = True

            st.success(
                "Login berhasil."
            )

            st.rerun()

        else:

            st.error(
                "Username atau Password salah."
            )

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
