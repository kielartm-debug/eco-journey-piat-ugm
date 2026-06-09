import base64
import html
import random
from pathlib import Path

import pandas as pd
import streamlit as st
from PIL import Image


st.set_page_config(
    page_title="Eco-Journey PIAT UGM",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)


def load_css():
    st.markdown(
        """
        <style>
        :root {
            --eco-dark: #2f4f2f;
            --eco-main: #4f7c42;
            --eco-soft: #e8f2d7;
            --cream: #f4efe4;
            --gold: #b98212;
            --sidebar: #314634;
            --text: #1e241c;
        }

        .stApp {
            background: var(--cream);
            color: var(--text);
        }

        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        [data-testid="stMainBlockContainer"] {
            background: var(--cream) !important;
            color: var(--text) !important;
        }

        [data-testid="stMain"] h1,
        [data-testid="stMain"] h2,
        [data-testid="stMain"] h3,
        [data-testid="stMain"] h4,
        [data-testid="stMain"] h5,
        [data-testid="stMain"] h6,
        [data-testid="stMain"] p,
        [data-testid="stMain"] li,
        [data-testid="stMain"] span,
        [data-testid="stMain"] label,
        [data-testid="stMain"] div[data-testid="stMarkdownContainer"],
        [data-testid="stMain"] div[data-testid="stMarkdownContainer"] * {
            color: var(--text);
        }

        [data-testid="stMain"] [data-testid="stWidgetLabel"],
        [data-testid="stMain"] [data-testid="stWidgetLabel"] *,
        [data-testid="stMain"] [data-testid="stRadio"] label,
        [data-testid="stMain"] [data-testid="stRadio"] label *,
        [data-testid="stMain"] [data-testid="stSlider"] label,
        [data-testid="stMain"] [data-testid="stSlider"] label *,
        [data-testid="stMain"] [data-testid="stTextInput"] label,
        [data-testid="stMain"] [data-testid="stTextInput"] label *,
        [data-testid="stMain"] [data-testid="stTextArea"] label,
        [data-testid="stMain"] [data-testid="stTextArea"] label * {
            color: var(--text) !important;
        }

        [data-testid="stMain"] [data-testid="stTextInput"] input,
        [data-testid="stMain"] [data-testid="stTextArea"] textarea {
            background: #fffdf4 !important;
            color: var(--text) !important;
            border: 1px solid rgba(49, 70, 52, 0.28) !important;
        }

        [data-testid="stMain"] [data-testid="stTextInput"] input::placeholder,
        [data-testid="stMain"] [data-testid="stTextArea"] textarea::placeholder {
            color: rgba(30, 36, 28, 0.58) !important;
        }

        [data-testid="stMain"] [data-testid="stRadio"] div[role="radiogroup"] label {
            background: rgba(255, 253, 244, 0.78);
            border-radius: 10px;
        }

        [data-testid="stMain"] [data-testid="stImageCaption"],
        [data-testid="stMain"] [data-testid="stImageCaption"] * {
            color: #314634 !important;
        }

        [data-testid="stMain"] [data-testid="stDataFrame"] {
            background: #fffdf4;
            color: var(--text);
        }

        .block-container {
            max-width: 1180px;
            padding-top: 2rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }

        header[data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #26392b 0%, #40563d 100%);
            border-right: 1px solid rgba(255, 255, 255, 0.12);
        }

        [data-testid="stSidebar"] * {
            color: #f8f1df;
            font-weight: 650;
        }

        [data-testid="stSidebar"] h1 {
            color: #e5bd45;
            font-family: Georgia, "Times New Roman", serif;
            font-size: 1.75rem;
            margin-top: 2rem;
        }

        [data-testid="stSidebar"] input {
            background: rgba(255, 255, 255, 0.12);
            border: 1px solid rgba(255, 255, 255, 0.22);
        }

        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
            display: flex;
            flex-direction: column;
            gap: 0.55rem;
        }

        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
            width: 100%;
            min-height: 46px;
            padding: 0.62rem 0.85rem;
            border-radius: 12px;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.12);
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.08);
            transition: background 160ms ease, transform 160ms ease, border-color 160ms ease;
        }

        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
            background: rgba(229, 189, 69, 0.18);
            border-color: rgba(229, 189, 69, 0.38);
            transform: translateX(3px);
        }

        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) {
            background: linear-gradient(135deg, rgba(229, 189, 69, 0.95), rgba(125, 151, 87, 0.88));
            border-color: rgba(255, 255, 255, 0.4);
            box-shadow: 0 10px 22px rgba(0, 0, 0, 0.18);
        }

        [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) * {
            color: #203225 !important;
        }

        [data-testid="stSidebar"] .stRadio input[type="radio"] {
            opacity: 0;
            width: 0;
            margin: 0;
        }

        .hero {
            margin-bottom: 1.4rem;
        }

        .banner-frame {
            width: 100%;
            height: clamp(180px, 24vw, 300px);
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 16px 34px rgba(48, 64, 42, 0.18);
            border: 1px solid rgba(63, 80, 47, 0.16);
            background: rgba(255, 255, 255, 0.45);
        }

        .banner-frame img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            object-position: center;
            display: block;
        }

        .hero h1 {
            color: var(--gold);
            font-family: Georgia, "Times New Roman", serif;
            font-size: 2.35rem;
            line-height: 1.16;
            margin: 1.4rem 0 0.45rem 0;
            letter-spacing: 0;
        }

        .hero p {
            font-size: 1.02rem;
            max-width: 900px;
            margin: 0;
            color: #32412f;
            font-weight: 550;
        }

        .hero-placeholder {
            min-height: 295px;
            border-radius: 16px;
            background:
                linear-gradient(120deg, rgba(38, 57, 43, 0.92), rgba(76, 103, 61, 0.74)),
                repeating-linear-gradient(45deg, rgba(255,255,255,0.12) 0 12px, transparent 12px 24px);
            display: flex;
            align-items: center;
            justify-content: center;
            color: #fff8e7;
            text-align: center;
            font-weight: 800;
            box-shadow: 0 16px 34px rgba(48, 64, 42, 0.18);
        }

        .eco-card {
            background: rgba(255, 255, 255, 0.96);
            border: 1px solid rgba(62, 77, 54, 0.08);
            border-radius: 14px;
            padding: 1.55rem;
            box-shadow: 0 14px 28px rgba(55, 45, 31, 0.12);
            margin-bottom: 1.15rem;
            color: #171c16;
        }

        .eco-card h2,
        .eco-card h3 {
            font-family: Georgia, "Times New Roman", serif;
            color: #111811;
            letter-spacing: 0;
        }

        .eco-card p {
            font-size: 1.02rem;
            line-height: 1.55;
        }

        .mini-card {
            min-height: 150px;
            border-left: 7px solid var(--eco-main);
        }

        .fact-card {
            min-height: 205px;
            position: relative;
            overflow: hidden;
            border-left: 0;
        }

        .fact-card::before {
            content: attr(data-number);
            position: absolute;
            right: 1.1rem;
            top: 0.4rem;
            color: rgba(185, 130, 18, 0.13);
            font-family: Georgia, "Times New Roman", serif;
            font-size: 5.4rem;
            line-height: 1;
            font-weight: 900;
        }

        .fact-label {
            display: inline-block;
            margin-bottom: 0.7rem;
            padding: 0.28rem 0.65rem;
            border-radius: 999px;
            background: #e8f2d7;
            color: #314634;
            font-weight: 800;
            font-size: 0.85rem;
        }

        .timeline-dot {
            position: relative;
            z-index: 1;
            width: 2.9rem;
            height: 2.9rem;
            border-radius: 999px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #fff8df;
            border: 3px solid #b98212;
            box-shadow: 0 8px 18px rgba(55, 45, 31, 0.14);
            color: #314634;
            font-weight: 900;
            margin: 0.65rem auto 0.9rem auto;
        }

        .timeline-card {
            background: rgba(255, 255, 255, 0.94);
            border: 1px solid rgba(62, 77, 54, 0.08);
            border-radius: 14px;
            padding: 1rem 1.15rem;
            box-shadow: 0 12px 26px rgba(55, 45, 31, 0.1);
            margin-bottom: 0.9rem;
        }

        .timeline-year {
            color: #b98212;
            font-family: Georgia, "Times New Roman", serif;
            font-size: 1.45rem;
            font-weight: 900;
            margin-bottom: 0.25rem;
        }

        .timeline-card p {
            margin: 0;
            color: #203225;
            line-height: 1.55;
            font-weight: 550;
        }

        .simulation-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 1rem;
            margin-bottom: 1.2rem;
        }

        .result-box {
            background: #fff8df;
            border-left: 7px solid #b98212;
            border-radius: 14px;
            padding: 1rem 1.15rem;
            box-shadow: 0 12px 26px rgba(55, 45, 31, 0.1);
            margin-top: 1rem;
        }

        .result-box h3 {
            margin-top: 0;
            color: #314634;
            font-family: Georgia, "Times New Roman", serif;
        }

        .score-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 6rem;
            height: 6rem;
            border-radius: 999px;
            background: linear-gradient(135deg, #b98212, #4f7c42);
            color: white;
            font-size: 1.7rem;
            font-weight: 900;
            box-shadow: 0 14px 28px rgba(55, 45, 31, 0.16);
            margin-bottom: 0.8rem;
        }

        .challenge-card {
            background: linear-gradient(135deg, #fffdf4, #e8f2d7);
            border: 1px solid rgba(79, 124, 66, 0.18);
            border-radius: 16px;
            padding: 1.25rem;
            box-shadow: 0 14px 28px rgba(55, 45, 31, 0.12);
        }

        .game-hero {
            background:
                linear-gradient(135deg, rgba(49, 70, 52, 0.96), rgba(79, 124, 66, 0.9)),
                radial-gradient(circle at top right, rgba(229, 189, 69, 0.38), transparent 34%);
            color: #fff8df;
            border-radius: 18px;
            padding: 1.6rem;
            box-shadow: 0 18px 36px rgba(49, 70, 52, 0.22);
            margin-bottom: 1.2rem;
        }

        .game-hero h2 {
            color: #e5bd45;
            font-family: Georgia, "Times New Roman", serif;
            font-size: 2rem;
            margin: 0 0 0.45rem 0;
        }

        .game-hero p {
            margin: 0;
            max-width: 860px;
            line-height: 1.55;
            font-weight: 650;
        }

        .mission-card {
            background: rgba(255, 255, 255, 0.96);
            border: 1px solid rgba(62, 77, 54, 0.1);
            border-radius: 16px;
            padding: 1.2rem;
            min-height: 155px;
            box-shadow: 0 14px 28px rgba(55, 45, 31, 0.11);
        }

        .mission-card h3 {
            margin: 0.3rem 0 0.5rem 0;
            color: #111811;
            font-family: Georgia, "Times New Roman", serif;
        }

        .mission-tag {
            display: inline-block;
            padding: 0.28rem 0.62rem;
            border-radius: 999px;
            background: #e8f2d7;
            color: #314634;
            font-size: 0.82rem;
            font-weight: 900;
        }

        .game-result {
            display: grid;
            grid-template-columns: auto 1fr;
            gap: 1rem;
            align-items: center;
            background: linear-gradient(135deg, #fffdf4, #e8f2d7);
            border: 1px solid rgba(79, 124, 66, 0.18);
            border-radius: 16px;
            padding: 1.15rem;
            box-shadow: 0 14px 28px rgba(55, 45, 31, 0.12);
            margin: 1rem 0;
        }

        .game-points {
            width: 4.8rem;
            height: 4.8rem;
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #314634;
            color: #e5bd45;
            font-size: 1.45rem;
            font-weight: 900;
            box-shadow: inset 0 0 0 2px rgba(229, 189, 69, 0.32);
        }

        @media (max-width: 900px) {
            .simulation-grid {
                grid-template-columns: 1fr;
            }
        }

        .section-title {
            color: var(--gold);
            font-family: Georgia, "Times New Roman", serif;
            font-size: 2rem;
            font-weight: 800;
            margin: 1rem 0 0.95rem 0;
            letter-spacing: 0;
        }

        .quote {
            background: #fff8df;
            border-left: 6px solid #ca8a04;
            border-radius: 12px;
            padding: 1rem 1.2rem;
            color: #713f12;
            font-style: italic;
            font-weight: 650;
            margin: 1rem 0;
        }

        .pill {
            display: inline-block;
            padding: 0.35rem 0.75rem;
            border-radius: 999px;
            background: rgba(245, 225, 157, 0.18);
            color: #f8f1df;
            font-weight: 700;
            margin: 0.25rem 0.35rem 0.25rem 0;
            border: 1px solid rgba(255, 255, 255, 0.18);
        }

        .metric-box {
            text-align: center;
            padding: 1rem;
            background: white;
            border-radius: 14px;
            border: 1px solid rgba(22, 101, 52, 0.12);
            box-shadow: 0 10px 24px rgba(55, 45, 31, 0.1);
        }

        .metric-box strong {
            display: block;
            font-size: 1.65rem;
            color: var(--gold);
            font-family: Georgia, "Times New Roman", serif;
        }

        .gallery-placeholder {
            min-height: 180px;
            border: 2px dashed rgba(79, 124, 66, 0.38);
            border-radius: 14px;
            background: rgba(232, 242, 215, 0.75);
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            color: #2f4f2f;
            font-weight: 700;
            padding: 1rem;
        }

        [data-testid="stImage"] img {
            border-radius: 16px;
            box-shadow: 0 16px 34px rgba(48, 64, 42, 0.18);
        }

        div.stButton > button {
            background: #4f7c42;
            color: white;
            border: 0;
            border-radius: 10px;
            padding: 0.65rem 1.05rem;
            font-weight: 750;
        }

        div.stButton > button:hover {
            background: #314634;
            color: white;
            border: 0;
        }

        div[data-testid="stAlert"] {
            border-radius: 12px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def show_hero(visitor_name):
    safe_name = html.escape(visitor_name.strip())
    name_text = f"Halo, {safe_name}! " if safe_name else ""
    cover_path = Path("images/image1.jpeg")

    if cover_path.exists():
        encoded_image = base64.b64encode(cover_path.read_bytes()).decode("utf-8")
        st.markdown(
            f"""
            <div class="banner-frame">
                <img src="data:image/jpeg;base64,{encoded_image}" alt="Header Eco-Journey PIAT UGM">
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="hero-placeholder">
                <div>
                    <div style="font-size: 2.4rem;">Eco-Journey PIAT UGM</div>
                    <div style="font-size: 1rem; margin-top: .4rem;">Tambahkan gambar utama di images/image1.jpeg</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="hero">
            <h1>Eco-Journey PIAT UGM</h1>
            <p>{name_text}Belajar agroteknologi, smart eco-bioproduction, dan pengelolaan
            limbah masa depan melalui ruang edukasi digital yang interaktif.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def eco_card(title, body, icon="🌿", extra_class=""):
    st.markdown(
        f"""
        <div class="eco-card {extra_class}">
            <h3>{icon} {title}</h3>
            <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def content_card(title, paragraphs):
    body = "".join(f"<p>{paragraph}</p>" for paragraph in paragraphs)
    st.markdown(
        f"""
        <div class="eco-card">
            <h2>{title}</h2>
            {body}
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_image_if_exists(image_path, caption):
    path = Path(image_path)
    if path.exists():
        image = Image.open(path)
        st.image(image, caption=caption, use_column_width=True)
    else:
        st.markdown(
            f"""
            <div class="gallery-placeholder">
                Gambar belum tersedia<br>
                <small>{image_path}</small>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.warning(f"File `{image_path}` belum ditemukan. Tambahkan gambar ke folder `images/`.")


def page_home(visitor_name):
    show_hero(visitor_name)

    st.markdown('<div class="section-title">Selamat Datang di Ruang Jelajah Hijau</div>', unsafe_allow_html=True)
    st.write(
        "Website ini mengajak kamu memahami bagaimana PIAT UGM menghubungkan pertanian "
        "berkelanjutan, teknologi modern, dan pengelolaan sampah terpadu."
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-box"><strong>1975</strong>Awal Kebun Percobaan Kalitirto</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-box"><strong>2015</strong>Transformasi menjadi PIAT UGM</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-box"><strong>100</strong>Skor maksimal quiz interaktif</div>', unsafe_allow_html=True)

    st.divider()

    col_a, col_b = st.columns(2)
    with col_a:
        eco_card(
            "Agroteknologi Lestari",
            "Mengenal praktik pertanian modern yang tetap menjaga keseimbangan alam.",
            "🌾",
        )
    with col_b:
        eco_card(
            "Pengelolaan Limbah",
            "Melihat bagaimana sampah dapat diproses menjadi kompos dan sumber manfaat baru.",
            "♻️",
        )


def page_profile():
    st.markdown('<div class="section-title">Profil Pembuat</div>', unsafe_allow_html=True)
    content_card(
        "Eco-Journey PIAT UGM",
        [
            'Website <strong>"Eco-Journey PIAT UGM: Belajar Agroteknologi dan Pengelolaan Limbah Masa Depan"</strong> merupakan ruang edukasi digital yang merangkum rangkaian studi lapangan kami. Melalui platform ini, kami ingin membagikan pandangan baru mengenai integrasi antara ilmu pertanian modern yang lestari dengan solusi nyata pengelolaan sampah demi menjaga masa depan bumi.',
            "Kami berharap rekam jejak perjalanan edukatif ini tidak sekadar menjadi tugas sekolah, tetapi juga mampu memantik kesadaran generasi muda akan pentingnya inovasi hijau dan kepedulian terhadap lingkungan sekitar.",
            "Langkah kami tentu belum sempurna. Oleh karena itu, ruang diskusi melalui kritik dan saran yang membangun dari kamu akan sangat berarti untuk penyempurnaan website ini ke depannya. Selamat menjelajah!",
        ],
    )

    st.markdown('<div class="section-title">Karya Digital Ini Dikembangkan Oleh</div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        eco_card("Faiza Syifa Nadia", "Kelas X-5", "🌱", "mini-card")
    with col2:
        eco_card("Qanita Sharah Hafizah", "Kelas X-5", "🌿", "mini-card")


def page_history():
    st.markdown('<div class="section-title">Napak Tilas PIAT UGM</div>', unsafe_allow_html=True)

    timeline_items = [
        ("1975", "Didirikan sebagai Kebun Percobaan Kalitirto."),
        (
            "Perkembangan",
            "Fokus meluas untuk menjawab perubahan iklim, ketahanan pangan, dan krisis sampah.",
        ),
        ("2015", "Resmi berganti nama menjadi Pusat Inovasi Agroteknologi (PIAT) UGM."),
        (
            "Kini",
            "Mengembangkan smart eco-bioproduction, Citrus Learning Center, dan pengelolaan sampah terpadu.",
        ),
    ]
    for index, (year, event) in enumerate(timeline_items, start=1):
        dot_col, card_col = st.columns([0.12, 0.88])
        with dot_col:
            st.markdown(f'<div class="timeline-dot">{index}</div>', unsafe_allow_html=True)
        with card_col:
            st.markdown(
                f"""
                <div class="timeline-card">
                    <div class="timeline-year">{year}</div>
                    <p>{event}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown(
        """
        <div style="
            height: 1px;
            margin: 1.2rem 0 1.6rem 0;
            background: linear-gradient(90deg, transparent, rgba(185, 130, 18, 0.55), rgba(79, 124, 66, 0.35), transparent);
        "></div>
        """,
        unsafe_allow_html=True,
    )

    content_card(
        "Dari Kebun Percobaan Menuju Pusat Inovasi",
        [
            "Perjalanan tempat ini dimulai sejak tahun 1975, di mana kawasan ini awalnya didirikan dengan nama <strong>Kebun Percobaan Kalitirto</strong>. Jauh sebelum secanggih sekarang, fungsinya berfokus sebagai laboratorium lapangan untuk mendukung kegiatan praktikum, penelitian, serta ruang uji coba teori bagi para dosen dan mahasiswa UGM langsung di alam terbuka, khususnya di sektor pertanian.",
            "Seiring berjalannya waktu, fokus tempat ini mulai meluas demi menjawab tantangan zaman seperti isu perubahan iklim, ancaman ketahanan pangan, hingga krisis penumpukan sampah yang semakin nyata. Kebun percobaan ini pun bertransformasi menjadi pusat pencarian solusi yang tidak lagi sekadar menjadi lahan hijau tempat menanam tanaman.",
        ],
    )

    st.markdown(
        '<div class="quote">"Inovasi sejati lahir ketika kebutuhan alam dan teknologi ramah lingkungan saling melengkapi."</div>',
        unsafe_allow_html=True,
    )

    content_card(
        "Transformasi Tahun 2015",
        [
            "Momen perubahan besar akhirnya terjadi pada tahun 2015 ketika tempat ini resmi berganti nama menjadi <strong>Pusat Inovasi Agroteknologi (PIAT) UGM</strong> dan bergerak sebagai pusat studi interdisipliner mandiri.",
            "Lewat wajah baru ini, PIAT UGM hadir sebagai pelopor konsep <strong>smart eco-bioproduction</strong> yang mengintegrasikan teknologi modern dengan kelestarian alam. Kini, melalui fasilitas unggulan seperti Citrus Learning Center dan sistem workshop pengelolaan sampah terpadu, tempat ini sukses menjadi bukti nyata bahwa inovasi pertanian berkelanjutan dapat berjalan beriringan dengan solusi pengelolaan limbah masa depan demi bumi yang lebih hijau.",
        ],
    )


def page_gallery():
    st.markdown('<div class="section-title">Galeri Kegiatan</div>', unsafe_allow_html=True)

    gallery_items = [
        (
            "images/image2.jpeg",
            "Akses Citrus Learning Center",
            "Akses masuk menuju pusat pembelajaran budidaya dan kelestarian berbagai varietas jeruk unggulan.",
        ),
        (
            "images/image3.jpeg",
            "Praktik Pengolahan Limbah Alami",
            "Praktik mengolah limbah alami (kohe, daun, batang pisang) menjadi pupuk, sekaligus mengamati mikroorganisme penjaga kesuburan tanah.",
        ),
        (
            "images/image4.jpeg",
            "Mikroorganisme dan Pupuk Organik",
            "Praktik mengolah limbah alami (kohe, daun, batang pisang) menjadi pupuk, sekaligus mengamati mikroorganisme penjaga kesuburan tanah.",
        ),
        (
            "images/image5.jpeg",
            "Rumah Kaca Modern",
            "Rumah kaca modern dengan kondisi lingkungan terkontrol untuk perawatan optimal tanaman hias dan anggrek.",
        ),
        (
            "images/image6.jpeg",
            "Area Bedengan Luar Ruangan",
            "Area bedengan luar ruangan untuk menguji sistem pertanian ramah lingkungan dan ketahanan pangan.",
        ),
        (
            "images/image7.jpeg",
            "Eco-Waste Management",
            "Pusat pemrosesan sampah terpadu yang memanfaatkan mesin pemilah untuk mendaur ulang limbah secara maksimal.",
        ),
    ]

    cols = st.columns(2)
    for index, (image_path, caption, description) in enumerate(gallery_items):
        with cols[index % 2]:
            show_image_if_exists(image_path, caption)
            st.markdown(f"### {caption}")
            st.write(description)
            st.write("")


def page_fun_fact():
    st.markdown('<div class="section-title">Fun Fact PIAT UGM</div>', unsafe_allow_html=True)

    facts = [
        (
            "01",
            "Rumah Spesialis Jeruk",
            "Memiliki Citrus Learning Center sebagai pusat pelestarian dan penyelamatan berbagai varietas jeruk unggulan Indonesia.",
            "🍊",
        ),
        (
            "02",
            "Penyihir Sampah Raksasa",
            "Menggunakan mesin pemilah mekanis untuk menyulap gunungan sampah rumah tangga menjadi pupuk kompos berguna.",
            "♻️",
        ),
        (
            "03",
            "Ramuan Pupuk Unik",
            "Mengombinasikan kotoran kambing, daun kirinyu, hingga cacahan batang pisang menjadi media tanam super subur.",
            "🧪",
        ),
        (
            "04",
            "Eksis Sejak 1975",
            "Sudah berdiri selama puluhan tahun, berawal dari kebun percobaan sederhana hingga kini menjadi pusat riset tercanggih UGM.",
            "📍",
        ),
    ]

    cols = st.columns(2)
    for index, (number, title, body, icon) in enumerate(facts):
        with cols[index % 2]:
            st.markdown(
                f"""
                <div class="eco-card fact-card" data-number="{number}">
                    <span class="fact-label">Fun Fact {number}</span>
                    <h3>{icon} {title}</h3>
                    <p>{body}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def page_quiz(visitor_name):
    st.markdown('<div class="section-title">Quiz Interaktif</div>', unsafe_allow_html=True)
    st.write("Jawab 5 soal berikut. Setiap jawaban benar bernilai 20 poin.")

    questions = [
        {
            "question": "Tahun berapakah Kebun Percobaan Kalitirto (cikal bakal PIAT UGM) pertama kali didirikan?",
            "options": ["1965", "1975", "2015"],
            "answer": "1975",
        },
        {
            "question": "Fasilitas di PIAT UGM yang khusus digunakan untuk melestarikan berbagai varietas jeruk unggulan adalah...",
            "options": ["Citrus Learning Center", "Greenhouse Anggrek", "Eco-Waste Management"],
            "answer": "Citrus Learning Center",
        },
        {
            "question": "Bahan alami unik apa saja yang diramu di area workshop untuk membuat media tanam super subur?",
            "options": [
                "Plastik, kertas, dan logam",
                "Kotoran kambing, daun kirinyu, dan batang pisang",
                "Pasir pantai, kerikil, dan tanah merah",
            ],
            "answer": "Kotoran kambing, daun kirinyu, dan batang pisang",
        },
        {
            "question": "Apa fungsi utama dari fasilitas Eco-Waste Management di PIAT UGM?",
            "options": [
                "Tempat menanam padi modern",
                "Pusat pemrosesan dan daur ulang sampah terpadu",
                "Laboratorium khusus pembibitan tanaman hias",
            ],
            "answer": "Pusat pemrosesan dan daur ulang sampah terpadu",
        },
        {
            "question": "Pada tahun 2015, Kebun Percobaan Kalitirto resmi bertransformasi dan berganti nama menjadi...",
            "options": [
                "Fakultas Pertanian UGM",
                "Pusat Inovasi Agroteknologi (PIAT) UGM",
                "Agro-Eco-Tourism UGM",
            ],
            "answer": "Pusat Inovasi Agroteknologi (PIAT) UGM",
        },
    ]

    with st.form("quiz_form"):
        answers = []
        for number, item in enumerate(questions, start=1):
            st.markdown(f"**{number}. {item['question']}**")
            selected = st.radio(
                "Pilih jawaban:",
                item["options"],
                key=f"quiz_{number}",
                label_visibility="collapsed",
            )
            answers.append(selected)
            st.write("")

        submitted = st.form_submit_button("Hitung Skor")

    if submitted:
        score = sum(20 for answer, item in zip(answers, questions) if answer == item["answer"])
        display_name = html.escape(visitor_name.strip()) if visitor_name.strip() else "Sobat Eco"

        st.markdown(f"### Skor {display_name}: {score}/100")
        st.progress(score / 100)

        if score == 100:
            st.balloons()
            st.success("Sangat baik! Kamu sudah memahami materi Eco-Journey PIAT UGM dengan luar biasa.")
        elif score >= 60:
            st.info("Baik! Pemahamanmu sudah bagus. Baca ulang bagian tertentu agar makin mantap.")
        else:
            st.warning("Ayo baca ulang materi Napak Tilas dan Fun Fact, lalu coba quiz ini lagi.")

        review_rows = []
        for number, (answer, item) in enumerate(zip(answers, questions), start=1):
            review_rows.append(
                {
                    "Soal": number,
                    "Jawaban Kamu": answer,
                    "Jawaban Benar": item["answer"],
                    "Status": "Benar" if answer == item["answer"] else "Perlu dicek",
                }
            )
        st.dataframe(pd.DataFrame(review_rows), hide_index=True, use_container_width=True)


def page_feedback(visitor_name):
    st.markdown('<div class="section-title">Feedback Pengunjung</div>', unsafe_allow_html=True)
    st.write("Masukan kamu akan ditampilkan kembali setelah tombol Kirim diklik. Belum ada database yang digunakan.")

    with st.form("feedback_form"):
        name = st.text_input("Nama pengunjung", value=visitor_name)
        origin = st.text_input("Kelas/asal")
        rating = st.slider("Rating pengalaman", min_value=1, max_value=5, value=5)
        message = st.text_area("Kritik dan saran", height=140)
        submitted = st.form_submit_button("Kirim Feedback")

    if submitted:
        if not name.strip() or not origin.strip() or not message.strip():
            st.error("Mohon lengkapi nama, kelas/asal, serta kritik dan saran terlebih dahulu.")
            return

        safe_name = html.escape(name.strip())
        safe_origin = html.escape(origin.strip())
        safe_message = html.escape(message.strip()).replace("\n", "<br>")

        st.success(f"Terima kasih, {safe_name}! Feedback kamu sudah diterima secara lokal di halaman ini.")
        st.markdown(
            f"""
            <div class="eco-card">
                <h3>Ringkasan Feedback</h3>
                <p><strong>Nama:</strong> {safe_name}</p>
                <p><strong>Kelas/asal:</strong> {safe_origin}</p>
                <p><strong>Rating:</strong> {rating}/5</p>
                <p><strong>Kritik dan saran:</strong><br>{safe_message}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def page_eco_lab():
    st.markdown(
        """
        <div class="game-hero">
            <h2>Eco Lab: Misi Penyelamat Lingkungan</h2>
            <p>
                Kamu berperan sebagai anggota tim Eco-Journey. Selesaikan misi pilah sampah,
                kumpulkan poin hijau, lalu buka tantangan harian untuk menjaga bumi tetap sehat.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="simulation-grid">
            <div class="mission-card">
                <span class="mission-tag">Misi 01</span>
                <h3>Pilah Bahan</h3>
                <p>Pilih bahan yang kamu temukan di area PIAT UGM.</p>
            </div>
            <div class="mission-card">
                <span class="mission-tag">Misi 02</span>
                <h3>Kumpulkan Poin</h3>
                <p>Setiap keputusan hijau menambah skor Eco Score.</p>
            </div>
            <div class="mission-card">
                <span class="mission-tag">Misi 03</span>
                <h3>Ambil Quest</h3>
                <p>Dapatkan tantangan kecil yang bisa dilakukan hari ini.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Misi 01: Pilah Bahan")
    waste_responses = {
        "Daun kering": (
            "Kompos",
            "Daun kering termasuk bahan organik. Bahan ini dapat dicacah dan diolah menjadi kompos untuk memperbaiki struktur tanah.",
            15,
        ),
        "Batang pisang": (
            "Media tanam organik",
            "Batang pisang dapat dicacah dan dicampur dengan bahan organik lain sebagai media tanam yang membantu menjaga kelembapan.",
            15,
        ),
        "Kotoran kambing": (
            "Pupuk organik",
            "Kotoran kambing dapat difermentasi menjadi pupuk organik. Prosesnya perlu waktu dan pengolahan agar aman untuk tanaman.",
            15,
        ),
        "Botol plastik": (
            "Daur ulang anorganik",
            "Botol plastik perlu dipisahkan dari sampah organik agar bisa masuk jalur daur ulang dan tidak mencemari kompos.",
            10,
        ),
        "Kertas bekas": (
            "Daur ulang kertas",
            "Kertas bekas dapat dikumpulkan terpisah untuk didaur ulang, selama tidak terlalu basah atau tercampur limbah makanan.",
            10,
        ),
        "Kaleng/logam": (
            "Daur ulang logam",
            "Kaleng atau logam harus dipilah karena masih punya nilai daur ulang dan tidak boleh masuk campuran kompos.",
            10,
        ),
        "Sampah campuran": (
            "Pilah ulang",
            "Sampah campuran perlu dipisahkan lebih dulu. Organik, plastik, kertas, dan logam memiliki jalur pengolahan berbeda.",
            5,
        ),
    }
    waste_type = st.radio(
        "Pilih item dari inventory Eco Lab:",
        list(waste_responses.keys()),
        horizontal=True,
    )
    category, explanation, decision_points = waste_responses[waste_type]

    st.markdown(
        f"""
        <div class="game-result">
            <div class="game-points">+{decision_points}</div>
            <div>
                <h3>Hasil Pilah: {category}</h3>
                <p>{explanation}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Misi 02: Hitung Eco Score")
    with st.form("eco_score_form"):
        tumbler = st.slider("Berapa kali kamu membawa tumbler minggu ini?", 0, 7, 3)
        sort_waste = st.slider("Berapa kali kamu memilah sampah minggu ini?", 0, 7, 3)
        reuse = st.slider("Berapa kali kamu memakai ulang barang minggu ini?", 0, 7, 2)
        plant_care = st.slider("Berapa kali kamu merawat tanaman atau ruang hijau minggu ini?", 0, 7, 2)
        submitted = st.form_submit_button("Selesaikan Misi dan Hitung Skor")

    if submitted:
        score = min(100, decision_points + tumbler * 8 + sort_waste * 9 + reuse * 7 + plant_care * 6)
        if score >= 85:
            rank = "Eco Guardian"
            message = "Luar biasa! Kebiasaan hijaumu sudah sangat kuat dan layak jadi contoh."
            st.balloons()
        elif score >= 60:
            rank = "Green Explorer"
            message = "Bagus! Kamu sudah punya kebiasaan ramah lingkungan. Tinggal dibuat lebih konsisten."
        else:
            rank = "Eco Rookie"
            message = "Masih bisa ditingkatkan. Mulai dari langkah kecil seperti memilah sampah dan membawa tumbler."

        st.markdown(
            f"""
            <div class="game-result">
                <div class="score-badge">{score}</div>
                <div>
                    <h3>Rank: {rank}</h3>
                    <p><strong>Eco Score Kamu: {score}/100</strong></p>
                    <p>{message}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.progress(score / 100)

    st.markdown("### Misi 03: Quest Hijau Hari Ini")
    challenges = [
        "Pilah minimal satu sampah organik dan satu sampah anorganik hari ini.",
        "Bawa tumbler atau botol minum sendiri agar mengurangi plastik sekali pakai.",
        "Cari satu bahan organik di rumah yang bisa dijadikan kompos.",
        "Ajak satu teman untuk membaca ulang bagian Fun Fact PIAT UGM.",
        "Amati satu tanaman di sekitar rumah/sekolah dan catat cara merawatnya.",
        "Gunakan kembali satu barang bekas sebelum memutuskan membuangnya.",
    ]

    if "daily_challenge" not in st.session_state:
        st.session_state.daily_challenge = random.choice(challenges)

    if st.button("Ambil Tantangan Baru"):
        st.session_state.daily_challenge = random.choice(challenges)

    st.markdown(
        f"""
        <div class="challenge-card">
            <span class="mission-tag">Daily Quest</span>
            <h3>Tantanganmu</h3>
            <p>{st.session_state.daily_challenge}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main():
    load_css()

    st.sidebar.title("🌱 Eco-Journey")
    st.sidebar.caption("PIAT UGM Learning Space")
    visitor_name = st.sidebar.text_input("Nama pengunjung", placeholder="Tulis namamu...")
    st.sidebar.divider()

    menu = st.sidebar.radio(
        "Menu",
        [
            "Beranda",
            "Profil Pembuat",
            "Napak Tilas",
            "Galeri",
            "Fun Fact",
            "Quiz Interaktif",
            "Eco Lab Interaktif",
            "Feedback",
        ],
    )

    st.sidebar.divider()
    st.sidebar.markdown(
        """
        <span class="pill">Agroteknologi</span>
        <span class="pill">Eco</span>
        <span class="pill">Limbah</span>
        """,
        unsafe_allow_html=True,
    )

    if menu == "Beranda":
        page_home(visitor_name)
    elif menu == "Profil Pembuat":
        page_profile()
    elif menu == "Napak Tilas":
        page_history()
    elif menu == "Galeri":
        page_gallery()
    elif menu == "Fun Fact":
        page_fun_fact()
    elif menu == "Quiz Interaktif":
        page_quiz(visitor_name)
    elif menu == "Eco Lab Interaktif":
        page_eco_lab()
    elif menu == "Feedback":
        page_feedback(visitor_name)


if __name__ == "__main__":
    main()
