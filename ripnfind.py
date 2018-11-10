#Recursive Incremental Improving Name Finder
import difflib
import json
from collections import Counter
import pandas as pd

person = pd.read_csv("hack4dk_police_person.csv")
# extract all last names
lastnames_col = person.lastname
firstnames_col = person.firstnames

# nr. of occurencies of last names
counter = Counter(lastnames_col)
counter_firstnames = Counter(firstnames_col)
common_first = counter_firstnames.most_common(14000)
common_firstnames = []
for fn in common_first:
    if isinstance(fn[0], str):
        common_firstnames.append(fn[0].lower())


#counter.most_common(20)
common_last = counter.most_common(4000)
common_lastnames = []
for fn in common_last:
    if isinstance(fn[0], str):
        common_lastnames.append(fn[0].lower())

with open('unique_lastnames.json') as f:
   firstnames = json.load(f)


#words_lower = []
#for w in counter.most_common(2500):
#    print(w[0])
#    if isinstance(w[0],str):
#        words_lower.append(w[0].lower())

#names = words_lower#['wilhelm', 'frederiksen','morkebla']#words_lower

alternativSpellings = {}
percentileThredshold = 0.6
cutoffThreshold = 0.5

def recursiveNearMatcher(sentence, alternativSpellings, currentPercent, currentCutoff):
    matches = list()

    words_lower = []
    for w in counter.most_common(int(5000*currentPercent)):
        #print(w[0])
        if isinstance(w[0],str):
            words_lower.append(w[0].lower())
    names = words_lower

    print("recursive with these settings. percent: %f, cutoff: %f" % (currentPercent, currentCutoff))
    print("using %d names and %d alternative spellings" % (len(names), len(alternativSpellings)))
    print("sentence %s" % sentence[0:100])

    # found = False
    # #print(sentence.split())
    # for w in sentence.split():
    #     if len(w)>3 and w in common_firstnames:
    #         found = True
    #         print("found first name %s" % w)
    #         break
    # #        break
    
    # if not found:
    #     print("returning nothing %s" % sentence)
    #     return list()

    while len(matches) == 0 and (currentPercent < percentileThredshold or currentCutoff > cutoffThreshold) and currentCutoff>0 and currentPercent<1:
        #print("HER!!!!!!!!!!!!!!!!! %d,%f,%f" % (len(matches), currentPercent, currentCutoff))
        for word in sentence.split()[0:20]:
            word = word.lower()
            word = word.replace(',','').replace('.','')

            if len(word)<4 or (word in common_firstnames):
                #print("short or firstname found")
                #print(word)
                continue

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
                #Add word to alternative spellings if unknown
                if closeMatches[0] not in common_firstnames and closeMatches[0] not in common_lastnames:
                    alternativSpellings[closeMatches[0]] = word

                break
        
        
        currentCutoff = currentCutoff-0.1
        currentPercent = currentPercent+0.1
        
        #No matches, reduced thresholds
        if len(matches) == 0:
            matches = recursiveNearMatcher(sentence, alternativSpellings, currentPercent, currentCutoff)
            
           
    return matches

print('found %d lines' % len(open('test.txt', encoding="latin-1").readlines()))
i = 0
matches = list()
try:
    for l in  open('test.txt', encoding="latin-1").readlines():
        curMatches = list()
        i = i+1
        print("current line %d" % i)
        curMatches = recursiveNearMatcher(l, alternativSpellings, 0.3, 0.95)
        if len(curMatches)>0:
            matches.append({"line": i, "matches" : curMatches})
except KeyboardInterrupt as k:
    pass
finally:
    with open('alternativSpellings.json', 'w') as outfile:
        json.dump(alternativSpellings, outfile)
    
    with open('matches.json', 'w') as outfile:
        json.dump(matches, outfile)

    print("%d matches found" % len(matches))
    for m in matches:
        #if m['matches'][0]['confidence'] > 0.9:
            print(m)

    print(alternativSpellings)    


        
        
        
           

