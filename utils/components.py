import streamlit as st


# ==========================================================
# SECTION TITLE
# ==========================================================

def section_title(title, subtitle=None):

    subtitle_html = ""

    if subtitle:

        subtitle_html = f"""

        <p class="section-subtitle">

            {subtitle}

        </p>

        """

    st.markdown(

        f"""

        <div class="section-title">

            <h2>{title}</h2>

            {subtitle_html}

        </div>

        """,

        unsafe_allow_html=True

    )


# ==========================================================
# HERO CARD
# ==========================================================

def hero_card(title, subtitle):

    st.markdown(

        f"""

        <div class="hero-card">

            <h1>{title}</h1>

            <p>{subtitle}</p>

        </div>

        """,

        unsafe_allow_html=True

    )


# ==========================================================
# METRIC CARD
# ==========================================================

def metric_card(title, value, icon="📊"):

    st.markdown(

        f"""

        <div class="metric-card">

            <div class="metric-icon">

                {icon}

            </div>

            <div class="metric-value">

                {value}

            </div>

            <div class="metric-title">

                {title}

            </div>

        </div>

        """,

        unsafe_allow_html=True

    )


# ==========================================================
# INFO CARD
# ==========================================================

def info_card(title, content):

    st.markdown(

        f"""

        <div class="info-card">

            <h4>{title}</h4>

            <p>{content}</p>

        </div>

        """,

        unsafe_allow_html=True

    )


# ==========================================================
# WARNING CARD
# ==========================================================

def warning_card(title, content):

    st.markdown(

        f"""

        <div class="warning-card">

            <h4>⚠️ {title}</h4>

            <p>{content}</p>

        </div>

        """,

        unsafe_allow_html=True

    )


# ==========================================================
# SUCCESS CARD
# ==========================================================

def success_card(message):

    st.markdown(

        f"""

        <div class="success-card">

            ✅ {message}

        </div>

        """,

        unsafe_allow_html=True

    )


# ==========================================================
# ANALYSIS CARD
# ==========================================================

def analysis_card(title, content, icon="💡"):

    st.markdown(

        f"""

        <div class="analysis-card">

            <h4>

                {icon} {title}

            </h4>

            <p>

                {content}

            </p>

        </div>

        """,

        unsafe_allow_html=True

    )


# ==========================================================
# RECOMMENDATION CARD
# ==========================================================

def recommendation_card(title, recommendations):

    items = ""

    for item in recommendations:

        items += f"<li>{item}</li>"

    st.markdown(

        f"""

        <div class="recommendation-card">

            <h4>{title}</h4>

            <ul>

                {items}

            </ul>

        </div>

        """,

        unsafe_allow_html=True

    )


# ==========================================================
# CLUSTER CARD
# ==========================================================

def cluster_card(cluster, nama_cluster, jumlah_data, persentase=None):

    persen = ""

    if persentase is not None:

        persen = f"""

        <div class="cluster-percent">

            {persentase:.2f}%

        </div>

        """

    st.markdown(

        f"""

        <div class="cluster-card">

            <div class="cluster-header">

                📌 {cluster}

            </div>

            <div class="cluster-name">

                {nama_cluster}

            </div>

            <div class="cluster-total">

                {jumlah_data} Transaksi

            </div>

            {persen}

        </div>

        """,

        unsafe_allow_html=True

    )


# ==========================================================
# EMPTY CARD
# ==========================================================

def empty_card(title, content):

    st.markdown(

        f"""

        <div class="empty-card">

            <h4>📂 {title}</h4>

            <p>{content}</p>

        </div>

        """,

        unsafe_allow_html=True

    )
