file_in=open('/home/vivek/Four_Square_tweets/spacy_ner_cali1_LOC_GPE.txt','r')
file_out=open('/home/vivek/Four_Square_tweets/spacy_ner_cali1_LOC_GPE_train.txt','w')
count=0
while (True):
    # prev=tweet
    tweet=file_in.readline()
    tag=file_in.readline()
    count+=1
    if((count%20)==0):
        print(tweet)
        print(tag)
        file_out.write(tweet)
        file_out.write(tag)
    if (not tag):
        break