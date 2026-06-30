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
    subgraph S1[Perimetre M3-B1 - sources qualifiees]
        SRC1[capteurs_iot.csv<br/>CSV, 51k lignes, ~3.73 Mo<br/>cadence: quasi temps reel]
        SRC2[erp_export.json<br/>JSON, 2k lignes, ~0.56 Mo<br/>cadence: export batch]
        SRC3[logs_machines.log<br/>LOG texte, 30k lignes, ~1.92 Mo<br/>cadence: evenementiel continu]
        SRC4[bonus PDF maintenance<br/>non fourni sur ce lot]
    end

    subgraph S2[Cible M3-B2 - chaine de traitement]
        INGEST[Ingestion multi-sources]
        QGATE{Controle qualite entree<br/>manquants, doublons, plages}
        PGATE{Filtre RGPD<br/>minimisation + pseudonymisation}
        BDD[(BDD pivot SQLite)]
    end

    MODEL[Modele existant Acerox<br/>prediction defauts qualite]

    SRC1 -->|mesures horodatees machine| INGEST
    SRC2 -->|ordres, statuts, quantites, ouvrier_id| INGEST
    SRC3 -.->|phase 2: parsing des evenements requis| INGEST
    SRC4 -.->|hors perimetre M3-B1| INGEST

    INGEST --> QGATE --> PGATE --> BDD -->|features consolidees| MODEL

    classDef source fill:#e1f5ff,stroke:#0277bd,stroke-width:1px,color:#111111
    classDef bonus fill:#f3f3f3,stroke:#6b6b6b,stroke-dasharray: 3 3,color:#111111
    classDef target fill:#fff4e1,stroke:#c97a00,stroke-width:1px,color:#111111
    classDef control fill:#ffe8e8,stroke:#b04040,stroke-width:1px,color:#111111
    classDef sink fill:#eaf7ea,stroke:#2e7d32,stroke-width:1px,color:#111111

    style S1 fill:#f8fbff,stroke:#0277bd,stroke-width:1px,color:#111111
    style S2 fill:#fffaf0,stroke:#c97a00,stroke-width:1px,color:#111111

    class SRC1,SRC2,SRC3 source
    class SRC4 bonus
    class INGEST,BDD target
    class QGATE,PGATE control
    class MODEL sink
```

## Légende

> Reformule en 5 lignes max ce que le schéma raconte (qui produit quelle
> donnée, qui consomme, contraintes critiques).

- **Producteurs** : atelier Acerox via capteurs IoT, ERP et logs machines.
- **Traitement cible** : une ingestion unique alimente un controle qualite, puis un filtre RGPD, avant stockage en BDD pivot.
- **Consommateur final** : le modele existant Acerox de prediction des defauts qualite.
- **Contraintes critiques** : cadences heterogenes (quasi temps reel, batch, evenementiel) et logs non structures.
- **Point RGPD operationnel** : `ouvrier_id` et traces operateur doivent etre pseudonymises avant mise a disposition analytique large.

## Décisions associées

- Source(s) retenues en priorité : `capteurs_iot.csv` et `erp_export.json` pour un premier socle prédictif robuste.
- Source(s) écartées : aucune écartée définitivement ; `logs_machines.log` est différée en phase 2 (nécessite parsing/structuration).
- Source bonus (PDF) traitée ? non, aucun PDF exploitable n'a été fourni dans ce lot de données.

---

*Schéma produit par <prénom>, <date>, dans le cadre du brief M3-B1 ATOS.*
