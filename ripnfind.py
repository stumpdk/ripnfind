#Recursive Incremental Improving Name Finder
import difflib
import json
from collections import Counter
import pandas as pd

person = pd.read_csv("hack4dk_police_person.csv")
# extract all last names
lastnames_col = person.lastname

# nr. of occurencies of last names
counter = Counter(lastnames_col)
#counter.most_common(20)

#with open('unique_lastnames.json') as f:
#   words = json.load(f)


#words_lower = []
#for w in counter.most_common(2500):
#    print(w[0])
#    if isinstance(w[0],str):
#        words_lower.append(w[0].lower())

#names = words_lower#['wilhelm', 'frederiksen','morkebla']#words_lower

alternativSpellings = {}
percentileThredshold = 0.25
cutoffThreshold = 0.75
def recursiveNearMatcher(sentence, alternativSpellings, currentPercent = 0.02, currentCutoff = 0.95):
    matches = list()
    
    words_lower = []
    for w in counter.most_common(int(5000*currentPercent)):
        #print(w[0])
        if isinstance(w[0],str):
            words_lower.append(w[0].lower())
    names = words_lower
    
    print("recursive with these settings: %f, %f" % (currentPercent, currentCutoff))
    print("using %d names and %d alternative spellings" % (len(names), len(alternativSpellings)))
    print("sentence %s" % sentence[0:100])

    while len(matches) == 0 and currentPercent < percentileThredshold and currentCutoff > cutoffThreshold:
        for word in sentence.split():
            word = word.lower()
            word = word.replace(',','').replace('.','')
            
            if len(word)<4:
                continue
            #print(word)

            #Exact match
            if word in names:
                print("exact match: %s" % word)
                matches.append({"match": word, "confidence": 1-currentPercent})
                break

            #Exact match, alternative spellings
            if word in alternativSpellings:
                print("alternative spelling match: %s" % word)
                matches.append({"match": alternativSpellings[word], "confidence": 1-currentPercent-0.2})
                break
            
            #Close match
            closeMatches = difflib.get_close_matches(word, names,cutoff=currentCutoff)
            if len(closeMatches) > 0:
                print("close match: %s" % closeMatches[0])
                matches.append({"match": closeMatches[0], "confidence": currentCutoff*(1-currentPercent)})
                #Add word to alternative spellings
                alternativSpellings[closeMatches[0]] = word
                break
        
        
        currentCutoff = currentCutoff-0.02
        currentPercent = currentPercent*2
        
        #No matches, reduced thresholds
        if len(matches) == 0:
            matches = recursiveNearMatcher(sentence, alternativSpellings, currentPercent, currentCutoff)

    return matches

print('found %d lines' % len(open('politiets_efterretninger_1867_I.txt', encoding="latin-1").readlines()))
i = 0
matches = list()
for l in  open('politiets_efterretninger_1867_I.txt', encoding="latin-1").readlines():
    curMatches = list()
    i = i+1
    print("current line %d" % i)
    curMatches = recursiveNearMatcher(l, alternativSpellings)
    if len(curMatches)>0:
        matches.append({"line": i, "matches" : curMatches})

print("%d matches found" % len(matches))
for m in matches:
    if m['matches'][0]['confidence'] > 0.9:
        print(m)

print(alternativSpellings)
        
        
        
           

