import time
import re
import string
import os
import pandas as pd
# from nltk.tag import StanfordNERTagger
from sklearn.feature_extraction import DictVectorizer
# Import the necessary package to process data in JSON format
import re
import csv
import spacy
from Clean_tweet import clean
from Verb_tense import *
# import en_core_web_sm
# nlp=en_core_web_sm.load()
nlp=spacy.load('en_core_web_sm')
# st = StanfordNERTagger('/local/vivek/Downloads/Stanford /stanford-ner-2016-10-31/classifiers/english.all.3class.distsim.crf.ser.gz','/local/vivek/Downloads/Stanford /stanford-ner-2016-10-31/stanford-ner.jar')
df=pd.DataFrame()
files_list=[]

vect=DictVectorizer()

def Extract_Features():
    path='/home/vivek/Four_Square_tweets/Annotations/Adjudicated_final/'
    for input_file in os.listdir(path):
        adj_file = pd.read_csv(path+input_file,header=None,names=['Tweet_ID','Loc','Tweet','bgt_A1','bgt_A2','bgt_Ad','bgt_R','blt_A1','blt_A2','blt_Ad','blt_R','dur_A1','dur_A2','dur_Ad','dur_R','alt_A1','alt_A2','alt_Ad','alt_R','agt_A1','agt_A2','agt_Ad','agt_R'],skiprows=3)
        files_list.append(adj_file)
    df = pd.concat(files_list,ignore_index=True)
    # print (df)
    # print(df.shape)

    # df_corenlp=
    # df_spacy=

    spacy_dict = df.iloc[2::4,2].to_dict()
    corenlp_dict = df.iloc[3::4, 2].to_dict()
    df_tweet_labels  = pd.DataFrame(df.iloc[::4,5::4])
    # print (df_tweet_labels)
    # print (df_tweet_labels.shape)
    df_cleaned_tweet = pd.DataFrame(df.iloc[::4,:3])
    # print (df_cleaned_tweet)
    # print (df_cleaned_tweet.shape)
    # df_with_features = pd.DataFrame(df.iloc[::])
    # print(df_cleaned_tweet.head())
    # df_cleaned_tweet['Tweet']=df_cleaned_tweet['Tweet'].bytes.decode("utf-8")
    # print(df_cleaned_tweet.head())

    # print(df_cleaned_tweet[])
    loc_start, loc_end, loc_spacy, loc_corenlp, loc_token, location_text = [], [], [], [], [], []

    pron_word,pron_tag,pron_first,pron_second,pron_quarter,pron_count=[],[],[],[],[],[]

    tweet_pron, tweet_location,tweet_verb,tweet_verb_tag,tweet_time=[],[],[],[],[]

    othr_loc_same_sentence,othr_loc_pron,othr_dist_loc_pron_max,othr_dist_loc_pron_avg,othr_dist_loc_pron_min,othr_person,othr_url,othr_hashtag,othr_temporal,othr_tweet_count,othr_tense=[],[],[],[],[],[],[],[],[],[],[]

    temp_pron=4
    pronoun_arr1=['i','we']
    pronoun_arr2=['you']
    pronoun_arr3=['he','she','it','they','him','her','them']


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
        othr_dist_loc_pron_val=0
        pron_count_val=0
        othr_dist_loc_pron_avg_val,othr_dist_loc_pron_max_val,othr_dist_loc_pron_min_val=0,0,1000
        othr_tense_val=''
        pron_reached_token_val,loc_reached_val=[],[]
        pron_reached = False
        pron_first_val, pron_second_val, pron_quarter_val = False,False,False
        cleaned_tweet=clean(row['Tweet'])
        # text = st.tag(cleaned_tweet.split())
        doc=nlp(cleaned_tweet)
        loc_reached=False
        loc=row['Loc'].split(':')[1].split("-")
        loc_spacy_text=''
        # print(doc.sents[0])

        ###################### Extract has URL, Hashtag ################
        URL_regexp = re.compile(r'(https:\/\/t\.co.*?( |\t|\n|\r|\f|\v|$))')
        if URL_regexp.search(row['Tweet']):
            othr_url.append(True)
        else:
            othr_url.append(False)
        Hashtag_regexp = re.compile('\#')
        if Hashtag_regexp.search(row['Tweet']):
            othr_hashtag.append(True)
        else:
            othr_hashtag.append(False)
        ###################### Extract has URL, Hashtag ################
        # location=row['Tweet'].split(" ")
        loc_start.append(loc[0])
        loc_end.append(loc[1])
        tweet_length=len(cleaned_tweet.split(' '))
        loc_token.append(int(loc[1]) - int(loc[0]))
        ########### Extracting spacy, CoreNLP NER type#############
        # if(index==4628):
        #     print("")

        ########### Extracting spacy, CoreNLP NER type#############
        for indx,word in enumerate(doc):
            #####Location of the tweet#####
            if(indx in range(int(loc[0]),int(loc[1]))):
                loc_reached=True
                tweet_pron.append(temp_pron)
                loc_reached_val.append(indx)
                loc_spacy_text+=word.text+' '
                # for ent in doc.ents:
                #     if(ent.text==word.text):
                #         loc_spacy_val = ent.label_
                #         break



                # print(loc_spacy_val)
                # tweet_spacy=spacy_dict[index+2].split(" ")
                # for entities in tweet_spacy:
                #     vals=entities.split(":")
                #     if(vals[1]==word.text):
                #         loc_spacy_val=vals[0].lower()
                try:
                    tweet_corenlp=corenlp_dict[index+3].split(" ")
                    for entities in tweet_corenlp:
                        if(not entities==''):
                            vals = entities.split(":")
                            if (vals[1] == word.text):
                                loc_corenlp_val=vals[0].lower()
                except:
                    print(index)
                if(pron_reached==True):
                    # othr_dist_loc_pron_val=indx-pron_reached_token_val
                    othr_dist_loc_pron_val=1
                    pron_reached_token_val.sort()
                    if(othr_dist_loc_pron_max_val<indx - min(pron_reached_token_val)):
                        othr_dist_loc_pron_max_val = indx - min(pron_reached_token_val)
                    # othr_dist_loc_pron_avg_val = indx - pron_reached_token_val[int(abs(len(pron_reached_token_val) / 2))]
                    othr_dist_loc_pron_avg_val = indx - int(abs((max(pron_reached_token_val)-min(pron_reached_token_val) / 2)))
                    if(othr_dist_loc_pron_min_val>indx - max(pron_reached_token_val)):
                        othr_dist_loc_pron_min_val = indx - max(pron_reached_token_val)

                # for i in text:
                #     if(i[0]==word.text):
                #         loc_corenlp_val=i[1]
                #         break
            #####Location of the tweet#####

            #### Extract the closest pronoun (first:0, Second:1, Third:2, Others: 3)####
            if (word.pos_ == 'PRON'):
                pron_count_val+=1
                if(pron_reached==False):
                    pron_reached=True
                    pron_reached_token_val.append(indx)
                    if(loc_reached==False):
                        if(word.text.lower() in pronoun_arr1):
                            temp_pron=0
                        elif(word.text.lower() in pronoun_arr2):
                            temp_pron=1
                        elif(word.text.lower() in pronoun_arr3):
                            temp_pron=2
                        else:
                            temp_pron=3
                    else:
                        if(othr_dist_loc_pron_val==0):
                            othr_dist_loc_pron_val=1
                            loc_reached_val.sort()
                            if(othr_dist_loc_pron_max_val < indx-min(loc_reached_val)):
                                othr_dist_loc_pron_max_val=indx-min(loc_reached_val)
                            # othr_dist_loc_pron_avg_val=indx-loc_reached_val[int(abs(len(loc_reached_val)/2))]
                            othr_dist_loc_pron_avg_val = indx - int(abs((max(loc_reached_val) - min(loc_reached_val) / 2)))
                            if(othr_dist_loc_pron_min_val>indx-max(loc_reached_val)):
                                othr_dist_loc_pron_min_val=indx-max(loc_reached_val)

                    pron_word_val=word.text.lower()
                    pron_tag_val=word.tag_
                    if (indx == 0):
                        loc_presence = indx
                        pron_first_val = True
                    elif (indx == 1):
                        pron_second_val = True
                    if (indx in range(0, int(abs(tweet_length / 4)))):
                        loc_presence = 3  # Here 3 represents the pronoun is in top 25% of the tweet
                        pron_quarter_val = True

            #### Extract the closest pronoun####

            ######## Extract the Verb########
            if(pron_reached==True):
                # pron_reached=False
                if(word.pos_=='VERB'):
                    # tweet_verb_tag.append(word.tag_)
                    # tweet_verb.append(word.text.lower())
                    tweet_verb_tag_val = word.tag_
                    tweet_verb_val=word.text.lower()
                    othr_tense_val, voice, is_perf, modal=get_eve_tense_voice(word)

            ######## End of Extract the Verb########


            ######## Extract the Date/Time Entity########
            if(loc_reached==True):
                if(word.ent_type_=='DATE' or word.ent_type_=='TIME'):
                    # tweet_time.append(word.text.lower())
                    tweet_time_val=word.text.lower()
            ######## Extract the Date/Time Entity########
        temp_spacy=spacy_dict[index+2]
        try:
            if loc_spacy_text[:-1] in temp_spacy:
                loc_spacy_val=spacy_dict[index+2].split(loc_spacy_text[:-1])[0].split(' ')[-1]
        except:
            loc_spacy_val='GPE'
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
        if(othr_dist_loc_pron_min_val==1000):
            othr_dist_loc_pron_min_val=0
        loc_spacy.append(loc_spacy_val[:-1])
        loc_corenlp.append(loc_corenlp_val)
        pron_word.append(pron_word_val)
        pron_tag.append(pron_tag_val)
        pron_first.append(pron_first_val)
        pron_second.append(pron_second_val)
        pron_quarter.append(pron_quarter_val)
        pron_count.append(pron_count_val)
        tweet_time.append(tweet_time_val)
        tweet_verb.append(tweet_verb_val)
        tweet_verb_tag.append(tweet_verb_tag_val)
        # othr_dist_loc_pron.append(othr_dist_loc_pron_val)
        othr_dist_loc_pron_max.append(othr_dist_loc_pron_max_val)
        othr_dist_loc_pron_avg.append(othr_dist_loc_pron_avg_val)
        othr_dist_loc_pron_min.append(othr_dist_loc_pron_min_val)
        othr_tense.append(othr_tense_val)
        location_text.append(loc_spacy_text)

    df_cleaned_tweet['loc_spacy']   = loc_spacy
    df_cleaned_tweet['loc_corenlp'] = loc_corenlp
    df_cleaned_tweet['loc_token']   = loc_token

    df_cleaned_tweet['pron_word']   = pron_word
    df_cleaned_tweet['pron_tag'] = pron_tag
    df_cleaned_tweet['pron_first'] = pron_first
    df_cleaned_tweet['pron_second'] = pron_second
    df_cleaned_tweet['pron_quarter'] = pron_quarter
    df_cleaned_tweet['pron_count']=pron_count

    df_cleaned_tweet['othr_hashtag']=othr_hashtag
    df_cleaned_tweet['othr_url'] = othr_url
    # df_cleaned_tweet['othr_dist_loc_pron']=othr_dist_loc_pron
    df_cleaned_tweet['othr_dist_loc_pron_max']=othr_dist_loc_pron_max
    df_cleaned_tweet['othr_dist_loc_pron_avg'] = othr_dist_loc_pron_avg
    df_cleaned_tweet['othr_dist_loc_pron_min'] = othr_dist_loc_pron_min
    df_cleaned_tweet['othr_tense'] = othr_tense
    # print(df_cleaned_tweet)
    # print (df_cleaned_tweet.shape)
    # print (df_cleaned_tweet['loc_spacy'].to_dict())
    # df_cleaned_tweet['loc_spacy'] = df_cleaned_tweet['loc_spacy'].astype('category')
    df_cleaned_tweet['tweet_time']     = tweet_time
    # df_cleaned_tweet['tweet_time']     = df_cleaned_tweet['tweet_time'].astype('category')
    df_cleaned_tweet['tweet_verb']     = tweet_verb
    # df_cleaned_tweet['tweet_verb']     = df_cleaned_tweet['tweet_verb'].astype('category')
    df_cleaned_tweet['tweet_verb_tag'] = tweet_verb_tag
    # df_cleaned_tweet['tweet_verb_tag'] = df_cleaned_tweet['tweet_verb_tag'].astype('category')
    df_cleaned_tweet['location_text']=location_text



    # print(len(tweet_verb))
    # print(len(tweet_time))
    # print(len(tweet_verb_tag))
    # print(df_tweet_labels.head())
            # print(type(row['Loc']))
            # print(type(row['Tweet']))
            # print(row['Tweet'])
            # temp_row=str(row['Tweet'])
            # print(temp_row)
            # print(row['Tweet'].decode('utf-8'))
    output_text=open('features.txt','w')
    for ind, row in df_cleaned_tweet.iterrows():
        output_text.write('Tweet Text: '+row['Tweet']+'\n')
        output_text.write('Location: '+row['location_text']+'\n')
        output_text.write('Spacy NER for Location: '+row['loc_spacy']+'\n')
        output_text.write('CoreNLP NER for Location: ' + row['loc_corenlp']+'\n')
        output_text.write('Length of the location: ' + str(row['loc_token'])+'\n')
        output_text.write('Pronoun Word: ' + row['pron_word']+'\n')
        output_text.write('Pronoun Tag: ' + row['pron_tag']+'\n')
        output_text.write('Is pronoun the first token: ' + str(row['pron_first'])+'\n')
        output_text.write('Is pronoun the second token: ' + str(row['pron_second'])+'\n')
        output_text.write('Is pronoun in the first quarter of the tweet: ' + str(row['pron_quarter'])+'\n')
        output_text.write('Pronoun count' + str(['pron_count']) + '\n')
        output_text.write('Has Hashtag: ' + str(row['othr_hashtag'])+'\n')
        output_text.write('Has URL: ' + str(row['othr_url'])+'\n')
        output_text.write('Maximum Location and pronoun distance: ' + str(row['othr_dist_loc_pron_max'])+'\n')
        output_text.write('Average Location and pronoun distance: ' + str(row['othr_dist_loc_pron_avg']) + '\n')
        output_text.write('Minimum Location and pronoun distance: ' + str(row['othr_dist_loc_pron_min']) + '\n')
        output_text.write('Tense of the verb: ' + row['othr_tense']+'\n')
        output_text.write('Word with Date/Time NER  after the location: ' + row['tweet_time']+'\n')
        output_text.write('Verb of the tweet: ' + row['tweet_verb']+'\n')
        output_text.write('Verb tag: ' + row['tweet_verb_tag']+'\n')
        output_text.write('\n')
        output_text.write('----------------------------------------------------------------------------------------')
        output_text.write('\n')
    df_cleaned_tweet.to_csv('features.csv', sep=',', encoding='utf-8')
    return df_cleaned_tweet,df_tweet_labels
