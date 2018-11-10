import pandas as pd 
import json

firstnames = []
lastnames = []
data = pd.read_csv("hack4dk_police_person.csv", low_memory=False) 
for l in data['firstnames']:
    if isinstance(l, str): 
        for fname in l.split():
            if fname.find('.') == -1 and fname.find(',') == -1 and fname.find(' ') == -1 and fname.find('-') == -1:
                if fname not in firstnames:
                    firstnames.append(fname)

file = open('firstnames.json', 'w')
file.write(json.dumps(firstnames))
file.close()
i = 0
for l in data['lastname']:
    i = i+1
    if(i%1000 == 0):
        print(i)
    if isinstance(l, str):
        for lname in l.split():
            if lname.find('.') == -1 and lname.find(',') == -1 and lname.find(' ') == -1 and lname.find('-') == -1:
                if lname not in lastnames:
                    lastnames.append(lname)

file = open('lastnames.json', 'w')
file.write(json.dumps(lastnames))
file.close()

print(len(firstnames))
print(len(lastnames))

print(firstnames[0:10])
print(lastnames[0:10])
        