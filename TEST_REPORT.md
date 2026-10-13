# Vérification finale — 12 octobre 2026

Parcours vérifié : ouverture locale → catalogue → session mélangée → correction par identifiants → sauvegarde locale → reprise → résultat → statistiques. Il n’y a ni API serveur ni base distante dans cette application.

## Résultats

| Contrôle | Résultat et preuve |
|---|---|
| Moteur et données | 12 tests Node réussis, 0 échec (`tests/core-results.txt`) |
| Catalogue | 40 noms dans l’ordre exact ; IDs distincts ; 17 modules disponibles et 23 vides |
| Rubrique vide | 0 question ; bouton d’examen désactivé ; création de session vide rejetée |
| Examens et mélange | Chaque question exactement une fois ; permutations sans perte de choix ; score fondé sur les IDs |
| Bilinguisme | Dictionnaires UI complets ; tous les énoncés et choix FR présents ; les traductions annoncées complètes sont validées par le schéma |
| Commandes | Options IOS et JSON comparées octet par octet EN / FR ; adresses IP des énoncés EN / FR comparées sans divergence |
| Images | 37 références d’illustrations identiques aux pixels originaux ou au rendu exact de leur rectangle PDF (`tests/topology-results.txt`) |
| Interface principale | `tests/browser.cjs` réussi : catalogue, filtres, progression automatique et soumission manuelle, favoris, résultats, reprise, langue, associations, mobile et file:// hors ligne |
| Examens et imports | `tests/extended-browser.cjs` réussi : examen complet à 100 %, absence de correction avant la fin, export/restauration, import réitéré sans doublons, ajout dans un module vide, glisser-déposer réel, expiration sans soumission automatique |
| Fermeture du navigateur | Chromium avec profil disque fermé puis rouvert : préférence FR conservée |
| Topologie dans l’interface | `tests/topology-browser.cjs` réussi : même fichier EN / FR, chargement complet, absence de débordement mobile, liens image entière et PDF source |
| Affichage | Captures ordinateur et mobile examinées ; figures non coupées, proportions conservées, commandes et questions lisibles |
| Console | Aucun événement pageerror dans les parcours testés |

## Choix explicitement conservés

Les éléments proposés sont mélangés, mais les emplacements d’association conservent l’ordre de leurs numéros/positions. Cela préserve le sens des séquences et les repères originaux. Les références A/B/C dans certaines explications désignent les lettres du PDF source ; un avertissement précise cette distinction après mélange des choix.

## Limites réelles

- Les tests navigateur ont été exécutés sur Chromium, aux largeurs de 1440 et 390 pixels, ainsi qu’avec une ouverture file:// hors ligne. Safari et Firefox n’ont pas été exécutés ici.
- La fidélité des figures est testée automatiquement et les recadrages scannés ont été vérifiés visuellement. Cela ne corrige pas une éventuelle erreur déjà présente dans la topologie du PDF : elle est conservée telle quelle.
- Toutes les questions source sont incluses dans les scores avec leurs clés originales. Les réserves documentaires n’entraînent plus d’exclusion.
- Huit explications restent en anglais avec indication de traduction à vérifier ; elles ne sont pas présentées comme des traductions françaises validées.
- L’import est un import de données préparées et relues, pas une certification automatique d’un PDF. Le test d’ajout utilise un pack temporaire dans un contexte navigateur de test ; aucune question fictive n’est ajoutée à la banque distribuée.
- La vérification des contenus et traductions est une revue interne par Codex, pas une certification Cisco ou une relecture externe.

## Refonte selon le HTML fourni

La présentation centrée, le catalogue à trois colonnes, la navigation compacte, les modes clair/sombre et le favicon turquoise remplacent la présentation initiale. Les tests du moteur (12), les parcours navigateur, les examens/sauvegardes/imports et les contrôles de topologie ont réussi après refonte. Le contrôle des 37 figures confirme encore leur correspondance exacte avec la source. Captures : `tests/design-catalog.png`, `tests/design-quiz.png`, `tests/design-dark.png` et `tests/mobile.png`.

## Frontend Excellence — vérification finale

La refonte des neuf vues et ses vérifications sont détaillées dans `FRONTEND_REPORT.md`. `tests/frontend-qa.cjs` couvre 93 scénarios visuels aux cinq largeurs demandées (360, 390, 768, 1024, 1440 px), les thèmes, le focus, les dialogues, la correction et les schémas. Les défauts de fin de session mobile et de notification de dialogue ont été corrigés. Les invariants du moteur et des sources restent vérifiés.

## 2026-10-13 — modèle CCNA Training Lab fourni par l’utilisateur

Le rendu suit désormais le HTML de référence : fond bleu nuit, barre latérale, bandeau d’accueil, cartes colorées et résultats centrés. L’accueil affiche les 17 modules disponibles, le catalogue conserve les 40 modules dans l’ordre d’origine. Toutes les clés et données de progression existantes sont préservées ; aucun contenu du petit exemple de référence n’a remplacé la banque validée.

Validation : 12 tests du moteur, parcours de `browser.cjs` et `extended-browser.cjs`, vérification des topologies et 93 scénarios de `frontend-qa.cjs` sur 360/390/768/1024/1440 px. Comparaison SHA-256 : 120 fichiers du moteur, de banque, de sources et d’assets inchangés. Comparaison avec les PDF : 37 références d’illustrations identiques. Vérification visuelle supplémentaire de l’accueil FR, quiz sombre, résultats desktop/mobile et paramètres mobiles. Le thème clair et les huit explications encore en anglais restent accessibles.

## Refonte de composition et correction - 13 octobre 2026

- Une question visible, progression automatique fondée uniquement sur le nombre de réponses attendu ou la complétude des associations. Si le nombre est absent, confirmation explicite de la sélection.
- Aucune navigation Next/Previous ou équivalente ; indicateurs de progression non interactifs.
- Submit/Soumettre apparaît uniquement après toutes les réponses. Aucune correction ni soumission automatique, même à l’expiration du chronomètre.
- Résultats ouverts sur une page, dans l’ordre réel de la tentative, avec toutes les propositions dans leur ordre de présentation. ✅ devant toutes les bonnes propositions ; ❌ devant les mauvaises propositions choisies ; espace neutre identique pour les autres.
- Score exact sans points partiels ; nouvelles tentatives enregistrées avec identifiant local, dates, réponses, ordre, réussites et erreurs. L’historique antérieur, les sauvegardes, les imports et les PDF téléchargeables sont conservés.
- Les 192 clés du HTML sont comparées automatiquement à la banque. Les 280 questions sont évaluables ; aucun énoncé, choix, corrigé, explication ni schéma n’est réécrit par cette refonte.
- Tests : `tests/composition.test.cjs`, `tests/composition-browser.cjs`, tests de moteur et d’import, tests navigateur existants adaptés, contrôle des PDF et des topologies.

Le suivi utilisateur demeure local à chaque navigateur, conformément à l’architecture existante. Le projet ne contient pas de service d’authentification ni de comptes connectés ; aucun service externe n’a été ajouté par cette refonte.
