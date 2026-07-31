import streamlit as st
from styles.assets_b64 import FOND_B64, LOGO_B64

# Palette logo PayMeTrust
PRIMARY = "#3070F0"
PRIMARY_DARK = "#1A4FC4"
PRIMARY_DEEP = "#0B2A6B"
NAVY = "#061428"
NAVY_SOFT = "#0A1F3D"
ACCENT = "#5B9DFF"
TEXT_ON_DARK = "#F5F9FF"
TEXT_MUTED = "#C5DCFF"
TEXT_DARK = "#1A2332"

def load_css():
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif !important;
        }}

        /* ===== FOND IMAGE + DÉGRADÉ SOMBRE ===== */
        .stApp {{
            background:
                linear-gradient(
                    165deg,
                    rgba(6, 20, 40, 0.88) 0%,
                    rgba(10, 31, 61, 0.90) 40%,
                    rgba(11, 42, 107, 0.92) 70%,
                    rgba(6, 20, 40, 0.94) 100%
                ),
                url("data:image/jpeg;base64,{FOND_B64}")
                center center / cover no-repeat fixed !important;
        }}
        .main .block-container {{
            padding-top: 1.2rem;
            padding-bottom: 2rem;
            max-width: 1400px;
        }}
        [data-testid="stAppViewContainer"] > .main {{
            background: transparent !important;
        }}
        [data-testid="stHeader"] {{
            background: rgba(6, 20, 40, 0.75) !important;
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(91, 157, 255, 0.15);
        }}

        /* ===== TEXTES LISIBLES SUR FOND SOMBRE ===== */
        .main h1, .main h2, .main h3, .main h4, .main h5, .main h6,
        [data-testid="stAppViewContainer"] h1,
        [data-testid="stAppViewContainer"] h2,
        [data-testid="stAppViewContainer"] h3,
        [data-testid="stAppViewContainer"] h4,
        [data-testid="stMarkdownContainer"] h1,
        [data-testid="stMarkdownContainer"] h2,
        [data-testid="stMarkdownContainer"] h3,
        [data-testid="stMarkdownContainer"] h4,
        .main .stHeading,
        .main [data-testid="stHeadingWithActionElements"] h1,
        .main [data-testid="stHeadingWithActionElements"] h2,
        .main [data-testid="stHeadingWithActionElements"] h3 {{
            color: {TEXT_ON_DARK} !important;
            text-shadow: 0 1px 3px rgba(0,0,0,0.45) !important;
        }}

        .main p, .main span, .main li, .main label,
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] span,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stCaptionContainer"],
        [data-testid="stCaption"],
        .stCaption,
        div[data-testid="stText"],
        .main [data-testid="stCaptionContainer"] p,
        .main .stCaption,
        section[data-testid="stMain"] [data-testid="stCaption"] {{
            color: {TEXT_MUTED} !important;
            opacity: 1 !important;
            text-shadow: 0 1px 2px rgba(0,0,0,0.35);
        }}

        /* Alertes : fond clair pour lisibilité */
        .main [data-testid="stAlert"] {{
            background: rgba(255, 255, 255, 0.95) !important;
            border-radius: 12px !important;
            border: 1px solid rgba(48,112,240,0.3) !important;
        }}
        .main [data-testid="stAlert"] p,
        .main [data-testid="stAlert"] span,
        .main [data-testid="stAlert"] div {{
            color: {TEXT_DARK} !important;
            text-shadow: none !important;
        }}

        .main [data-testid="stExpander"] {{
            background: rgba(6, 20, 40, 0.65) !important;
            border: 1px solid rgba(91, 157, 255, 0.28) !important;
            border-radius: 12px !important;
        }}
        .main [data-testid="stExpander"] summary,
        .main [data-testid="stExpander"] summary span,
        .main [data-testid="stExpander"] p {{
            color: {TEXT_ON_DARK} !important;
        }}

        /* ===== SIDEBAR ===== */
        section[data-testid="stSidebar"] {{
            background: linear-gradient(175deg, {NAVY} 0%, {NAVY_SOFT} 40%, {PRIMARY_DEEP} 100%) !important;
            border-right: 1px solid rgba(91, 157, 255, 0.18);
        }}
        section[data-testid="stSidebar"] > div {{
            background: transparent !important;
        }}
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] .stMarkdown p,
        section[data-testid="stSidebar"] .stMarkdown span,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
        section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] span {{
            color: #ffffff !important;
        }}
        section[data-testid="stSidebar"] .stCaption,
        section[data-testid="stSidebar"] small,
        section[data-testid="stSidebar"] [data-testid="stCaption"] {{
            color: #A8C8F0 !important;
        }}

        section[data-testid="stSidebar"] [data-testid="stDateInput"] input,
        section[data-testid="stSidebar"] input[type="text"] {{
            background: rgba(255,255,255,0.95) !important;
            color: {TEXT_DARK} !important;
            border: 1px solid rgba(91,157,255,0.45) !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
        }}
        section[data-testid="stSidebar"] [data-testid="stDateInput"] label,
        section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {{
            color: #ffffff !important;
        }}

        section[data-testid="stSidebar"] [data-testid="stFileUploader"] {{
            background: rgba(48, 112, 240, 0.12) !important;
            border: 1px solid rgba(91, 157, 255, 0.35) !important;
            border-radius: 14px !important;
            padding: 0.55rem !important;
        }}
        section[data-testid="stSidebar"] [data-testid="stFileUploader"] section,
        section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {{
            background: rgba(255, 255, 255, 0.05) !important;
            border: 1.5px dashed rgba(91, 157, 255, 0.45) !important;
            border-radius: 12px !important;
            color: #e8f0ff !important;
        }}
        section[data-testid="stSidebar"] [data-testid="stFileUploader"] button,
        section[data-testid="stSidebar"] [data-testid="stFileUploader"] [data-testid="stBaseButton-secondary"],
        section[data-testid="stSidebar"] [data-testid="stFileUploader"] [data-testid="baseButton-secondary"] {{
            background: rgba(48, 112, 240, 0.35) !important;
            color: #ffffff !important;
            border: 1px solid rgba(91, 157, 255, 0.5) !important;
            border-radius: 10px !important;
        }}
        section[data-testid="stSidebar"] [data-testid="stFileUploader"] svg {{
            fill: #ffffff !important;
            color: #ffffff !important;
        }}
        section[data-testid="stSidebar"] [data-testid="stFileUploader"] p,
        section[data-testid="stSidebar"] [data-testid="stFileUploader"] span,
        section[data-testid="stSidebar"] [data-testid="stFileUploader"] small,
        section[data-testid="stSidebar"] [data-testid="stFileUploader"] label {{
            color: #e8f0ff !important;
        }}
        section[data-testid="stSidebar"] [data-testid="stFileUploaderFile"],
        section[data-testid="stSidebar"] [data-testid="stFileUploaderFileName"],
        section[data-testid="stSidebar"] [data-testid="stFileUploaderFileData"] {{
            background: rgba(48, 112, 240, 0.18) !important;
            color: #ffffff !important;
            border-radius: 8px !important;
        }}
        section[data-testid="stSidebar"] [data-testid="stFileUploaderFileName"],
        section[data-testid="stSidebar"] [data-testid="stFileUploaderFileData"] span,
        section[data-testid="stSidebar"] [data-testid="stFileUploaderFileData"] small {{
            color: #ffffff !important;
        }}

        section[data-testid="stSidebar"] .stButton > button {{
            background: linear-gradient(135deg, {PRIMARY} 0%, {PRIMARY_DARK} 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            box-shadow: 0 6px 18px rgba(48, 112, 240, 0.35) !important;
        }}
        section[data-testid="stSidebar"] .stButton > button:hover {{
            background: linear-gradient(135deg, {ACCENT} 0%, {PRIMARY} 100%) !important;
        }}

        /* ===== HEADER ===== */
        .pmt-header {{
            background: linear-gradient(120deg, rgba(6,20,40,0.95) 0%, rgba(26,79,196,0.90) 55%, rgba(48,112,240,0.85) 100%);
            border: 1px solid rgba(91, 157, 255, 0.4);
            border-radius: 20px;
            padding: 1.4rem 1.8rem;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 1.25rem;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.35);
            backdrop-filter: blur(12px);
        }}
        .pmt-header img {{
            width: 72px;
            height: 72px;
            object-fit: contain;
            filter: drop-shadow(0 4px 12px rgba(48,112,240,0.45));
        }}
        .pmt-header-text h1 {{
            margin: 0;
            font-weight: 800;
            font-size: 1.55rem;
            color: #ffffff !important;
            letter-spacing: -0.02em;
            text-shadow: none !important;
        }}
        .pmt-header-text p {{
            margin: 0.25rem 0 0 0;
            color: #C5DCFF !important;
            font-weight: 400;
            font-size: 0.95rem;
        }}
        .pmt-badge {{
            margin-left: auto;
            background: rgba(255,255,255,0.15);
            border: 1px solid rgba(255,255,255,0.3);
            color: #fff !important;
            padding: 0.35rem 0.85rem;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 600;
            white-space: nowrap;
        }}

        /* ===== TABS ===== */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 0.4rem;
            background: rgba(6, 20, 40, 0.55);
            padding: 0.4rem;
            border-radius: 14px;
            border: 1px solid rgba(91, 157, 255, 0.25);
        }}
        .stTabs [data-baseweb="tab"] {{
            border-radius: 10px !important;
            color: {TEXT_MUTED} !important;
            font-weight: 500;
        }}
        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, {PRIMARY}, {PRIMARY_DARK}) !important;
            color: #ffffff !important;
        }}

        /* Cartes / graphiques / tableaux : fond clair pour le contenu data */
        /* Cartes HTML metric_card — texte NOIR, fond blanc, accent bleu logo */
        .main .pmt-metric-card {{
            background: #FFFFFF !important;
            border: 1px solid rgba(48,112,240,0.18) !important;
            box-shadow: 0 4px 16px rgba(48,112,240,0.12) !important;
        }}
        .main .pmt-metric-card,
        .main .pmt-metric-card h3,
        .main .pmt-metric-card p,
        .main .pmt-metric-card span {{
            color: #000000 !important;
            text-shadow: none !important;
        }}
        .main .pmt-metric-card h3 {{
            color: #000000 !important;
            font-weight: 600 !important;
        }}
        .main .pmt-metric-card p {{
            color: #000000 !important;
            font-weight: 800 !important;
        }}

        /* st.metric natifs — fond blanc, texte noir, hauteur égale */
        div[data-testid="stMetric"] {{
            background: #FFFFFF !important;
            border-radius: 14px !important;
            padding: 0.85rem 1rem 0.75rem 1rem !important;
            border: 1px solid rgba(48,112,240,0.18) !important;
            border-left: 4px solid #3070F0 !important;
            box-shadow: 0 4px 16px rgba(48,112,240,0.12) !important;
            min-height: 120px !important;
            height: 100% !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
        }}
        div[data-testid="stMetric"] label,
        div[data-testid="stMetric"] [data-testid="stMetricLabel"],
        div[data-testid="stMetric"] [data-testid="stMetricLabel"] p,
        div[data-testid="stMetric"] [data-testid="stMetricLabel"] span {{
            color: #000000 !important;
            text-shadow: none !important;
            font-weight: 600 !important;
        }}
        div[data-testid="stMetric"] [data-testid="stMetricValue"],
        div[data-testid="stMetric"] [data-testid="stMetricValue"] > div {{
            color: #000000 !important;
            text-shadow: none !important;
            font-weight: 800 !important;
            font-size: 1.55rem !important;
        }}
        div[data-testid="stMetric"] [data-testid="stMetricDelta"],
        div[data-testid="stMetric"] [data-testid="stMetricDelta"] span {{
            color: #166534 !important;
            text-shadow: none !important;
        }}
        [data-testid="stHorizontalBlock"] > [data-testid="column"] {{
            display: flex !important;
            flex-direction: column !important;
        }}
        [data-testid="stHorizontalBlock"] > [data-testid="column"] > div {{
            flex: 1 1 auto !important;
        }}

        /* Graphiques Rapport — taille harmonisée */
        .stPlotlyChart {{
            background: #FFFFFF;
            border-radius: 16px;
            padding: 0.4rem;
            box-shadow: 0 4px 16px rgba(48,112,240,0.10);
            border: 1px solid rgba(48, 112, 240, 0.12);
            min-height: 320px !important;
            max-height: 340px !important;
        }}
        .stPlotlyChart > div {{
            min-height: 300px !important;
            max-height: 320px !important;
        }}
        [data-testid="stHorizontalBlock"] {{
            align-items: stretch !important;
        }}
        /* Deux colonnes graphiques : largeurs égales */
        [data-testid="stHorizontalBlock"] {{
            align-items: stretch !important;
        }}

        .stDataFrame, [data-testid="stDataFrame"] {{
            border-radius: 14px !important;
            overflow: hidden;
            box-shadow: 0 6px 18px rgba(0,0,0,0.15);
            background: rgba(255,255,255,0.97) !important;
        }}

        .stButton > button {{
            border-radius: 12px;
            background: linear-gradient(135deg, {PRIMARY}, {PRIMARY_DARK});
            color: white !important;
            border: none;
            font-weight: 600;
            box-shadow: 0 4px 14px rgba(48, 112, 240, 0.3);
        }}
        .stDownloadButton > button {{
            background: linear-gradient(135deg, {PRIMARY} 0%, {PRIMARY_DARK} 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
        }}

        .main [data-testid="stSpinner"] > div {{
            color: {TEXT_ON_DARK} !important;
        }}

        .pmt-footer {{
            text-align: center;
            padding: 1.5rem;
            color: {TEXT_MUTED} !important;
            font-size: 0.88rem;
            border-top: 1px solid rgba(91, 157, 255, 0.22);
            margin-top: 1rem;
        }}
        .pmt-footer strong, .pmt-footer p {{
            color: {TEXT_MUTED} !important;
        }}

        .sidebar-logo {{
            text-align: center;
            padding: 0.5rem 0 1rem 0;
        }}
        .sidebar-logo img {{
            width: 88px;
            height: 88px;
            object-fit: contain;
            filter: drop-shadow(0 4px 14px rgba(48,112,240,0.55));
        }}
        .sidebar-logo .brand {{
            color: #fff !important;
            font-weight: 700;
            font-size: 0.95rem;
            margin-top: 0.4rem;
            letter-spacing: 0.04em;
        }}

        .main [data-testid="stWidgetLabel"] p,
        .main [data-testid="stWidgetLabel"] span {{
            color: {TEXT_ON_DARK} !important;
        }}
    
        /* ===== FORCE NOIR sur metric cards Vue Globale (spécificité max) ===== */
        section[data-testid="stMain"] .pmt-metric-card,
        section[data-testid="stMain"] div.pmt-metric-card,
        [data-testid="stMarkdownContainer"] .pmt-metric-card,
        [data-testid="stMarkdownContainer"] div.pmt-metric-card {{
            background: #FFFFFF !important;
            color: #000000 !important;
        }}
        section[data-testid="stMain"] .pmt-metric-card h3,
        section[data-testid="stMain"] .pmt-metric-card p,
        section[data-testid="stMain"] .pmt-metric-card span,
        section[data-testid="stMain"] .pmt-metric-card *,
        [data-testid="stMarkdownContainer"] .pmt-metric-card h3,
        [data-testid="stMarkdownContainer"] .pmt-metric-card p,
        [data-testid="stMarkdownContainer"] .pmt-metric-card span,
        [data-testid="stMarkdownContainer"] .pmt-metric-card * {{
            color: #000000 !important;
            text-shadow: none !important;
            opacity: 1 !important;
            -webkit-text-fill-color: #000000 !important;
        }}

    </style>
    """, unsafe_allow_html=True)


def render_header():
    st.markdown(f"""
    <div class="pmt-header">
        <img src="data:image/png;base64,{LOGO_B64}" alt="PayMeTrust Logo" />
        <div class="pmt-header-text">
            <h1>APPLICATION DE RÉCONCILIATION REVENU ASSURANCE</h1>
            <p>Plateforme de réconciliation des flux partenaires — PayMeTrust</p>
        </div>
        <div class="pmt-badge">V2.1</div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar_logo():
    st.sidebar.markdown(f"""
    <div class="sidebar-logo">
        <img src="data:image/png;base64,{LOGO_B64}" alt="PayMeTrust" />
        <div class="brand">PAYMETRUST</div>
    </div>
    """, unsafe_allow_html=True)
