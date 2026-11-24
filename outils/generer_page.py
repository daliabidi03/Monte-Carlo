"""Génère docs/index.html : la page de résultats du notebook exécuté.

Usage (depuis la racine du dépôt) :
    jupyter nbconvert --to notebook --execute --inplace Projet_MonteCarlo_Call.ipynb
    python outils/generer_page.py

La page reprend chaque partie du notebook : texte et équations, résultats (tableaux, figures)
et, sous chaque résultat, le code de la cellule qui l'a produit (bouton « Code »).
"""
import html
import json
import re
import sys
from pathlib import Path

import mistune
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

RACINE = Path(__file__).resolve().parent.parent
NOTEBOOK = RACINE / "Projet_MonteCarlo_Call.ipynb"
SORTIE = RACINE / "docs" / "index.html"

markdown = mistune.create_markdown(plugins=["table"], escape=False)
ANCRE = re.compile(r'<a id="(partie-[^"]+)"></a>')
RETOUR = re.compile(r"<small>\[↑ Retour au sommaire\]\(#sommaire\)</small>")


def md_vers_html(texte):
    """Markdown -> HTML en protégeant les formules LaTeX (rendues ensuite par MathJax)."""
    formules = []

    def proteger(m):
        formules.append(m.group(0))
        return f"\x00{len(formules) - 1}\x00"

    texte = RETOUR.sub("", texte)
    texte = re.sub(r"\$\$.+?\$\$", proteger, texte, flags=re.S)
    texte = re.sub(r"\$[^$\n]+?\$", proteger, texte)
    rendu = markdown(texte)
    return re.sub(r"\x00(\d+)\x00", lambda m: html.escape(formules[int(m.group(1))], quote=False), rendu)


def sorties_vers_html(cellule):
    morceaux = []
    for sortie in cellule.get("outputs", []):
        if "text" in sortie:
            morceaux.append(f'<pre class="sortie">{html.escape("".join(sortie["text"]))}</pre>')
        donnees = sortie.get("data", {})
        if "image/png" in donnees:
            morceaux.append(f'<img class="figure" src="data:image/png;base64,{donnees["image/png"].strip()}" alt="figure">')
        elif "text/plain" in donnees and sortie.get("output_type") == "execute_result":
            morceaux.append(f'<pre class="sortie">{html.escape("".join(donnees["text/plain"]))}</pre>')
        if sortie.get("output_type") == "error":
            morceaux.append(f'<pre class="sortie erreur">{html.escape(sortie["ename"] + ": " + sortie["evalue"])}</pre>')
    return "\n".join(morceaux)


def main():
    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    if not any(c.get("outputs") for c in nb["cells"] if c["cell_type"] == "code"):
        sys.exit("Le notebook n'a pas de sorties : exécutez-le d'abord (voir l'en-tête de ce script).")

    sections, menu, courante = [], [], None
    entete = ""
    formateur = HtmlFormatter(nowrap=True)
    for cellule in nb["cells"]:
        source = "".join(cellule["source"])
        if cellule["cell_type"] == "markdown":
            ancre = ANCRE.search(source)
            if ancre:
                titre = re.search(r"^## (.+)$", source, re.M).group(1)
                titre_court = re.sub(r"\s*<small>.*?</small>", "", titre)
                menu.append((ancre.group(1), titre_court))
                courante = {"id": ancre.group(1), "html": []}
                sections.append(courante)
                source = ANCRE.sub("", source)
            if courante is None:   # cellule de titre : on retire le sommaire, remplacé par le menu
                entete = md_vers_html(source.split('<a id="sommaire">')[0])
                continue
            if RETOUR.fullmatch(source.strip()):
                continue
            courante["html"].append(f'<div class="texte">{md_vers_html(source)}</div>')
        else:
            code = highlight(source, PythonLexer(), formateur)
            courante["html"].append(
                '<div class="cellule">'
                f'<div class="resultat">{sorties_vers_html(cellule) or "<p class=vide>(cellule sans affichage : elle définit des fonctions)</p>"}</div>'
                f'<details class="code"><summary>Code de la cellule</summary><pre class="highlight">{code}</pre></details>'
                "</div>"
            )

    liens = "\n".join(f'<a href="#{i}">{html.escape(t)}</a>' for i, t in menu)
    corps = "\n".join(
        f'<section id="{s["id"]}"><button class="basculer" onclick="basculer(this)">Afficher tout le code de la partie</button>'
        + "\n".join(s["html"]) + "</section>"
        for s in sections
    )
    page = MODELE.format(entete=entete, liens=liens, corps=corps, style_code=formateur.get_style_defs(".highlight"))
    SORTIE.parent.mkdir(exist_ok=True)
    SORTIE.write_text(page, encoding="utf-8")
    print(f"Page écrite : {SORTIE.relative_to(RACINE)} ({len(sections)} parties)")


