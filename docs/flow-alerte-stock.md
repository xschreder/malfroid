# Alerte retour en stock — Shopify Flow + Shopify Inbox

Objectif : quand un produit épuisé revient en stock, prévenir **la boutique** (pour préparer la
mise en avant) et **le client** qui a demandé à être averti. Aucune application payante.

## Briques Shopify utilisées

| Brique | Rôle |
|---|---|
| Shopify Flow (gratuit) | Déclencheur « Quantité d'inventaire modifiée », conditions, actions e-mail / Inbox |
| Shopify Inbox (ex-Messaging) | Boîte de réception boutique ; reçoit la notification interne et sert à répondre au client |
| Formulaire « Me prévenir » (Shopify Forms ou bloc thème) | Capture l'e-mail du client + le produit demandé, pose un tag client `restock:<handle>` |
| Shopify Email (gratuit jusqu'à 10 000 envois/mois) | Envoi au client |

## Flux 1 — alerte boutique

1. **Déclencheur** : `Inventory quantity changed`.
2. **Condition** : `inventoryLevel.quantityBefore <= 0` **et** `inventoryLevel.quantityAfter > 0`
   **et** `product.status = active`.
3. **Action** : `Send internal email` à contact@malfroid.com (ou l'adresse boutique Ternes) avec
   `{{ product.title }}`, `{{ productVariant.title }}`, `{{ inventoryLevel.location.name }}`,
   `{{ inventoryLevel.quantityAfter }}`.
4. **Action** (facultatif) : `Send Shopify Inbox message` vers la boîte boutique pour qu'un
   conseiller puisse relancer les clients ayant demandé le modèle.

## Flux 2 — alerte client

Pré-requis : le formulaire « Me prévenir » ajoute au client le tag `restock:<handle-produit>`
(Shopify Forms permet une action « Ajouter un tag » à la soumission ; le handle se passe en champ
caché depuis la fiche produit).

1. **Déclencheur** : `Inventory quantity changed` (même condition que le flux 1).
2. **Action** : `Get customer data` avec la requête `tag:restock:{{ product.handle }}`.
3. **Boucle** `For each customer` :
   - **Action** : `Send marketing email` (Shopify Email, modèle « Retour en stock ») avec lien
     vers `{{ product.onlineStoreUrl }}` ;
   - **Action** : `Remove customer tags` → `restock:{{ product.handle }}`.
4. Le client n'est contacté qu'une fois ; s'il se réinscrit, le tag revient.

Limite : `Send marketing email` exige le consentement marketing du client. Le formulaire doit donc
cocher « J'accepte de recevoir des e-mails » ou, à défaut, utiliser `Send internal email` vers la
boutique qui répond via Inbox.

## Mise en place

1. Installer Shopify Flow et Shopify Inbox (gratuits) depuis l'App Store Shopify.
2. Créer le formulaire « Me prévenir du retour en stock » dans Shopify Forms (champ e-mail,
   champ caché `product_handle`, action « Ajouter un tag » `restock:{{ product_handle }}`).
3. Placer le bloc formulaire sur la fiche produit, visible uniquement si la variante est épuisée
   (bloc conditionnel du thème ou code `{% unless product.available %}`).
4. Créer les deux flux ci-dessus dans Flow, les tester sur un produit avec un stock passé de 0 à 1.
5. Quand Klaviyo sera branché (Site n° 15), le flux 2 peut être remplacé par le flux Klaviyo
   « Back in stock » natif ; le flux 1 reste utile pour la boutique.
