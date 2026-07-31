def metric_card(title, value, color="#3070F0", icon=None):
    if icon:
        title = f"{icon} {title}"
    return f"""
    <div class="pmt-metric-card" style="
        border-radius:14px;
        padding:16px 18px;
        background:#FFFFFF !important;
        box-shadow:0 4px 16px rgba(48,112,240,0.12);
        border:1px solid rgba(48,112,240,0.18);
        border-left:5px solid {color};
        height:120px;
        min-width:200px;
        display:flex;
        flex-direction:column;
        justify-content:center;
        overflow:hidden;
        color:#000000 !important;
    ">
        <div style="color:#000000 !important;-webkit-text-fill-color:#000000 !important;font-size:13px;font-weight:600;margin:0 0 8px 0;white-space:nowrap;">
            {title}
        </div>
        <div style="color:#000000 !important;-webkit-text-fill-color:#000000 !important;font-size:20px;font-weight:800;margin:0;font-family:Inter,monospace;line-height:1.25;word-break:break-all;">
            {value}
        </div>
    </div>
    """


def safe_show(df, max_rows=3000, label=None):
    """Affiche un DataFrame sans pagination forcée pour les petits tableaux (TCD)."""
    import streamlit as st
    import pandas as pd

    if df is None:
        st.info("Aucune donnée")
        return
    if not isinstance(df, pd.DataFrame):
        st.write(df)
        return

    display_df = df.copy()
    if not isinstance(display_df.index, pd.RangeIndex) or display_df.index.name is not None:
        display_df = display_df.reset_index()

    n = len(display_df)
    if label:
        st.caption(f"{label} — {n:,} lignes")
    else:
        st.caption(f"{n:,} lignes")

    if n == 0:
        st.info("Tableau vide")
        return

    if n > max_rows:
        st.warning(
            f"Aperçu des {max_rows:,} premières lignes sur {n:,} "
            "(export Excel pour le détail complet)."
        )
        st.dataframe(display_df.head(max_rows), use_container_width=True)
    else:
        st.dataframe(display_df, use_container_width=True, hide_index=True)


def filter_succes_abs_by_reco_date(df, reco_start=None, reco_end=None, date_col="Date"):
    """Filtre SUCCESS absents partenaire sur [reco_start, reco_end] inclus."""
    import pandas as pd
    if df is None or not isinstance(df, pd.DataFrame) or df.empty:
        return df, 0
    if reco_start is None and reco_end is None:
        return df, len(df)
    before = len(df)
    if date_col not in df.columns:
        return df, before

    series = pd.to_datetime(df[date_col], errors="coerce")
    mask = pd.Series(True, index=df.index)

    if reco_start is not None:
        try:
            start = pd.to_datetime(reco_start).normalize()
        except Exception:
            start = pd.to_datetime(str(reco_start)[:10], errors="coerce")
        if pd.notna(start):
            mask &= series.dt.normalize() >= start

    if reco_end is not None:
        try:
            end = pd.to_datetime(reco_end).normalize()
        except Exception:
            end = pd.to_datetime(str(reco_end)[:10], errors="coerce")
        if pd.notna(end):
            mask &= series.dt.normalize() <= end

    return df.loc[mask].copy(), before
