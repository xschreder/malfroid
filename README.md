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

### Contenu différent par produit (métachamps)

Par défaut, le contenu saisi dans l'éditeur est le même pour tous les produits du template.
Neuf définitions de métachamps produit ont été créées (espace de noms `content`, épinglées sur
la fiche produit dans l'admin) :

| Section | Image (fichier image) | Titre (texte) | Texte (texte enrichi) |
| --- | --- | --- | --- |
| Description — Modèle | `content.modele_image` | `content.modele_titre` | `content.modele_texte` |
| Description — Cuir | `content.cuir_image` | `content.cuir_titre` | `content.cuir_texte` |
| Description — Semelle | `content.semelle_image` | `content.semelle_titre` | `content.semelle_texte` |
| Détails (libre, par produit) | `content.details_image` | `content.details_titre` | `content.details_texte` |

Pour les brancher :

1. Dans l'admin, sur chaque produit, remplir les champs « Modèle — Image », « Modèle — Titre »,
   « Modèle — Texte », etc. (section Métachamps en bas de la fiche produit).
2. Dans l'éditeur de thème, sur chaque section, cliquer l'icône **Connecter une source dynamique**
   (petit cylindre) à côté de Image, Titre et Texte, puis choisir le métachamp correspondant.
   À faire une seule fois : le branchement est enregistré dans le template et vaut pour tous les produits.

La section est masquée automatiquement sur la boutique si l'image, le titre et le texte sont vides,
donc un produit sans métachamps renseignés n'affiche pas de bloc vide.

### Guide d'entretien (5000 caractères)

Le champ standard Shopify `descriptors.care_guide` (« Guide d'entretien ») est limité à 500 caractères
et cette limite n'est pas modifiable. Il a été remplacé par le champ personnalisé
`content.guide_entretien` (« Guide d'entretien (5000 car.) », texte multiligne, 5000 caractères max.,
épinglé sur la fiche produit). L'ancien champ reste en place mais n'est plus épinglé. Si un bloc du
thème pointait vers l'ancien champ, le rebrancher sur `content.guide_entretien` via la source dynamique.

## Pages « La cordonnerie du Bon Marché » et « Films » (brief DA du 13/10/2026)

Montées sur le thème brouillon **« Malfroid x NFBS - 1.0 + cordonnerie & films »** (copie du thème publié).
Templates versionnés dans `templates/` :

| Fichier | Rôle |
| --- | --- |
| `templates/page.la-cordonnerie-du-bon-marche.json` | Page Cordonnerie : hero pleine largeur, titre + sous-titre (bloc Rich text MTO), 4 blocs « Editorial image » en 2 × 2, logo Le Bon Marché centré, adresse centrée |
| `templates/page.mto.json` | Page MTO sans les blocs situés sous le bouton « Je veux mon modèle » |
| `templates/blog.films.json` | Sommaire du blog Films (format Les Portraits, titre seul) |
| `templates/article.film.json` | Article Film : titre « FILMS » centré, titre du film en navy, vidéo YouTube pleine largeur |

Contenus créés dans Shopify : page `la-cordonnerie-du-bon-marche` (template `la-cordonnerie-du-bon-marche`),
blog `films` (template `films`), fichier `le-bon-marche-rive-gauche-logo.png` (225 px, à remplacer par un HD).
Les articles du blog Films se créent avec le suffixe de template `film` et un iframe YouTube dans le corps.

Thème publié le 13/10/2026. Les entrées de menu « La cordonnerie du Bon Marché par Malfroid » (Services → Entretien)
et « Films » (Notre univers) pointent vers la page et le blog.

Blog Films alimenté le 15/10/2026 avec les 5 vidéos de la chaîne YouTube « Malfroid Shoes »
(chaîne `UCy-b_k_74eLJX9v8btEdKUw`), un article par vidéo (template `film`, vignette YouTube, date = date de la vidéo).

## Nettoyage du catalogue en masse (16/10/2026)

Script `scripts/catalogue/process.py` : à partir d'un export `bulkOperationRunQuery` (JSONL produits + médias,
avec `descriptionHtml`, `seo { title }`, le métachamp `content.colorReference` et les médias), il produit
`product_updates.jsonl` (entrées `productUpdate`) et `file_updates.jsonl` (entrées `fileUpdate`).
Le connecteur Shopify bloquant `bulkOperationRunMutation`, les fichiers ont été envoyés en mutations
groupées par alias (15 produits ou 100 images par appel).

Résultat appliqué sur la boutique :

| Chantier | Volume | Règle |
| --- | --- | --- |
| Descriptions (Technique n°2) | 100 fiches | Suppression des mentions « Permanent / Limited / Édition limitée / Collection permanente » alignées à droite, des boutons « Lire Plus / Lire Moins » (`wpsm-*`, `show_more`) et des `<div>` orphelins WordPress ; texte inchangé |
| Titres SEO (Technique n°13) | 116 fiches | `Titre – Coloris` quand plusieurs fiches partagent le même titre et qu'aucun titre SEO n'existait |
| Textes alternatifs (Technique n°14) | 874 images | `Titre – Coloris`, ou titre seul sans coloris ; les images ayant déjà un alt n'ont pas été touchées |
| Filtres (Site n°24) | 2 valeurs | Métaobjets `collection_filters` : Seasonal → Saisonnier, Special series → Série spéciale |

Limites connues : la fiche « Mocassin Newport Superleggera – Veau velours chocolat » garde sa mention
« Limited » (paragraphe avec attribut `dir="ltr"`, non reconnu par l'expression régulière) ; à retirer à la main si souhaité.

## Marchés et prix export (19/10/2026)

Reco appliquée : France + UE au même prix TTC, et un marché **Export** (hors UE) avec
prix plus élevé pour absorber frais de port, douane et SAV à distance.

### Ce qui est en ligne

- Profil de livraison général, zone UE : tarif « Standard Europe » passé à **25 €**
  (France inchangée).

### Ce qui est préparé mais **non activé** (statut Brouillon)

| Objet Shopify | Valeur |
|---|---|
| Marché `Export` (ex-INTER) | GB, CH, US, CA, JP, AU, SG, HK, statut **DRAFT** |
| Catalogue « Export » | lié au marché Export |
| Liste de prix « Export » | EUR, ajustement parent **+5 %**, prix barrés neutralisés |
| Publication du catalogue | vide par défaut, **chaussures uniquement** (111 produits actifs, hors accessoires / entretien / services / carte cadeau) |
| Prix fixes par variante | `arrondi(prix_FR_TTC × 1,05 / 5) × 5` (≈ HT + 25 %), posés le 20/10 sur les 1 542 variantes des 111 chaussures, suppléments de pointure conservés ; table complète dans `content/markets/prix-export-2026-10-20.tsv` |

Activation : Shopify admin > Paramètres > Marchés > Export > **Activer**. Avant d'activer,
décider du pourcentage export définitif (5 % TTC arrondi est une base, La Botte Gardiane
était plus haut) et vérifier l'affichage droits/taxes (Marchés > Export > Droits et taxes).

Pour changer le pourcentage : les prix fixes priment sur l'ajustement +5 % de la liste ; il faut les recalculer et les reposer (`priceListFixedPricesByProductUpdate` pour les 62 produits à prix unique, `priceListFixedPricesAdd` pour les 49 produits avec supplément de pointure).

Limites : les mutations `priceListFixedPricesAdd` acceptent 250 variantes par appel ;
`publishablePublish` est envoyé par lots de 37 produits (coût API max 1000 par requête).

## Thème « Malfroid x NFBS - 1.1 (validations 23/10) »

Copie du thème publié (« 1.0 + cordonnerie & films ») créée le 23/10/2026 par l'API pour
regrouper les corrections validées, l'API interdisant l'écriture sur le thème publié.
Elle hérite des traductions Translate & Adapt du thème publié (272 textes de thème traduits par
Malfroid les 21-23/10, vérifié) ; les 172 textes traduits par NF-BS le 19/10 sur la copie
« + langue » y sont tous déjà couverts.

| Fichier | Origine | Point de recette |
|---|---|---|
| `blocks/video.liquid` | ce dépôt | Site n° 2 : vidéo mobile distincte dans le bloc vidéo |
| `layout/theme.liquid` | copie « + langue » | Site n° 5 : logo et icônes noirs sur l'en-tête transparent mobile ; largeur des pages politiques |
| `snippets/localization-form.liquid` | copie « + langue » | Site n° 26 / 38 : sélecteur de langue FR / EN |
| `sections/header-group.json` | copie « + langue » | Site n° 4 : en-tête non transparent sur fiches produit et collections |
| `config/settings_data.json` (5 valeurs) | copie « + langue » | Logo sombre par défaut, logo blanc en inverse (va avec l'en-tête non transparent) ; bouton principal : contour navy sur le schéma 1, fond navy sur le schéma 2 (Site n° 9). Le reste des réglages est celui du thème publié. |

Non repris de « + langue » : `locales/en.default.json` (la version du thème publié contient des
clés checkout plus récentes) et `templates/index.json` / `templates/product.json` (le thème
publié a évolué depuis la copie, ses versions font foi).

Mise en ligne : Boutique en ligne > Thèmes > « 1.1 (validations 23/10) » > Aperçu sur mobile,
puis Publier. Les réglages faits entre-temps dans l'éditeur du thème publié ne sont pas dans la
copie : refaire la copie juste avant publication si des réglages ont changé.

## Traductions anglaises reprises de l'ancien site (23/10/2026)

Décision Malfroid du 23/10 : préférer les textes anglais rédigés de l'ancien site WooCommerce
(malfroid.com/en) à la traduction automatique Translate & Adapt du 13/10.

Source : API publique WooCommerce Store (`/wp-json/wc/store/v1/products`, 396 fiches dont
209 en anglais), sans export ni Matrixify. Correspondance Shopify ↔ ancien site par le
handle (= slug WooCommerce FR), puis FR ↔ EN par le SKU ou, à défaut, par le lien
`hreflang="en"` de la page FR. L'import n'a été fait que pour les fiches dont le texte FR
actuel de Shopify est encore celui de l'ancien site (similarité ≥ 85 %).

| Champ Shopify (locale en) | Source WooCommerce EN | Volume |
|---|---|---|
| Description produit (`body_html`) | texte éditorial (`short_description`), nettoyé des balises WordPress comme en FR | 148 |
| Titre (`title`) | nom EN, seulement si le titre EN était encore automatique ; les 65 titres corrigés à la main le 22/10 sont conservés | 69 |
| Métachamp `content.description` (fiche technique) | `description`, si la valeur FR correspond encore à l'ancien site | 130 |

Non repris : 12 produits sans fiche anglaise (services cordonnerie, ceintures Junot, chaussettes,
porte-clés, carte cadeau, Defender City II, Vauban copie, Newport Superleggera à patiner), la
Bottine Explorer II (texte FR réécrit) et 5 fiches techniques vides ou réécrites.
Table de contrôle : `content/translations/import-anglais-2026-10-23.tsv`.

Reste à traduire à la main dans Translate & Adapt : les compléments FR ajoutés par Paul après
l'ancien site (blocs « Caractéristiques techniques » et « Le mot du chausseur » sur quelques
fiches), visibles comme traductions « obsolètes » si le FR change à nouveau.

## Thème 1.1 — corrections du 26/10

Appliquées sur la copie **« Malfroid x NFBS - 1.1 (validations 23/10) »** (non publiée), fichiers
dans `theme/`. Envoi par l'API depuis l'URL brute GitHub du commit, checksums relus identiques.

| Point de recette | Fichier | Changement |
|---|---|---|
| Resynchro thème publié | `locales/en.default.json`, `templates/cart.json` | Reprise des modifications faites sur le thème publié après la copie (clés checkout Shopify du 23/10, « À découvrir également » et réglages du 26/10 sur le panier) |
| Site n°23, textes anglais | `templates/cart.json` | « Cart » → « Panier », « View all » → « Tout voir » |
| Site n°23 | `templates/404.json` | « Page not found » → « Page introuvable », « Discover something new » → « À découvrir », « SHOP ALL » → « TOUT VOIR » |
| Site n°23 | `templates/product.json`, `templates/product.entretien-et-cordo.json` | Libellés « Read more / Read less » restants → « Lire plus / Lire moins » |
| Site n°23 | traductions du thème | Valeurs anglaises réenregistrées pour ces 20 textes (Cart, View all, Page not found, Read more…) afin que /en/ reste en anglais |
| Site n°29 / 42 | `templates/page.json` | Suppression du bloc « Select the preferred style below and follow the measuring guide. » du gabarit de page générique |
| Site n°50 | `snippets/variant-main-picker.liquid` | L'option « Pointure » est traduite « Shoe size » en anglais : ajout de ce nom pour garder le titre et le sélecteur UK / EU / US |
| Site n°19 | `snippets/color-swatches.liquid` | Infobulle et libellé accessible des pastilles = nom du coloris (métaobjet `color_name`), titre produit en repli |
| Site n°20 | `blocks/email-signup.liquid` | Message « Merci de vous être abonné(e) » affiché aussi au retour `?customer_posted=true`, en filet de sécurité |
| Site n°47 | `blocks/_product-tab-item.liquid`, `templates/product.json` | Nouveau réglage « Masquer l'onglet si le métachamp Fit est vide », activé sur l'onglet Fit ; lien du guide corrigé vers `/pages/guide-de-pointures` |
| Site n°51 | `templates/cart.json` | Récapitulatif de la page panier : le jeu de couleurs inexistant (boutons noirs par défaut) est remplacé par l'héritage du jeu de la page, comme le panier tiroir |
| NF3 | `assets/size-conversions.json` | Rien à faire : la ligne UK 4,5 est déjà présente sur le thème publié et la copie |
| NF5 | contenu de l'article | Rien à faire dans le thème : l'extrait du portrait Thierry Bigaignon contient déjà le saut de ligne |

Cirage, porte-cartes et autres produits d'entretien ou accessoires utilisent des gabarits sans
onglet Fit ; le masquage concerne les produits du gabarit par défaut sans Fit (gants, collection
femme).
