import csv
# import spacy
# nlp=spacy.load('en_core_web_sm')
import pandas as pd
input1='/home/vivek/Desktop/Thesis/Four_Square_tweets/Batch7/Batch7_Combined.csv'
# input2='/home/vivek/Four_Square_tweets/Annotations/Batch4/Batch4_Alakananda2.csv'
x_file=open(input1,'r',encoding='utf8')
# y_file=open(input2,'r',encoding='utf8')
x_reader=csv.reader(x_file,delimiter=',',quotechar='"',quoting=csv.QUOTE_ALL)
# y_reader=csv.reader(y_file,delimiter=',',quotechar='"',quoting=csv.QUOTE_ALL)

dict_x1={key:{'CY':0,'PY':0,'Unknown':0,'PN':0,'CN':0,'Invalid':0} for key in range(0,6)}
# dict_x2={key:{'CY':0,'PY':0,'Unknown':0,'PN':0,'CN':0,'Invalid':0} for key in range(0,6)}
# dict_x3={key:{'CY':0,'PY':0,'Unknown':0,'PN':0,'CN':0,'Invalid':0} for key in range(0,6)}
# dict_x4={key:{'CY':0,'PY':0,'Unknown':0,'PN':0,'CN':0,'Invalid':0} for key in range(0,6)}
# dict_y1={key:{'CY':0,'PY':0,'Unknown':0,'PN':0,'CN':0,'Invalid':0} for key in range(0,6)}
# dict_y2={key:{'CY':0,'PY':0,'Unknown':0,'PN':0,'CN':0,'Invalid':0} for key in range(0,6)}
# dict_y3={key:{'CY':0,'PY':0,'Unknown':0,'PN':0,'CN':0,'Invalid':0} for key in range(0,6)}
# dict_y4={key:{'CY':0,'PY':0,'Unknown':0,'PN':0,'CN':0,'Invalid':0} for key in range(0,6)}
count=0
# pronoun_arr1=['i','we']
# pronoun_arr2=['you']
# pronoun_arr3=['he','she','it','they','him','her','them']
temp=0
combined_file=pd.read_csv(input1,header=None,skiprows=3)
df=pd.DataFrame(combined_file)
df1=pd.DataFrame(df.iloc[::4,5::4])
for i in df1:
    # print(i)
    print(df1[i].value_counts())
