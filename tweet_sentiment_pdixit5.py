import sys
import json
import re
from collections import defaultdict,OrderedDict
from collections import Counter
affinwords={}
terms_all=[]
tweetscore=OrderedDict()
unigrams={}
bigrams={}
trigrams={}


def main():
    sent_file = sys.argv[1]
    tweet_file = sys.argv[2]
    #TODO: Implement
    
    with open(tweet_file,'r') as tfileinput:
        for line in tfileinput:
            tweet=json.loads(line)
            if tweet['lang']=='en':
                terms_all.append(tweet['text'].lower())
                
    with open(sent_file,'r') as afileinput:
        for line in afileinput:
            term, score = line.split("\t") 
            affinwords[term] = float(score)
    
    for term,score in affinwords.items():
        if term.count(' ')==2:
            trigrams[term]=score
        elif term.count(' ')==1:
            bigrams[term]=score
        else:
            unigrams[term]=score
            
    #print (bigrams)
    #print (trigrams)
    
    
    for eachfilteredtweet in terms_all:
            orgtweet=eachfilteredtweet
            score=0
            unitokens=[]
            uniwords=[]
            for key in trigrams:
                if key in eachfilteredtweet:
                    score=score+trigrams[key]
                    splitwords=key.split()
                    eachfilteredtweet.replace(splitwords[0],"")
                    eachfilteredtweet.replace(splitwords[1],"")
                    eachfilteredtweet.replace(splitwords[2],"")
            for key in bigrams:
                if  key in eachfilteredtweet:
                    score=score+bigrams[key]
                    splitwords=key.split()
                    eachfilteredtweet.replace(splitwords[0],"")
                    eachfilteredtweet.replace(splitwords[1],"")
            #uniwords=eachfilteredtweet.split() 
            unitokens=re.findall(r"[\w']+", eachfilteredtweet)
            for key in unitokens:
                if key in unigrams:
                    score=score+unigrams[key]
                    
                else:
                    pass
                    
            tweetscore[orgtweet]=score
            #print (orgtweet,score)
            
    printtop10=0       
    for v in sorted(tweetscore,key=tweetscore.get,reverse=True):
        if printtop10<10:
            print (tweetscore[v],v)
            printtop10+=1
    
    printbot10=0
    for v in sorted(tweetscore,key=tweetscore.get):
        if printbot10<10:
            print (tweetscore[v],v)
            printbot10+=1
                    
if __name__ == '__main__':
    main()
