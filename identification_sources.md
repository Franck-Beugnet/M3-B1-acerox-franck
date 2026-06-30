# Note d'identification des sources — Acerox Métallurgie

> Document remis à **Sébastien Marchand** (chef de projet industrialisation
> Acerox). **2-3 pages max.** Public : décideur métier non-technique —
> langage courant, pas de jargon scikit-learn ou SQL.
> Auteur : `<prénom>` — Date : `<date>`

## 1. Contexte

Acerox Métallurgie veut enrichir son modèle de prédiction de défauts qualité avec de nouvelles sources de données. 
Leur chef de projet, Sébastien Marchand, n'est pas data scientist.


## 2. Demande métier reformulée

### Demande exprimee par Sebastien (verbatim metier)

Sébastien demande de diminuer le taux de défaut et d'anticiper plus tôt les dérives en production.
Il insiste aussi sur la réduction des faux positifs qui déclenchent des contrôles inutiles.

### Besoin metier reformule (pour decision)

Acerox a besoin d'un dispositif d'alerte qualité plus en amont, qui combine signaux capteurs et contexte de production, afin de réduire les défauts réels sans dégrader la charge atelier par des alertes non pertinentes.

## 3. Inventaire des sources


| Source | Format | Volume | Fréquence | Qualité observée | Risques RGPD | Pertinence métier |
|---|---|---|---|---|---|---|
| `data/capteurs_iot.csv` | CSV tabulaire | 51 000 lignes, 7 colonnes, ~3,73 Mo | Quasi temps réel (mesures horodatées sur le mois) | 749 valeurs manquantes sur `vibration_mms` (~1,47%), valeurs extrêmes de `temperature_c` (max 160, 5 252 lignes >120), plateau suspect `vibration_mms=12.0` (5 194 lignes) | Faible à modéré : pas de donnée directement nominative, mais données industrielles potentiellement sensibles (site, ligne, capteur, horaires) | Très forte pour détection d'anomalies, monitoring process, corrélation défaut qualité / dérive machine |
| `data/erp_export.json` | JSON (liste d'objets) | 2 000 lignes, 9 colonnes, ~0,56 Mo | Export ponctuel (snapshot ERP reçu) | 109 valeurs manquantes sur `ouvrier_id` (~5,45%), pas de doublon sur `ordre_id`, cohérence temporelle OK (`date_fin_prevue >= date_lancement`) | Élevé : `ouvrier_id` = identifiant RH pseudonymisé (donnée personnelle), combiné à site/ligne/date peut permettre une ré-identification | Très forte pour pilotage production (ordres, statuts, quantités) et mise en contexte des signaux IoT |
| `data/logs_machines.log` | LOG texte brut | 30 000 lignes, 1 colonne (chargement brut), ~1,92 Mo | Événementiel continu (logs minute/seconde) | 1 ligne dupliquée détectée, format texte non structuré (parsing nécessaire pour exploitation avancée), mélange INFO/WARN/ERROR dans une seule colonne | Faible à modéré : pas d'identifiant personnel explicite dans l'échantillon, mais traces horodatées de comportements opérateur (`operator_login`, `reason=operator`) | Forte pour expliquer incidents (arrêts d'urgence, perte communication) et enrichir les alertes IoT |

## 4. Recommandations

> 3-5 puces. Quelles sources ingérer en priorité ? Lesquelles écarter et
> pourquoi ?

- Prioriser l'ingestion conjointe de `capteurs_iot.csv` + `erp_export.json` : c'est le meilleur couple pour relier signaux machine (température, vibration, débit) et contexte opérationnel (ordre, statut, quantité), donc directement utile pour prédire les défauts plus tôt.
- Intégrer `logs_machines.log` en second temps, après structuration minimale : la source est très utile pour expliquer les incidents, mais son format texte brut impose un parsing avant d'être exploitable dans un modèle.
- Ne pas écarter les valeurs extrêmes IoT à ce stade : les températures hautes et vibrations plafonnées peuvent être de vrais signaux de dérive ; en revanche, il faut tracer ces cas comme "à vérifier" avant entraînement.
- Mettre en place un contrôle qualité d'entrée simple dès l'ingestion : suivi des valeurs manquantes (`vibration_mms`, `ouvrier_id`), des doublons et des plages attendues, pour éviter d'alimenter le modèle avec des incohérences silencieuses.
- Encadrer l'usage des données ERP et logs côté RGPD : limiter l'accès aux identifiants opérateur (`ouvrier_id`), appliquer minimisation/pseudonymisation et valider les finalités avec le DPO avant industrialisation.

## 5. Points à clarifier avec Sébastien

> 3-5 questions ouvertes restantes — preuve de lucidité sur ce qu'on ne
> sait pas encore.

1. Quel est le KPI prioritaire pour le pilote : baisse du taux de défaut global, réduction des défauts critiques, ou diminution des faux positifs de contrôle ?
2. Quel délai de prédiction est attendu pour être utile en atelier (ex. alerte 10 min, 30 min, 2 h avant le défaut) ?
3. À quelle fréquence l'ERP peut-il être exporté (quotidien, horaire, quasi temps réel) pour rester cohérent avec les capteurs IoT ?
4. Les événements `operator_login` et `reason=operator` dans les logs peuvent-ils être exploités analytiquement, et avec quel niveau d'anonymisation accepté par Acerox ?
5. Existe-t-il une table de référence qui relie officiellement `sensor_id` / `line_id` / ordres ERP pour fiabiliser le rapprochement entre sources ?

## 6. Limites de cette note

> Ce qu'on n'a **pas** fait, et qu'il faudrait faire plus tard.

- Pas d'analyse statistique fouillée des sources (M3-B1 = identification,
  pas EDA complète)
- Pas d'AIPD juridique formelle (recommandation : escalader au DPO Acerox)
- ...

---

*Note produite par franck le 30/06/2026, dans le cadre du brief M3-B1 ATOS.*