for xline in x_reader:
    count += 1
    if(count>3 and (count-3)%4==1):
        # doc = nlp(xline[2])Calculate_counts.py:31
        # is_visited=[]
        # for word in doc:
        #     if (word.pos_ == 'PRON'):
        #         if( word.text.lower() in pronoun_arr1):
                    # print(prev_x[3:8])
                    # temp+=1
                    # print(count)
                    # if(not 'pronoun_arr1' in is_visited):
        print(xline[5::4])
        dict_x1[xline[5::4].count('CY')]['CY']+=1
        dict_x1[xline[5::4].count('PY')]['PY']+=1
        dict_x1[xline[5::4].count('Unknown')]['Unknown']+=1
        dict_x1[xline[5::4].count('PN')]['PN']+=1
        dict_x1[xline[5::4].count('CN')]['CN']+=1
        dict_x1[xline[5::4].count('Invalid')]['Invalid']+=1
        # dict_y1[yline[3:8].count('CY')]['CY']+=1
        # dict_y1[yline[3:8].count('PY')]['PY']+=1
        # dict_y1[yline[3:8].count('Unknown')]['Unknown']+=1
        # dict_y1[yline[3:8].count('PN')]['PN']+=1
        # dict_y1[yline[3:8].count('CN')]['CN']+=1
        # dict_y1[yline[3:8].count('Invalid')]['Invalid']+=1
                        # break
                #         is_visited.append('pronoun_arr1')
                # elif (word.text.lower() in pronoun_arr2):
                    # print(prev_x[3:8])
                    # temp+=1
                    # print(count)
                    # if(not 'pronoun_arr2' in is_visited):
                    #     dict_x2[xline[3:8].count('CY')]['CY'] += 1
                    #     dict_x2[xline[3:8].count('PY')]['PY'] += 1
                    #     dict_x2[xline[3:8].count('Unknown')]['Unknown'] += 1
                    #     dict_x2[xline[3:8].count('PN')]['PN'] += 1
                    #     dict_x2[xline[3:8].count('CN')]['CN'] += 1
                    #     dict_x2[xline[3:8].count('Invalid')]['Invalid'] += 1
                    #     dict_y2[yline[3:8].count('CY')]['CY'] += 1
                    #     dict_y2[yline[3:8].count('PY')]['PY'] += 1
                    #     dict_y2[yline[3:8].count('Unknown')]['Unknown'] += 1
                    #     dict_y2[yline[3:8].count('PN')]['PN'] += 1
                    #     dict_y2[yline[3:8].count('CN')]['CN'] += 1
                    #     dict_y2[yline[3:8].count('Invalid')]['Invalid'] += 1
                    #     is_visited.append('pronoun_arr2')
                        # break
                # elif (word.text.lower() in pronoun_arr3):
                #     # print(prev_x[3:8])
                #     # temp+=1
                #     # print(count)
                #     if (not 'pronoun_arr3' in is_visited):
                #         dict_x3[xline[3:8].count('CY')]['CY'] += 1
                #         dict_x3[xline[3:8].count('PY')]['PY'] += 1
                #         dict_x3[xline[3:8].count('Unknown')]['Unknown'] += 1
                #         dict_x3[xline[3:8].count('PN')]['PN'] += 1
                #         dict_x3[xline[3:8].count('CN')]['CN'] += 1
                #         dict_x3[xline[3:8].count('Invalid')]['Invalid'] += 1
                #         dict_y3[yline[3:8].count('CY')]['CY'] += 1
                #         dict_y3[yline[3:8].count('PY')]['PY'] += 1
                #         dict_y3[yline[3:8].count('Unknown')]['Unknown'] += 1
                #         dict_y3[yline[3:8].count('PN')]['PN'] += 1
                #         dict_y3[yline[3:8].count('CN')]['CN'] += 1
                #         dict_y3[yline[3:8].count('Invalid')]['Invalid'] += 1
                #         is_visited.append('pronoun_arr3')
                    # break
                # else:
                #     # print(prev_x[3:8])
                #     # temp+=1
                #     # print(count)
                #     # print(word.text.lower())
                #     if (not 'rest' in is_visited):
                #         dict_x4[xline[3:8].count('CY')]['CY'] += 1
                #         dict_x4[xline[3:8].count('PY')]['PY'] += 1
                #         dict_x4[xline[3:8].count('Unknown')]['Unknown'] += 1
                #         dict_x4[xline[3:8].count('PN')]['PN'] += 1
                #         dict_x4[xline[3:8].count('CN')]['CN'] += 1
                #         dict_x4[xline[3:8].count('Invalid')]['Invalid'] += 1
                #         dict_y4[yline[3:8].count('CY')]['CY'] += 1
                #         dict_y4[yline[3:8].count('PY')]['PY'] += 1
                #         dict_y4[yline[3:8].count('Unknown')]['Unknown'] += 1
                #         dict_y4[yline[3:8].count('PN')]['PN'] += 1
                #         dict_y4[yline[3:8].count('CN')]['CN'] += 1
                #         dict_y4[yline[3:8].count('Invalid')]['Invalid'] += 1
                #         is_visited.append('rest')
                    # break
# prev_x = xline
    # prev_y = yline
# print(count)
k=0
sum_val=0
keys=['CY','PY','Unknown','PN','CN','Invalid']
for i in [dict_x1]:#,dict_x2,dict_x3,dict_x4,dict_y1,dict_y2,dict_y3,dict_y4]:
    print("--------------------------")
    print(i)
    print("--------------------------")
    for key, value in i.items():
        if(key>0):
        # if(k==0):
        #     k+=1
        #     print(value.keys())
            print("")
            print("%d times repeated"%key)
            print(keys)

            for j in keys:
                print(value[j],end=" ")
                sum_val+=value[j]*key
print('')
print (sum_val)
# print(dict_x1.values())
# print(dict_x2.values())
# print(dict_x3.values())
# print(dict_x4.values())
# print(dict_y1.values())
# print(dict_y2.values())
# print(dict_y3.values())
# print(dict_y4.values())
# print(temp)