import sys
import json
import re
from collections import Counter
from collections import defaultdict,OrderedDict
finaldict={}
    
def main():
    stopwords_file= sys.argv[1]
    tweets_file = sys.argv[2]
  #  print (tweets_file)
    terms_all=[]
    finaltokens=[] 
    finalfilteredtokens=[]
    stopwords=[]
   

        
    with open(tweets_file,'r') as tfileinput:
        for line in tfileinput:
            tweet=json.loads(line)
            if tweet['lang']=='en':
                terms_all.append(tweet['text'])
        
    
    
    for line in terms_all:
        linelowcase = line.lower()
        linetokens=linelowcase.split()
           # print (linetokens)
        for word in linetokens:
            dividedlinetokens=re.split(';|:|_|,|\*|\n|\|/|"|\\|\\\|//|///|\\\/',word)
            for entry in dividedlinetokens:
                tokens=entry.split('.')
                for eachtoken in tokens:
                    if eachtoken.isalnum():
                        finaltokens.append(eachtoken)
                            
    #print (finaltokens)
    
    with open(stopwords_file,'r') as fileinput:
        for eachstopword in fileinput:
            stopwords.append(eachstopword.strip())
    
    #print (stopwords)
    

    for eachfinaltoken in finaltokens:
            if eachfinaltoken.lower() in stopwords:
                #print (eachfinaltoken,stopwords)
                pass
            else:
                finalfilteredtokens.append(eachfinaltoken)
    
    filterwords=[]
    filterwordsfreq=[]
    sumallfreq=len(finalfilteredtokens)
    #print (sumallfreq)
    
    
    #----------------------------------------
    terms=[]
    values=[]
    termvalues=OrderedDict() 
    #termvalues=OrderedDict()
    x = Counter(finalfilteredtokens)
    total = sum(x.values(), 0.0)
    for key in x:
        x[key] /= total
       

    
    for k in sorted(x,key=x.get,reverse=True):
        print (k,x[k])
            

                    

if __name__ == '__main__':
    main()
