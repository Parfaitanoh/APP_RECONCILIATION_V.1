def metric_card(title, value, color, icon=None):
    if icon:
        title = f"{icon} {title}"
    return f"""
    <div style="
        border-radius: 10px;
        padding: 15px;
        background-color: white;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border-left: 5px solid {color};
        height: 120px;
        min-width: 200px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        overflow: hidden;
    ">
        <h3 style="
            color: #555;
            font-size: 16px;
            margin: 0 0 8px 0;
            font-weight: normal;
            white-space: nowrap;
        ">{title}</h3>
        <p style="
            color: #222;
            font-size: 15px;
            font-weight: bold;
            margin: 0;
            font-family: 'Courier New', monospace;
            word-break: break-all;
            line-height: 1.2;
        ">{value}</p>
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

    # Remettre l'index en colonnes (DATEOP, DateCourte, Statut…)
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
        # Pas de hauteur fixe → pas de barre de défilement / pagination artificielle
        st.dataframe(display_df, use_container_width=True, hide_index=True)
