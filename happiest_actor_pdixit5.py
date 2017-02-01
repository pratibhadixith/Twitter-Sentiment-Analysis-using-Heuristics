import sys
import csv
import re
from collections import defaultdict,OrderedDict
actorstweets=OrderedDict()
onlytweets=[]
unigrams={}
bigrams={}
trigrams={}
affinwords={}
noftweetsofactorcons=OrderedDict()
finalscoredict=OrderedDict()

def main():
    sent_file = sys.argv[1]
    csv_file = sys.argv[2]
    file_reader = csv.reader(open(csv_file,'r'))
    #TODO: Implement
    # tweetcount=0
    for row in file_reader:
        if row[0] not in actorstweets:
            tweetcount=0
            actorstweets[row[0]]=row[1].lower()
            tweetcount+=1
        else:
            actorstweets[row[0]]=actorstweets[row[0]].lower()+row[1].lower()
            tweetcount+=1
            
        noftweetsofactorcons[row[0]]=tweetcount
    #print (row[0],tweetcount)
    # for k,v in noftweetsofactorcons.items():
        # print (k,v)
        
    
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
    scorelist=[]   
    for actor,eachfilteredtweet in actorstweets.items():
        score=0
       # print (eachfilteredtweet)
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
            unitokens=re.findall(r"[\w']+", eachfilteredtweet)
            for key in unitokens:
                if key in unigrams:
                    score=score+unigrams[key]
                    
                else:
                    pass
        scorelist.append(score)
   
    countlist=[]
    count_actors=[]
    
    for actor,tweecount in noftweetsofactorcons.items():
        countlist.append(noftweetsofactorcons[actor])
        count_actors.append(actor)
    countlist.pop(0)
    scorelist.pop(0)
    count_actors.pop(0)
       
    finalist1 = [s/c for s,c in zip(scorelist,countlist)]   
  
    dictprint=OrderedDict(zip(count_actors,finalist1))
    
    
    for k in sorted(dictprint,key=dictprint.get,reverse=True):
        print (str(dictprint[k])+":"+k)
            
        
            
        

if __name__ == '__main__':
    main()
