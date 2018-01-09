import pandas as pd
import os
df=pd.DataFrame()
files_list=[]
path='/home/vivek/Four_Square_tweets/Annotations/Adjudicated_final/'
for input_file in sorted(os.listdir(path)):
    adj_file = pd.read_csv(path+input_file,header=None,names=['Tweet_ID','Loc','Tweet','bgt_A1','bgt_A2','bgt_Ad','bgt_R','blt_A1','blt_A2','blt_Ad','blt_R','dur_A1','dur_A2','dur_Ad','dur_R','alt_A1','alt_A2','alt_Ad','alt_R','agt_A1','agt_A2','agt_Ad','agt_R'],skiprows=3)
    files_list.append(adj_file)
df = pd.concat(files_list,ignore_index=True)
# del df['bgt_Ad']
df.to_csv('Corpus_sorted.csv', sep=',', encoding='utf-8')