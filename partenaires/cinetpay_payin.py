import pandas as pd
import streamlit as st
import csv
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
from itertools import combinations
from collections import Counter
import zipfile
import io
import os
from streamlit_extras.stylable_container import stylable_container
import plotly.figure_factory as ff
from utils.helpers import metric_card, safe_show, filter_succes_abs_by_reco_date


class CinetpayPayinProcessor:
    def __init__(self, data_file, partner_file, reco_start=None, reco_end=None):
        self.data_file = data_file
        self.partner_file = partner_file
        self.reco_start = reco_start
        self.reco_end = reco_end
        self._partner_label = "CINETPAY PAYIN" # Augmenter la limite avant tout traitement
   
    
    def load_file(self, file):
        # Votre fonction de chargement existante
        try:
            if file.name.endswith(".csv"):
                raw_data = file.read().decode("utf-8", errors="ignore")
                dialect = csv.Sniffer().sniff(raw_data.split("\n")[0])
                delimiter = dialect.delimiter
                file.seek(0)
                return pd.read_csv(file, delimiter=delimiter, encoding="utf-8", low_memory=False)
            elif file.name.endswith((".xlsx", ".xls")):
                return pd.read_excel(file)
            else:
                st.error("Format non supporté.")
                return None
        except Exception as e:
            st.error(f"Erreur lors du chargement : {e}")
            return None
    
    def process(self):
        # Charger les données
        pmt = self.load_file(self.data_file)
        dfop = self.load_file(self.partner_file)
        
        # Votre code de traitement existant pour Cinetpay
        def extractday(dated):
            parts=dated.split(' ')
            return parts[0]
        pmt['Date']= pmt['created_at'].apply(extractday)

        pmt["amount"] = pd.to_numeric(pmt["amount"], errors="coerce")
        pmt = pmt.drop_duplicates(subset='transaction_id', keep='first')
        dfpmt = pmt.rename(columns={
                'created_at': 'Created Date',
                'payment_date': 'Payment Date',
                'operator': 'Operator',
                'merchant_name': 'Merchant Name',
                'transaction_id': 'Transaction ID',
                'id_operator': 'ID Opérateur',
                'phone_number': 'Phone Number',
                'amount': 'Montant',
                'country':'Pays',
                'fee_amount': 'Fee amount',
                'merchant_amount': 'Merchant amount',
                'statut': 'Statut'
            })
        
        dfpmt['Phone Number'] = dfpmt['Phone Number'].astype(object)
        dfop['Date'] = dfop['Date Creation'].apply(lambda x: x.split(' ')[0])
        refused = dfop.loc[(dfop['Statut'] == 'REFUSED')]
        dfcinetpay= dfop.loc[(dfop['Statut'] == 'ACCEPTED')]
        
        # --- Nettoyage & transformation CHEZ LE PARTENAIRE-------------------------------
        
         # Calcul des KPI------------------------------------
        
         # Calcul des KPI-----------------------------------------
        
        #MISE EN PLACE DE RECHERCHE X POUR RECUPERATION CHEZ LE PARTENAIRE
        
        correspondance_statut_op= dfop.set_index('ID transaction')['Statut']
        correspondance_statut_refused= refused.set_index('ID transaction')['Statut']
        correspondance_date_op = dfop.set_index('ID transaction')['Date']
        correspondance_id_op = dfop.set_index('ID transaction')['ID Operator']
        correspondance_statut_pmt = dfpmt.set_index('Transaction ID')['Statut']
        correspondance_commentaire = refused.set_index('ID transaction')['Commentaire']
        correspondance_operator = dfop.set_index('ID transaction')['Opérateur']
        
        dfpmt['DATE_OP'] = dfpmt['Transaction ID'].map(correspondance_date_op)
        refused['STATUT_PMT'] = refused['ID transaction'].map(correspondance_statut_pmt)
        dfpmt['STATUT_OP'] = dfpmt['Transaction ID'].map(correspondance_statut_op)
        dfpmt['REFUSED'] = dfpmt['Transaction ID'].map(correspondance_statut_refused)
        dfpmt['ID_OP'] = dfpmt['Transaction ID'].map(correspondance_id_op)
        dfpmt['Comment'] = dfpmt['Transaction ID'].map(correspondance_commentaire)
        dfpmt['OPERATOROP'] = dfpmt['Transaction ID'].map(correspondance_operator)
        
        
        # Définir les taux de commission pour chaque opérateur
        commission_rates = {
            'TMONEYTG': 0.03,
            'MOOVML': 0.025,
            'FLOOZTG': 0.025,
            'MOOVBF': 0.03,
            'FLOOZ' : 0.003,
            'OMCM': 0.025,
            'MTNGN':0.025,
            'MTNCM':0.025,
            'AIRTELCD':0.035,
            'OMGN' :0.035,
            'MPESACD' :0.038,
            'OMML':0.03,
            'MTNBJ':0.027,
            'WAVECI':0.03,
            'OM':0.03,
            'MOMO':0.03
        }
        
        # Fonction pour calculer les frais d'opérateur
        def calculate_frais_op(row):
            operator = row['OPERATOROP']
            montant = row['Montant']
            commission_rate = commission_rates.get(operator, 0)
            return montant * commission_rate
        
        # Ajouter une colonne 'frais_op' avec les frais d'opérateur calculés
        dfpmt['frais_op'] = dfpmt.apply(calculate_frais_op, axis=1)
        dfpmt['Frais_pmt'] = dfpmt['Fee amount'] - dfpmt['frais_op']
        dfpmt['Tauxop']=dfpmt['frais_op'] / dfpmt['Montant']
        dfop['Taux(%)'] = dfop['Commission'] / dfop['Montant Payé']
        dfpmt['Taux_merchant']=dfpmt['Fee amount'] / dfpmt['Montant']
        dfpmt['Nombre']= dfpmt['Montant']
        dfcinetpay['Nombre']=dfcinetpay['Montant Payé']

        select_taux_operator = dfop.groupby('Opérateur')['Taux(%)'].apply(list)
        select_taux_operator.reset_index()
        
        #NBSI PMT &CINETPAY
        dfpmt['CINETPAY'] = dfpmt['Transaction ID'].isin(dfcinetpay['ID transaction']).astype(int)
        dfcinetpay['PMT'] = dfcinetpay['ID transaction'].isin(dfpmt['Transaction ID']).astype(int)
        dfpmt['REFUSED'] = dfpmt['Transaction ID'].isin(refused['ID transaction']).astype(int)
        
        df_filtered = dfcinetpay[(dfcinetpay['PMT'] == 1) | (dfcinetpay['PMT'] == 0)]

        

        # --- Création des onglets ---

        tabs = st.tabs(["📊 Vue Globale", "👥 Rapport Reconciliation", "🔄 Rapport", "📈 Analytics Avancés"])
    
            # ==================================
               # Onglet 1 : Vue Globale
           # ==================================
        with tabs[0]:
            st.subheader("Vue Globale")
            #Nouveau: Sélecteur de période
            montant_total = dfpmt["Montant"].sum()
            nombre_transaction = dfpmt['Transaction ID'].count()
            taux_succes = (dfpmt[dfpmt['Statut'] == 'SUCCESS'].shape[0] / nombre_transaction) * 100
            trx_succes = (dfpmt[dfpmt['Statut'] == 'SUCCESS'])
            select=trx_succes['Transaction ID'].count()

            # Affichage dans des metric cards améliorées
            col1, col2, col3, col4 = st.columns(4)
            col1.markdown(metric_card("Transactions", nombre_transaction, "#3070F0", "🔄"), unsafe_allow_html=True)
            col2.markdown(metric_card("Transactions Succès", select, "#3070F0", "🔄"), unsafe_allow_html=True)
            col3.markdown(metric_card("Montant Total", f"{montant_total:,.2f}", "#3070F0", "💰"), unsafe_allow_html=True)
            col4.markdown(metric_card("Taux de Succès", f"{taux_succes:.1f}%", "#3070F0", "✅"), unsafe_allow_html=True)
            
            
            # Nouveau: Graphique combiné montant/nombre de transactions
            st.subheader("Évolution Journalière")
            daily_data = dfpmt.groupby('Date').agg(
                Montant=('Montant', 'sum'),
                Transactions=('Transaction ID', 'count')
            ).reset_index()
            
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            fig.add_trace(
                px.line(daily_data, x='Date', y='Montant').data[0],
                secondary_y=False,
            )
            fig.add_trace(
                px.bar(daily_data, x='Date', y='Transactions').data[0],
                secondary_y=True,
            )
            fig.update_layout(
                title="Volume et Nombre de Transactions",
                yaxis_title="Montant (XOF)",
                yaxis2_title="Nombre de Transactions",
                template="plotly_white"
            )
            st.plotly_chart(fig, use_container_width=True)
            
        # ================================
    # Onglet 2  : Opérations
