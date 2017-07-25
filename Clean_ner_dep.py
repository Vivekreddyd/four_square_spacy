# clean spacy related tweets

file_in=open('/home/vivek/Four_Square_tweets/spacy_ner_cali1_dep.txt','r')
file_out=open('/home/vivek/Four_Square_tweets/spacy_ner_cali1_dep_LOC_GPE.txt','w')
while (True):
    # prev=tweet
    tweet=file_in.readline()
    tag=file_in.readline()
    if("hiring" in tweet.lower() or len(tweet)<4 or tag.strip()=="GPE:" or tag.strip()=="LOC:"):
        continue
    if("LOC" in tag or "GPE" in tag):
        print (tweet)
        print (tag)
        file_out.write(tweet)
        file_out.write(tag)
    if(not tag):
        break
file_out.close()