# Ajouter un nouveau PDF sans modifier l’application

1. Copier le PDF réellement reçu dans `sources/`. Ne pas utiliser un nom de capture d’écran comme preuve d’accès.
2. Lire le titre, toutes les questions, les choix, les marques de correction et les explications. Comparer avec le catalogue dans `scripts/catalog.cjs` pour sélectionner l’ID existant. Les suffixes 2 et 3 ne doivent pas être fusionnés.
3. Relever le SHA-256 (`sha256sum sources/nom.pdf`). Transcrire l’anglais fidèlement. Les scripts d’extraction sont des aides et ne remplacent pas la relecture.
4. Extraire les figures originales sans les redessiner, avec toutes les étiquettes et marges. Ne jamais modifier l’ordre spatial des équipements ou les connexions. Conserver une référence à la page d’origine et une empreinte de pixels dans `data/topologies.json`.
5. Créer un pack JSON au schéma 1. Conserver des IDs permanents de questions, choix et cibles. Vérifier le nombre de bonnes réponses et leur cohérence technique. Si une source est ambiguë, utiliser `verified: false` et renseigner `issue.en` / `issue.fr`.
6. Ajouter les traductions avant publication. Comparer sens, négations, quantificateurs, nombres et nombre de choix attendu. Ne pas traduire les commandes, configurations, adresses ou interfaces. Utiliser `partial` ou `pending` si la vérification n’est pas finie ; laisser le champ FR incertain absent.
7. Importer puis vérifier. Les autres modules et leurs résultats restent inchangés.

## Exemple de structure (à remplir depuis une vraie source)

```json
{
  "schemaVersion": 1,
  "questions": [
    {
      "id": "ccna-03-nouvelle-source-q001",
      "module": "ccna-03",
      "type": "choice",
      "prompt": {"en": "TEXTE ORIGINAL", "fr": "TRADUCTION VÉRIFIÉE"},
      "options": [
        {"id": "a", "text": {"en": "CHOIX ORIGINAL", "fr": "CHOIX TRADUIT"}},
        {"id": "b", "text": {"en": "AUTRE CHOIX", "fr": "AUTRE CHOIX TRADUIT"}}
      ],
      "answers": ["b"],
      "required": 1,
      "explanation": {"en": "EXPLICATION SOURCE", "fr": "EXPLICATION TRADUITE"},
      "images": [],
      "verified": true,
      "translationStatus": "validated",
      "source": {
        "file": "nom.pdf",
        "sha256": "REMPLACER PAR 64 CARACTÈRES HEXADÉCIMAUX",
        "question": 1,
        "page": 1
      }
    }
  ]
}
```

Il s’agit d’un schéma documentaire, pas d’une question à importer. Un pack conforme complet et réel peut être obtenu en sélectionnant des objets dans `data/questions.json`.

Pour une association : `type: "match"`, options à IDs permanents, tableau `targets: [{id, text: {en, fr}}]`, `solution: {"t1": "o3", "t2": "o1"}`, `required` égal au nombre de cibles et `answers: []`. Les catégories peuvent être réutilisées. Le moteur n’évalue pas l’ordre d’une catégorie : il compare les associations exactes par ID.

## Import permanent dans le dossier

```bash
node scripts/import.cjs /chemin/pack-verifie.json
node --test tests/core.test.cjs
```

L’import valide le module, les IDs, les traductions annoncées complètes, le SHA du vrai PDF dans `sources/` et l’existence des images. Il met à jour `data/questions.json`, puis génère `data/bank.js`. La plateforme fonctionne ensuite immédiatement, sans modifier le moteur. Pour une nouvelle figure, lancer aussi le contrôle de pixels avant de valider sa provenance dans le manifeste.

## Import depuis l’interface

Paramètres → Importer une banque de questions validée. Le pack est fusionné et persisté dans ce navigateur. Les compteurs et le statut du module sont immédiatement actualisés. Les images et PDF référencés doivent déjà exister dans le dossier de l’application ; le navigateur n’installe pas automatiquement ces fichiers. La validation de l’interface vérifie le schéma, mais la relecture et le contrôle des empreintes de PDF doivent avoir été réalisés avant l’import. Pour partager le contenu entre appareils, préférez l’import permanent et recopiez tout le dossier.

## PDF anglais téléchargeable par module

Chaque module disposant d’énoncés et de réponses source complets possède un PDF unique dans `assets/pdf/ccna-XX.pdf`. Il contient toutes ses questions dans l’ordre source, chaque correction immédiatement après la question, puis l’explication lorsqu’elle existe. Les consignes, choix, associations, commandes et images restent en anglais, quelle que soit la langue du site. Les questions hors score sont également conservées dans ces documents. Aucun PDF n’est créé pour un module vide ou incomplet.

Après un ajout ou une correction permanente du contenu, régénérer les PDF puis la banque :

```bash
python3 scripts/generate-module-pdfs.py
node scripts/build.cjs
python3 tests/module-pdfs.py
```

Le script Python nécessite ReportLab, Pillow et PyMuPDF. Le runtime Python fourni par Codex contient ces dépendances. `data/module-pdfs.json` référence les fichiers, leurs empreintes et l’ordre des questions. Le build n’expose pas de liens vers des PDF obsolètes. Les imports effectués uniquement dans un navigateur restent fonctionnels ; un module modifié localement masque son ancien lien tant que son PDF n’a pas été régénéré dans le dossier partagé.

Le contrôle navigateur `node tests/module-pdf-browser.cjs` utilise le serveur local sur le port 8765. Il vérifie les téléchargements natifs en anglais sur ordinateur, en français au format mobile, ainsi que le téléchargement hors ligne par `file://`.

## Doublons et corrections de contenu

Un réimport identique est ignoré. Les empreintes module + SHA PDF + numéro de question et les énoncés déjà présents empêchent une duplication même sous un nouvel ID. Un ID existant avec un contenu différent provoque un conflit explicite : traiter une correction de source comme une révision documentée, jamais comme une suppression silencieuse de progrès.

## Reconstruction des sources initiales

Les scripts Python nécessitent PyMuPDF et Pillow. `scripts/ocr.py` est une aide de reconnaissance pour les quatre PDF scannés ; ses chemins décrivent le runtime OCR local utilisé pendant la création. Les originaux et les sorties OCR intégrales sont conservés dans `sources/extracted/` pour la vérification ultérieure. Ne relancer le pipeline d’extraction initial que pour reconstruire ces documents : pour enrichir la banque, utiliser l’import de packs afin de conserver les ajouts.
