import spacy
from spacy.symbols import pobj

#import en_core_web_sm
# import spacy
import re
nlp=spacy.load('en_core_web_sm')
# nlp=spacy.load('en')
#nlp = en_core_web_sm.load()
in_file=open('/home/vivek/Four_Square_tweets/California/cali_all_tweets1','r')
out_file=open('/home/vivek/Four_Square_tweets/spacy_ner_cali1_dep_temp.txt','w')
for tweet in in_file:
    # out_file.write("\n")
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    tweet=emoji_pattern.sub(r'',tweet)  # no emoji
    tweet=tweet.replace('[URL]','')
    tweet=tweet.replace('[NEW LINE]', '')

    if(not '@' in tweet and not 'Click to apply' in tweet and not 'Join' in tweet):
        doc = nlp(tweet)
        l,gpe,loc = "","",""

        for ent in doc.ents:
            if(ent.label_=='GPE'):
                l+=" GPE"+":"+ent.text
                gpe=ent.text
            elif(ent.label_=='FACILITY'):
                l += "FACILITY" + ":" + ent.text
            elif(ent.label_=='ORG' and ent.text.strip()):
                l += " ORG" + ":" + ent.text
            elif(ent.label_=='LOC'):
                l += " LOC" + ":" + ent.text
                loc=ent.text
        if (not l == "" and ('GPE' in l or 'LOC' in l)):
            # tweet = tweet.decode('utf-8')
            # Dependencies
            # Finding a verb with a subject from below — good
            verbs = set()
            for possible_subject in doc:
                if possible_subject.dep == pobj and (str(possible_subject)==loc or str(possible_subject)==gpe): #and possible_subject.head.pos == VERB:
                    #verbs.add(possible_subject.head)
                    print(tweet + l)
                    out_file.write(tweet + l)
                    out_file.write("\n")
                    break

out_file.close()