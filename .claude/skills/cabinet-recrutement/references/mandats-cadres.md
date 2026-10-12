# Mandats cadres — recrutement de consultants et de managers (executive search)

Deuxième activité du cabinet : M&C Capital (International) Ltd recrute aussi des cadres
(consultants, managers) pour des cabinets de conseil, en France notamment, sous contrat cadre
avec honoraires au succès. Le pipeline à 3 agents s'applique, avec les adaptations ci-dessous.

> Ce dépôt est public : ne jamais y écrire le nom d'un client, ses conditions commerciales,
> ni des données de candidats. Les dossiers de mission vivent hors du dépôt (scratchpad, Drive,
> artefact privé).

## Étape 0 — Mandat

Lire le contrat cadre et la fiche de mission. En extraire :
- les besoins (intitulé, séniorité, mission, démarrage, rémunération cible) ;
- les viviers cibles (cabinets d'origine prioritaires, puis secondaires) ;
- les règles qui conditionnent les honoraires : délai pour que le client déclare un candidat
  « déjà connu », définition de la Présentation et du Placement, garantie, confidentialité.
- Relever toute incohérence entre contrat et fiche (montants, taux, dates de facturation) et
  la signaler à l'utilisateur avant de démarrer.

## Agent 1 — Qualification du profil

Source : réseau LinkedIn de l'utilisateur (export `Connections.csv` → `scripts/linkedin_sourcing.py`),
recherches LinkedIn / Sales Navigator, CV reçus.

- Cabinet actuel et précédents, intitulé, ancienneté **en conseil** (pas l'ancienneté totale).
- Niveau : Consultant confirmé (≈3–5 ans) · Manager (≈5–9 ans) · Senior Manager (≈8–12 ans).
- Langue, localisation, mobilité, disponibilité / préavis (souvent 3 mois en France pour un cadre).
- Doublon : déjà présenté à ce client ? déjà approché dans les 12 derniers mois ?

## Agent 2 — Grille d'évaluation par besoin

Pour chaque besoin, 5 critères vérifiables, chacun noté 0 / 1 / 2 (total sur 10, ramené sur 100) :

| Critère | 2 | 1 | 0 |
|---|---|---|---|
| Pedigree conseil | Vivier primaire | Vivier secondaire / cabinet équivalent | Hors conseil |
| Séniorité | Dans la fourchette du besoin | ±1 an | Hors fourchette |
| Expertise du besoin | Mission identique déjà menée | Proche | Absente |
| Secteur client | Secteur actif du client | Secteur en développement | Autre |
| Posture / exposition | C-level, encadrement démontré | Client direct | Back-office |

Verdict `Match` si score ≥ 60 **et** séniorité ≠ 0. Routage identique au skill principal :
Match → approche ; No Match mais senior → escalade (piste business builder ou autre besoin) ;
sinon → écarté (pas de message, simple trace).

## Agent 3 — Approche et présentation

1. **Approche** (message LinkedIn ou e-mail) : court, personnalisé, client anonymisé
   au premier contact (« cabinet de conseil parisien en construction »). Ne révéler le nom
   qu'après marque d'intérêt.
2. **Qualification téléphonique** (20–30 min) : motivation, package actuel (fixe + variable),
   prétentions, préavis, autres process en cours.
3. **Accord du candidat** obligatoire avant toute transmission de son CV au client (RGPD :
   le candidat doit savoir à qui et pourquoi ses données sont transmises).
4. **Présentation** au client : fiche synthétique + CV, **datée** (elle déclenche le délai
   pendant lequel le client doit dire s'il connaît déjà le candidat). Conserver la preuve
   d'envoi.
5. Suivi : entretiens, offre, acceptation, date d'arrivée → déclenchement facture selon le
   contrat ; suivi de la période de garantie.

## Déontologie

- Ne jamais approcher un candidat chez le client lui-même ni chez un client du client sans accord.
- Ne pas filtrer sur l'âge, le sexe, l'origine, la situation familiale, le handicap.
- RGPD (candidats en France / UE) : n'utiliser que les données utiles, informer le candidat
  au premier contact de l'origine de ses données et de son droit d'opposition, supprimer
  sur demande.
- Ne jamais envoyer un message LinkedIn ou un e-mail au nom de l'utilisateur sans validation.

## Suivi (hors dépôt)

```
date,besoin,nom,cabinet,niveau,score,decision,etape,date_presentation,prochaine_action
```
`etape` ∈ `identifie · approche · interesse · qualifie · presente · entretien · offre · place · ecarte`.
