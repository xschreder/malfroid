# Reprise : upsell panier + page 404 sur la copie 1.1

État au 27/10 : les fichiers sont prêts dans `theme/` (commit `639e4cb`) mais **rien n'est encore écrit sur la copie 1.1**. Le connecteur Shopify s'est déconnecté avant l'envoi.

## Étapes

1. **Vérifier la boutique.** `{ shop { myshopifyDomain } }` doit renvoyer `malfroid-fr.myshopify.com`. Le connecteur se reconnecte parfois sur WEINSANTO ou Mister k. : ne rien écrire dans ce cas.
2. **Vérifier la copie 1.1.** `themes(first:20) { nodes { id name role updatedAt } }`. Elle doit être `UNPUBLISHED`.
   - Si elle a été publiée (rôle `MAIN`), ne rien écrire dessus : dupliquer le thème en ligne (`themeDuplicate`, champ de retour `newTheme`) et appliquer les fichiers sur la nouvelle copie.
   - Si le `templates/404.json` du thème en ligne a changé depuis le 26/10 20:49, refaire la fusion : garder ses textes et ne changer que « SHOP ALL » en « TOUT VOIR ».
3. **Envoyer les 8 fichiers.** `themeFilesUpsert(themeId, files)`. Chaque fichier a un corps de type `URL` qui pointe vers
   `https://raw.githubusercontent.com/xschreder/malfroid/639e4cb59ec890a834ca24edbb2681d5fcf65a39/theme/<fichier>`.
4. **Relire les checksums** (`theme.files(filenames:[…]) { nodes { filename checksumMd5 } }`) :

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

   Shopify peut reformater les JSON, donc un MD5 différent sur un `.json` n'est pas forcément une erreur. Dans ce cas, relire le fichier et comparer son contenu, surtout `locales/fr.json`.
5. **Traductions anglaises de la 404.** `translationsRegister` sur la ressource `OnlineStoreTheme` de la copie, locale `en`. Récupérer d'abord les clés exactes et leurs digests avec `translatableResource`.

   | Bloc | Anglais |
   |---|---|
   | `text_Ua9XAW` | `<p>The link may be incorrect, or the page has been removed.</p>` |
   | `button_PAQMwR` | `Continue shopping` |
   | `product_list_text_BrfRNU` | `<h3>You may also like</h3>` |
   | `collection_link_button_x6FBXn` | `SHOP ALL` |

   « To go with your shoes » et « Add » sont déjà dans `locales/en.default.json` (`cart_upsell_title`, `cart_upsell_add`) : rien à enregistrer.
6. **Contrôler.**
   - Sur la page panier, la liste `product_list_fUKeNV` pointe sur `accessoires-indispensables` avec 4 produits au plus.
   - Dans les réglages du thème, rubrique Panier, l'upsell du tiroir est activé sur la même collection.
7. **Sheet.** Passer la ligne Site n°35 (upsell) en fait.
