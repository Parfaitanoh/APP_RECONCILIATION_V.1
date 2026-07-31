"""
Générateur de rapport Excel multi-onglets pour la réconciliation.
"""
import pandas as pd
import io
import re
from datetime import datetime
from typing import Dict, Optional, Any


class ExcelExporter:
    """Crée un rapport Excel professionnel à partir des résultats de réconciliation."""

    @staticmethod
    def _prepare_df(df: pd.DataFrame) -> pd.DataFrame:
        if not isinstance(df, pd.DataFrame):
            return pd.DataFrame(df)
        if not isinstance(df.index, pd.RangeIndex) or df.index.name is not None:
            export_df = df.reset_index()
        else:
            export_df = df.copy()
        return export_df

    @staticmethod
    def _fmt_date(value) -> str:
        if value is None or value == "":
            return ""
        try:
            return pd.to_datetime(value).strftime("%Y%m%d")
        except Exception:
            s = str(value).replace("-", "").replace("/", "")[:8]
            return s if s.isdigit() else ""

    @staticmethod
    def _safe_partner(name: str) -> str:
        s = (name or "PARTENAIRE").strip().upper()
        s = re.sub(r"\s+", "_", s)
        s = re.sub(r"[^A-Z0-9_]", "", s)
        return s or "PARTENAIRE"

    @staticmethod
    def build_filename(partner_name: str, reco_start=None, reco_end=None) -> str:
        """
        Format : {date_du_jour}_{partenaire}_{date_debut}_{date_fin}.xlsx
        Exemple : 20260730_WAVE_CI_PAYIN_20260729_20260730.xlsx
        """
        today = datetime.now().strftime("%Y%m%d")
        partner = ExcelExporter._safe_partner(partner_name)
        d_start = ExcelExporter._fmt_date(reco_start)
        d_end = ExcelExporter._fmt_date(reco_end)

        parts = [today, partner]
        if d_start:
            parts.append(d_start)
        if d_end and d_end != d_start:
            parts.append(d_end)

        return "_".join(parts) + ".xlsx"

    @staticmethod
    def create_report(partner_name: str, metrics: Dict[str, Any], sheets: Dict[str, pd.DataFrame]) -> bytes:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            summary_rows = [
                ["Rapport de Réconciliation", partner_name],
                ["Date de génération", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                ["Version app", "V2.1"],
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
                    ExcelExporter._prepare_df(df).to_excel(writer, sheet_name=safe_name, index=False)
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
        label: str = None,
        key: str = "download_report",
        reco_start=None,
        reco_end=None,
    ):
        import streamlit as st

        try:
            filename = ExcelExporter.build_filename(
                partner_name, reco_start=reco_start, reco_end=reco_end
            )

            # Cache des bytes Excel : évite de régénérer à chaque clic / rerun
            cache_key = (
                partner_name,
                str(reco_start),
                str(reco_end),
                tuple(sorted(sheets.keys())),
                tuple((k, str(v)) for k, v in sorted(metrics.items())),
            )
            prev_key = st.session_state.get("excel_report_cache_key")
            if (
                prev_key == cache_key
                and st.session_state.get("excel_report_bytes")
                and st.session_state.get("excel_report_name") == filename
            ):
                data = st.session_state["excel_report_bytes"]
            else:
                data = ExcelExporter.create_report(partner_name, metrics, sheets)
                st.session_state["excel_report_bytes"] = data
                st.session_state["excel_report_name"] = filename
                st.session_state["excel_report_cache_key"] = cache_key

            st.info(f"**V2.1** — Fichier : `{filename}`")
            btn_label = label or f"📥 Télécharger {filename}"
            st.download_button(
                label=btn_label,
                data=data,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key=key,
                use_container_width=True,
            )
        except Exception as e:
            st.error(f"Impossible de générer le rapport : {e}")