# ================================

        with tabs[1]:
            st.subheader("Rapport Reconciliation CINETPAY PAYIN")
            df_filteredpmt = dfpmt[dfpmt['CINETPAY'] == 1]
            maj=df_filteredpmt[(df_filteredpmt['Statut']=='FAILED') | (df_filteredpmt['Statut']=='PENDING')]
            
            # Nouveau: Métriques de réconciliation
            matched = df_filteredpmt['CINETPAY'].sum()
            nbre_maj=maj['Transaction ID'].count()
            unmatched = len(dfpmt) - matched
            reconciliation_rate = (matched / len(dfpmt)) * 100
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Transactions Matchées", matched, delta=f"{reconciliation_rate:.1f}%")
            col2.metric("Total Transactions", len(dfpmt))
            col3.metric("Nombre transaction MAJ", nbre_maj)
            col4.metric("Transactions Non Matchées", unmatched)
            # Création du tableau croisé dynamique
            tcdcinetpay = pd.pivot_table(
                df_filtered,
                values=['Montant Payé', 'Nombre'],
                index=['Date', 'Opérateur','Statut'],
                aggfunc={'Nombre': 'count','Montant Payé': 'sum' },
                fill_value=0,
                margins=True,
                margins_name='Total'
            )
            
            df_filteredpmt = dfpmt[dfpmt['CINETPAY'] == 1]
            
            # Création du tableau croisé dynamique
            tcdpmt = pd.pivot_table(
                df_filteredpmt,
                values=['Montant', 'Nombre','frais_op', 'Frais_pmt'],
                index=['DATE_OP','OPERATOROP','Statut'],
                aggfunc={'Nombre': 'count','Montant': 'sum' ,'frais_op': 'sum', 'Frais_pmt': 'sum' },
                fill_value=0,
                margins=True,
                margins_name='Total'
            )

            tab1, tab2, tab3, tab4,tab5 = st.tabs(["Données PMT", "Données Partenaire", "TCD PMT", "TCD Partenaire","Rapport Taux Appliqué"])
            
            with tab1:
                safe_show(dfpmt)
                
            with tab2:
                st.write(dfop)
                
            with tab3:
                st.write(tcdpmt.style.format("{:,.2f}"))
                
            with tab4:
                st.write(tcdcinetpay)
                
            with tab5:
                st.write(select_taux_operator)
            
            # LES TRANSACTIONS A METTRE A JOUR
            
            maj_failed_a_succes = dfpmt.loc[(dfpmt['Statut'] == 'FAILED') & (dfpmt['CINETPAY'] == 1)]
            maj_pending_a_succes = dfpmt.loc[(dfpmt['Statut'] == 'PENDING') & (dfpmt['CINETPAY'] == 1)]
            majf=maj_failed_a_succes[['Transaction ID','Phone Number','Statut','STATUT_OP','ID_OP']]
            majp=maj_pending_a_succes[['Transaction ID','Phone Number','Statut','STATUT_OP','ID_OP']]
            trx_succes_abs = dfpmt.loc[(dfpmt['Statut'] == 'SUCCESS') & (dfpmt['CINETPAY'] == 0)]
            trx_succes_abs, _n_before_date = filter_succes_abs_by_reco_date(
                trx_succes_abs,
                reco_start=getattr(self, 'reco_start', None),
                reco_end=getattr(self, 'reco_end', None),
                date_col='Date',
            )
            trx_en_attente_abs= dfpmt.loc[(dfpmt['Statut']=='PENDING') & (dfpmt['CINETPAY'] == 0)]
            trx_succes_cinetpay_abs_pmt = dfcinetpay.loc[(dfcinetpay['Statut']=='ACCEPTED') & (dfcinetpay['PMT'] == 0)]
            select_marchand=df_filteredpmt.groupby(['Pays','Merchant Name','Operator']).agg(
                Nombre=('Montant', 'count'),
                Volume_transaction=('Montant','sum')
            )
            
            select_country_marchand_statut = df_filteredpmt.groupby(['Pays']).agg(
                Nombre=('Montant', 'count'),
                Volume=('Montant', 'sum')
            )
            st.subheader("🔴 Transactions failed à mettre à jour en SUCCESS")
            st.write(majf)
            
            st.subheader("🟡 Transactions PENDING à mettre à jour en SUCCESS")
            st.write(majp)
            
            st.subheader("🔵 Transactions en attente PMT absentes chez partenaire")
            safe_show(trx_en_attente_abs)
            
            st.subheader("🟢 Transactions SUCCES absentes chez PMT")
            safe_show(trx_succes_cinetpay_abs_pmt)
            
            st.subheader("🟠 Transactions SUCCES absentes partenaire (filtrées date reco)")
            if getattr(self, 'reco_start', None) is not None or getattr(self, 'reco_end', None) is not None:
                _ds = self.reco_start.strftime('%d/%m/%Y') if getattr(self, 'reco_start', None) and hasattr(self.reco_start, 'strftime') else (self.reco_start or '…')
                _de = self.reco_end.strftime('%d/%m/%Y') if getattr(self, 'reco_end', None) and hasattr(self.reco_end, 'strftime') else (self.reco_end or '…')
                st.caption(
                    f"Filtrées sur la période de réconciliation : {_ds} → {_de}"
                    f" — {len(trx_succes_abs):,} ligne(s)"
                )
            safe_show(trx_succes_abs)

            st.subheader("TRANSACTION PAR OPERATEUR ET MARCHAND")
            safe_show(select_marchand)
            
            st.subheader("TRANSACTION PAR OPERATEUR ET PAYS")
            safe_show(select_country_marchand_statut)
        
        with tabs[2]:
            c_title1, c_title2 = st.columns(2)
            with c_title1:
                st.subheader("Vue globale par Statut")
            with c_title2:
                st.subheader("Vue globale par Pays")
            chart1, chart2 = st.columns(2)
            with chart1:
                fig = px.pie(dfpmt, values="Montant", names="Statut", template="plotly_white",
                             color_discrete_sequence=["#3070F0", "#5B9DFF", "#94B8F5", "#1A4FC4"])
                fig.update_layout(height=320, margin=dict(l=10, r=10, t=20, b=10),
                                  paper_bgcolor="white", font=dict(color="#000000", size=12),
                                  showlegend=True, legend=dict(orientation="v", yanchor="middle", y=0.5))
                fig.update_traces(textposition="inside", textfont_color="#000000")
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            with chart2:
                monthly_statut = dfpmt.groupby("Pays")["Montant"].sum().reset_index()
                fig_month = px.bar(monthly_statut, x="Pays", y="Montant", text_auto=True,
                                   color="Montant",
                                   color_continuous_scale=["#5B9DFF", "#3070F0"],
                                   template="plotly_white")
                fig_month.update_layout(height=320, margin=dict(l=10, r=10, t=20, b=10),
                                        paper_bgcolor="white", plot_bgcolor="white",
                                        font=dict(color="#000000", size=12),
                                        coloraxis_showscale=False)
                st.plotly_chart(fig_month, use_container_width=True, config={"displayModeBar": False})


        with tabs[3]:
            st.subheader("Analytics Avancés")
            

            # Analyse temporelle avancée
            st.subheader("Analyse Temporelle")
            dfpmt['Date'] = pd.to_datetime(dfpmt['Date'])
            dfpmt['Jour'] = dfpmt['Date'].dt.day_name(locale='fr')
            dfpmt['Heure'] = pd.to_datetime(dfpmt['Created Date']).dt.hour
            
            col1, col2 = st.columns(2)
            with col1:
                day_order = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
                by_day = dfpmt.groupby('Jour').agg({'Montant': 'sum', 'Transaction ID': 'count'}).reindex(day_order)
                fig = px.line(by_day, x=by_day.index, y='Montant', 
                             title="Volume par Jour de la Semaine",
                             labels={'x': 'Jour', 'y': 'Montant'})
                st.plotly_chart(fig, use_container_width=True)
                
            with col2:
                by_hour = dfpmt.groupby('Heure').agg({'Montant': 'sum', 'Transaction ID': 'count'})
                fig = px.area(by_hour, x=by_hour.index, y='Montant', 
                             title="Volume par Heure de la Journée",
                             labels={'x': 'Heure', 'y': 'Montant'})
                st.plotly_chart(fig, use_container_width=True)
            
