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
counter_firstnames = Counter(firstnames_col)
common_firstnames = []
for fn in counter_firstnames.most_common(14000):
    if isinstance(fn[0], str):
        common_firstnames.append(fn[0].lower())

counter = Counter(lastnames_col)
common_lastnames = []
for fn in counter.most_common(4000):
    if isinstance(fn[0], str):
        common_lastnames.append(fn[0].lower())

#with open('unique_lastnames.json') as f:
#   firstnames = json.load(f)

alternativSpellings = {}
percentileThredshold = 0.6
cutoffThreshold = 0.75

def recursiveNearMatcher(sentence, alternativSpellings, namesCounter, stopWords, currentPercent, currentCutoff):
    matches = list()

    if len(sentence)<15:
        return matches

    #Get the most common names based on currentPercent
    words_lower = []
    for w in namesCounter.most_common(int(len(namesCounter)*currentPercent)):
        if isinstance(w[0],str):
            words_lower.append(w[0].lower())
    names = words_lower

    #print("recursive with these settings. percent: %f, cutoff: %f\nusing %d names and %d alternative spellings\nsentence %s" % (currentPercent, currentCutoff,len(names), len(alternativSpellings),sentence[0:50]))
   # print("using %d names and %d alternative spellings" % (len(names), len(alternativSpellings)))
   # print("sentence %s" % sentence[0:50])

    while len(matches) == 0 and (currentPercent < percentileThredshold or currentCutoff > cutoffThreshold) and currentCutoff>0 and currentPercent<1:
        #print("HER!!!!!!!!!!!!!!!!! %d,%f,%f" % (len(matches), currentPercent, currentCutoff))
        for word in sentence.split()[0:20]:
            word = word.lower()
            word = word.replace(',','').replace('.','')

            if len(word)<4 or (word in stopWords):
                #print("short or firstname found")
                #print(word)
                continue

            #Exact match
            if word in names:
                print("\rexact match: %s" % word, end ="")
                matches.append({"match": word, "confidence": 1-currentPercent, "sentence": sentence})
                break

            #Exact match, alternative spellings
            if word in alternativSpellings:
                print("\ralternative spelling match: %s" % word, end =" ")
                matches.append({"match": alternativSpellings[word], "confidence": 1-currentPercent-0.2, "sentence": sentence})
                break
            
            #Close match
            closeMatches = difflib.get_close_matches(word, names,cutoff=currentCutoff)
            if len(closeMatches) > 0:
                print("\rclose match: %s" % closeMatches[0], end =" ")
                matches.append({"match": closeMatches[0], "confidence": currentCutoff*(1-currentPercent), "sentence": sentence})
                #Add word to alternative spellings if unknown
                if closeMatches[0] not in common_firstnames and closeMatches[0] not in common_lastnames:
                    alternativSpellings[closeMatches[0]] = word

                break
        
        
        #If no matches, reduce thresholds
        currentCutoff = currentCutoff-0.1
        currentPercent = currentPercent+0.1
        
        if len(matches) == 0:
            matches = recursiveNearMatcher(sentence, alternativSpellings, namesCounter, stopWords, currentPercent, currentCutoff)
            
           
    return matches

print('found %d lines' % len(open('test.txt', encoding="latin-1").readlines()))
i = 0
matches = list()
try:
    for l in  open('test.txt', encoding="latin-1").readlines():
        curMatches = list()
        i = i+1
        print("current line %d" % i)
        curMatches = recursiveNearMatcher(l, alternativSpellings, counter, common_firstnames, 0.3, 0.95)
        if len(curMatches)>0:
            matches.append({"line": i, "matches" : curMatches})
except KeyboardInterrupt as k:
    pass
finally:
    with open('alternativSpellings.json', 'w') as outfile:
        json.dump(alternativSpellings, outfile)
    
    with open('matches.json', 'w') as outfile:
        json.dump(matches, outfile)

    print("\r%d matches found" % len(matches),end="")
    for m in matches:
        #if m['matches'][0]['confidence'] > 0.9:
            print(m)

    print(alternativSpellings,end="")    
    print("found %d matches" % len(matches),end="")

completeMatches = list()
persons = list()
try:
    for m in matches:
        curMatches = list()
        i = i+1
        print("\rcurrent line %d" % i,end="")
        curMatches = recursiveNearMatcher(m['matches'][0]['sentence'], alternativSpellings, counter_firstnames, common_lastnames, 0.3, 0.95)
        if len(curMatches)>0:
            completeMatches.append({"line": i, "matches" : curMatches})
            persons.append({
                'line': m['line'],
                'matchLastname': m['matches'][0]['match'],
                'lastnameConf': m['matches'][0]['confidence'],
                'matchFirstname': curMatches[0]['match'],
                'firstnameConf': curMatches[0]['confidence']
            })
except KeyboardInterrupt as k:
    pass
finally:
    for m in persons:
        #if m['matches'][0]['confidence'] > 0.9:
        print(m)

        
        
        
           

