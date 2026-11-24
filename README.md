# Monte-Carlo — Valorisation d'un call européen

Projet du module **Mathématiques et Assurance** — ESPRIT, 2026-2027.
Encadrant : M. Mohsen Chebbi.

On calcule le prix d'un **call européen** par simulation de Monte-Carlo (tirages gaussiens par **Box-Muller**), on le compare au prix exact de **Black-Scholes** (C = 10,4506), puis on réduit la variance avec deux méthodes : **variables antithétiques** et **variable de contrôle**.

[![Ouvrir dans Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/daliabidi03/Monte-Carlo/blob/main/Projet_MonteCarlo_Call.ipynb)

## Résultats (N = 10^6)

| Méthode | Prix | SE | Erreur \|C − Ĉ\| | Gain de variance | Erreur moyenne (50 calculs) |
|---|---|---|---|---|---|
| Standard | 10,4370 | 0,01471 | 0,0136 | ×1,00 | 0,0127 |
| Antithétique | 10,4600 | 0,01039 | 0,0094 | ×2,00 | 0,0080 |
| Contrôle | 10,4472 | 0,00562 | 0,0034 | ×6,86 | 0,0044 |

Coefficient de contrôle : c* = 0,640505 (simulé), c = 0,640762 (analytique), erreur 0,000257.

## Contenu du dépôt

| Chemin | Contenu |
|---|---|
| `Projet_MonteCarlo_Call.ipynb` | Le notebook (code commenté, 9 parties) |
| `figures/` | Les figures produites par le notebook |
| `docs/Rapport.pdf` | Le rapport complet |
| `docs/Explication_du_code.pdf` | Explication du code, partie par partie, avec questions/réponses |
| `docs/Presentation_Demo_du_code.pdf` | La présentation (démo du code) |
| `docs/Chra7_presentation_tounsi.pdf` | Explication de la présentation en tunisien |
| `docs/Projet_MonteCarlo_Call.html` | Le notebook exécuté, lisible dans un navigateur |
| `rapport/` | Sources LaTeX du rapport, de l'explication du code et du chra7 |

## Exécuter le code

**Sans rien installer :** cliquer sur le badge « Open in Colab » ci-dessus, puis *Exécution → Tout exécuter*.

**Sur sa machine :**
```bash
pip install -r requirements.txt
jupyter notebook Projet_MonteCarlo_Call.ipynb
```
Le générateur est fixé (graine 2026) : en exécutant le notebook du début à la fin, on retrouve tous les nombres du rapport. Seuls les temps de calcul (et donc l'efficacité) changent d'une machine à l'autre.

## Compiler les documents LaTeX

```bash
cd rapport
latexmk -pdf rapport.tex             # rapport
latexmk -pdf guide_code.tex          # explication du code
latexmk -pdf explication_tounsi.tex  # chra7 de la présentation
```
Ou importer le dossier dans Overleaf (les figures sont dans `../figures/`, les images des slides dans `rapport/slides_img/`).

## Travailler à plusieurs

1. Chaque membre accepte l'invitation de collaborateur sur GitHub.
2. Avant de modifier : `git pull`.
3. Après la modification : `git add .`, `git commit -m "ce qui a changé"`, `git push`.
4. Si on modifie le notebook, le ré-exécuter en entier (*Restart & Run All*) avant de le pousser, pour que les sorties et les figures restent cohérentes.
