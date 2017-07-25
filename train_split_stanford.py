import re
file_in=open('/home/vivek/Four_Square_tweets/stanford_ner_cali1_temp.txt','r')
file_out=open('/home/vivek/Four_Square_tweets/stanford_ner_cali1_cleaned.txt','w')
# count=0
emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

while (True):
    # prev=tweet
    tweet=file_in.readline()
    tag=file_in.readline()
    tweet = emoji_pattern.sub(r'', tweet)  # no emoji
    tweet = tweet.replace('[URL]', '')
    tweet = tweet.replace('[NEW LINE]', '')
    if("@" in tweet.lower() or len(tweet.split(' '))<4 or '#job' in tweet):
        continue
    # count += 1
    # if ((count % 10) == 0):
    print (tweet)
    print (tag)
    file_out.write(tweet)
    file_out.write(tag)
    if(not tag):
        break
file_out.close()

# while (True):
#     # prev=tweet
#     tweet=file_in.readline()
#     tag=file_in.readline()
#
#
#         print(tweet)
#         print(tag)
#         file_out.write(tweet)
#         file_out.write(tag)
#     if (not tag):
#         break