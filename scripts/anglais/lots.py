"""Prépare les lots de mutations Shopify pour les titres / handles anglais et les redirections.

  python3 scripts/anglais/lots.py traductions <reponses_digests.json> <dossier_sortie>
  python3 scripts/anglais/lots.py redirections <reponses_redirections.json> <dossier_sortie>
  python3 scripts/anglais/lots.py verifier <reponses_relecture.json>

Les fichiers d'entrée sont les réponses brutes de l'API (un objet ou une liste de réponses) :
  - traductions : translatableResourcesByIds(...) { nodes { resourceId translatableContent { key digest } } }
  - redirections : urlRedirects(...) { nodes { id path target } }
Chaque lot écrit est un {"query", "variables"} à envoyer tel quel à graphql_mutation.
"""
import json, os, sys

ICI = os.path.dirname(os.path.abspath(__file__))
DEPOT = os.path.dirname(os.path.dirname(ICI))
DONNEES = os.path.join(DEPOT, 'content/translations/titres-slugs-anglais-2026-10-28.json')


def objets(x, cles):
    """Tous les objets JSON contenant les clés données, quelle que soit l'imbrication."""
    if isinstance(x, dict):
        if all(k in x for k in cles):
            yield x
        for v in x.values():
            yield from objets(v, cles)
    elif isinstance(x, list):
        for v in x:
            yield from objets(v, cles)


def ecrire(lots, nom, dossier):
    os.makedirs(dossier, exist_ok=True)
    for i, lot in enumerate(lots, 1):
        with open(os.path.join(dossier, f'{nom}-{i:02d}.json'), 'w') as f:
            json.dump(lot, f, ensure_ascii=False)
    print(f'{len(lots)} lots écrits dans {dossier}')


def traductions(entree, dossier, taille=25):
    produits = json.load(open(DONNEES))
    digests = {}
    for n in objets(json.load(open(entree)), ('resourceId', 'translatableContent')):
        digests[n['resourceId']] = {c['key']: c['digest'] for c in n['translatableContent']}
    a_faire, manquants = [], []
    for p in produits:
        d = digests.get(p['id'])
        if not d or 'title' not in d or 'handle' not in d:
            manquants.append(p['handle'])
            continue
        a_faire.append((p['id'], [
            {'key': 'title', 'locale': 'en', 'value': p['title_en'], 'translatableContentDigest': d['title']},
            {'key': 'handle', 'locale': 'en', 'value': p['handle_en'], 'translatableContentDigest': d['handle']},
        ]))
    if manquants:
        print('Sans digest (produit supprimé ou absent de la réponse) :', ', '.join(manquants))
    lots = []
    for i in range(0, len(a_faire), taille):
        bloc = a_faire[i:i + taille]
        sig = ', '.join(f'$r{j}: ID!, $t{j}: [TranslationInput!]!' for j in range(len(bloc)))
        corps = ' '.join(f'm{j}: translationsRegister(resourceId: $r{j}, translations: $t{j}) '
                         '{ translations { key value } userErrors { field message } }' for j in range(len(bloc)))
        variables = {}
        for j, (rid, trs) in enumerate(bloc):
            variables[f'r{j}'], variables[f't{j}'] = rid, trs
        lots.append({'query': f'mutation({sig}) {{ {corps} }}', 'variables': variables})
    print(f'{len(a_faire)} produits (titre + handle)')
    ecrire(lots, 'titres-handles', dossier)


def redirections(entree, dossier, taille=60):
    nouveau = {'/en/products/' + p['handle']: '/en/products/' + p['handle_en'] for p in json.load(open(DONNEES))}
    vues = {r['id']: r for r in objets(json.load(open(entree)), ('id', 'path', 'target'))}
    a_faire = [(r['id'], r['path'], nouveau[r['target']]) for r in vues.values() if r['target'] in nouveau]
    print(f'{len(vues)} redirections lues, {len(a_faire)} à repointer vers le handle anglais')
    lots = []
    for i in range(0, len(a_faire), taille):
        bloc = a_faire[i:i + taille]
        sig = ', '.join(f'$i{j}: ID!, $u{j}: UrlRedirectInput!' for j in range(len(bloc)))
        corps = ' '.join(f'm{j}: urlRedirectUpdate(id: $i{j}, urlRedirect: $u{j}) '
                         '{ urlRedirect { path target } userErrors { field message } }' for j in range(len(bloc)))
        variables = {}
        for j, (rid, path, cible) in enumerate(bloc):
            variables[f'i{j}'], variables[f'u{j}'] = rid, {'path': path, 'target': cible}
        lots.append({'query': f'mutation({sig}) {{ {corps} }}', 'variables': variables})
    ecrire(lots, 'redirections', dossier)


def verifier(entree):
    attendu = {p['id']: p for p in json.load(open(DONNEES))}
    lus, ecarts = 0, []
    for n in objets(json.load(open(entree)), ('resourceId', 'translations')):
        if n['resourceId'] not in attendu:
            continue
        lus += 1
        p, tr = attendu[n['resourceId']], {t['key']: t['value'] for t in n['translations']}
        for cle, valeur in (('title', p['title_en']), ('handle', p['handle_en'])):
            if tr.get(cle) != valeur:
                ecarts.append(f"{p['handle']} {cle} : {tr.get(cle)!r} au lieu de {valeur!r}")
    print(f'{lus} produits relus, {len(ecarts)} écart(s)')
    for e in ecarts:
        print(' ', e)


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == 'verifier':
        verifier(sys.argv[2])
    elif len(sys.argv) == 4 and sys.argv[1] in ('traductions', 'redirections'):
        {'traductions': traductions, 'redirections': redirections}[sys.argv[1]](sys.argv[2], sys.argv[3])
    else:
        sys.exit(__doc__)
