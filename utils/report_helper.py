"""
Helper pour enregistrer les résultats de réconciliation dans la session
et afficher le bouton de téléchargement du rapport Excel.
"""
import streamlit as st
import pandas as pd
from typing import Dict, Any, Optional
from utils.excel_export import ExcelExporter


def save_and_offer_report(
    partner_name: str,
    metrics: Dict[str, Any],
    sheets: Dict[str, Optional[pd.DataFrame]],
    key_suffix: str = "default",
):
    """
    Enregistre les résultats dans st.session_state et affiche
    un bouton de téléchargement du rapport Excel.
    """
    # Nettoyer les dataframes vides / None
    clean_sheets = {
        name: df for name, df in sheets.items()
        if df is not None and isinstance(df, pd.DataFrame) and not df.empty
    }

    st.session_state["reco_results"] = {
        "partner_name": partner_name,
        "metrics": metrics,
        "sheets": clean_sheets,
    }

    st.markdown("---")
    st.subheader("📥 Générer le rapport final")
    ExcelExporter.download_button(
        partner_name=partner_name,
        metrics=metrics,
        sheets=clean_sheets,
        key=f"report_btn_{key_suffix}",
    )
