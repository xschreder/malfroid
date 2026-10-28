# Reste à faire avant la migration (état au 28/10)

À faire par Xavier et Alexandre depuis le connecteur Shopify de Malfroid. Liste tirée des lignes
encore ouvertes du Google Sheet de recette (onglets Site, Technique & lancement, E-mails) et des
notes de ce dépôt.

Règles pour le connecteur :
- Vérifier `{ shop { myshopifyDomain } }` = `malfroid-fr.myshopify.com` avant toute écriture.
- Le connecteur n'écrit pas sur le thème publié et ne publie pas de thème : les fichiers vont sur
  la copie 1.1, la publication se fait à la main dans l'admin.

## 1. Thème : finir la copie 1.1, puis la publier

| # | Action | Comment | Sheet |
|---|---|---|---|
| 1.1 | Envoyer l'upsell du tiroir panier et la page 404 sur la copie 1.1 | connecteur, pas à pas dans `docs/reprise-upsell-404.md` | Site 35 |
| 1.2 | Trancher la table des pointures du thème : UK 5 = EU 38,5 (thème) ou 39,5 (guide Malfroid) | décision Malfroid, puis corriger `assets/size-conversions.json` sur la copie | NF3 |
| 1.3 | Page « Se connecter » aux couleurs Malfroid | encore à faire sur la copie | Site 3 |
| 1.4 | Aperçu de la copie 1.1 sur mobile et ordinateur, en FR et en /en/ | vérifier en-tête des fiches produit (4), infobulle coloris (19), textes anglais traduits (23), onglet Fit (47), titre des tailles en EN (50), boutons de la page panier (51), vidéo mobile (2), upsell (35) | Technique 24 |
| 1.5 | Si le thème publié a été modifié depuis le 26/10 : refaire la copie à partir du thème publié et réappliquer les fichiers de `theme/` | connecteur | Technique 24 |
| 1.6 | **Publier** la copie 1.1 | à la main : Boutique en ligne > Thèmes > Publier | Technique 24 |
| 1.7 | Film court en portrait (9:16) : le choisir dans le réglage « Vidéo mobile » du bloc vidéo de l'accueil | Malfroid, éditeur de thème | Site 2 |

## 2. Contenu, pages et textes

| # | Action | Comment | Sheet |
|---|---|---|---|
| 2.1 | Nettoyage des pages : d'abord repointer le lien CGV du menu « Nous » vers `/policies/terms-of-service`, puis dépublier les 11 pages et créer leurs redirections | accord de Xavier attendu ; liste dans `docs/pages-a-nettoyer.md` ; connecteur | Site 49 |
| 2.2 | Renommer la boutique « Malfroid-fr » en « Malfroid » (titre des pages, paiement, copyright, e-mails) | Paramètres > Général > Nom de la boutique, puis vérifier le nom d'expéditeur des e-mails | Site 21, E-mails 2 |
| 2.3 | Politique de confidentialité : remplacer « Malfroid-fr », l'e-mail Gmail et l'adresse 63 rue des Vignoles (→ MALFROID SARL, contact@malfroid.com, 7 rue Villebois-Mareuil) | Paramètres > Politiques ; reprendre aussi SARL et le capital social, comme dans les autres politiques | Technique 4 |
| 2.4 | Lien « Mentions légales » dans le menu de pied de page du thème | Contenu > Menus | Technique 3 |
| 2.5 | CGV : confirmer l'adhésion CMAP, les frais de retour, les délais et pays de livraison, les moyens de paiement | Malfroid | Technique 5 |
| 2.6 | Textes du paiement encore en anglais | éditeur du paiement > Langue (lien dans le Sheet) | Site 23 |
| 2.7 | Traduire à la main les compléments FR de Paul (« Caractéristiques techniques », « Le mot du chausseur ») et les 12 produits sans anglais sur l'ancien site | Translate & Adapt | Site 38 |
| 2.8 | Filtre « Style » (Élégant / Casual) à cocher dans Search & Discovery, et liens du menu Souliers vers les collections | Malfroid, application (pas d'API) | Site 6 |
| 2.9 | Recréer la carte cadeau Shopify | Alex | Site 41 |
| 2.10 | Fiches incomplètes et fiches de moins de 3 photos (15 produits) | Paul | Site 18, Technique 16 |
| 2.11 | Image de partage pour les réseaux | Boutique en ligne > Préférences | Technique 26 |
| 2.12 | E-mail d'accusé de réception d'une demande de retour (Shopify Forms, sinon Flow) | Alex | E-mails 17 |

## 3. Paiement, livraison, douane

| # | Action | Comment | Sheet |
|---|---|---|---|
| 3.1 | Dossier Shopify Payments terminé (Kbis, pièce d'identité valide du dirigeant, RIB) puis Klarna | `docs/pieces-shopify-payments-klarna.md` | Site 33, Technique 25 |
| 3.2 | Commandes test : carte, PayPal, Klarna, remboursement partiel, retrait en boutique ; vérifier la TVA « dont » dans les e-mails | après l'activation des paiements | Technique 12 |
| 3.3 | Revoir les tarifs de livraison : le Sheet indique UE Standard 15 €, le tarif a été passé à 25 € le 19/10 | Paul, Paramètres > Expédition | Technique 11 |
| 3.4 | Application Chronopost : saisir les identifiants web service (n° de compte à 8 chiffres + mot de passe web service) | Malfroid | Technique 11 |
| 3.5 | Douane DDP / DAP, codes HS, origine du cuir : le marché Export reste en brouillon tant que Victor et Chronopost n'ont pas répondu | Victor | Technique 27, Site 28 |

## 4. Jour de la migration

| # | Action | Comment | Sheet |
|---|---|---|---|
| 4.1 | Réexport complet de l'ancien site (clients, newsletter avec consentement, commandes) puis import | Kuba / Matrixify | Technique 9 |
| 4.2 | Stocks : import du stock agrégé (Ternes = référence), connecteur Hiboutik, alignement des 239 nouvelles variantes | Hiboutik : abonnement 49 €/an | Technique 10, 20 |
| 4.3 | Déconnecter Matrixify une fois les imports terminés | | Technique 21 |
| 4.4 | Brancher le domaine malfroid.com, retirer le mot de passe | Paramètres > Domaines, Préférences | |
| 4.5 | Tester une dizaine d'anciennes adresses FR et EN (fiche, catégorie, page, article) en navigation privée ou `curl -I` ; tester l'inscription newsletter | redirections déjà créées | Technique 1, Site 20 |
| 4.6 | Google Search Console : vérifier le domaine, soumettre `/sitemap.xml` ; PageSpeed mobile | | Technique 15, 18 |
| 4.7 | Envoyer le CSV des redirections à Arnaud | `content/redirections/redirections-301-2026-10-26.csv` | Technique 1 |
| 4.8 | GitHub : transférer le dépôt à Malfroid et connecter le thème | GitHub > Settings > Transfer ownership, puis application Shopify GitHub | Technique 23 |

## Après le lancement (non bloquant)

Réassurance accueil et fiche produit (Site 1, 10), « Payez en 3 ou 4 fois » sous le prix (14,
avec Klarna), alerte retour en stock (15, `docs/flow-alerte-stock.md`), avis clients (16), guide
des formes (17), « Outlet » → « Archives » (36), texte de la newsletter (37), retrait en boutique
sur la fiche (39, après POS), page « Travaillons ensemble » (42), bouton rendez-vous (8), sommaire
des portraits (NF5).
