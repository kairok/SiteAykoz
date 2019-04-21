import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

import json

from  MorfoKZ import pyMorfkz
morf=pyMorfkz.pyMorfKz()





app = Flask(__name__)


@app.route('/')
def index(name=None):
    return render_template('index.html', name='')



@app.route('/mine/new', methods=['POST'])
def mine():
    values = request.form
    txt=values['textkz']
    sentenses = morf.SentenceExtract(txt)
    out=''
    inn=1
    verb2 = []
    for key in morf.verb2words:
        print(key)
        verb2.append(key + " ")
    for sent in sentenses:
        if len(sent)==0:
            continue
        words = morf.WordExtract(sent)
        out = out +str(inn)+' -> '+ sent + '\n'
        inn+=1
        print(u"Парсинг")
        for word in words:
            ok = 0
            verb = ""
            vb=""
            for vb in verb2:
                if word.lower() + " " in vb:
                    if vb.find(word) == 0:
                        i = words.index(word)
                        verb = vb
                        sl = vb.split(' ')
                        for s in sl:
                            if len(s) > 0:
                                if words[i] in s:
                                    i += 1
                                    ok = 1
                                else:
                                    ok = 0
                                    break

                        if ok == 1:
                            break
            if ok == 1:
                p = 1
                print("{0}  -  {1}".format(vb, morf.verb2words[vb[:len(vb) - 1]]))
                s=vb+ " - "+morf.verb2words[vb[:len(vb) - 1]]
                out = out + s + '\n'
            m = morf.parse(word, 1)
            for t in m:
                ok = 1
                print(t['token'] + ' | ' + t['norm_word'] + ' <' + t['tag'] + ' | ' + t['tagrus'] + '>')
                try:
                    s=t['token'] + ' | ' + t['norm_word'] + ' <' + t['tag']  + '>'+' <'+t['analitic']+'>'
                except:
                    s = t['token'] + ' | ' + t['norm_word'] + ' <' + t['tag']
                out = out + s + '\n'

    ok=1
    return render_template('index.html',text=txt, name=out)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
