

import utilm as util
import csv
import os

DATA_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(DATA_DIR, 'data')
f = open('slovar.txt', 'w')
slovar={}
with open(u'/home/kai/PythonWork/slovar.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='"')
    for row in spamreader:
         print ', '.join(row)
         word=row[0].lower().decode('utf-8').strip()
         pos=row[1].lower().decode('utf-8').strip()
         s = word+" : "+pos
         f.write(s.encode('utf-8')+'\n')

         try:
             # ps=[]
             ps1 = slovar[word]
             ps1.append(pos)
             slovar[word] = ps1
         except:
             ps = []
             ps.append(pos)
             slovar[word] = ps


util.saveslovar(slovar, os.path.join(DATA_DIR,'slovar'))
print "Done"



