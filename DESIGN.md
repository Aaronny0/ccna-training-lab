# Direction — CCNA Training Lab

## Référence et audit

La référence retenue est le fichier fourni par l’utilisateur `CCNA_Training_Lab (1).html`. Sa direction remplace la précédente interface lumineuse : bleu nuit, barre latérale, bandeau d’accueil, accents bleus et cartes de modules arrondies. Les proportions et couleurs sont reprises ; les petites tailles de texte et le contraste des boutons sont améliorés.

L’ancienne interface ne suivait pas cette composition, privilégiait un tableau et présentait les modules vides avant les modules utilisables sur la page d’entrée. Le modèle fourni contient quatre modules et sa propre banque de questions : ces données ne remplacent pas la banque validée du projet.

## Composition retenue

Barre latérale limitée aux six destinations principales, sans liste de modules ni informations redondantes, de 265 px, réduite à 230 px sur petit ordinateur ; contenu principal plafonné à 1280 px avec marges de 22 à 66 px. Accueil : bandeau avec action d’examen mixte, trois statistiques réelles, grille de deux colonnes pour les 17 modules disponibles puis activité et révision. Catalogue dédié : recherche, filtres et 40 modules dans l’ordre prescrit. Quiz : question principale et navigation latérale de session. Résultats centrés, corrections, favoris, historique et paramètres utilisent les mêmes composants.

Sur tablette et smartphone, la navigation devient une barre horizontale accessible au clavier et au toucher ; sa sélection reste visible. Les modules sont accessibles depuis l’accueil et le catalogue. Les cartes passent à une colonne sous 590 px. Le bandeau garde le texte et l’action, son illustration de marque disparaît. La navigation des questions passe au-dessus de la question avec accès à la fin de session.

## Tokens

- Fond sombre `#090e1a`, barre latérale `#0e1626`, surface `#121c30`, bordure `#293750`.
- Texte `#f4f7ff`, secondaire `#a7b4cd`, accent `#7eb2ff` ; accents des modules cyan, violet, ambre et rose issus de la référence.
- Succès `#48d5a2`, erreur `#ff8fa2` ; les réponses utilisent aussi des icônes et libellés.
- Bouton principal : bleu `#2869d5` vers violet `#655dda`, texte blanc ; contraste minimal des extrémités 5,08:1.
- Police système locale, échelle 11–16 px pour libellés/texte, 18–28 px pour titres, 30–42 px pour l’accueil. Aucun téléchargement de police.
- Rayons : 10 px contrôles, 14–20 px panneaux, 22 px bandeau. Thème clair conservé et traité explicitement.

## Préservation

Le moteur, les identifiants, les règles, les fichiers de banque, les PDF et les images sont inchangés. La clé de sauvegarde et les anciens exports restent compatibles. EN/FR ne réordonne pas une session. L’illustration circulaire de marque est décorative, distincte des schémas PDF. Ces derniers restent blancs, complets, avec proportions originales et lien vers leur taille native ; aucune retouche ni reconstruction.

Le skill fourni `/home/aaron/Téléchargements/SKILL (1).md` est appliqué. Son annexe `references/visual-qa.md` n’a pas été fournie ni trouvée. La validation est documentée dans FRONTEND_REPORT.md : Chromium, parcours complets et cinq largeurs de 360 à 1440 px.
