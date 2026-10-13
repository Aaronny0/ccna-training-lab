# Architecture

## Artefacts et responsabilités

| Chemin | Rôle |
|---|---|
| `index.html`, `style.css` | Point d’entrée sans compilation, mise en page adaptative |
| `app.js` | Navigation, catalogue, sessions, favoris, historique, import/export, chronomètre |
| `core.js` | Fonctions pures : permutations, correction par ID, score, maîtrise, statistiques, validation, dédoublonnage |
| `i18n.js` | Dictionnaires complets de l’interface EN / FR |
| `scripts/catalog.cjs` | 40 modules et traductions ; ordre et IDs permanents |
| `data/questions.json` | Banque canonique des questions extraites et vérifiées |
| `data/bank.js` | Banque de distribution générée, chargée par une balise script (compatible file://) |
| `data/sources.json` | PDF originaux, empreintes, module, pages, détection de doublon |
| `data/topologies.json` | Origine et vérification géométrique des figures |
| `sources/` | Copies des 18 PDF reçus, plus extraits textuels / OCR archivés |
| `assets/` | Illustrations locales fidèles aux sources |
| `scripts/import.cjs`, `scripts/build.cjs` | Import vérifié, validation et production de la banque navigateur |
| `tests/` | Tests du moteur, parcours navigateur et comparaison des schémas |

## Identifiants

Les IDs de modules ne changent jamais. Les IDs de questions publiées ne changent jamais et commencent par leur ID de module. Les choix et les cibles ont des IDs permanents. Une réponse est une liste d’IDs ou un dictionnaire cible → ID de choix, jamais une lettre de position ni un texte traduit.

Une session stocke l’ordre des questions, l’ordre des options par question, l’ordre des cibles, les réponses choisies, l’index courant et les validations. La langue est un état de présentation séparé. Le changement EN/FR rerend les textes sans appeler Fisher–Yates. L’examen complet utilise toutes les questions évaluables du périmètre sélectionné, sans remplacement ni duplication.

## Persistance

`packetlab-progress-v1` dans localStorage : langue, statistiques par question, favoris, historique et session active. `packetlab-packs-v1` : packs de contenu importés localement. Les IDs conservés rendent les progrès insensibles à l’ajout de questions. Les compteurs sont recalculés à partir de la banque fusionnée. L’import de contenu ne modifie jamais les progrès. Les conflits de contenu sur un ID existant sont rejetés, plutôt que d’effacer ou de réinterpréter les réponses antérieures.

L’export inclut progression et packs. La restauration demande une confirmation explicite puisqu’elle remplace la progression locale. Les erreurs d’écriture localStorage sont signalées. Les origines HTTP et file:// ont des stockages distincts : exporter avant de changer de mode d’ouverture, de chemin, de navigateur ou d’appareil.

## Contenu et traduction

Les originaux anglais restent en données, avec proposition et réponse source fidèles. Les pages sources scannées ont été lues visuellement pour corriger l’OCR. Les commentaires, menus et anciennes statistiques des pages 9tut ne font pas partie de la banque de questions. Les explications ambiguës ne sont pas corrigées silencieusement : l’original et le problème sont conservés séparément.

`verified` signifie que la question est admise dans les sessions notées après contrôle de sa source et de sa cohérence ; ce n’est pas une certification Cisco. Les questions à corriger restent dans une zone de consultation dédiée. `translationStatus` vaut `validated`, `partial` ou `pending`. La vérification des traductions décrit une comparaison interne EN/FR réalisée par Codex ; elle ne prétend pas à une relecture certifiée par un expert externe. Les champs non vérifiés n’ont pas de traduction française affichée.

## Hors ligne

Aucune requête applicative, CDN, police distante, API ou bibliothèque distante. HTML, CSS, JS, données, figures et PDF sont locaux. Le navigateur peut ouvrir le dossier avec file://. Un serveur local est facultatif pour prévisualiser et tester, sans devenir une dépendance de l’application. Aucun service worker n’est nécessaire au fonctionnement file:// ; une URL HTTP ne reste pas navigable après l’arrêt de son serveur.

## Frontend Excellence : présentation et préférences

La refonte conserve le HTML/CSS/JavaScript statique sans dépendance ni réseau. `app.js` rend neuf vues dans le même document : catalogue, suivi, module, quiz, résultats, révision, favoris, historique et paramètres. Le catalogue indexé reste la page d’entrée et respecte l’ordre des 40 modules.

`style.css` centralise les tokens, la typographie, les contrôles et les points de rupture. La largeur utile est limitée à 1160 px ; le catalogue passe de trois à deux puis une colonne. La navigation du quiz reste latérale sur grand écran et précède la feuille de question sur tablette/mobile. Le bouton de fin de session reste accessible sur toutes les questions.

Le champ facultatif `state.theme` vaut `light`, `dark` ou `system` et est enregistré avec les préférences existantes. Les anciennes sauvegardes sans ce champ restent compatibles. La résolution du thème ne modifie aucune réponse, permutation, durée ni progression. Le focus est restauré après les interactions et passe au titre lors d’un changement de vue.

Les dimensions intrinsèques des figures proviennent du manifeste original ; elles réservent l’espace sans altérer les assets. Les images du quiz chargent immédiatement et leurs liens permettent de voir la source en taille réelle. Aucune recoloration, découpe ni reconstitution de topologie n’est effectuée.

Les erreurs de sélection d’un examen mixte sont affichées dans le dialogue natif, avec un message bilingue accessible. Les notifications transitoires sont retirées lors du changement de vue ou de langue. Le moteur, la banque, les sources et les identifiants restent inchangés.

La direction et l’audit sont documentés dans `DESIGN.md`. Les captures et scénarios sont dans `tests/visual-qa/` et `tests/frontend-qa.cjs`.
