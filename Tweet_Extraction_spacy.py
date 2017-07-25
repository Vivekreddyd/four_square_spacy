from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import re
import string
import os

# Import the necessary package to process data in JSON format
import re
import csv
import spacy
nlp=spacy.load('en_core_web_sm')
from spacy.symbols import pobj
from nltk.tag import StanfordNERTagger
st = StanfordNERTagger('/local/vivek/Downloads/Stanford /stanford-ner-2016-10-31/classifiers/english.all.3class.distsim.crf.ser.gz','/local/vivek/Downloads/Stanford /stanford-ner-2016-10-31/stanford-ner.jar')
try:
    import json
except ImportError:
    import simplejson as json
tweet_id=0
noise_words=['hiring','click to apply','join','job','earthquake','forecast','weather','checkpointalert','@']
emoji_pattern = re.compile("["
                            u"\U0001F600-\U0001F64F"  # emoticons
                            u"\u2700-\u27BF"  # Dingbats
                            u"\U0001F30D-\U0001F567"  #Other additional symbols
                            u"\u24C2-\U0001F251"  # Enclosed characters
                            u"\U0001F600-\U0001F64F"  # Additional emoticons
                            u"\U0001F300-\U0001F5FF"  # Other Characters
                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
                            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
# We use the file saved from last step as example
new_path='/home/vivek/Four_Square_tweets/California/all_tweets/'
csv_file=open(os.path.join(new_path,"cali_all_tweets_final_test"),"w")
#CSV writer
tweets_new_file=csv.writer(csv_file,delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)

#tweets_new_file = open(os.path.join(new_path,"cali_all_tweets_final_test"), "w")
for root, dirs, files in os.walk('/home/vivek/Four_Square_tweets/California'):
    for file in files:
        with open(os.path.join(root,file),"r") as tweets_file:
            #tweets_filename = '/home/vivek/tweepy_dataset/trip.009.txt'
            # tweets_new_file = open(os.path.join(new_path,"all_tweets"), "w")
            prev_line=None
            for line in tweets_file:
                try:
                    # Read in one line of the file, convert it into a json object
                    tweet = json.loads(line.strip())
                    #print tweet['text'] # content of the tweet
                    if 'text' in tweet: # only messages contains 'text' field is a tweet
                        #print tweet['id'] # This is the tweet's id
                        #print tweet['created_at'] # when the tweet posted
                        line = tweet['text']
                        lang = tweet['lang']
                        # place= tweet['place']
                        # language=tweet['lang']
                        #if(place["place_type"]=="poi" and language=='en'):
                        # Delete the tweet if it is a retweet
                        if 'RT' in line or not lang=='en': #or not '#travel' in line:
                             continue
                        if any(word in line for word in noise_words):
                            continue
                        #clean_line=re.sub('#.* ?','',line)
                        clean_line=line
                        clean_line = emoji_pattern.sub(r'', clean_line)  # no emoji
                        #print clean_line
                        # Replace the https with [URL]
                        clean_line1 = re.sub('(\n)', ' ', clean_line)
                        clean_line1=re.sub('(https:\/\/t\.co.*?( |\t|\n|\r|\f|\v|$))','',clean_line1)
                        #printable = set(string.printable)
                        #clean_line2=filter(lambda x: x in printable, clean_line1)
                        clean_line2=clean_line1
                        length=len(clean_line2)
                        if (len(clean_line2.split())<3):
                            continue
                        #print clean_line2

                        ######################
                        ##Spacy NER
                        doc = nlp(clean_line2)
                        l = ""
                        gpe_loc_text=[]
                        l_index={}
                        # l_end = ""
                        gpe, loc = [], []
                        for ent in doc.ents:
                            if (ent.label_ == 'GPE'):
                                l += " GPE" + ":" + ent.text
                                gpe_loc_text.append(ent.text)
                                temp=ent.text.split(' ')
                                for k in temp:
                                    if(not k in l_index):
                                        l_index[k]=[(ent.start,ent.end)]
                                    else:
                                        l_index[k].append([(ent.start,ent.end)])
                                gpe.extend(temp)
                            elif (ent.label_ == 'FACILITY'):
                                l += "FACILITY" + ":" + ent.text
                            elif (ent.label_ == 'ORG' and ent.text.strip()):
                                l += " ORG" + ":" + ent.text
                            elif (ent.label_ == 'LOC'):
                                l += " LOC" + ":" + ent.text
                                gpe_loc_text.append(ent.text)
                                temp = ent.text.split(' ')
                                for k in temp:
                                    if(not k in l_index):
                                        l_index[k]=[(ent.start, ent.end)]
                                    else:
                                        l_index[k].append([(ent.start,ent.end)])
                                loc.extend(temp)
                        #################
                        if (not l == ""):
                            ######################
                            ##Stanford NER
                            text = st.tag(clean_line2.split())
                            #################
                            l1 = ""
                            loc_standford=[]
                            loc_index=[]
                            for i in text:
                                # word,ner=i.split(',')
                                if ('ORGANIZATION' == i[1]):
                                    l1 += " " + i[1] + ":" + i[0]
                                elif ('LOCATION' == i[1]):
                                    l1 += " " + i[1] + ":" + i[0]
                                    if(i[0] in l_index):
                                        if(i[0] in loc_standford):
                                            loc_index.append(l_index[i[0]][1])
                                        else:
                                            loc_index.append(l_index[i[0]][0])
                                    else:
                                        loc_index.append('')
                                    loc_standford.append(i[0])
                            for indx,j in enumerate(loc_standford):
                                if(j in gpe or j in loc):
                                    for delindex, entity in enumerate(gpe_loc_text):  ## To make sure that the sentence is only written to file only once for "Santa Cruz"
                                        if (j in str(entity)):
                                            del gpe_loc_text[delindex]
                                            x,y=tuple(loc_index[indx])
                                            tweet_id += 1
                                            tweet_temp=str(tweet_id)+":"+str(x)+"-"+str(y)
                                            tweets_new_file.writerow([str(tweet_id),tweet_temp,str(line)])  # +"::"+str(place["name"]))
                                            # tweets_new_file.write("\n")
                                            # tweet_id += 1
                                            tweets_new_file.writerow([str(tweet_id),tweet_temp,str(clean_line2.encode('utf8'))])#+"::"+str(place["name"]))
                                            # tweets_new_file.write("\n")
                                            # tweet_id += 1
                                            tweets_new_file.writerow([str(tweet_id),tweet_temp,str(l)])  # +"::"+str(place["name"]))
                                            # tweets_new_file.write("\n")
                                            # tweet_id += 1
                                            tweets_new_file.writerow([str(tweet_id),tweet_temp,str(l1)])  # +"::"+str(place["name"]))
                                            # tweets_new_file.write("\n")
                                            print (line)
                                            print (clean_line2)#+"::"+str(place["name"])
                                            # break

                        #clean_line2=re.compile("["u"\U0001F600-\U0001F64F"u"\U0001F300-\U0001F5FF"u"\U0001F680-\U0001F6FF"u"\U0001F1E0-\U0001F1FF""]+", flags=re.UNICODE)
                        #print (clean_line2.sub(r'', clean_line1))

                        #print tweet['text'] # content of the tweet
                        #print tweet['user']['id'] # id of the user who posted the tweet
                        #print tweet['user']['name'] # name of the user, e.g. "Wei Xu"
                        #print tweet['user']['screen_name'] # name of the user account, e.g. "cocoweixu"

                    '''hashtags = []
                        for hashtag in tweet['entities']['hashtags']:
                            hashtags.append(hashtag['text'])
                        #print hashtags'''

                except:
                    # read in a line is not in JSON format (sometimes error occured)
                    continue
                prev_line=line
tweets_new_file.close()