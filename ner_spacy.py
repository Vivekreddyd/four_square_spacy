import spacy
#import en_core_web_sm
# import spacy
import re
nlp=spacy.load('en_core_web_sm')
# nlp=spacy.load('en')
#nlp = en_core_web_sm.load()
in_file=open('/home/vivek/Four_Square_tweets/California/cali_all_tweets1','r')
out_file=open('/home/vivek/Four_Square_tweets/spacy_ner_cali1.txt','w')
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
        l = ""
        for ent in doc.ents:
            if(ent.label_=='GPE'):
                l+=" GPE"+":"+ent.text
            elif(ent.label_=='FACILITY'):
                l += "FACILITY" + ":" + ent.text
            elif(ent.label_=='ORG' and ent.text.strip()):
                l += " ORG" + ":" + ent.text
            elif(ent.label_=='LOC'):
                l += " LOC" + ":" + ent.text
        if (not l == ""):
            # tweet = tweet.decode('utf-8')
            print(tweet + l)
            out_file.write(tweet+l)
            out_file.write("\n")
out_file.close()