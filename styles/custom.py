import streamlit as st

def load_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;500;700&display=swap');
        * { font-family: 'Inter', sans-serif; box-sizing: border-box; }
        .main { background: #f4f6f8; color: #333; }

        /* ===== SIDEBAR ===== */
        section[data-testid="stSidebar"] {
            background: linear-gradient(160deg, #03045e 0%, #023e8a 55%, #0077b6 100%) !important;
        }
        section[data-testid="stSidebar"] > div {
            background: transparent !important;
        }
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] .stMarkdown p,
        section[data-testid="stSidebar"] .stMarkdown span,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
        section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] span {
            color: #ffffff !important;
        }
        section[data-testid="stSidebar"] .stCaption,
        section[data-testid="stSidebar"] small {
            color: #c8d6f0 !important;
        }

        /* File uploader container */
        section[data-testid="stSidebar"] [data-testid="stFileUploader"] {
            background: rgba(255, 255, 255, 0.10) !important;
            border: 1px solid rgba(255, 255, 255, 0.28) !important;
            border-radius: 12px !important;
            padding: 0.5rem !important;
        }
        section[data-testid="stSidebar"] [data-testid="stFileUploader"] section,
        section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
            background: rgba(255, 255, 255, 0.06) !important;
            border: 1.5px dashed rgba(255, 255, 255, 0.40) !important;
            border-radius: 10px !important;
            color: #e8f0ff !important;
        }
        section[data-testid="stSidebar"] [data-testid="stFileUploader"] button,
        section[data-testid="stSidebar"] [data-testid="stFileUploader"] [data-testid="stBaseButton-secondary"],
        section[data-testid="stSidebar"] [data-testid="stFileUploader"] [data-testid="baseButton-secondary"] {
            background: rgba(255, 255, 255, 0.18) !important;
            color: #ffffff !important;
            border: 1px solid rgba(255, 255, 255, 0.40) !important;
            border-radius: 8px !important;
        }
        section[data-testid="stSidebar"] [data-testid="stFileUploader"] svg {
            fill: #ffffff !important;
            color: #ffffff !important;
        }
        section[data-testid="stSidebar"] [data-testid="stFileUploader"] p,
        section[data-testid="stSidebar"] [data-testid="stFileUploader"] span,
        section[data-testid="stSidebar"] [data-testid="stFileUploader"] small,
        section[data-testid="stSidebar"] [data-testid="stFileUploader"] label {
            color: #e8f0ff !important;
        }

        /* Fichier chargé : forcer fond sombre + texte clair */
        section[data-testid="stSidebar"] [data-testid="stFileUploaderFile"],
        section[data-testid="stSidebar"] [data-testid="stFileUploaderFileName"],
        section[data-testid="stSidebar"] [data-testid="stFileUploaderFileData"],
        section[data-testid="stSidebar"] [data-testid="stFileUploader"] > div > div {
            background: rgba(255, 255, 255, 0.12) !important;
            color: #ffffff !important;
            border-radius: 8px !important;
        }
        section[data-testid="stSidebar"] [data-testid="stFileUploaderFileName"],
        section[data-testid="stSidebar"] [data-testid="stFileUploaderFileData"] span,
        section[data-testid="stSidebar"] [data-testid="stFileUploaderFileData"] small {
            color: #ffffff !important;
        }
        /* Icône / bouton supprimer fichier */
        section[data-testid="stSidebar"] [data-testid="stFileUploaderDeleteBtn"],
        section[data-testid="stSidebar"] [data-testid="stFileUploader"] button[kind="secondary"] {
            color: #ffffff !important;
            background: transparent !important;
        }

        /* Metrics sidebar */
        section[data-testid="stSidebar"] [data-testid="stMetricValue"],
        section[data-testid="stSidebar"] [data-testid="stMetricLabel"] {
            color: #ffffff !important;
        }

        /* Boutons sidebar */
        section[data-testid="stSidebar"] .stButton > button {
            background: linear-gradient(135deg, #00b4d8, #0077b6) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25) !important;
        }
        section[data-testid="stSidebar"] .stButton > button:hover {
            background: linear-gradient(135deg, #48cae4, #0096c7) !important;
        }

        /* Success message sidebar */
        section[data-testid="stSidebar"] [data-testid="stAlert"] {
            background: rgba(0, 180, 100, 0.25) !important;
            color: #ffffff !important;
            border: 1px solid rgba(255,255,255,0.3) !important;
        }

        /* ===== HEADER ===== */
        .banking-header {
            background: linear-gradient(135deg, #03045e 0%, #023e8a 100%);
            padding: 2.5rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            color: white;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }

        .stPlotlyChart {
            border: none;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .dataframe {
            border-radius: 15px !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .stButton > button {
            border-radius: 8px;
            background-color: #FF6F61;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            font-size: 1rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .stButton > button:hover {
            background-color: #FF3B3F;
        }

        .action-card {
            background: white;
            border: 2px solid #023e8a;
            border-radius: 14px;
            padding: 1.5rem 2rem;
            text-align: center;
            box-shadow: 0 4px 14px rgba(2, 62, 138, 0.12);
            margin: 1rem 0 2rem 0;
        }
        .action-card h3 { color: #023e8a; margin: 0 0 0.5rem 0; }
        .action-card p { color: #555; margin: 0; }
    </style>
    """, unsafe_allow_html=True)
