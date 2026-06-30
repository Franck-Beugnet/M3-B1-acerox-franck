# Schéma des flux de données — Acerox Métallurgie

> Schéma Mermaid à compléter. Doit montrer :
> - **Sources** (capteurs IoT, ERP, logs, *bonus PDF*)
> - **Ingestion** (à concevoir en M3-B2)
> - **BDD pivot** (à modéliser en M3-B2)
> - **Modèle existant** Acerox (placeholder, hors-sujet ici)
>
> Légende explicite : qui produit, qui consomme, contraintes.

## Schéma

```mermaid
flowchart LR
    SRC1[📡 capteurs_iot.csv<br/>CSV, 51k lignes, ~3.73 Mo<br/>quasi temps réel]
    SRC2[📋 erp_export.json<br/>JSON, 2k lignes, ~0.56 Mo<br/>export batch]
    SRC3[📝 logs_machines.log<br/>LOG texte, 30k lignes, ~1.92 Mo<br/>événementiel continu]
    SRC4[📄 bonus PDF maintenance<br/>non fourni sur ce lot]

    INGEST[🔄 Ingestion<br/>à concevoir en M3-B2]
    BDD[(🗄️ BDD pivot<br/>SQLite)]
    MODEL[🧠 Modèle existant Acerox<br/>prédiction défauts qualité]

    SRC1 -->|mesures horodatées machine| INGEST
    SRC2 -->|ordres, statuts, quantités| INGEST
    SRC3 -.->|événements INFO/WARN/ERROR à parser| INGEST
    SRC4 -.->|hors périmètre M3-B1| INGEST
    INGEST -->|normalisation + dédup| BDD
    BDD -->|consommée par| MODEL

    classDef source fill:#e1f5ff,stroke:#0277bd
    classDef bonus fill:#f3f3f3,stroke:#6b6b6b,stroke-dasharray: 3 3
    classDef tofix fill:#fff4e1,stroke:#c97a00,stroke-dasharray: 5 5
    class SRC1,SRC2,SRC3 source
    class SRC4 bonus
    class INGEST tofix
```

## Légende

> Reformule en 5 lignes max ce que le schéma raconte (qui produit quelle
> donnée, qui consomme, contraintes critiques).

- **Producteurs** : ateliers Acerox via capteurs IoT, système ERP et journaux machines.
- **Consommateur final** : le modèle existant de prédiction des défauts qualité, alimenté via la BDD pivot.
- **Chaîne de valeur** : les données brutes convergent vers une ingestion unique puis vers SQLite pour croiser signaux process et contexte ERP.
- **Contraintes critiques** : rythme hétérogène (quasi temps réel vs batch), qualité variable (valeurs manquantes et logs non structurés).
- **Point RGPD** : `ouvrier_id` et certaines traces opérateur doivent être minimisés/pseudonymisés avant exploitation large.

## Décisions associées

- Source(s) retenues en priorité : `capteurs_iot.csv` et `erp_export.json` pour un premier socle prédictif robuste.
- Source(s) écartées : aucune écartée définitivement ; `logs_machines.log` est différée en phase 2 (nécessite parsing/structuration).
- Source bonus (PDF) traitée ? non, aucun PDF exploitable n'a été fourni dans ce lot de données.

---

*Schéma produit par <prénom>, <date>, dans le cadre du brief M3-B1 ATOS.*
