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
        <div style="text-align:center;">

            <div style="font-size:55px;">
                🍽️
            </div>

            <h1 style="
                margin-top:5px;
                margin-bottom:8px;
                color:#1f2937;
                font-weight:700;">
                Buffet The Padang Pasir
            </h1>

            <p style="
                color:#6b7280;
                font-size:17px;
                line-height:1.7;
                margin-bottom:35px;">

                Sistem Analisis Pola Transaksi Shopee Food
                <br>

                Menggunakan Metode K-Means Clustering

            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    # ======================================================
    # CARD LOGIN
    # ======================================================

    left, center, right = st.columns([2.5, 2, 2.5])

    with center:

        with st.container(border=True):

            st.markdown(
                """
                <h2 style="text-align:center;margin-bottom:5px;">
                    🔐 Login Administrator
                </h2>
                """,
                unsafe_allow_html=True
            )

            st.caption(
                "Silakan login menggunakan akun administrator untuk mengakses sistem."
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
    st.write("")

    st.markdown(
        """
        <div style="
            text-align:center;
            color:#9ca3af;
            font-size:14px;">

            © 2026 Buffet The Padang Pasir

        </div>
        """,
        unsafe_allow_html=True
    )
