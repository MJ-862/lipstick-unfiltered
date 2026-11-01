import pandas as pd, re, json
df = pd.read_excel('nykaa_lipstick_voc_dataset.xlsx')
NEG = [
 ("Drying / uncomfortable on lips", r"\bdry(ing|ness)?\b|dries|flak|crack|chapp|dehydrat|uncomfortable|tight on|peel", "Test a more moisturising base (e.g. added oils or balm layer) and add a lip-prep tip on pack and PDP."),
 ("Shade looks different from photo/swatch", r"different (shade|colou?r)|(shade|colou?r).{0,30}(different|not same|doesn.?t match|not as|differ)|not (the )?same|(darker|lighter|duller|brighter) than|looks? (very |way )?different|wrong (shade|colou?r)|does(n.?t| not) (match|suit)|not matching", "Add a virtual try-on and real-skin-tone swatches on the product page, and tighten photo colour accuracy."),
 ("Doesn't last / transfers", r"doesn.?t last|not long.?lasting|fades?\b|fading|transfer|smudg|smear|bleed|feather|wears? off|rubs? off|short.?lived", "Run a wear-time test on the weakest shades and test a longer-wear formula variant."),
 ("Patchy / uneven application", r"patch|uneven|streak|clump|cakey|settles? into|creas|hard to (apply|blend)|drag|tugg|sticky|gloopy|thick", "Improve texture and bullet shape, and add an application guide (prep, liner, layering)."),
 ("Weak pigmentation", r"not (very |so |that )?pigment|less pigment|low pigment|sheer|transparent|(colou?r|pigment).{0,15}(weak|poor|doesn.?t show)|barely (visible|show)", "Check pigment load by shade and clearly label sheer versus full-coverage shades."),
 ("Packaging / product defects", r"broken|broke\b|leak|damag|melt|packag|fake|duplicate|counterfeit|expired|dented|defect|stuck|seal", "Audit packaging and shipping quality, and add tamper-proof seals and better transit protection."),
 ("Price / value concerns", r"expensive|overpriced|pricey|costly|not worth|waste of money|price", "Clarify value (quantity, wear time) and test bundles or minis."),
 ("Smell / taste", r"smell|odou?r|fragrance|taste|scent", "Test a lower-fragrance or fragrance-free variant."),
]
POS = [
 ("Great pigmentation / colour payoff", r"pigment|payoff|rich colou?r|vibrant|bold colou?r|opaque"),
 ("Long-lasting", r"long.?lasting|lasts? (all|for|long)|stays? (put|on|all)|all day|transfer.?proof|smudge.?proof"),
 ("Comfortable / hydrating", r"hydrat|moistur|creamy|comfortable|non.?drying|smooth|lightweight|soft"),
 ("Beautiful shades", r"love (the )?(shade|colou?r)|perfect (shade|colou?r)|(shade|colou?r)s?.{0,20}(beautiful|pretty|perfect|gorgeous|lovely|range)|nude"),
 ("Value for money", r"worth (it|the|every)|value for money|affordable|budget|good price"),
 ("Easy application", r"easy to (apply|use)|appl(y|ies) (smoothly|easily)|glides|blends? (well|easily)"),
]
negrx=[re.compile(p,re.I) for _,p,_ in NEG]; posrx=[re.compile(p,re.I) for _,p in POS]
neg_clean=re.compile(r"(not|non|no|never|without|doesn'?t|isn'?t)[- ]\w*[ -]?(dry|drying|dryness)",re.I)
prods=sorted(df['Product'].unique()); cats=sorted(df['Category'].unique())
shades=sorted(s for s in df['Shade'].dropna().unique() if s)
pi={p:i for i,p in enumerate(prods)}; ci={c:i for i,c in enumerate(cats)}; si={s:i for i,s in enumerate(shades)}
rows=[]
for _,r in df.iterrows():
    t=(str(r['Title'] or '').strip()+'. '+str(r['Review Text'] or '').strip()).strip('. ')
    t=re.sub(r'\s+',' ',t)[:450]; tc=neg_clean.sub('',t)
    rows.append([pi[r['Product']],int(r['Rating']),str(r['Date']),shades[si[r['Shade']]] if isinstance(r['Shade'],str) and r['Shade'] else '',int(r['Likes']),t,
      [i for i,x in enumerate(negrx) if x.search(tc)],[i for i,x in enumerate(posrx) if x.search(t)],ci[r['Category']]])
data={"p":prods,"c":cats,"neg":[{"name":n,"action":a} for n,_,a in NEG],"pos":[{"name":n} for n,_ in POS],"r":rows}
html=open('tpl.html',encoding='utf-8').read().replace('__DATA__',json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/'))
open('index.html','w',encoding='utf-8').write(html)
print(len(html)//1024,'KB')
