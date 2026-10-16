import json,re,sys,collections
src=sys.argv[1]; out=sys.argv[2]
prods={}; media=collections.defaultdict(list)
for line in open(src,encoding='utf-8'):
    o=json.loads(line)
    if o['id'].startswith('gid://shopify/Product/'): prods[o['id']]=o
    elif o['id'].startswith('gid://shopify/MediaImage/') or o.get('mediaContentType'): media[o['__parentId']].append(o)
LABELS={'Permanent','Limited','Édition limitée','Collection permanente'}
def clean(h):
    if not h: return h,False
    o=h
    h=re.sub(r'<p style="text-align: right;"><em>(Permanent|Limited|Édition limitée|Collection permanente)</em></p>\s*','',h)
    h=re.sub(r'<p class="wpsm-(?:show|hide)"[^>]*>.*?</p>\s*','',h,flags=re.S)
    n=0
    for tag in ('<div class="show_more">','<div class="wpsm-content">'):
        c=h.count(tag); n+=c; h=h.replace(tag,'')
    # remove n closing divs from the end (they close the unwrapped divs)
    for _ in range(n):
        i=h.rfind('</div>')
        if i<0: break
        h=h[:i]+h[i+6:]
    h=re.sub(r'^(\s*<p>(?:\s|&nbsp;|\xa0)*</p>\s*)+','',h)   # leading empty paragraphs
    h=re.sub(r'^\s*<br\s*/?>\s*','',h)
    # lignes de texte nu (hors balise) héritées de WordPress : les envelopper dans <p>, retirer les <br> isolés
    lines=[]
    for ln in h.split('\n'):
        t=ln.strip()
        if re.fullmatch(r'<br\s*/?>',t): continue
        if t and not t.startswith('<') and not t.endswith('>'): t='<p>'+t+'</p>'
        lines.append(t if t else '')
    h='\n'.join(lines)
    h=re.sub(r'\n{2,}','\n',h)
    h=h.strip()
    return h,(h!=o)
titles=collections.Counter(p['title'] for p in prods.values())
upd=[]; alts=[]; stats=collections.Counter()
for pid,p in prods.items():
    color=((p.get('color') or {}).get('reference') or {}).get('displayName')
    inp={'id':pid}
    raw=p.get('descriptionHtml') or ''
    if re.search(r'wpsm|show_more|<p style="text-align: right;"><em>(Permanent|Limited|Édition limitée|Collection permanente)</em></p>',raw):
        h2,changed=clean(raw)
        if changed: inp['descriptionHtml']=h2; stats['desc']+=1
    if titles[p['title']]>1 and color and not (p.get('seo') or {}).get('title'):
        inp['seo']={'title':f"{p['title']} – {color}"}; stats['seo']+=1
    if len(inp)>1: upd.append({'input':inp})
    alt=f"{p['title']} – {color}" if color else p['title']
    for m in media.get(pid,[]):
        if m.get('mediaContentType')=='IMAGE' and not (m.get('alt') or '').strip():
            alts.append({'id':m['id'],'alt':alt}); stats['alt']+=1
open(out+'/product_updates.jsonl','w',encoding='utf-8').write(''.join(json.dumps(u,ensure_ascii=False)+'\n' for u in upd))
# fileUpdate: 50 images per line
with open(out+'/file_updates.jsonl','w',encoding='utf-8') as f:
    for i in range(0,len(alts),50): f.write(json.dumps({'files':alts[i:i+50]},ensure_ascii=False)+'\n')
print('products',len(prods),'media',sum(len(v) for v in media.values()),dict(stats),'update lines',len(upd),'file lines',(len(alts)+49)//50)
# leftovers check
left=[p['title'] for p in prods.values() if re.search(r'wpsm|show_more|Lire ?(Plus|Moins)',clean(p.get('descriptionHtml'))[0] or '')]
print('still containing leftovers after clean:',left)
