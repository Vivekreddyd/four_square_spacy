import time
import re
import string
import os
import pandas as pd
from nltk.tag import StanfordNERTagger
# Import the necessary package to process data in JSON format
import re
import csv
import spacy
nlp=spacy.load('en_core_web_sm')
# st = StanfordNERTagger('/local/vivek/Downloads/Stanford /stanford-ner-2016-10-31/classifiers/english.all.3class.distsim.crf.ser.gz','/local/vivek/Downloads/Stanford /stanford-ner-2016-10-31/stanford-ner.jar')
from Clean_tweet import clean
df=pd.DataFrame()
files_list=[]

def Extract_Features():
    path='/home/vivek/Desktop/Thesis/Vivek/eduardoblanco-Vivek/Notebooks/Adjudicated/'
    for input_file in os.listdir(path):
        adj_file = pd.read_csv(path+input_file,header=None,names=['Tweet_ID','Loc','Tweet','bgt_A1','bgt_A2','bgt_Ad','bgt_R','blt_A1','blt_A2','blt_Ad','blt_R','dur_A1','dur_A2','dur_Ad','dur_R','alt_A1','alt_A2','alt_Ad','alt_R','agt_A1','agt_A2','agt_Ad','agt_R'],skiprows=3)
        files_list.append(adj_file)
    df = pd.concat(files_list)
    print(df.shape)


    df_tweet_labels  = pd.DataFrame(df.iloc[::4,5::4])
    df_cleaned_tweet = pd.DataFrame(df.iloc[::4,:3])
    # df_with_features = pd.DataFrame(df.iloc[::])
    # print(df_cleaned_tweet.head())
    # df_cleaned_tweet['Tweet']=df_cleaned_tweet['Tweet'].bytes.decode("utf-8")
    # print(df_cleaned_tweet.head())

    # print(df_cleaned_tweet[])
    tweet_pron, tweet_location,tweet_verb,tweet_verb_tag,tweet_time=[],[],[],[],[]

    loc_start,loc_end,loc_spacy, loc_token=[],[],[],[]

    othr_loc_same_sentence,othr_loc_pron,othr_dist_loc_pron,othr_person,othr_url_hashtag,othr_temporal,othr_tweet_count=[],[],[],[],[],[],[]
    temp_pron=4
    pronoun_arr1=['i','we']
    pronoun_arr2=['you']
    pronoun_arr3=['he','she','it','they','him','her','them']
    pron_reached=False

    ################# Features ############################

    #Location : NE Type from Spacy
                #NE Type from CoreNLP
                # Number of tokens
    #Pronoun  : Word and POS Tag
                #Is_first token / Is_second token / first 25 % of the token

    # Other   : Location in the same sentence as the pronoun
                # Locaition before / After Pronoun
                # Tokens between lcoation and pronoun
                # Does tweet have a person NE
                # has URL, Has # ?
                # has temporal clue (Present, past, Future)
                #



    ############## End of Features ########################
    for index,row in df_cleaned_tweet.iterrows():
        tweet_time_val,tweet_verb_tag_val,tweet_verb_val, loc_spacy_val,loc_corenlp_val='','','','',''
        cleaned_tweet=clean(row['Tweet'])
        # text = st.tag(cleaned_tweet.split())
        doc=nlp(cleaned_tweet)
        loc_reached=False
        loc=row['Loc'].split(':')[1].split("-")
        location=row['Tweet'].split(" ")
        loc_start.append(loc[0])
        loc_end.append(loc[1])
        tweet_length=len(cleaned_tweet.split(' '))
        for indx,word in enumerate(doc):
            #####Location of the tweet#####
            if(indx in range(int(loc[0]),int(loc[1])) and loc_reached==False):
                loc_reached=True
                tweet_pron.append(temp_pron)
                loc_spacy_val=word.text.lower()
                loc_token.append(int(loc[1])-int(loc[0])-1)
                if(indx in range(1,3)):
                    loc_presence=indx
                elif(indx in range(0,int(abs(tweet_length/4)))):
                    loc_presence=3 # Here 3 represents the pronoun is in top 25% of the tweet
            #####Location of the tweet#####

            #### Extract the closest pronoun (first:0, Second:1, Third:2, Others: 3)####
            if (word.pos_ == 'PRON' and pron_reached==False):
                pron_reached=True
                if(loc_reached==False):
                    if(word.text.lower() in pronoun_arr1):
                        temp_pron=0
                    elif(word.text.lower() in pronoun_arr2):
                        temp_pron=1
                    elif(word.text.lower() in pronoun_arr3):
                        temp_pron=2
                    else:
                        temp_pron=3
                pron_word=word.text.lower()
                pron_tag=word.tag_

            #### Extract the closest pronoun####

            ######## Extract the Verb########
            if(pron_reached==True):
                pron_reached==False
                if(word.pos_=='VERB'):
                    # tweet_verb_tag.append(word.tag_)
                    # tweet_verb.append(word.text.lower())
                    tweet_verb_tag_val = word.tag_
                    tweet_verb_val=word.text.lower()
            ######## End of Extract the Verb########

            ######## Extract the Date/Time Entity########
            if(loc_reached==True):
                if(word.ent_type_=='DATE' or word.ent_type_=='TIME'):
                    # tweet_time.append(word.text.lower())
                    tweet_time_val=word.text.lower()
            ######## Extract the Date/Time Entity########


        # if(not len(tweet_time)==indx+1):
            # tweet_time.append('')
        # if(not len(tweet_verb_tag)==indx+1):
            # tweet_verb_tag.append('')
        # if (not len(tweet_verb) == indx + 1):
            # tweet_verb.append('')
        # if (not len(tweet_location) == indx + 1):
            # tweet_location.append('')
        # if (not len(tweet_time) == indx + 1):
            # tweet_verb.append('')
        tweet_time.append(tweet_time_val)
        tweet_verb.append(tweet_verb_val)
        tweet_verb_tag.append(tweet_verb_tag_val)
        loc_spacy.append(loc_spacy_val)
    df_cleaned_tweet['loc_spacy'] = loc_spacy
    df_cleaned_tweet['loc_spacy'] = df_cleaned_tweet['loc_spacy'].astype('category')
    df_cleaned_tweet['tweet_time']     = tweet_time
    df_cleaned_tweet['tweet_time']     = df_cleaned_tweet['tweet_time'].astype('category')
    df_cleaned_tweet['tweet_verb']     = tweet_verb
    df_cleaned_tweet['tweet_verb']     = df_cleaned_tweet['tweet_verb'].astype('category')
    df_cleaned_tweet['tweet_verb_tag'] = tweet_verb_tag
    df_cleaned_tweet['tweet_verb_tag'] = df_cleaned_tweet['tweet_verb_tag'].astype('category')
    # df_cleaned_tweet['loc_token']      = loc_token



    print(len(tweet_verb))
    print(len(tweet_time))
    print(len(tweet_verb_tag))
    print(df_tweet_labels.head())
            # print(type(row['Loc']))
            # print(type(row['Tweet']))
            # print(row['Tweet'])
            # temp_row=str(row['Tweet'])
            # print(temp_row)
            # print(row['Tweet'].decode('utf-8'))
    return df_cleaned_tweet,df_tweet_labels
