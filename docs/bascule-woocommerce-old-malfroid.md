# Bascule : WooCommerce sur old.malfroid.com, Shopify sur malfroid.com

Objectif : le jour de la migration, malfroid.com et www.malfroid.com pointent sur Shopify, et
l'ancien site WooCommerce reste consultable (admin, commandes, clients) sur **old.malfroid.com**,
protégé et non indexé.

## État relevé le 30/10/2026 (vérifié à nouveau le 30/10 : old.malfroid.com absent du DNS, WordPress enregistré sur https://malfroid.com)

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
   Au 30/10, il n'existe pas encore : les serveurs DNS Ionos répondent « domaine inexistant ».
4. **Certificat SSL** pour `old.malfroid.com` : l'activer dans Ionos (certificat inclus dans
   l'hébergement).
5. **Vérifier que old.malfroid.com répond** avant d'aller plus loin : `https://old.malfroid.com`
   doit renvoyer vers `https://malfroid.com` (WordPress redirige vers l'adresse enregistrée dans
   sa base : c'est normal à ce stade). S'il ne répond pas du tout, le sous-domaine ou le
   certificat n'est pas prêt : **ne rien changer dans WordPress tant que ce n'est pas le cas.**
6. **Repérer l'adresse de connexion WordPress** : `wp-login.php` répond 404, la page de connexion
   est masquée par une extension de sécurité. Noter l'adresse personnalisée (dans les réglages de
   l'extension) et vérifier qu'on peut se connecter avec.
7. **Noter le préfixe des tables** (`$table_prefix` dans `wp-config.php`, souvent `wp_`) et les
   extensions de cache, de sécurité ou de SSL installées (WP Rocket, Really Simple SSL, etc.).
8. **Côté Shopify** : Paramètres > Domaines > Connecter un domaine existant > `malfroid.com`.
   Shopify affiche les valeurs à poser chez Ionos (en principe A `23.227.38.65` et CNAME `www` →
   `shops.myshopify.com` ; reprendre celles affichées par Shopify).
9. **Inventaire des branchements de WooCommerce** à couper le jour J (voir étape 2.3) : paiements
   (Stripe / PayPal / Alma et leurs webhooks), Hiboutik (stocks), newsletter / emailing, pixel Meta
   et catalogue, Google Analytics, flux Google Merchant Center, plugin Chronopost, e-mails
   automatiques (paniers abandonnés, avis), tâches planifiées.

## 2. Jour J (matin, trafic faible) — dans cet ordre

1. **Fermer les commandes sur WooCommerce** (mode maintenance ou boutique en catalogue) et noter
   l'heure. Faire le **dernier export des commandes et clients** depuis le précédent, pour l'import
   Shopify.
2. **Dernière sauvegarde** base + fichiers.
3. **Couper les branchements** listés en 1.9, en priorité Hiboutik (sinon l'ancien site continue
   de modifier les stocks), les passerelles de paiement et les e-mails automatiques.
4. **Passer WordPress sur old.malfroid.com**, uniquement si l'étape 1.5 est validée :
   - **forcer l'adresse dans `wp-config.php`** (SFTP), juste avant la ligne
     `/* That's all, stop editing! */` :

     ```php
     define( 'WP_HOME', 'https://old.malfroid.com' );
     define( 'WP_SITEURL', 'https://old.malfroid.com' );
     ```

     Ces deux lignes l'emportent sur les adresses enregistrées dans la base : le site démarre
     tout de suite sur old.malfroid.com, sans passer par l'admin. Ne pas modifier « Adresse web »
     dans Réglages > Général à la place : si l'adresse ne répond pas encore, on se retrouve
     bloqué hors de l'admin.
   - se connecter sur `https://old.malfroid.com/<adresse de connexion personnalisée>` ;
   - **remplacer les adresses restantes dans la base** (liens dans les contenus, réglages
     WooCommerce, Elementor, médias) avec l'extension **Better Search Replace** (Outils >
     Better Search Replace, toutes les tables, d'abord en simulation) ou en WP-CLI :
     `wp search-replace 'https://malfroid.com' 'https://old.malfroid.com' --all-tables --dry-run`,
     puis sans `--dry-run` ; idem pour `https://www.malfroid.com` et `http://malfroid.com`.
     **Ne jamais faire ce remplacement en SQL direct dans phpMyAdmin** : les réglages WordPress
     sont stockés en données sérialisées, un remplacement brut les casse (réglages WooCommerce,
     widgets, Elementor perdus) ;
   - Réglages > Permaliens > Enregistrer (régénère les règles d'adresses) ; si Elementor :
     Elementor > Outils > Régénérer les fichiers ; vider les caches (extension de cache, Ionos) ;
   - vérifier `https://old.malfroid.com/wp-admin`, une fiche produit et une commande.
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

## Dépannage : WordPress ne redémarre pas après le changement d'adresse

| Symptôme | Cause | Correction |
|---|---|---|
| old.malfroid.com ne répond pas du tout (erreur DNS, « site inaccessible ») | sous-domaine pas créé ou pas encore propagé | Ionos : créer le sous-domaine et l'attacher à l'espace web, attendre la propagation (étape 1.5) |
| old.malfroid.com renvoie vers malfroid.com (donc vers Shopify après la bascule) | la base contient encore `https://malfroid.com` dans `siteurl` / `home` | ajouter `WP_HOME` / `WP_SITEURL` dans `wp-config.php` (étape 2.4) ; à défaut, phpMyAdmin > table `<préfixe>options` > lignes `siteurl` et `home` → `https://old.malfroid.com` (seules ces deux lignes se modifient à la main) |
| Boucle de redirection ou erreur de certificat | certificat SSL absent sur old.malfroid.com, ou règle HTTPS / domaine figée dans `.htaccess` ou dans une extension (Really Simple SSL…) | activer le certificat Ionos ; chercher `malfroid.com` dans `.htaccess` ; désactiver l'extension en renommant son dossier dans `wp-content/plugins/` |
| `wp-admin` ou `wp-login.php` en 404 | page de connexion masquée par une extension de sécurité | utiliser l'adresse de connexion personnalisée (étape 1.6) ; si inconnue, renommer le dossier de l'extension dans `wp-content/plugins/` le temps de se connecter |
| Admin accessible mais images, liens ou mise en page cassés | adresses `malfroid.com` restantes dans les contenus, cache | Better Search Replace (étape 2.4), Permaliens > Enregistrer, régénérer Elementor, vider les caches |
| Réglages WooCommerce ou widgets vides après remplacement | remplacement fait en SQL direct sur des données sérialisées | restaurer la sauvegarde de la base (étape 2.2) et refaire avec Better Search Replace ou WP-CLI |

## Retour arrière

Si Shopify pose problème le jour J : remettre chez Ionos les A et AAAA d'origine de `@` et `www`
(`217.160.0.92`, `2001:8d8:100f:f000::26b`), retirer les deux lignes `WP_HOME` / `WP_SITEURL` de
`wp-config.php`, relancer le remplacement d'adresses en sens inverse (`old.malfroid.com` →
`malfroid.com`) et rouvrir les commandes WooCommerce.
