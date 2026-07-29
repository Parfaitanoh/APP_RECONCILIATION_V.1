# APP RECONCILIATION — Guide d'optimisation

## Changements réalisés

### 1. Limite d'upload relevée (plus de plafond 200 Mo)
Fichier créé : `.streamlit/config.toml`

```toml
[server]
maxUploadSize = 2048   # 2 Go
maxMessageSize = 2000
```

Redémarrez Streamlit après modification de ce fichier.

### 2. Bouton « Rapport final Excel »
À la fin de chaque réconciliation, un bouton **📥 Télécharger le rapport final Excel** apparaît.

Le fichier généré contient :
- **Résumé** : métriques (total, matchés, taux, montant)
- **PMT_complet** / **Partenaire**
- **TCD_PMT** / **TCD_Partenaire**
- **MAJ_FAILED_to_SUCCESS**, **MAJ_PENDING_to_SUCCESS**
- Transactions absentes de chaque côté
- Agrégats par marchand / pays
- Refound & Recouvrement (si présents)

Les onglets très volumineux sont limités à 100 000 lignes pour rester compatibles avec Excel.

### 3. Améliorations UX (`main.py`)
- Affichage de la taille des fichiers chargés
- Bouton explicite « Lancer la réconciliation »
- Spinner de progression
- Gestion d'erreurs avec traceback détaillé
- Instructions d'utilisation quand aucun fichier n'est chargé

## Lancement

```bash
cd PROJECT_APP_RECO
pip install -r requirements.txt
streamlit run main.py
```

## Partenaires supportés
Wave CI/SN/BF (payin & payout), CinetPay, Bizao, MTN CI/CM, Orange Money BF/CI, Moov CI, iFutur.

Le nom du fichier partenaire doit contenir le code partenaire + `payin` ou `payout`
(ex. `waveci_payin_juin.csv`).
