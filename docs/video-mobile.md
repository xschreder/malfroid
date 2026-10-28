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

## État au 23/10

- La section **héro** (Horizon natif) a déjà sa vidéo mobile : réglage « Média mobile
  personnalisé » avec `Campagne FW26-27_mobile.mp4`. Rien à coder.
- Le **bloc vidéo** de la section suivante (film `Malfroid-film-short_V2.mp4`, 16/9 pleine
  largeur) n'avait pas de source mobile : le fichier `blocks/video.liquid` de ce dépôt ajoute le
  réglage « Vidéo mobile (portrait, facultative) » et bascule sous 750 px. Il est installé sur la
  copie **« Malfroid x NFBS - 1.1 (validations 23/10) »** ; à reporter sur le thème principal
  (copier le fichier dans l'éditeur de code) ou publier cette copie.
- Reste à fournir par Malfroid : le film court en version portrait, puis le sélectionner dans
  le bloc vidéo de l'accueil.

## Correctif du 28/10

Avec une vidéo mobile choisie, la vidéo de la section rétrécissait : les enveloppes
`.video-block--desktop` / `--mobile` (en `display: block`) devenaient l'élément flex de la section et
se réduisaient à leur contenu. Elles passent en `display: contents` ; envoyé sur la copie 1.1
(checksum `bb8e80d72d31255d5a565ef9c215cc0f`).

## Mise en place

1. Modifier la section sur une copie du thème principal (l'API refuse l'écriture sur le thème
   publié), vérifier sur téléphone avec l'aperçu, puis reporter le fichier sur le thème principal
   (décision du 21/10 : les validations vont sur le thème principal).
2. Si Horizon propose déjà un réglage « vidéo mobile » dans la version installée, l'utiliser tel
   quel : le code ci-dessus n'est alors pas nécessaire.
