# -*- coding: utf-8 -*-




filename=u'D:\slovarkz.txt'

f = open(filename)
text = ''
slovar = {}
for line in f:
    s = line.decode('utf-8').strip()
    if len(s.strip()) == 0:
        continue
    k=s.index('.')+1
    try:
        w=s[k:]
        sw=w.split('/')
        word=sw[0].strip()
        pos=sw[1].strip()
        k = pos.find('.')
        if k>0:
            pos=pos[:-1]
        ok=1
        print word
        try:
            # ps=[]
            ps1=slovar[word]
            ps1.append(pos)
            slovar[word]=ps1
        except:
            ps=[]
            ps. append(pos)
            slovar[word]=ps


    except:
        print "Error!"
        break



import pickle
file='slovarR'
output = open(file, 'wb')
pickle.dump(slovar, output)
output.close()
