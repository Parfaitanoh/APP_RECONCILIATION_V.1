import streamlit as st

st.set_page_config(
    page_title="APP Reconciliation",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

import pandas as pd
from styles.custom import load_css
from partenaires import get_processor
from utils.helpers import metric_card
from datetime import datetime
import traceback

load_css()

st.markdown("""
    <div class='banking-header'>
        <h1 style='margin:0; font-weight:700;'>📊 APP DE RECONCILIATION REVENU ASSURANCE</h1>
        <p style='opacity:0.9; font-weight:300;'>Plateforme de réconciliation des flux partenaires</p>
    </div>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
st.sidebar.markdown("### 📁 Chargement des fichiers")
st.sidebar.caption("Limite relevée à **10 Go** par fichier")

st.sidebar.markdown("**1️⃣ Fichier Données PMT**")
data_file = st.sidebar.file_uploader(
    "PMT (CSV / Excel)",
    type=["csv", "xlsx", "xls"],
    help="Fichier extrait de la plateforme PMT",
    key="pmt_uploader",
)

st.sidebar.markdown("**2️⃣ Fichier Partenaire**")
partenaire_file = st.sidebar.file_uploader(
    "Partenaire (CSV / Excel)",
    type=["csv", "xlsx", "xls"],
    help="Fichier fourni par le partenaire (Wave, MTN, CinetPay…)",
    key="partner_uploader",
)

files_ready = bool(data_file and partenaire_file)
already = st.session_state.get("already_processed", False)

# Reset si les fichiers changent
file_sig = (
    (data_file.name if data_file else None, data_file.size if data_file else 0),
    (partenaire_file.name if partenaire_file else None, partenaire_file.size if partenaire_file else 0),
)
if st.session_state.get("file_sig") != file_sig:
    st.session_state["file_sig"] = file_sig
    st.session_state["already_processed"] = False
    already = False

# ---------- Zone principale selon l'état ----------
if not files_ready:
    st.info("👈 Veuillez charger les **deux fichiers** dans la barre latérale pour démarrer la réconciliation.")
    st.markdown("""
    ### Comment utiliser l'application
    1. Chargez le fichier **PMT** (export de votre système)
    2. Chargez le fichier **Partenaire** (export Wave, MTN, CinetPay, Bizao…)
    3. L'application détecte automatiquement le type de partenaire
    4. Cliquez sur **Lancer la réconciliation** dans la barre latérale
    5. Consultez les onglets puis **Télécharger le rapport final** (Excel multi-onglets)
    """)
    st.stop()

# Un seul bouton : Lancer → Relancer après exécution
st.sidebar.markdown("---")
if already:
    if st.sidebar.button("🔄 Relancer", type="primary", use_container_width=True, key="rerun_btn"):
        st.session_state["already_processed"] = False
        st.rerun()
    run_btn = False
else:
    run_btn = st.sidebar.button(
        "🚀 Lancer la réconciliation",
        type="primary",
        use_container_width=True,
        key="run_sidebar",
    )
    st.caption("👈 Cliquez sur **Lancer la réconciliation** dans la barre latérale pour démarrer.")

if run_btn or already:
    st.session_state["already_processed"] = True

    with st.spinner(f"Traitement en cours… ({partenaire_file.name})"):
        try:
            processor = get_processor(partenaire_file.name, data_file, partenaire_file)
            processor.process()

        except ValueError as e:
            st.error(f"❌ Type de partenaire non reconnu : {e}")
            st.info(
                "Le nom du fichier partenaire doit contenir le nom du partenaire "
                "et le type d'opération (ex: `waveci_payin.csv`, `mtnci_payout.xlsx`)."
            )
            st.session_state["already_processed"] = False
        except Exception as e:
            st.error(f"❌ Erreur de traitement : {e}")
            with st.expander("Détails techniques"):
                st.code(traceback.format_exc())
            st.session_state["already_processed"] = False

# Pied de page amélioré
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #666; font-size: 0.9rem;">
    <p>📊 <strong>APPLICATION Reconciliation V1.0</strong> | Développé par RA PMT</p>
    <p>🔄 Traitement des fichiers jusqu'à 2 GB | 📈 Analytics avancés | 📥 Rapports exportables</p>
    <p style="font-size: 0.8rem; margin-top: 10px;">
        Support technique : revenu.assurancepmt@paymetrust.net | 
        <a href="#" style="color: #023e8a; text-decoration: none;">Documentation</a>
    </p>
</div>
""", unsafe_allow_html=True)
