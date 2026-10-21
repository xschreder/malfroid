# Flux de stock — avant et après Shopify POS

## 1. Situation à la migration (conservée pour le lancement)

Principe retenu le 21/10 : un **stock agrégé** des boutiques est exposé sur le site ; la boutique
de **Ternes** sert de référence comptable et d'expédition. Pas de stock par site dans Shopify.

```mermaid
flowchart LR
    subgraph Boutiques["Boutiques physiques"]
        T[Ternes<br/>référence comptable + expédition]
        A[Autres boutiques]
    end
    HB[(Hiboutik<br/>caisse / stock réel)]
    T --> HB
    A --> HB
    HB -- "connecteur Hiboutik → Shopify<br/>(stock agrégé, 1 emplacement)" --> SH[(Shopify<br/>emplacement « Ternes »)]
    SH --> SITE[Site malfroid.com]
    SITE -- commande --> SH
    SH -- "commande à préparer" --> T
    T -- "Chronopost<br/>(étiquette Chronopost Pro)" --> CL[Client]
    SH -. "décrément du stock agrégé" .-> HB
```

Points d'attention :

- une vente en boutique et une vente web peuvent consommer la même dernière paire : le
  connecteur doit synchroniser dans les deux sens, sinon risque de survente ;
- l'emplacement Shopify unique s'appelle « Ternes » pour que les commandes partent du bon point ;
- les 239 variantes créées à 0 sans SKU (Technique n° 10) doivent recevoir un SKU identique à
  Hiboutik avant que le connecteur ne les reconnaisse.

## 2. Cible après Shopify POS

Shopify POS remplace Hiboutik en caisse ; chaque boutique devient un **emplacement Shopify** avec
son propre stock, et le site vend sur la somme des emplacements (ou sur une sélection).

```mermaid
flowchart LR
    subgraph Emplacements["Emplacements Shopify"]
        T[Ternes<br/>POS + expédition web]
        B1[Boutique 2<br/>POS]
        B2[Boutique 3<br/>POS]
    end
    SH[(Shopify<br/>stock par emplacement)]
    T <--> SH
    B1 <--> SH
    B2 <--> SH
    SH --> SITE[Site malfroid.com<br/>disponibilité = somme des emplacements]
    SITE -- commande --> SH
    SH -- "routage : Ternes d'abord,<br/>sinon l'emplacement qui a la pointure" --> T
    SH -- "retrait en boutique<br/>(Click & Collect)" --> B1
    T -- Chronopost --> CL[Client]
```

Ce que POS débloque :

- **Click & Collect** par boutique (Site n° 39) et affichage « disponible en boutique » sur la fiche ;
- **transferts** entre boutiques tracés dans Shopify ;
- comptabilité toujours centralisée sur Ternes si souhaité (rapports par emplacement) ;
- suppression du connecteur Hiboutik (Technique n° 20) et de l'abonnement associé.

Pré-requis : un abonnement POS Pro par boutique si plusieurs caisses, inventaire initial par
emplacement, et un routage des commandes paramétré dans Paramètres > Expédition > Priorité des
emplacements.