# 



        

        # ========== RAPPORT FINAL EXCEL ==========
        try:
            from utils.report_helper import save_and_offer_report
            _loc = locals()

            def _safe_df(name):
                obj = _loc.get(name)
                if isinstance(obj, pd.DataFrame) and not obj.empty:
                    return obj
                return None

            _dfpmt = _safe_df("dfpmt")
            _filtered = _safe_df("df_filteredpmt")
            _total = int(_dfpmt.shape[0]) if _dfpmt is not None else 0
            _matched = int(_filtered.shape[0]) if _filtered is not None else 0
            _rate = round((_matched / _total * 100), 1) if _total else 0
            _montant = float(_dfpmt["Montant"].sum()) if _dfpmt is not None and "Montant" in _dfpmt.columns else 0.0

            _metrics = {
                "Total transactions PMT": _total,
                "Transactions matchées": _matched,
                "Taux de réconciliation (%)": _rate,
                "Date début": str(getattr(self, "reco_start", "") or ""),
                "Date fin": str(getattr(self, "reco_end", "") or ""),
                "Montant total": f"{_montant:,.2f}",
            }

            _sheets = {}
            for _name, _var in [
                ("TCD_PMT", "tcdpmt"),
                ("TCD_Partenaire", "tcdwave"),
                ("TCD_Partenaire", "tcdpartner"),
                ("TCD_Partenaire", "tcdcinetpay"),
                ("TCD_Partenaire", "tcdmoovci"),
                ("TCD_Partenaire", "tcdmtnci"),
                ("TCD_Partenaire", "tcdmtncm"),
                ("TCD_Partenaire", "tcdombf"),
                ("TCD_Partenaire", "tcdomci"),
                ("TCD_Partenaire", "tcdop"),
                ("MAJ_FAILED_to_SUCCESS", "maj_failed_a_succes"),
                ("MAJ_PENDING_to_SUCCESS", "maj_pending_a_succes"),
                ("SUCCESS_absents_partenaire", "trx_succes_abs"),
                ("PENDING_absents_partenaire", "trx_en_attente_abs"),
                ("SUCCESS_partenaire_absents_PMT", "trx_succes_cinetpay_abs_pmt"),
                ("Par_Marchand", "select_marchand"),
                ("Par_Pays", "select_country_marchand_statut"),
                ("Refound", "refound"),
                ("Recouvrement", "recouvrement"),
            ]:
                df = _safe_df(_var)
                if df is not None and _name not in _sheets:
                    # Limiter les très gros onglets pour Excel (max 100k lignes)
                    _sheets[_name] = df.head(100000)

            save_and_offer_report(
                partner_name=getattr(self, "_partner_label", "RECONCILIATION"),
                metrics=_metrics,
                sheets=_sheets,
                key_suffix=getattr(self, "_partner_label", "default").replace(" ", "_"),
                reco_start=getattr(self, "reco_start", None),
                reco_end=getattr(self, "reco_end", None),
            )
        except Exception as _e:
            st.warning(f"Rapport Excel non généré : {_e}")


        #Processed Cinetpay payin fin-