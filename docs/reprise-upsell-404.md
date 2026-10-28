# Reprise depuis le connecteur Malfroid (état au 28/10)

Trois envois restent à faire dans Shopify. Notre connecteur ne répond plus depuis le 27/10 après-midi. Tout est prêt dans ce dépôt :

- **A.** Upsell du tiroir panier et page 404 sur la copie de thème 1.1.
- **B.** Titres et handles (adresses) anglais des produits, repris de l'ancien site WooCommerce.
- **C.** Redirections des anciennes adresses anglaises vers les nouveaux handles anglais.

Faire B avant C. A est indépendant.

Avant toute écriture, `{ shop { myshopifyDomain } }` doit renvoyer `malfroid-fr.myshopify.com`. Le connecteur se reconnecte parfois sur une autre boutique : dans ce cas, ne rien écrire.

## A. Upsell panier et page 404 sur la copie 1.1

Fichiers dans `theme/` (commit `639e4cb`).

1. **Vérifier la copie 1.1.** `themes(first:20) { nodes { id name role updatedAt } }` : « Malfroid x NFBS - 1.1 (validations 23/10) » doit être `UNPUBLISHED`.
   - Si elle a été publiée (rôle `MAIN`), ne rien écrire dessus. Dupliquer le thème publié (`themeDuplicate`, champ de retour `newTheme`) et travailler sur la nouvelle copie.
   - Si le `templates/404.json` du thème publié a changé depuis le 26/10 20:49, refaire la fusion : garder ses textes et ne changer que « SHOP ALL » en « TOUT VOIR ».
2. **Envoyer les 8 fichiers** avec `themeFilesUpsert(themeId, files)`. Chaque fichier a un corps de type `URL` :
   `https://raw.githubusercontent.com/xschreder/malfroid/639e4cb59ec890a834ca24edbb2681d5fcf65a39/theme/<fichier>`
3. **Relire les checksums** avec `theme.files(filenames:[…]) { nodes { filename checksumMd5 } }` :

   | Fichier | MD5 attendu |
   |---|---|
   | templates/404.json | `f7e75c5adaad0fe9df9735e60c78d913` |
   | templates/cart.json | `93cbf30bb7c61ef90c4e81d0dcdae1d3` |
   | snippets/cart-drawer-upsell.liquid | `8c6893b09edb88f7a23f03c689e0ad6e` |
   | assets/cart-drawer-upsell.js | `fa260e7ba3ceb070569a5f34b58a1cd9` |
   | snippets/header-actions.liquid | `9b841277ec01dcae4f6a6171bc41c0a3` |
   | config/settings_schema.json | `3f7cea85c2b4bbc7704b94c2a567e46c` |
   | locales/fr.json | `88cacccf771cc95c60255efa6aa0ae35` |
   | locales/en.default.json | `7e96c9bd680f617402a5b9f87cf5978f` |

   Shopify peut reformater les JSON : un MD5 différent sur un `.json` n'est pas forcément une erreur. Dans ce cas, relire le fichier et comparer son contenu, surtout `locales/fr.json`.
4. **Traductions anglaises de la 404.** Enregistrer avec `translationsRegister` sur la ressource `OnlineStoreTheme` de la copie, locale `en`. Récupérer d'abord les clés exactes et leurs digests avec `translatableResource`.

   | Bloc | Anglais |
   |---|---|
   | `text_Ua9XAW` | `<p>The link may be incorrect, or the page has been removed.</p>` |
   | `button_PAQMwR` | `Continue shopping` |
   | `product_list_text_BrfRNU` | `<h3>You may also like</h3>` |
   | `collection_link_button_x6FBXn` | `SHOP ALL` |

   « To go with your shoes » et « Add » sont déjà dans `locales/en.default.json` : rien à enregistrer.
5. **Contrôler.**
   - Page panier : la liste `product_list_fUKeNV` affiche la collection `accessoires-indispensables`, 4 produits au plus.
   - Paramètres du thème > Panier : l'upsell du tiroir est activé.
   - Sheet : passer Site n°35 en fait.

## B. Titres et handles anglais des produits

Source : `content/translations/titres-slugs-anglais-2026-10-28.json`, soit 150 produits. Le même contenu est en version lisible dans `content/translations/titres-slugs-anglais-2026-10-28.tsv`, avec le titre FR et l'état du titre anglais avant reprise.

Il donne, pour chaque produit, le nom et le slug de sa fiche anglaise sur l'ancien site. La correspondance entre fiche Shopify et fiche anglaise se fait par le SKU (131 produits) ou, à défaut, par le lien `hreflang` de la page FR (19 produits). Les 12 produits sans fiche anglaise ne sont pas touchés.

