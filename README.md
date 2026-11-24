# Monte-Carlo pour la valorisation d'options

Projet du module **Mathématiques et Assurance** · ESPRIT · 2026-2027 · Encadrant : M. Mohsen Chebbi
Équipe : Mohamed Derbel, Oumaima Mrabet, Tasnim Ghodbane, Adem Ben Ali, Mariem Hamouda.

On calcule le prix d'un **call européen** par simulation de Monte-Carlo et on le compare au prix exact de **Black-Scholes** ($C_{BS} = 10{,}4506$). On réduit ensuite l'erreur avec deux techniques de réduction de variance : les **variables antithétiques** et la **variable de contrôle**. Enfin, on applique la méthode à une **option asiatique** (moyenne arithmétique), qui n'a pas de formule fermée. Tous les tirages gaussiens sont fabriqués par la **méthode de Box-Muller**.

[![Ouvrir dans Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/daliabidi03/Monte-Carlo/blob/main/Projet_MonteCarlo_Call.ipynb)

## Voir les résultats

| Pour… | Ouvrir |
|---|---|
| Parcourir les résultats partie par partie, avec le code de chaque résultat | [`docs/index.html`](docs/index.html) (à télécharger puis ouvrir dans un navigateur) |
| Exécuter le code sans rien installer | le badge **Open in Colab** ci-dessus, puis *Exécution → Tout exécuter* |
| Lire la théorie et les démonstrations | [`docs/Rapport.pdf`](docs/Rapport.pdf) |

La page [`docs/index.html`](docs/index.html) a un sommaire fixe à gauche (une entrée par partie). Sous chaque tableau ou figure, le bouton **Code de la cellule** montre le code exact qui l'a produit, et **Afficher tout le code de la partie** déplie tout le code d'une partie.

## Ce que contient le notebook

Chaque partie commence par une courte introduction et l'équation utilisée ; chaque cellule de code est précédée d'une phrase qui dit ce qu'elle fait.

| Partie | Contenu | Énoncé | Fonctions |
|---|---|---|---|
| 1 | Paramètres et outils | | `generateur`, `enregistrer` |
| 2 | Méthode de Box-Muller | | `box_muller` |
| 3 | Formule de Black-Scholes (prix de référence) | Étape 1 | `prix_call_bs` |
| 4 | Discrétisation du mouvement brownien géométrique : schéma exact et schéma d'Euler | Étape 2.1 | `simuler_trajectoires` |
| 5 | Monte-Carlo standard, IC à 95 % pour $10^3 \le N \le 10^6$ | Étapes 2.2, 2.3 | `mc_standard` |
| 6 | Variables antithétiques | Étape 3 | `mc_antithetique` |
| 7 | Variable de contrôle $X = S_T$ ($c^*$ analytique et estimé) | Étape 3 | `mc_controle` |
| 8 | Comparaison : biais, MSE empirique, gain de variance, temps, efficacité | Étape 3.2 | |
| 9 | Courbe de gain | Étape 3.2 | |
| 10 | Option asiatique : grille complète, prix, sensibilité à $M$ et à $N$, variable de contrôle géométrique | Étape 4 | `mc_asiatique`, `prix_asiatique_geometrique` |

## Principaux résultats

Call européen, $S_0 = K = 100$, $T = 1$ an, $r = 5\,\%$, $\sigma = 20\,\%$, budget de $N = 10^6$ payoffs par méthode, 50 répétitions :

| Méthode | Prix (un calcul) | SE | MSE empirique | Gain de variance | Efficacité (temps compris) |
|---|---|---|---|---|---|
| Standard | 10,4419 | 0,01471 | 2,2·10⁻⁴ | ×1,0 | ×1,0 |
| Antithétique | 10,4373 | 0,01035 | 1,3·10⁻⁴ | ×2,0 | ×3,7 |
| Variable de contrôle | 10,4499 | 0,00561 | 3,5·10⁻⁵ | ×6,9 | ×6,5 |

Le coefficient de contrôle estimé sur un échantillon pilote vaut $c^* = 0{,}6413$, pour une valeur analytique de $0{,}6408$. Les temps (donc l'efficacité) dépendent de la machine ; les prix et les gains de variance, non.

Call asiatique arithmétique (mêmes paramètres, moyenne sur $M$ dates, $N = 10^5$ trajectoires, variable de contrôle = call asiatique géométrique, qui a une formule fermée) :

| $M$ (dates de moyenne) | 1 | 4 | 12 (mensuel) | 52 (hebdomadaire) | 252 (quotidien) |
|---|---|---|---|---|---|
| Prix | 10,4506 (= call européen) | 6,9394 | 6,1551 | 5,8536 | 5,7810 |
| SE avec contrôle | 0 | 0,0009 | 0,0007 | 0,0007 | 0,0007 |

Le prix baisse quand $M$ augmente, car la moyenne lisse la volatilité. La variable de contrôle géométrique divise la variance par environ 1 300.

## Exécuter le projet

**Sans rien installer :** badge **Open in Colab** ci-dessus, puis *Exécution → Tout exécuter* (environ une minute).

**Sur sa machine :**
```bash
pip install -r requirements.txt
jupyter notebook Projet_MonteCarlo_Call.ipynb
```

Chaque partie a son propre générateur aléatoire à graine fixée : le notebook redonne toujours les mêmes chiffres, et une partie peut être réexécutée seule (après la partie 1 et les fonctions qu'elle utilise).

**Mettre à jour les figures et la page de résultats** après une modification du notebook :
```bash
jupyter nbconvert --to notebook --execute --inplace Projet_MonteCarlo_Call.ipynb
python outils/generer_page.py
```

**Compiler le rapport :** `cd rapport && latexmk -pdf rapport.tex`, puis copier `rapport.pdf` vers `docs/Rapport.pdf` (ou importer le dossier `rapport/` dans Overleaf ; les figures sont lues dans `../figures/`).

## Organisation du dépôt

| Chemin | Contenu |
|---|---|
| `Projet_MonteCarlo_Call.ipynb` | Le notebook, exécuté (code, résultats et figures) |
| `docs/index.html` | La page de résultats générée à partir du notebook |
| `docs/Rapport.pdf` | Le rapport (LaTeX) |
| `docs/Explication_du_code.pdf` | Explication du code avec questions et réponses |
| `docs/Presentation_Demo_du_code.pdf` | La présentation (démo du code) |
| `figures/` | Les figures produites par le notebook (utilisées par le rapport) |
| `rapport/` | Sources LaTeX du rapport et de l'explication du code |
| `outils/generer_page.py` | Le script qui génère `docs/index.html` |

## Travailler à plusieurs

1. Avant de modifier : `git pull`.
2. Si on modifie le notebook, le réexécuter en entier puis régénérer la page (commandes ci-dessus), pour que résultats, figures et page restent cohérents.
3. `git add .`, `git commit -m "ce qui a changé"`, `git push`.
