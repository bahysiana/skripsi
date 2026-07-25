import streamlit as st
from utils.auth import verify_login


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
        <div class="section-title">
            <h2>🍽️ Buffet The Padang Pasir</h2>
        </div>

        <div class="section-subtitle">
            Sistem Analisis Pola Transaksi Shopee Food<br>
            Menggunakan Metode K-Means Clustering
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # ======================================================
    # LOGIN FORM
    # ======================================================

    left, center, right = st.columns([2, 3, 2])

    with center:

        with st.container(border=True):

            st.subheader("🔐 Login Administrator")

            st.caption(
                "Silakan login menggunakan akun administrator untuk mengakses sistem."
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

    st.markdown(
        """
        <div style="text-align:center;color:#6c757d;">
            © 2026 Buffet The Padang Pasir
        </div>
        """,
        unsafe_allow_html=True
    )