**Titres.** Ils remplacent tous les titres anglais actuels, sur décision Malfroid de préférer les textes de l'ancien site :

| Titre anglais actuel | Produits |
|---|---|
| Déjà repris le 23/10 | 64 |
| Repris le 23/10 avec des entités HTML restées dans le texte (`&rsquo;`, `&#8211;`, `&#038;`), corrigées ici | 5 |
| Corrigé à la main par Paul / Alex le 22/10, **remplacé** | 65 |
| Encore automatique, nom anglais identique au FR (Derby Defender…) | 15 |
| Bottine Explorer II, non reprise le 23/10 | 1 |

Les 65 titres corrigés à la main sont à parcourir avec Alexandre dans le TSV avant l'envoi. Pour en garder un, retirer la ligne du JSON.

**Handles.** Clé de traduction `handle`, ce qui donne des adresses `/en/products/<slug WooCommerce>`. Aucun doublon, aucun conflit avec un handle FR. Au 23/10, aucun produit n'avait de handle anglais. Quelques slugs gardent les fautes de l'ancien site ; les reprendre tels quels assure la continuité, les corriger reste possible dans le JSON avant l'envoi :

- `cart-holder-*` (3 porte-cartes) ;
- `boots-berriere-ii-chcolate-brown` ;
- `richelieu-astoria-black-grained-calf-form-361-copy` ;
- `mercerised-cotton-socks-black` (chaussettes grises) ;
- `derby-explorer-ii-low-2-2`.

Étapes :

1. **Sauvegarde et digests.** La liste des `id` est dans le JSON. Lancer en 3 appels de 50 identifiants :

   ```graphql
   query($ids: [ID!]!) {
     translatableResourcesByIds(resourceIds: $ids, first: 50) {
       nodes { resourceId translatableContent { key digest } translations(locale: "en") { key value } }
     }
   }
   ```

   Enregistrer les 3 réponses dans `content/translations/sauvegarde-en-avant-reprise.json`, une liste de réponses. Committer ce fichier : c'est la sauvegarde pour revenir en arrière.
2. **Préparer les lots.** `python3 scripts/anglais/lots.py traductions content/translations/sauvegarde-en-avant-reprise.json /tmp/lots`
   On obtient 6 lots de 25 `translationsRegister` (titre + handle). Le script signale les produits sans digest, par exemple un produit supprimé depuis.
3. **Envoyer** chaque lot avec `graphql_mutation`, `query` et `variables` tels quels. Chaque `userErrors` doit être vide.
4. **Vérifier.** Relancer la requête de l'étape 1 et enregistrer les réponses, puis lancer `python3 scripts/anglais/lots.py verifier <réponses>`. Le résultat attendu est « 150 produits relus, 0 écart ».

Sans terminal, on peut construire les mutations à la main sur le même modèle : `translationsRegister(resourceId, translations: [{key:"title"…}, {key:"handle"…}])` avec `locale: "en"` et le digest de chaque clé.

## C. Redirections vers les handles anglais

Le plan `content/redirections/redirections-301-2026-10-26.csv` est déjà à jour dans le dépôt. Les 150 redirections de fiches produit anglaises pointent maintenant vers `/en/products/<handle anglais>` au lieu de `/en/products/<handle FR>`. Il reste à faire la même chose dans Shopify, où les 1 085 redirections existent déjà.

1. **Lire toutes les redirections** (5 pages de 250) et enregistrer les réponses en une liste :

   ```graphql
   query($c: String) {
     urlRedirects(first: 250, after: $c) { nodes { id path target } pageInfo { hasNextPage endCursor } }
   }
   ```

2. **Préparer les lots.** `python3 scripts/anglais/lots.py redirections <réponses> /tmp/lots`
   On obtient 3 lots de 60 `urlRedirectUpdate`, pour les 150 redirections plus les éventuels doublons sans préfixe `/en/`.
3. **Envoyer** chaque lot. Chaque `userErrors` doit être vide.
4. **Relire** et vérifier qu'il ne reste aucune cible `/en/products/<handle FR>`, par exemple `/en/products/mocassin-newport-3`.
5. **Envoyer à Arnaud** le CSV à jour.

Le jour de la mise en ligne, une fois le domaine branché, ouvrir en navigation privée :

| Adresse | Résultat attendu |
|---|---|
| `/en/shop/loafers/round-loafers/penny-loafer-newport-3/` | la fiche anglaise `/en/products/penny-loafer-newport-3` |
| `/en/products/mocassin-newport-3` (ancien handle sous `/en/`) | Shopify doit renvoyer vers le handle anglais ; sinon, le signaler |

## Après les envois

- Sheet : Site n°35 (upsell) et Site n°38 (multilingue) à mettre à jour.
- README : section « Traductions anglaises reprises » à compléter avec les titres et handles.
