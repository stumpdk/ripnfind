import difflib
import json

with open('unique_lastnames.json') as f:
    words = json.load(f)

words_lower = []
for w in words:
    words_lower.append(w.lower())

#print(difflib.get_close_matches("A nderSson", words_lower,cutoff=0.6))

print('found %d lines' % len(open('politiets_efterretninger_1867_I.txt', encoding="latin-1").readlines()))
i = 0
for l in  open('politiets_efterretninger_1867_I.txt', encoding="latin-1").readlines():
    i = i+1
    print("line %d" % i)
    if len(l)> 200:
        continue
    for w in l.split():
        if len(w) < 3:
            continue
        
        matches = difflib.get_close_matches(w, words_lower,cutoff=0.9)
        if(len(matches)>0):
            print('match')
            print(l)
            print(matches)   
