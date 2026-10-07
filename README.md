# Malfroid — sections Shopify personnalisées

Thème : **Malfroid x NFBS** (base Shopify « Horizon »).

## Sections « Description produit » (image + encart texte)

Trois sections indépendantes, à ajouter sur le template produit depuis l'éditeur de thème :

| Fichier | Nom dans l'éditeur | Usage |
| --- | --- | --- |
| `sections/product-description-model.liquid` | Description — Modèle | Présenter le modèle |
| `sections/product-description-leather.liquid` | Description — Cuir | Présenter le cuir |
| `sections/product-description-sole.liquid` | Description — Semelle | Présenter la semelle |

Les trois sections partagent exactement le même code et les mêmes réglages ; seuls le nom et les
textes par défaut diffèrent. Elles reprennent le rendu de la section « Product Story » existante
(image en colonne, encart texte semi-transparent en superposition, texte empilé sous l'image sur mobile).

### Réglages disponibles

- **Contenu** : image, titre (avec choix de la balise H2/H3/H4/P), texte riche (gras, italique,
  liens, listes, paragraphes).
- **Mise en page** : image à gauche ou à droite, mode colonne ou pleine largeur, largeur de la
  colonne image (35 % à 80 %), hauteur de la rangée (40 % à 100 % de l'écran).
- **Image** : couvrir / contenir, point de focus (9 positions), ratio sur mobile.
- **Encart texte — position** : horizontal (gauche / centre / droite), vertical (haut / centre / bas),
  décalage horizontal et vertical depuis le bord, largeur de l'encart.
- **Encart texte — apparence** : couleur de fond, **opacité** (ordinateur), opacité sur mobile,
  flou d'arrière-plan (verre dépoli), marges internes, arrondi des angles.
- **Typographie du titre** : police, taille, graisse, style, casse, espacement des lettres,
  espace sous le titre, couleur.
- **Typographie du texte** : police, taille, graisse, interligne, couleur.
- **Section** : jeu de couleurs, marges haut / bas.

### État de l'installation

Les 3 sections sont installées sur le thème **« Malfroid x NFBS - 1.0 + sections description »**
(copie du thème publié « Malfroid x NFBS - 1.0 (fix pointure 4,5) », créée le 7 octobre 2026).
L'API Shopify interdit l'écriture directe sur le thème publié : pour mettre en ligne, soit publier
cette copie, soit recopier les 3 fichiers dans le thème publié (voir ci-dessous).

### Installation manuelle (2 minutes)

1. Shopify admin → **Boutique en ligne → Thèmes** → sur le thème voulu, **… → Modifier le code**.
2. Dans le dossier **sections**, cliquer **Ajouter une nouvelle section**, choisir le type
   *liquid*, nommer `product-description-model`, puis coller le contenu du fichier
   `sections/product-description-model.liquid`. Enregistrer.
3. Répéter pour `product-description-leather` et `product-description-sole`.
4. Ouvrir **Personnaliser** → page **Produit par défaut** → **Ajouter une section** → onglet
   *Produit* → « Description — Modèle », « Description — Cuir », « Description — Semelle ».
5. Glisser les sections à l'endroit souhaité (par ex. sous « Informations sur le produit ») et
   remplir image + texte.

> Le snippet `snippets/spacing-style.liquid` est déjà présent dans le thème ; aucun autre fichier
> n'est nécessaire.

### Contenu différent par produit

Par défaut, le contenu saisi dans l'éditeur est le même pour tous les produits du template.
Pour un texte / une image propre à chaque produit :

1. Créer des métachamps produit (Paramètres → Données personnalisées → Produits), par exemple
   `custom.modele_image` (fichier), `custom.modele_titre` (texte) et `custom.modele_texte`
   (texte enrichi) — et de même pour le cuir et la semelle.
2. Dans l'éditeur de thème, sur chaque réglage Image / Titre / Texte, cliquer l'icône
   **Connecter une source dynamique** et choisir le métachamp correspondant.

La section est masquée automatiquement sur la boutique si l'image, le titre et le texte sont vides.
