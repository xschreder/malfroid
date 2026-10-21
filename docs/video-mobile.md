# Vidéo d'accueil — source distincte pour mobile

Décision du 21/10 : la vidéo d'accueil (paysage, 34 Mo après compression) est mal cadrée sur
téléphone. On ajoute une **seconde source vidéo, en portrait**, servie uniquement sous 750 px.

## Principe

Dans la section vidéo du thème Horizon (`sections/video.liquid` ou le bloc vidéo de la section
héro), ajouter un réglage `video_mobile` (type `video`) et, dans le rendu, deux balises `<video>`
dont l'affichage dépend de la largeur d'écran. Pas de JavaScript : le navigateur ne charge que la
source visible, car la balise masquée reçoit `preload="none"`.

```liquid
{%- comment -%} Réglage à ajouter dans le schema de la section {%- endcomment -%}
{
  "type": "video",
  "id": "video_mobile",
  "label": "Vidéo mobile (portrait, facultative)"
}
```

```liquid
{%- comment -%} Rendu {%- endcomment -%}
{%- if section.settings.video_mobile != blank -%}
  <div class="video-desktop">
    {{ section.settings.video | video_tag: autoplay: true, loop: true, muted: true, controls: false, playsinline: true, preload: 'metadata' }}
  </div>
  <div class="video-mobile">
    {{ section.settings.video_mobile | video_tag: autoplay: true, loop: true, muted: true, controls: false, playsinline: true, preload: 'metadata' }}
  </div>
{%- else -%}
  {{ section.settings.video | video_tag: autoplay: true, loop: true, muted: true, controls: false, playsinline: true }}
{%- endif -%}

{% stylesheet %}
  .video-mobile { display: none; }
  @media screen and (max-width: 749px) {
    .video-desktop { display: none; }
    .video-mobile { display: block; }
    .video-mobile video { width: 100%; height: 100svh; object-fit: cover; }
  }
{% endstylesheet %}
```

## Fichier vidéo à fournir par Malfroid

- Cadrage **portrait 9:16**, 1080 × 1920 px, H.264, 25 ou 30 i/s, sans piste audio.
- Durée identique à la vidéo paysage, poids visé **≤ 15 Mo** (débit ≈ 4 à 6 Mbit/s).
- Téléversement dans Contenu > Fichiers, puis sélection dans le réglage « Vidéo mobile » de la
  section depuis l'éditeur de thème.

## Mise en place

1. Modifier la section sur une copie du thème principal (l'API refuse l'écriture sur le thème
   publié), vérifier sur téléphone avec l'aperçu, puis reporter le fichier sur le thème principal
   (décision du 21/10 : les validations vont sur le thème principal).
2. Si Horizon propose déjà un réglage « vidéo mobile » dans la version installée, l'utiliser tel
   quel : le code ci-dessus n'est alors pas nécessaire.
