# Packet Lab — CCNA hors ligne

**Ouvrez `index.html` dans votre navigateur.** Aucun serveur ni connexion Internet nécessaires. Copiez le dossier complet pour emporter les questions, figures et PDF.

40 modules fixes, 36 disponibles et 4 à venir. Les 280 questions sont incluses dans les quiz avec les réponses indiquées dans les sources PDF et HTML fournies. L’interface reste bilingue ; les contenus français non disponibles utilisent le repli anglais signalé.

Les topologies proviennent directement des PDF ; elles ne sont jamais redessinées. Équipements, liaisons et libellés conservent leur géométrie. Vous pouvez ouvrir la figure complète et le PDF original depuis chaque question. Elles restent identiques en EN et FR.

## Utilisation

- Vue d’ensemble : résultats, maîtrise, couverture du catalogue, reprise de session.
- Catalogue : recherche et filtres, puis choix entraînement, examen complet ou révision ciblée.
- Entraînement : une seule question visible, passage automatique après sélection complète, puis correction globale après un clic manuel sur Submit / Soumettre. Aucun bouton Next ou Previous. Les questions et les choix sont mélangés à chaque tentative.
- Examen : même composition automatique et soumission finale exclusivement manuelle ; examen mixte pour combiner plusieurs modules. L’expiration du chronomètre ne soumet jamais automatiquement.
- Révision intelligente : erreurs, questions non maîtrisées et révisions arrivées à échéance. Trois réussites consécutives établissent la maîtrise.
- Favoris et historique : toutes les propositions corrigées restent visibles dans l’ordre de la tentative. Les icônes ✅ et ❌ précèdent directement les propositions concernées. Les anciennes tentatives, les réponses et les erreurs sont conservées. Les nouvelles tentatives possèdent un identifiant de profil local au navigateur.
- Paramètres : langue, export/restauration de progression et import de banques JSON vérifiées.

Les données sont sauvegardées dans ce navigateur. Exportez-les avant de changer de navigateur, d’emplacement ou d’origine (`file://` / serveur local). Le chronomètre mesure le temps actif et se suspend à la mise en pause, à la fermeture et lorsque l’onglet est masqué.

## Documents

- `REPORT.md` : modules, chiffres réels et état de livraison.
- `SPECIFICATION.md` et `ARCHITECTURE.md` : périmètre et architecture.
- `IMPORT.md` : ajouter les futurs PDF sans modifier le moteur.
- `SOURCE_ISSUES.md` : questions source ambiguës et observations éditoriales.
- `TRANSLATION_ISSUES.md` : explications françaises restant à vérifier.
- `TEST_REPORT.md` : vérifications finales et limites.

## Maintenance

Après modification de `data/questions.json` :

```bash
node scripts/build.cjs
node --test tests/core.test.cjs tests/composition.test.cjs tests/mi-content.test.cjs
```

Les scripts Python de contrôle des figures nécessitent PyMuPDF et Pillow :

```bash
python3 tests/topologies.py
```

Les tests navigateur utilisent Playwright et un Chromium installé. Les chemins locaux du runtime utilisé ici figurent dans `tests/browser.cjs` et `tests/extended-browser.cjs` ; adaptez-les sur un autre appareil. Pour lancer leur prévisualisation facultative :

```bash
python3 -m http.server 8765 --bind 127.0.0.1
```

L’application distribuée ne dépend d’aucun de ces outils de maintenance.

## Interface Frontend Excellence

L’accueil CCNA Training Lab est la page d’entrée : bandeau d’entraînement, statistiques réelles et cartes des 17 modules disponibles. Le catalogue conserve les 40 modules dans leur ordre initial. Le thème sombre est le défaut des appareils sans préférence enregistrée. La navigation donne accès au suivi, à la révision, aux favoris, à l’historique et aux paramètres. EN/FR reste accessible dans l’en-tête. Le bouton d’apparence et les paramètres permettent de choisir un thème clair, sombre ou système ; ce choix est enregistré sur cet appareil.

Voir `DESIGN.md` pour la direction retenue et `FRONTEND_REPORT.md` pour les vérifications et captures de la refonte. Les fichiers PDF, questions et topologies n’ont pas été modifiés.
