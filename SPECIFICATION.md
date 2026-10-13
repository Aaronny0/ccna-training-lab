# Packet Lab — cahier des charges livré

Application locale de préparation CCNA, créée dans ce dossier initialement vide. Les anciennes limites de quatre documents et 32 questions sont abandonnées. La demande utilisateur complète est conservée dans `REQUEST.md`.

## Catalogue et contenu

- Exactement 40 rubriques, noms anglais et ordre fournis inchangés. Identifiants permanents `ccna-01` à `ccna-40` ; les suffixes 2 et 3 sont des modules distincts.
- Les PDF accessibles ont été copiés dans `sources/`. Leur empreinte SHA-256 et leur classement figurent dans `data/sources.json`. Deux copies identiques de Drag Drop Quiz 2 alimentent une seule banque.
- Données séparées du moteur ; nombres calculés à partir des questions. Une rubrique sans questions reste visible, avec 0 Questions, Coming Soon et bouton d’examen désactivé.
- Questions ambiguës conservées dans la consultation des sources, exclues des entraînements et examens notés. Voir `SOURCE_ISSUES.md`.
- Aucun contenu créé pour les rubriques vides.

## Topologies : priorité absolue

Les figures ne sont jamais redessinées. Les images embarquées dans les PDF textuels sont converties sans perte en PNG, avec leurs pixels originaux. Les figures des PDF scannés sont rendues directement depuis la page source à une échelle uniforme, sans déplacer ou retoucher leurs éléments. Les recadrages possèdent des marges et ont été examinés visuellement.

Équipements, liens, positions, adresses, masques, noms d’interfaces et annotations restent inchangés. Le bouton EN/FR utilise le même fichier image. Un lien ouvre chaque image entière et un autre ouvre le PDF original à sa page. `data/topologies.json` enregistre leur provenance, géométrie et empreinte de pixels. `tests/topologies.py` compare les figures référencées aux pixels sources ou au rendu exact de leur rectangle PDF.

## Apprentissage

- Fisher–Yates pour les questions, réponses et éléments d’association à chaque nouvelle tentative.
- Entraînement : validation immédiate d’une réponse simple ; d’un QCM quand le nombre attendu de réponses est atteint ; d’une association quand tous les emplacements sont remplis.
- Examen complet d’un module ou examen mixte de modules choisis : chaque question évaluable exactement une fois ; réponses modifiables et correction seulement à la fin. Durée mixte configurable de 1 à 240 minutes ; examen de module de 60 minutes.
- Score par question, tout ou rien, y compris QCM et associations ; seuil d’entraînement de 80 %, sans prétendre reproduire le barème officiel Cisco.
- Correction finale, réponses choisies, bonnes réponses, explications, références, filtre des erreurs et nouvelle tentative des erreurs.
- Favoris, historique, persistance et reprise d’une session avec son ordre exact.
- Maîtrise : trois tentatives consécutives correctes d’une question. Une erreur remet la série à zéro. Révision ciblée selon erreurs, notions non maîtrisées et échéances espacées de 2, 4, 8, 16 puis 30 jours.
- Chronomètre en temps actif : il est suspendu lors de la sauvegarde, d’une navigation, de la fermeture ou du masquage de l’onglet. Une expiration termine automatiquement l’examen.

## Statistiques distinctes

Couverture = modules ayant des questions évaluables / 40. Maîtrise = questions maîtrisées / questions évaluables. Performance = bonnes réponses / questions des examens terminés. Aucune performance n’est présentée avant un premier examen. Les entraînements sont dans l’historique mais ne modifient pas la performance des examens. Les rubriques vides ne diminuent ni maîtrise ni performance.

## Bilinguisme

L’anglais est affiché au premier lancement. EN/FR couvre l’interface, les modules, les énoncés, choix et consignes. La préférence est sauvegardée. Les identifiants corrects, les permutations et la progression ne changent jamais avec la langue.

Les traductions sont écrites dans les données, sans appel à un traducteur externe ou une API. Les commandes, adresses, chiffres et blocs techniques sont conservés. Les labels de figures restent originaux conformément à la priorité utilisateur. Les explications dont la comparaison complète EN/FR n’est pas terminée restent en anglais avec un avertissement explicite. `TRANSLATION_ISSUES.md` donne la liste exacte et le niveau de vérification réellement effectué.

## Exploitation

Ouvrir `index.html` directement : aucun serveur, compilation, CDN ni accès réseau nécessaires. Le serveur de prévisualisation est uniquement un outil facultatif de vérification. Les résultats sont locaux au navigateur et à l’emplacement de l’application ; export et restauration JSON permettent de changer de navigateur ou d’appareil.

Importer de nouveaux PDF consiste à copier la source, produire un pack de questions vérifié selon `IMPORT.md`, puis l’importer par CLI ou dans Paramètres. Le moteur et les composants restent inchangés. Le code ne prétend pas certifier automatiquement les réponses à partir d’un PDF.
