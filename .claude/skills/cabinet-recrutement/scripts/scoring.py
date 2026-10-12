#!/usr/bin/env python3
"""
Scoring déterministe du pipeline de recrutement M&C Capital (agents 2 + routage).

Usage :
    python3 scoring.py lot.json

Format de lot.json :
{
  "poste": {
    "poste_id": "BTP-MAC",
    "competences_requises": ["maçonnerie", "coffrage", "lecture de plan", "dosage béton"],
    "atouts": ["ferraillage"],
    "annees_min": 3
  },
  "candidats": [
    {"nom": "Rakoto Jean", "competences": ["maçonnerie", "coffrage", "ferraillage"],
     "annees_experience": 5, "bloquants": []}
  ]
}

Les compétences doivent déjà être normalisées (synonymes résolus) par l'agent 1.
"""
import json
import sys

SEUIL_MATCH = 60


def niveau(annees: int) -> str:
    if annees <= 2:
        return "Débutant"
    if annees <= 6:
        return "Confirmé"
    return "Senior"


def evaluer(poste: dict, candidat: dict) -> dict:
    norm = lambda xs: {x.strip().lower() for x in xs}
    requises = norm(poste.get("competences_requises", []))
    atouts = norm(poste.get("atouts", []))
    competences = norm(candidat.get("competences", []))
    annees = int(candidat.get("annees_experience", 0))

    couvertes = sorted(requises & competences)
    manquantes = sorted(requises - competences)
    score = len(couvertes) * 100 // len(requises) if requises else 0
    verdict = "Match" if score >= SEUIL_MATCH and annees >= poste.get("annees_min", 0) else "No Match"
    niv = niveau(annees)

    if candidat.get("bloquants"):
        decision = "escalade"
    elif verdict == "Match":
        decision = "convocation"
    elif niv == "Senior":
        decision = "escalade"
    else:
        decision = "refus"

    return {
        "nom": candidat.get("nom", "Inconnu"),
        "niveau": niv,
        "annees_experience": annees,
        "score": score,
        "verdict": verdict,
        "decision": decision,
        "competences_couvertes": couvertes,
        "competences_manquantes": manquantes,
        "atouts_couverts": sorted(atouts & competences),
        "bloquants": candidat.get("bloquants", []),
    }


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as f:
        lot = json.load(f)
    ordre = {"convocation": 0, "escalade": 1, "refus": 2}
    resultats = sorted(
        (evaluer(lot["poste"], c) for c in lot["candidats"]),
        key=lambda r: (ordre[r["decision"]], -r["score"]),
    )
    print(json.dumps({"poste_id": lot["poste"].get("poste_id"), "resultats": resultats},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
