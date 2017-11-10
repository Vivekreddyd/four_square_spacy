import csv
import spacy
import os
nlp=spacy.load('en')
import pandas as pd
input1='/home/vivek/Desktop/Thesis/Vivek/eduardoblanco-Vivek/Notebooks/Adjudicated'
# input2='/home/vivek/Four_Square_tweets/Annotations/Batch4/Batch4_Alakananda2.csv'
# x_file=open(input1,'r',encoding='utf8')
# # y_file=open(input2,'r',encoding='utf8')
# x_reader=csv.reader(x_file,delimiter=',',quotechar='"',quoting=csv.QUOTE_ALL)
# # y_reader=csv.reader(y_file,delimiter=',',quotechar='"',quoting=csv.QUOTE_ALL)
pr1_count=0
pr2_count=0
pr3_count=0
pr4_count=0
total_pron_count=0
tweet_count=0
verb_list={}
prn_verb_count={}
prn_non_verb_count={}
verb_count=0
not_verb_count=0
dict_x1={key:{'CY':0,'PY':0,'Unknown':0,'PN':0,'CN':0,'Invalid':0} for key in range(0,6)}
dict_x2={key:{'CY':0,'PY':0,'Unknown':0,'PN':0,'CN':0,'Invalid':0} for key in range(0,6)}
dict_x3={key:{'CY':0,'PY':0,'Unknown':0,'PN':0,'CN':0,'Invalid':0} for key in range(0,6)}
dict_x4={key:{'CY':0,'PY':0,'Unknown':0,'PN':0,'CN':0,'Invalid':0} for key in range(0,6)}
dict_y1={key:{'CY':0,'PY':0,'Unknown':0,'PN':0,'CN':0,'Invalid':0} for key in range(0,3)}
dict_y2={key:{'CY':0,'PY':0,'Unknown':0,'PN':0,'CN':0,'Invalid':0} for key in range(0,3)}
dict_y3={key:{'CY':0,'PY':0,'Unknown':0,'PN':0,'CN':0,'Invalid':0} for key in range(0,3)}
dict_y4={key:{'CY':0,'PY':0,'Unknown':0,'PN':0,'CN':0,'Invalid':0} for key in range(0,3)}
for file in os.listdir(input1):
    x_file = open(os.path.join(input1,file), 'r', encoding='utf8')
    x_reader = csv.reader(x_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    count=0
    prev_tweet=''
    prev_line=''
    pronoun_arr1=['i','we','me','us']
    pronoun_arr2=['you']
    pronoun_arr3=['he','him','she','her','it','they','them']
    temp=0
    combined_file=pd.read_csv(os.path.join(input1,file),header=None,skiprows=3)
    df=pd.DataFrame(combined_file)
    df1=pd.DataFrame(df.iloc[::4,5::4])
    # for i in df1:
        # print(i)
        # print(df1[i].value_counts())
    for xline in x_reader:
        count += 1
        # if (count > 3 and (count - 3) % 4 == 1):
        #     prev_line=xline
        if(count>3 and (count-3)%4==1):
            if (not prev_tweet == xline[2]):
                prev_tweet = xline[2]
                tweet_count += 1
            else:
                continue
            # temp=str(xline[2],'utf-8')
            # xline=prev_line
            doc = nlp(xline[2])
            is_visited=[]
            verb_occured=False
            pron_visited=False
            for word in doc:
                if(word.pos_ == 'VERB'):
                    print(word)
                    if(verb_occured==False):
                        verb_count+=1
                        # print(word)
                        verb_occured=True
                        dict_y1[2][xline[5]] += 1
                        dict_y1[2][xline[9]] += 1
                        dict_y1[2][xline[13]] += 1
                        dict_y1[2][xline[17]] += 1
                        dict_y1[2][xline[21]] += 1
                    if(word.tag_ in verb_list):
                        verb_list[word.tag_]+=1
                    else:
                        verb_list[word.tag_] = 1
                if (word.pos_ == 'PRON'):
                    if(pron_visited==False):
                        pron_visited=True
                        total_pron_count += 1
                    if( word.text.lower() in pronoun_arr1):
                        # print(prev_x[3:8])
                        # temp+=1
                        # print(count)
                        if(not 'pronoun_arr1' in is_visited):
                            pr1_count += 1
                            # print(xline[5::4])
                            dict_x1[xline[5::4].count('CY')]['CY']+=1
                            dict_x1[xline[5::4].count('PY')]['PY']+=1
                            dict_x1[xline[5::4].count('Unknown')]['Unknown']+=1
                            dict_x1[xline[5::4].count('PN')]['PN']+=1
                            dict_x1[xline[5::4].count('CN')]['CN']+=1
                            dict_x1[xline[5::4].count('Invalid')]['Invalid']+=1
                            dict_y1[1][xline[5]]+=1
                            dict_y1[1][xline[9]]+=1
                            dict_y1[1][xline[13]]+=1
                            dict_y1[1][xline[17]]+=1
                            dict_y1[1][xline[21]]+=1
                            # dict_y1[1][xline[25]]+=1
                            # break
                            is_visited.append('pronoun_arr1')
                    elif (word.text.lower() in pronoun_arr2):
                        # print(prev_x[3:8])
                        # temp+=1
                        # print(count)
                        if(not 'pronoun_arr2' in is_visited):
                            pr2_count += 1
                            dict_x2[xline[3:8].count('CY')]['CY'] += 1
                            dict_x2[xline[3:8].count('PY')]['PY'] += 1
                            dict_x2[xline[3:8].count('Unknown')]['Unknown'] += 1
                            dict_x2[xline[3:8].count('PN')]['PN'] += 1
                            dict_x2[xline[3:8].count('CN')]['CN'] += 1
                            dict_x2[xline[3:8].count('Invalid')]['Invalid'] += 1
                            dict_y2[1][xline[5]] += 1
                            dict_y2[1][xline[9]] += 1
                            dict_y2[1][xline[13]] += 1
                            dict_y2[1][xline[17]] += 1
                            dict_y2[1][xline[21]] += 1
                            is_visited.append('pronoun_arr2')
                            # break
                    elif (word.text.lower() in pronoun_arr3):
                        # print(prev_x[3:8])
                        # temp+=1
                        # print(count)
                        if (not 'pronoun_arr3' in is_visited):
                            pr3_count += 1
                            dict_x3[xline[3:8].count('CY')]['CY'] += 1
                            dict_x3[xline[3:8].count('PY')]['PY'] += 1
                            dict_x3[xline[3:8].count('Unknown')]['Unknown'] += 1
                            dict_x3[xline[3:8].count('PN')]['PN'] += 1
                            dict_x3[xline[3:8].count('CN')]['CN'] += 1
                            dict_x3[xline[3:8].count('Invalid')]['Invalid'] += 1
                            dict_y3[1][xline[5]] += 1
                            dict_y3[1][xline[9]] += 1
                            dict_y3[1][xline[13]] += 1
                            dict_y3[1][xline[17]] += 1
                            dict_y3[1][xline[21]] += 1
                            is_visited.append('pronoun_arr3')
                        # break
                    else:
                        # print(prev_x[3:8])
                        # temp+=1
                        # print(count)
                        # print(word.text.lower())
                        if (not 'rest' in is_visited):
                            # print(word)
                            pr4_count += 1
                            dict_x4[xline[3:8].count('CY')]['CY'] += 1
                            dict_x4[xline[3:8].count('PY')]['PY'] += 1
                            dict_x4[xline[3:8].count('Unknown')]['Unknown'] += 1
                            dict_x4[xline[3:8].count('PN')]['PN'] += 1
                            dict_x4[xline[3:8].count('CN')]['CN'] += 1
                            dict_x4[xline[3:8].count('Invalid')]['Invalid'] += 1
                            dict_y4[1][xline[5]] += 1
                            dict_y4[1][xline[9]] += 1
                            dict_y4[1][xline[13]] += 1
                            dict_y4[1][xline[17]] += 1
                            dict_y4[1][xline[21]] += 1
                            is_visited.append('rest')
                        # break
            if(verb_occured==True):
                for prn in is_visited:
                    if(prn in prn_verb_count):
                        prn_verb_count[prn]+=1
                    else:
                        prn_verb_count[prn] = 1
            elif(verb_occured==False):
                not_verb_count += 1
                dict_y2[2][xline[5]] += 1
                dict_y2[2][xline[9]] += 1
                dict_y2[2][xline[13]] += 1
                dict_y2[2][xline[17]] += 1
                dict_y2[2][xline[21]] += 1
                for prn in is_visited:
                    if(prn in prn_non_verb_count):
                        prn_non_verb_count[prn]+=1
                    else:
                        prn_non_verb_count[prn] = 1
            prev_tweet=xline[2]
# prev_x = xline
    # prev_y = yline
# print(count)
# print(pr1_count,pr2_count,pr3_count,pr4_count)
print("tweet_counts:",tweet_count)
# print("Pronoun counts:",total_pron_count)
print("Verb Occurances:", verb_count)

for verb,count in verb_list.items():
    print(verb,':',count)
#
# k=0
sum_val=0
labels=['CY','PY','Unknown','PN','CN','Invalid']
for i in [dict_x1,dict_x2,dict_x3,dict_x4]:#,dict_y1,dict_y2,dict_y3,dict_y4]:
    # print("--------------------------")
    # print(i)
    # print("--------------------------")
    # print("\n")
    for key, value in i.items():
        if(key==5):

        # if(k==0):
        #     k+=1
        #     print(value.keys())
        #     print("")os.path.join(input1,file)
        #     print("%d times repeated"%key)
        #     print(keys)

            for j in ['Unknown']:
                # print(value[j],)
                # sum_val+=value[j]*key
                sum_val+=value[j]
print('')
print (sum_val)
# sum_val=0
# for i in [dict_y1,dict_y2,dict_y3,dict_y4]:
#     print()
#     print("--------------------------")
#     print(i)
#     print("--------------------------")
#
#     for key, value in i.items():
#         if(key==2):
#         # if(k==0):
#         #     k+=1
#         #     print(value.keys())
#         #     print("")os.path.join(input1,file)
#         #     print("%d times repeated"%key)
#         #     print(keys)
#
#             for j in labels:
#                 print(value[j],end=' ')
#                 sum_val+=value[j]*key
# print('')
# print (sum_val)
# print("Verb counts")
# for prn_verb,pv_count in prn_verb_count.items():
#     print(prn_verb,':',pv_count)
# print("Non verb counts")
# for prn_verb, pv_count in prn_non_verb_count.items():
#     print(prn_verb, ':', pv_count)

# print(dict_x1.values())
# print(dict_x2.values())
# print(dict_x3.values())
# print(dict_x4.values())
# print(dict_y1.values())
# print(dict_y2.values())
# print(dict_y3.values())
# print(dict_y4.values())
# print(temp)