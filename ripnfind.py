#Recursive Incremental Improving Name Finder
import difflib
import json


with open('unique_lastnames.json') as f:
    words = json.load(f)

words_lower = []
for w in words:
    words_lower.append(w.lower())

names = words_lower#['wilhelm', 'frederiksen','morkebla']#words_lower

alternativSpellings = {}
percentileThredshold = 0.9
cutoffThreshold = 0.7
def recursiveNearMatcher(sentence, names, alternativSpellings, currentPercent = 0.8, currentCutoff = 0.95):
    matches = list()
    
    print("recursive with these settings: %f, %f" % (currentPercent, currentCutoff))
    print("using %d names and %d alternative spellings" % (len(names), len(alternativSpellings)))
    print("sentence %s" % sentence[0:100])

    while len(matches) == 0 and currentPercent < percentileThredshold and currentCutoff > cutoffThreshold:
        for word in sentence.split():
            word = word.lower()
            if len(word)<4:
                continue
            #print(word)

            #Exact match
            if word in names:
                print("exact match: %s" % word)
                matches.append({"match": word, "confidence": 1})
                break

            #Exact match, alternative spellings
            if word in alternativSpellings:
                print("alternative spelling match: %s" % word)
                matches.append({"match": alternativSpellings[word], "confidence": 0.8})
                break
            
            #Close match
            closeMatches = difflib.get_close_matches(word, names,cutoff=currentCutoff)
            if len(closeMatches) > 0:
                print("close match: %s" % closeMatches[0])
                matches.append({"match": closeMatches[0], "confidence": currentCutoff*currentPercent})
                #Add word to alternative spellings
                alternativSpellings[closeMatches[0]] = word
                break
        
        
        currentCutoff = currentCutoff-0.1
        currentPercent = currentPercent+0.0
        
        #No matches, reduced thresholds
        if len(matches) == 0:
            matches = recursiveNearMatcher(sentence, names, alternativSpellings, currentPercent, currentCutoff)

    return matches

print('found %d lines' % len(open('test.txt', encoding="latin-1").readlines()))
i = 0
matches = list()
for l in  open('test.txt', encoding="latin-1").readlines():
    curMatches = list()
    i = i+1
    print("current line %d" % i)
    curMatches = recursiveNearMatcher(l,names, alternativSpellings)
    if len(curMatches)>0:
        matches.append({"line": i, "matches" : curMatches})

print("%d matches found" % len(matches))
for m in matches:
    print(m)

print(alternativSpellings)
        
        
        
           

