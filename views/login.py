import streamlit as st
from utils.auth import verify_login


# ==========================================================
# CSS
# ==========================================================

st.markdown("""
<style>

/* =====================================================
   HALAMAN
===================================================== */

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
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

/* =====================================================
   HEADER
===================================================== */

.title{
    text-align:center;
    font-size:34px;
    font-weight:700;
    color:#222222;
    margin-bottom:5px;
}

.subtitle{
    text-align:center;
    font-size:16px;
    color:#666666;
    line-height:1.7;
    margin-bottom:25px;
}

.footer{
    text-align:center;
    color:#888888;
    margin-top:20px;
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

    st.markdown("""
<div class="title">
🍽️ Buffet The Padang Pasir
</div>

<div class="subtitle">
Sistem Analisis Pola Transaksi Shopee Food<br>
Menggunakan Metode K-Means Clustering
</div>
""", unsafe_allow_html=True)

    st.write("")

    # ======================================================
    # LOGIN DI TENGAH
    # ======================================================

    col1, col2, col3 = st.columns([1.2, 2, 1.2])

    with col2:

        with st.container(border=True):

            st.subheader("🔐 Login Administrator")

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

    st.write("")

    st.markdown("""
<div class="footer">
© 2026 Buffet The Padang Pasir
</div>
""", unsafe_allow_html=True)
