"""
Générateur de rapport Excel multi-onglets pour la réconciliation.
"""
import pandas as pd
import io
from datetime import datetime
from typing import Dict, Optional, Any


class ExcelExporter:
    """Crée un rapport Excel professionnel à partir des résultats de réconciliation."""

    @staticmethod
    def _prepare_df(df: pd.DataFrame) -> pd.DataFrame:
        """Remet l'index en colonnes (DateCourte, DATEOP, Statut, etc.)."""
        if not isinstance(df, pd.DataFrame):
            return pd.DataFrame(df)
        # Toujours reset_index si l'index n'est pas un RangeIndex purement numérique sans nom
        if not isinstance(df.index, pd.RangeIndex) or df.index.name is not None:
            export_df = df.reset_index()
        else:
            export_df = df.copy()
        # Supprimer colonnes d'index techniques inutiles
        if "index" in export_df.columns and export_df.columns.tolist().count("index") == 1:
            # garder si c'était un vrai index nommé "index"
            pass
        return export_df

    @staticmethod
    def create_report(
        partner_name: str,
        metrics: Dict[str, Any],
        sheets: Dict[str, pd.DataFrame],
    ) -> bytes:
        output = io.BytesIO()

        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            summary_rows = [
                ["Rapport de Réconciliation", partner_name],
                ["Date de génération", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                ["", ""],
            ]
            for k, v in metrics.items():
                summary_rows.append([k, v])

            pd.DataFrame(summary_rows, columns=["Métrique", "Valeur"]).to_excel(
                writer, sheet_name="Résumé", index=False
            )

            for sheet_name, df in sheets.items():
                if df is None or (isinstance(df, pd.DataFrame) and df.empty):
                    continue
                safe_name = str(sheet_name)[:31]
                try:
                    export_df = ExcelExporter._prepare_df(df)
                    export_df.to_excel(writer, sheet_name=safe_name, index=False)
                except Exception as e:
                    pd.DataFrame({"Erreur": [str(e)]}).to_excel(
                        writer, sheet_name=safe_name, index=False
                    )

        output.seek(0)
        return output.getvalue()

    @staticmethod
    def download_button(
        partner_name: str,
        metrics: Dict[str, Any],
        sheets: Dict[str, pd.DataFrame],
        label: str = "📥 Télécharger le rapport final Excel",
        key: str = "download_report",
    ):
        import streamlit as st

        try:
            data = ExcelExporter.create_report(partner_name, metrics, sheets)
            filename = f"Rapport_Reco_{partner_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
            st.download_button(
                label=label,
                data=data,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key=key,
                use_container_width=True,
            )
        except Exception as e:
            st.error(f"Impossible de générer le rapport : {e}")
