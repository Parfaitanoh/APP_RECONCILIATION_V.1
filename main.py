import streamlit as st

st.set_page_config(
    page_title="PayMeTrust Reconciliation V2.1",
    page_icon="assets/logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

from styles.custom import load_css, render_header, render_sidebar_logo
from partenaires import get_processor
from datetime import date, timedelta
import traceback

load_css()
render_sidebar_logo()
render_header()

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

st.sidebar.markdown("---")
st.sidebar.markdown("### 📅 Période de réconciliation")

_today = date.today()
_default_start = _today - timedelta(days=1)

col_d1, col_d2 = st.sidebar.columns(2)
with col_d1:
    reco_start = st.date_input(
        "Date début",
        value=_default_start,
        help="Début de la période (inclus) pour filtrer les SUCCESS PMT absents chez le partenaire.",
        key="reco_start_input",
    )
with col_d2:
    reco_end = st.date_input(
        "Date fin",
        value=_today,
        help="Fin de la période (inclus) pour filtrer les SUCCESS PMT absents chez le partenaire.",
        key="reco_end_input",
    )

if reco_start and reco_end and reco_start > reco_end:
    st.sidebar.error("⚠️ Date début > Date fin — corrigez la plage.")
    range_ok = False
else:
    range_ok = True
    st.sidebar.caption(
        f"Plage active : **{reco_start.strftime('%d/%m/%Y')}** → **{reco_end.strftime('%d/%m/%Y')}**"
    )

files_ready = bool(data_file and partenaire_file)
already = st.session_state.get("already_processed", False)

file_sig = (
    (data_file.name if data_file else None, data_file.size if data_file else 0),
    (partenaire_file.name if partenaire_file else None, partenaire_file.size if partenaire_file else 0),
    str(reco_start),
    str(reco_end),
)
if st.session_state.get("file_sig") != file_sig:
    st.session_state["file_sig"] = file_sig
    st.session_state["already_processed"] = False
    st.session_state.pop("excel_report_bytes", None)
    st.session_state.pop("excel_report_name", None)
    st.session_state.pop("reco_results", None)
    already = False

if not files_ready:
    st.info("👈 Veuillez charger les **deux fichiers** dans la barre latérale pour démarrer la réconciliation.")
    st.markdown("""
    ### Comment utiliser l'application
    1. Chargez le fichier **PMT** (export de votre système)
    2. Chargez le fichier **Partenaire** (export Wave, MTN, CinetPay, Bizao…)
    3. Sélectionnez la **période de réconciliation** (date début / date fin)
    4. Cliquez sur **Lancer la réconciliation**
    5. Consultez les onglets puis **Télécharger le rapport final**
    6. Exemple de nom de fichier partenaire : `waveci_payin`, `mtnci_payout`,`orangeci_payout` (le nom du partenaire et le type de transaction doivent être inclus dans le nom du fichier)

    """)
    st.stop()

if not range_ok:
    st.warning("Corrigez la période de réconciliation (date début ≤ date fin) avant de lancer.")
    st.stop()

st.sidebar.markdown("---")
if already:
    if st.sidebar.button("🔄 Relancer", type="primary", use_container_width=True, key="rerun_btn"):
        st.session_state["already_processed"] = False
        st.session_state.pop("excel_report_bytes", None)
        st.session_state.pop("excel_report_name", None)
        st.session_state.pop("reco_results", None)
        st.rerun()
    run_btn = False
else:
    run_btn = st.sidebar.button(
        "🚀 Lancer la réconciliation",
        type="primary",
        use_container_width=True,
        key="run_sidebar",
    )
    st.markdown(
        '<p style="color:#C5DCFF;font-weight:500;text-shadow:0 1px 3px rgba(0,0,0,0.45);">'
        '👈 Cliquez sur <strong style="color:#FFFFFF;">Lancer la réconciliation</strong> '
        'dans la barre latérale pour démarrer.</p>',
        unsafe_allow_html=True,
    )


def _run_processor():
    processor = get_processor(
        partenaire_file.name,
        data_file,
        partenaire_file,
        reco_start=reco_start,
        reco_end=reco_end,
    )
    processor.process()


if run_btn:
    st.session_state["already_processed"] = True
    st.session_state.pop("excel_report_bytes", None)
    st.session_state.pop("excel_report_name", None)
    with st.spinner(
        f"Traitement en cours… ({partenaire_file.name}) — "
        f"Période : {reco_start.strftime('%d/%m/%Y')} → {reco_end.strftime('%d/%m/%Y')}"
    ):
        try:
            _run_processor()
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

elif already:
    try:
        _run_processor()
    except Exception as e:
        st.error(f"❌ Erreur de traitement : {e}")
        with st.expander("Détails techniques"):
            st.code(traceback.format_exc())
        st.session_state["already_processed"] = False

st.markdown("---")
st.markdown("""
<div class="pmt-footer">
    <p>📊 <strong>APPLICATION Reconciliation V2.1</strong> · PayMeTrust</p>
    <p>🔄 Fichiers jusqu'à 2 GB · 📅 Plage date début / fin · 📥 Rapport sans rechargement</p>
    <p style="font-size: 0.8rem; margin-top: 8px;">
        Support : revenu.assurancepmt@paymetrust.net
    </p>
</div>
""", unsafe_allow_html=True)
