import streamlit as st

from utils.auth import verify_login


# ==========================================================
# LOGIN PAGE
# ==========================================================

def show_login():

    if "logged_in" not in st.session_state:

        st.session_state.logged_in = False

    st.title("🔐 Login Admin")

    st.caption(
        "Sistem Analisis Pola Transaksi Shopee Food"
    )

    st.divider()

    with st.form("login_form"):

        username = st.text_input(
            "Username"
        )

        password = st.text_input(
            "Password",
            type="password"
        )

        login = st.form_submit_button(
            "Login",
            use_container_width=True
        )

    if login:

        if verify_login(username, password):

            st.session_state.logged_in = True

            st.success(
                "Login berhasil."
            )

            st.rerun()

        else:

            st.error(
                "Username atau password salah."
            )