MODELE = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Monte-Carlo pour la valorisation d'options : résultats</title>
<script>window.MathJax = {{tex: {{inlineMath: [["$", "$"]], displayMath: [["$$", "$$"]]}}}};</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
<style>
:root {{ --bleu: #143c82; --gris: #f4f5f7; --bord: #dde1e7; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; font: 16px/1.6 system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; color: #1d2330; }}
nav {{ position: fixed; top: 0; left: 0; bottom: 0; width: 290px; overflow-y: auto; background: var(--gris);
       border-right: 1px solid var(--bord); padding: 20px 14px; }}
nav h2 {{ font-size: 15px; margin: 0 0 12px; color: var(--bleu); }}
nav a {{ display: block; padding: 6px 10px; border-radius: 6px; color: #1d2330; text-decoration: none; font-size: 14px; }}
nav a:hover, nav a.actif {{ background: #e3e8f2; color: var(--bleu); }}
nav .outils {{ margin-top: 18px; border-top: 1px solid var(--bord); padding-top: 12px; }}
nav button {{ width: 100%; margin-bottom: 6px; }}
main {{ margin-left: 290px; padding: 24px 48px 80px; max-width: 1180px; }}
h1 {{ color: var(--bleu); }}
section {{ border-top: 2px solid var(--bord); padding-top: 8px; margin-top: 36px; position: relative; }}
section h2 {{ color: var(--bleu); margin-right: 260px; }}
button {{ font: inherit; font-size: 13px; padding: 5px 10px; border: 1px solid var(--bord); border-radius: 6px;
          background: white; color: var(--bleu); cursor: pointer; }}
button:hover {{ background: #e3e8f2; }}
.basculer {{ position: absolute; right: 0; top: 22px; }}
table {{ border-collapse: collapse; margin: 10px 0; }}
th, td {{ border: 1px solid var(--bord); padding: 4px 10px; }}
th {{ background: var(--gris); }}
.cellule {{ border: 1px solid var(--bord); border-radius: 8px; margin: 12px 0 22px; overflow: hidden; }}
.resultat {{ padding: 10px 14px; }}
.resultat .vide {{ color: #777; font-style: italic; margin: 0; }}
pre.sortie {{ background: #fbfbfc; border-left: 3px solid var(--bleu); padding: 8px 12px; overflow-x: auto; font-size: 13.5px; }}
pre.erreur {{ border-left-color: #b00020; color: #b00020; }}
img.figure {{ max-width: 100%; display: block; margin: 6px auto; }}
details.code {{ border-top: 1px solid var(--bord); background: var(--gris); }}
details.code summary {{ cursor: pointer; padding: 6px 14px; font-size: 14px; color: var(--bleu); font-weight: 600; }}
details.code pre {{ margin: 0; padding: 10px 14px; overflow-x: auto; font-size: 13.5px; background: white; }}
@media (max-width: 900px) {{ nav {{ position: static; width: auto; }} main {{ margin-left: 0; padding: 16px; }} }}
{style_code}
</style>
</head>
<body>
<nav>
<h2>Sommaire</h2>
{liens}
<div class="outils">
<button onclick="toutLeCode(true)">Afficher tout le code</button>
<button onclick="toutLeCode(false)">Masquer tout le code</button>
</div>
</nav>
<main>
{entete}
<p><em>Sous chaque résultat, le bouton « Code de la cellule » montre le code exact qui l'a produit.</em></p>
{corps}
</main>
<script>
function toutLeCode(ouvrir) {{ document.querySelectorAll("details.code").forEach(d => d.open = ouvrir); }}
function basculer(bouton) {{
  const blocs = bouton.parentElement.querySelectorAll("details.code");
  const ouvrir = [...blocs].some(d => !d.open);
  blocs.forEach(d => d.open = ouvrir);
  bouton.textContent = ouvrir ? "Masquer le code de la partie" : "Afficher tout le code de la partie";
}}
const liens = document.querySelectorAll("nav a");
const observateur = new IntersectionObserver(entrees => entrees.forEach(e => {{
  if (e.isIntersecting) liens.forEach(a => a.classList.toggle("actif", a.getAttribute("href") === "#" + e.target.id));
}}), {{rootMargin: "-20% 0px -70% 0px"}});
document.querySelectorAll("section").forEach(s => observateur.observe(s));
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
