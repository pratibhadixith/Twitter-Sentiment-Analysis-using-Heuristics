import sys
import json
import re
from collections import defaultdict,OrderedDict
from collections import Counter
states=OrderedDict()
stateAndtweets=OrderedDict()
unigrams={}
bigrams={}
trigrams={}
affinwords={}

def main():
    sent_file = sys.argv[1]
    tweet_file = sys.argv[2]
    #TODO: Implement
    statesmap=OrderedDict({ 'AL': 'Alabama',
    'AK': 'Alaska',
    'AS': 'American Samoa',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'DC': 'District Of Columbia',
    'FM': 'Federated States Of Micronesia',
    'FL': 'Florida',
    'GA': 'Georgia',
    'GU': 'Guam',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MH': 'Marshall Islands',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'MP': 'Northern Mariana Islands',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PW': 'Palau',
    'PA': 'Pennsylvania',
    'PR': 'Puerto Rico',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VI': 'Virgin Islands',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming'}) 
    
    expndtoabr=OrderedDict({
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District Of Columbia': 'DC',
    'Federated States Of Micronesia': 'FM',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Marshall Islands': 'MH',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands': 'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Palau': 'PW',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
  })
    abbrstates=[]
    expndstates=[]
    
    
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
            
            
    for k,v in statesmap.items():
        abbrstates.append(k)
        expndstates.append(v)
    #print (abbrstates)
    #print ("----------------------")
        
    tweetstates=[]
    with open(tweet_file,'r') as tfileinput:
        for line in tfileinput:
            tweet=json.loads(line)
            if tweet['lang']=='en':
                if tweet['place']!=None:
                    if tweet['place']['country']!=None:
                        if tweet['place']['country']=='United States':
                            if tweet['place']['full_name'] !=None:
                                #print (tweet['place']['full_name'])
                                stateAndtweets[tweet['place']['full_name']]=tweet['text']
                                
                elif tweet['user']['location']!=None:
                    if tweet['user']['location']in abbrstates:
                        if tweet['user']['location'] not in stateAndtweets:
                            stateAndtweets[tweet['user']['location']]=tweet['text']
                        else: 
                            stateAndtweets[tweet['user']['location']]= stateAndtweets[tweet['user']['location']]+"|||"+tweet['text']
                       # print (tweet['user']['location']+"^^^^"+tweet['text'])
                    elif tweet['user']['location'] in expndstates:
                        if tweet['user']['location'] not in stateAndtweets:
                            stateAndtweets[tweet['user']['location']]=tweet['text']
                        else:
                            stateAndtweets[tweet['user']['location']]= stateAndtweets[tweet['user']['location']]+"|||"+tweet['text']
                            # #print (tweet['user']['location']+"--"+tweet['text'])
                        
                        
                                        
    # for k,v in stateAndtweets.items():
        # print (k,v)
        
    dirtystates=[]
    cleanstates=[]
    dirtytweets=[]
    for k,v in stateAndtweets.items():
        dirtystates.append(k)
        dirtytweets.append(v)
   # print (len(dirtystates))
        
    for line in dirtystates:
        if ',' not in line:
            for keys in expndtoabr:
                if keys in line:
                    cleanstates.append(expndtoabr[keys].lstrip())
            for keys in statesmap:
                if keys in line:
                    cleanstates.append(keys.lstrip())
        elif ',' in line:
            splitwords=line.split(',')
            if splitwords[1]!=' USA':
                cleanstates.append(splitwords[1].lstrip())
            else:
                for keys in expndtoabr:
                    if keys in splitwords[0]:
                        cleanstates.append(expndtoabr[keys].lstrip())
        else:
            #print (line)
            pass
            #cleanstates.append(line.lstrip())
                  
    # print (len(dirtystates))
    #print (len(cleanstates))
    filteredDict=OrderedDict()
    
    for state,tweet in zip(cleanstates, dirtytweets):
        if state not in filteredDict:
            filteredDict[state]=tweet
        elif state in filteredDict:
            filteredDict[state]=filteredDict[state]+"|||"+tweet
          
    nonredundantstates=[]
    for k,v in filteredDict.items():
       # print (k+"------->"+v)
        nonredundantstates.append(k)
       
        
   
    
    
    
    scorelist=[]   
    for state,eachfilteredtweet in filteredDict.items():
        score=0
        tweetcount=0
        orgtweet=eachfilteredtweet
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
        tweetcount=orgtweet.count('|||')+1
        #print (tweetcount)
        scorelist.append(score/tweetcount)
    # print (scorelist)
    Dictoprint=OrderedDict(zip(nonredundantstates,scorelist))
    
    
    for k in sorted(Dictoprint,key=Dictoprint.get,reverse=True):
        print (str(Dictoprint[k])+":"+k)
           
        
                
                
    
                                        
                                
                                    
                                    
                                    
                               
                                
                            

if __name__ == '__main__':
    main()
