#!/usr/bin/env python3
"""
Pré-qualification d'un réseau LinkedIn pour un mandat de recrutement cadre.

Entrée : le fichier Connections.csv de l'export officiel LinkedIn
(Préférences > Confidentialité des données > Obtenir une copie de vos données > Relations).
Colonnes attendues : First Name, Last Name, URL, Email Address, Company, Position, Connected On.

Usage :
    python3 linkedin_sourcing.py Connections.csv mandat.json [sortie.csv]

Format de mandat.json :
{
  "viviers_primaires":   {"PwC": ["pwc", "pricewaterhousecoopers"], ...},
  "viviers_secondaires": {"Deloitte": ["deloitte"], ...},
  "besoins": {
    "B1": {"intitule": "Chef de projet digitalisation", "mots_cles": ["digital", "cio"]},
    ...
  }
}

L'export ne donne ni l'ancienneté ni la langue : la séniorité est estimée à partir de
l'intitulé de poste (fourchette indicative 3–10 ans) et doit être vérifiée sur le profil.
"""
import csv
import io
import json
import re
import sys
import unicodedata

# Intitulé -> (séniorité estimée, dans la cible 3–10 ans ?)
# L'ordre compte : le premier motif trouvé l'emporte.
SENIORITE = [
    (r"\b(stagiaire|intern|internship|alternan|apprenti|working student)", "Stage / alternance", "hors"),
    (r"\b(junior|analyst|analyste)\b", "Junior (0–2 ans)", "hors"),
    (r"\b(partner|associe|associate partner|managing director|vice president|vp)\b", "Partner / Directeur (>10 ans)", "bonus"),
    (r"\b(director|directeur|directrice|head of)\b", "Directeur (≈10+ ans)", "bonus"),
    (r"\bsenior manager\b", "Senior Manager (≈8–12 ans)", "cible"),
    (r"\bmanager\b", "Manager (≈5–9 ans)", "cible"),
    (r"\b(senior consultant|consultant senior|consultant confirme|senior associate|experienced consultant|senior)\b",
     "Consultant senior (≈3–5 ans)", "cible"),
    (r"\b(chef de projet|project manager|lead|architecte?|architect)\b", "Chef de projet / Lead (≈4–8 ans)", "cible"),
    (r"\bconsultant(e)?\b", "Consultant (≈1–4 ans)", "limite"),
]

POINTS_SENIORITE = {"cible": 3, "limite": 1, "bonus": 1, "hors": -10}


def normaliser(texte: str) -> str:
    texte = unicodedata.normalize("NFKD", texte or "").encode("ascii", "ignore").decode()
    return texte.lower()


def lire_connexions(chemin: str) -> list[dict]:
    with open(chemin, encoding="utf-8-sig") as f:
        lignes = f.read().splitlines()
    # L'export LinkedIn commence par quelques lignes de notes avant l'en-tête.
    debut = next(i for i, l in enumerate(lignes) if l.startswith("First Name"))
    return list(csv.DictReader(io.StringIO("\n".join(lignes[debut:]))))


def trouver_vivier(entreprise: str, viviers: dict) -> str | None:
    e = normaliser(entreprise)
    for nom, alias in viviers.items():
        if any(re.search(rf"\b{re.escape(normaliser(a))}\b", e) for a in alias):
            return nom
    return None


def estimer_seniorite(poste: str) -> tuple[str, str]:
    p = normaliser(poste)
    for motif, libelle, statut in SENIORITE:
        if re.search(motif, p):
            return libelle, statut
    return "Indéterminée", "limite"


def besoins_correspondants(poste: str, besoins: dict) -> list[str]:
    p = normaliser(poste)
    trouves = []
    for code, b in besoins.items():
        if any(normaliser(m) in p for m in b["mots_cles"]):
            trouves.append(code)
    return trouves


def qualifier(c: dict, mandat: dict) -> dict | None:
    entreprise, poste = c.get("Company", ""), c.get("Position", "")
    vivier = trouver_vivier(entreprise, mandat["viviers_primaires"])
    points = 3 if vivier else 0
    if not vivier:
        vivier = trouver_vivier(entreprise, mandat.get("viviers_secondaires", {}))
        points = 1 if vivier else 0
    if not vivier:
        return None

    seniorite, statut = estimer_seniorite(poste)
    if statut == "hors":
        return None
    points += POINTS_SENIORITE[statut]
    besoins = besoins_correspondants(poste, mandat["besoins"])
    points += 2 if besoins else 0

    a_verifier = ["ancienneté réelle (3–10 ans)", "français courant", "basé(e) Île-de-France"]
    if statut == "bonus":
        a_verifier.insert(0, "au-delà de 10 ans : piste Business builder uniquement")

    return {
        "points": points,
        "nom": f"{c.get('First Name', '')} {c.get('Last Name', '')}".strip(),
        "entreprise": entreprise,
        "vivier": vivier,
        "poste": poste,
        "seniorite_estimee": seniorite,
        "besoins_suggeres": " ".join(besoins) or "à qualifier",
        "url": c.get("URL", ""),
        "connecte_le": c.get("Connected On", ""),
        "a_verifier": " · ".join(a_verifier),
    }


def main() -> None:
    if len(sys.argv) not in (3, 4):
        sys.exit(__doc__)
    with open(sys.argv[2], encoding="utf-8") as f:
        mandat = json.load(f)
    resultats = [r for c in lire_connexions(sys.argv[1]) if (r := qualifier(c, mandat))]
    resultats.sort(key=lambda r: (-r["points"], r["vivier"], r["nom"]))

    sortie = open(sys.argv[3], "w", encoding="utf-8", newline="") if len(sys.argv) == 4 else sys.stdout
    if resultats:
        w = csv.DictWriter(sortie, fieldnames=list(resultats[0]))
        w.writeheader()
        w.writerows(resultats)
    print(f"{len(resultats)} contact(s) retenu(s).", file=sys.stderr)


if __name__ == "__main__":
    main()
