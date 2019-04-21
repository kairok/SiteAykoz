# -*- coding: utf-8 -*-

import re


class tokeniz:
    re_non_word_chars = r"(?:[?!)\";}\]\*:@\'\({\[])"
    punctuation=[',','.','!','?','[',']','{','}','"','\'','(',')','-'] #,'\«','\»'
    """Characters that cannot appear within words"""

    def extract_punct(self, word,spis):
        #spis=[]
        if word[0] in self.punctuation:
            spis.append(word[0])
            word=word[1:]
        if word[len(word)-1] in self.punctuation:
            # add word
            spis.append(word[:len(word)-1])
            # add end punct word
            spis.append(word[len(word)-1])
            return spis
        spis.append(word)
        return spis


    def word_tokenize(self, text):
        text=text.replace('\n',' ')
        s=text.split()
        mure=re.compile(r'(\w+)([,;()\.!?"\'«»:])?',re.UNICODE)
        s3=mure.split(text)
        listwords = []
        for i in range(len(s3)-1):
            k=s3[i]
            if s3[i] is None:
                #s3.pop(i)
                continue
            if s3[i].strip()=='':
                #s3.pop(i)
                continue
            if len(s3[i].strip()) == 0:
                # s3.pop(i)
                continue
            if len(k) == 0:
                # s3.pop(i)
                continue
            listwords.append(s3[i])

        #s4=re.split('(\W+)', text)
       # listwords=[]
       # for word in s:
        #    listwords=self.extract_punct(word,listwords)

     #  ok=1
        return listwords


