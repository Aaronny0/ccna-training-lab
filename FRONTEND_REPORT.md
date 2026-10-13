# Livraison — Frontend Excellence

## Direction et périmètre

Refonte des neuf vues selon le nouveau fichier de référence `CCNA_Training_Lab (1).html` fourni par l’utilisateur. Direction : CCNA Training Lab bleu nuit, barre latérale, bandeau d’accueil, accents colorés et cartes de modules. L’accueil présente les 17 modules disponibles ; le catalogue dédié conserve les 40 modules et leur ordre. Les fonctionnalités et la banque validée du projet sont conservées.

Le skill `/home/aaron/Téléchargements/SKILL (1).md` a été lu intégralement et appliqué. L'audit, les tokens et les choix responsive sont détaillés dans [DESIGN.md](DESIGN.md). L'annexe `references/visual-qa.md` citée par le skill n'a pas été fournie et n'a pas été trouvée ; les vérifications prescrites dans le corps du skill ont été effectuées.

## Modifications effectives

- Barre latérale et fil d’Ariane inspirés du modèle, navigation mobile défilante, EN/FR et contrôle d’apparence.
- Accueil et catalogue en cartes à deux ou une colonne, recherche instantanée, filtres, compteur de résultats et reprise de session. Ordre des 40 modules conservé.
- Suivi avec données réelles, métriques distinctes, derniers résultats et accès à la révision.
- Choix de modes sous forme de lignes explicites ; les questions ambiguës restent consultables à part et exclues des scores.
- Quiz avec feuille de question, instructions, choix lisibles, navigation de session, favori, code en monospace et source accessible. Les contrôles de fin de session restent accessibles sur mobile.
- Correction avec symboles et texte, colonnes « votre réponse / réponses correctes », explications et figures originales.
- Résultats avec score, bonnes réponses, erreurs, durée et corrections dépliables ; historique et listes de révision harmonisés.
- Paramètres organisés en préférences, sauvegarde/restauration, import et vérification de contenu.
- Thème sombre par défaut sans préférence enregistrée ; thèmes clair/sombre/système persistants et anciennes sauvegardes compatibles.
- Focus clavier conservé après les interactions, passage au titre lors des changements de vue, navigation active visible après redimensionnement. Dialogues natifs fermables avec Échap.
- Erreur de sélection vide visible dans le dialogue d'examen mixte. Notifications transitoires retirées au changement de vue ou de langue.

Fichiers principaux : `app.js`, `style.css`, `i18n.js`, `index.html`. Aucun framework, service, dépendance ou police distante ajouté.

## Vérifications

Commandes lancées depuis le projet :

```sh
node --check app.js
node --test tests/core.test.cjs
node tests/browser.cjs
node tests/extended-browser.cjs
node tests/topology-browser.cjs
node tests/frontend-qa.cjs
/home/aaron/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 tests/topologies.py
```

Les tests du moteur (12) passent. Les parcours navigateur vérifient les modules vides, les permutations EN/FR, les choix multiples, l'association réelle par glisser-déposer, la correction différée des examens, le chronomètre, les favoris, les sauvegardes, la reprise, les imports et le fonctionnement hors ligne en `file://`.

Le test `frontend-qa.cjs` couvre 93 couples d'écran/largeur, avec captures pleine page et captures de viewport supplémentaires. Toutes les vues principales sont testées en **360, 390, 768, 1024 et 1440 px**, y compris les états vides et remplis, corrections, examens, dialogues et topologies. Aucun débordement horizontal involontaire, titre coupé ou erreur JavaScript détecté. Le thème persiste ; EN/FR conserve les permutations ; la navigation au clavier et les erreurs de dialogue sont testées.

Les vues principales ont été inspectées visuellement sur desktop et mobile et comparées à la référence. L’espacement des panneaux de paramètres et le centrage des résultats mobiles ont été corrigés puis revérifiés. Contrastes calculés : texte principal sombre 15,87:1, texte secondaire sombre 8,14:1, secondaire sur blanc 5,85:1 ; texte blanc des boutons de 5,08 à 5,16:1 aux extrémités du dégradé. Ce contrôle ne constitue pas une certification WCAG complète.

Le test des topologies confirme **37 références de figures identiques aux pixels/rendus sources**. Une comparaison SHA-256 confirme que les **120 fichiers** du moteur, de la banque et des sources présents avant la refonte sont inchangés. Aucun équipement, lien, adresse ou interface n'a été redessiné, déplacé, coupé ou recoloré.

Le test d'import a été rendu déterministe : il attend désormais la notification de fin de lecture asynchrone avant d'en vérifier le contenu.

## Captures

- [Accueil FR selon le nouveau modèle](tests/visual-qa/reference-home-fr-1440.png).
- [Quiz sombre](tests/visual-qa/reference-quiz-dark-1440.png) et [résultats mobiles sombres](tests/visual-qa/reference-results-dark-390.png).

- [Catalogue desktop](tests/visual-qa/catalog-1440-viewport.png) et [mobile](tests/visual-qa/catalog-390-viewport.png).
- [Suivi desktop](tests/visual-qa/dashboard-empty-1440-viewport.png) et [mobile](tests/visual-qa/dashboard-empty-390-viewport.png).
- [Module desktop](tests/visual-qa/module-1440-viewport.png) et [mobile](tests/visual-qa/module-390-viewport.png).
- [Quiz desktop](tests/visual-qa/quiz-1440-viewport.png) et [mobile](tests/visual-qa/quiz-390-viewport.png).
- [Correction desktop](tests/visual-qa/quiz-feedback-1440-viewport.png) et [mobile](tests/visual-qa/quiz-feedback-390-viewport.png).
- [Résultats desktop](tests/visual-qa/results-1440-viewport.png) et [mobile](tests/visual-qa/results-390-viewport.png).
- [Révision desktop](tests/visual-qa/review-1440-viewport.png) et [mobile](tests/visual-qa/review-390-viewport.png).
- [Favoris desktop](tests/visual-qa/favorites-1440-viewport.png) et [mobile](tests/visual-qa/favorites-390-viewport.png).
- [Historique desktop](tests/visual-qa/history-1440-viewport.png) et [mobile](tests/visual-qa/history-390-viewport.png).
- [Paramètres desktop](tests/visual-qa/settings-1440-viewport.png) et [mobile](tests/visual-qa/settings-390-viewport.png).
- [Topologie desktop](tests/visual-qa/topology-1440-viewport.png) et [mobile](tests/visual-qa/topology-390-viewport.png), [version sombre FR](tests/visual-qa/topology-fr-dark-390.png).
- [Glisser-déposer desktop](tests/visual-qa/matching-1440-viewport.png) et [mobile](tests/visual-qa/matching-390-viewport.png).

Liste complète des scénarios : [checks.json](tests/visual-qa/checks.json). Les résultats et réponses affichés dans ces captures proviennent de tentatives exécutées dans des profils de test isolés ; ils ne sont pas injectés dans la plateforme ni dans la progression de l'utilisateur.

## Limites et contenu conservé

Les vérifications automatisées ont été effectuées avec Chromium, sur des viewports simulés. Firefox, Safari, les appareils physiques et les lecteurs d'écran n'ont pas été testés. L'application reste statique et hors ligne, sans compilation, backend ou authentification à migrer.

Les exigences initiales imposent une indication individuelle pour les modules vides ; leurs messages restent présents malgré leur répétition. Les 23 modules vides, 15 questions exclues des scores et 8 explications encore en anglais sont conservés et signalés comme avant. Les traductions ou réponses n'ont pas été modifiées pendant cette refonte visuelle.
