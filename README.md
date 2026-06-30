# Acerox - M3-B1 (entretien + identification des sources)

Ce depot contient la livraison M3-B1 pour Acerox: prise de besoin, cartographie des sources, schema de flux et exploration initiale des donnees.

## Lecture rapide (3 min)

- Contexte entretien: notes_entretien.md
- Note d'identification (livrable principal): identification_sources.md
- Schema des flux (Mermaid): flux_donnees.md
- Exploration des 3 sources: notebooks/M3-B1_template_franck.ipynb

## Contenu livre

- Source 1: data/capteurs_iot.csv (CSV capteurs IoT)
- Source 2: data/erp_export.json (export ERP)
- Source 3: data/logs_machines.log (logs machine bruts)
- Analyse d'exploration non destructive dans le notebook (lecture, info, head, describe)
- Recommandations de priorisation et points de vigilance RGPD dans la note

## Prerequis

- Python 3.11+
- pip

## Reproduction locale

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate

pip install -r requirements.txt
jupyter notebook notebooks/M3-B1_template_franck.ipynb
```

## Structure

```text
.
|- data/
|  |- capteurs_iot.csv
|  |- erp_export.json
|  |- logs_machines.log
|- notebooks/
|  |- M3-B1_template_franck.ipynb
|- ressources/
|- notes_entretien.md
|- identification_sources.md
|- flux_donnees.md
|- requirements.txt
```

## Perimetre M3-B1

- Objectif: identifier et qualifier les sources pour alimenter le modele existant Acerox.
- Hors perimetre: feature engineering, pipeline d'ingestion industrialise, entrainement modeles.

## Etat des principaux livrables

- Identification des sources: completee
- Schema de flux: complet
- Notebook d'exploration: complet

## Limites connues

- Le parsing structure des logs machines est reserve a l'etape suivante.
- Les validations RGPD detaillees (AIPD) sont a conduire avec le DPO.
