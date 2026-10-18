import json
CH=json.load(open('ch.json'))
def meter(num,den):
    if den==4: return [1]*num
    if den==2: return [2]*num
    if den==8: return [1.5]*(num//3) if num%3==0 else [0.5]*num
    if den==16:
        a=[1]*(num//4); 
        if num%4: a.append((num%4)/4)
        return a
    return [4/den]*num
def chart_labels(nr,from_bar,n_beats):
    c=CH.get(str(nr)) or {'m':[[1,4,4,120]],'end':999}
    out=[]; bar=from_bar
    while len(out)<n_beats:
        s=c['m'][0]
        for x in c['m']:
            if x[0]<=bar: s=x
        q=meter(s[1],s[2])
        for k in range(len(q)): out.append((bar,k,len(q)))
        bar+=1
    return out[:n_beats]
