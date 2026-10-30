# Bascule : WooCommerce sur old.malfroid.com, Shopify sur malfroid.com

Objectif : le jour de la migration, malfroid.com et www.malfroid.com pointent sur Shopify, et
l'ancien site WooCommerce reste consultable (admin, commandes, clients) sur **old.malfroid.com**,
protégé et non indexé.

## État relevé le 30/10/2026

| Élément | Valeur actuelle | Le jour J |
|---|---|---|
| Serveurs DNS | Ionos (`ns1016.ui-dns.biz`, `ns1029.ui-dns.de`, `ns1041.ui-dns.org`, `ns1045.ui-dns.com`) | inchangés : tout se règle dans Ionos |
| `malfroid.com` A | `217.160.0.92` (hébergement Ionos, Apache, PHP 8.1) | → Shopify |
| `malfroid.com` AAAA | `2001:8d8:100f:f000::26b` (Ionos) | **à supprimer** |
| `www.malfroid.com` A / AAAA | mêmes valeurs | → CNAME Shopify, AAAA **à supprimer** |
| MX | `mx00.ionos.fr`, `mx01.ionos.fr` | **ne pas toucher** (boîtes mail Ionos) |
| TXT | SPF `v=spf1 include:_spf-eu.ionos.com ~all`, vérification Facebook | à conserver |
| `_dmarc` | `v=DMARC1; p=none;` | à conserver |
| `old.malfroid.com` | n'existe pas encore | à créer, pointe sur l'hébergement Ionos |

Point de vigilance n°1 : les enregistrements **AAAA (IPv6)**. Si on change seulement le A, les
visiteurs en IPv6 (une grande partie des mobiles) continueront d'arriver sur l'ancien site Ionos.

## 1. Préparation (J-3 à J-1)

1. **Sauvegardes**, gardées hors Ionos :
   - base de données WordPress : Ionos > Hébergement > Bases de données > phpMyAdmin > Exporter (SQL complet) ;
   - fichiers du site (dossier de l'espace web, en SFTP), surtout `wp-content/uploads` et `wp-config.php` ;
   - exports WooCommerce : commandes, clients, produits (CSV), pour l'import Shopify et l'archive.
2. **Baisser la durée de vie (TTL)** des enregistrements `@` et `www` au plus bas proposé par Ionos,
   pour que la bascule se propage vite (à faire au moins 24 h avant).
3. **Créer le sous-domaine** `old.malfroid.com` dans Ionos (Domaines & SSL > malfroid.com >
   Sous-domaines > Créer), rattaché à l'**espace web, même dossier que le site actuel**.
   Tant que WordPress n'est pas modifié, old.malfroid.com renverra vers malfroid.com : c'est normal.
4. **Certificat SSL** pour `old.malfroid.com` : l'activer dans Ionos (certificat inclus dans
   l'hébergement) et vérifier qu'il est actif avant le jour J.
5. **Côté Shopify** : Paramètres > Domaines > Connecter un domaine existant > `malfroid.com`.
   Shopify affiche les valeurs à poser chez Ionos (en principe A `23.227.38.65` et CNAME `www` →
   `shops.myshopify.com` ; reprendre celles affichées par Shopify).
6. **Inventaire des branchements de WooCommerce** à couper le jour J (voir étape 2.3) : paiements
   (Stripe / PayPal / Alma et leurs webhooks), Hiboutik (stocks), newsletter / emailing, pixel Meta
   et catalogue, Google Analytics, flux Google Merchant Center, plugin Chronopost, e-mails
   automatiques (paniers abandonnés, avis), tâches planifiées.

## 2. Jour J (matin, trafic faible) — dans cet ordre

1. **Fermer les commandes sur WooCommerce** (mode maintenance ou boutique en catalogue) et noter
   l'heure. Faire le **dernier export des commandes et clients** depuis le précédent, pour l'import
   Shopify.
2. **Dernière sauvegarde** base + fichiers.
3. **Couper les branchements** listés en 1.6, en priorité Hiboutik (sinon l'ancien site continue
   de modifier les stocks), les passerelles de paiement et les e-mails automatiques.
4. **Passer WordPress sur old.malfroid.com** :
   - Réglages > Général : « Adresse web de WordPress » et « Adresse web du site » →
     `https://old.malfroid.com` (ou `WP_HOME` / `WP_SITEURL` dans `wp-config.php`) ;
   - remplacer les adresses dans la base (extension Better Search Replace, ou WP-CLI :
     `wp search-replace 'https://malfroid.com' 'https://old.malfroid.com' --all-tables --dry-run`,
     puis sans `--dry-run`, et idem pour `https://www.malfroid.com`) ;
   - vérifier que `https://old.malfroid.com/wp-admin` fonctionne.
5. **Protéger old.malfroid.com** :
   - Réglages > Lecture : cocher « Demander aux moteurs de recherche de ne pas indexer ce site » ;
   - mot de passe sur tout le site (protection de répertoire Ionos ou extension type
     « Password Protected »), pour que personne ne commande ni ne tombe dessus via Google.
6. **DNS chez Ionos (malfroid.com)** : passer l'utilisation du domaine de « Espace web » à des
   enregistrements DNS personnalisés, puis :
   - `@` A → valeur Shopify (`23.227.38.65`) ; **supprimer l'AAAA de `@`** ;
   - `www` : supprimer A et **AAAA**, créer CNAME → `shops.myshopify.com` ;
   - **vérifier que MX, SPF, DMARC, TXT Facebook et les CNAME d'authentification des e-mails
     Shopify sont toujours là** (Ionos peut réécrire la zone quand on change l'utilisation du domaine) ;
   - `old.malfroid.com` garde son pointage vers l'hébergement Ionos.
7. **Shopify** : vérifier la connexion du domaine, définir `malfroid.com` comme domaine principal
   (www redirigé dessus), attendre le certificat SSL (souvent quelques minutes, jusqu'à 48 h), puis
   retirer le mot de passe de la boutique (Boutique en ligne > Préférences).

## 3. Contrôles (J et J+1)

- `https://malfroid.com` et `https://www.malfroid.com` ouvrent Shopify en HTTPS, y compris en 4G
  (IPv6) ; contrôle DNS : `dig malfroid.com A`, `dig malfroid.com AAAA` (plus d'AAAA Ionos).
- Une dizaine d'anciennes adresses FR et EN (fiche, catégorie, page, article) redirigent vers
  Shopify (redirections déjà en place, voir `content/redirections/`).
- Une commande test sur Shopify ; réception des e-mails de commande.
- **Messagerie Ionos** : envoyer et recevoir un e-mail sur une adresse @malfroid.com.
- `https://old.malfroid.com` demande le mot de passe, l'admin WordPress fonctionne, les commandes
  historiques sont consultables.
- Google Search Console : soumettre `https://malfroid.com/sitemap.xml`.

## 4. Après la bascule

- **Ne pas résilier l'hébergement Ionos** : il porte old.malfroid.com (et peut-être la messagerie,
  à vérifier dans le contrat).
- Durée de conservation à décider (ex. 6 à 12 mois), puis export complet (base + fichiers +
  factures PDF éventuelles, à garder 10 ans pour la comptabilité) avant de fermer l'ancien site.
- Mettre à jour WordPress et les extensions tant que old.malfroid.com reste en ligne.

## Retour arrière

Si Shopify pose problème le jour J : remettre chez Ionos les A et AAAA d'origine de `@` et `www`
(`217.160.0.92`, `2001:8d8:100f:f000::26b`), relancer le remplacement d'adresses en sens inverse
(`old.malfroid.com` → `malfroid.com`) et rouvrir les commandes WooCommerce.
