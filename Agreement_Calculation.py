# import unicodecsv as csv
import csv,codecs
import scipy
from scipy.stats.stats import pearsonr
from sklearn.metrics import cohen_kappa_score
from nltk.metrics import interval_distance, binary_distance
from nltk import agreement
import csv
import pandas as pd
# from itertools import zip
# input1=input()
# input2=input()
input1='/home/vivek/Desktop/Thesis/Four_Square_tweets/Batch9/Batch9_Vivek.csv'
input2='/home/vivek/Desktop/Thesis/Four_Square_tweets/Batch9/Batch9_Alakananda.csv'
# input1.decode('utf-8').strip()
# input2.decode('utf-8').strip()
# x_reader=pd.read_csv(input1,quotechar='"',delimiter=',')
# y_reader=pd.read_csv(input2,quotechar='"',delimiter=',')
# with codecs.open(input2, "r",encoding='utf-8', errors='ignore') as x_file:
#     x_reader=csv.reader(x_file)
#     for line in x_reader:
#         print(line)
#
# for xline,yline in zip(x_reader,y_reader):
#     print(xline)
#     print(yline)
x_file=codecs.open(input1,'r',encoding='utf-8', errors='ignore')
y_file=codecs.open(input2,'r',encoding='utf-8', errors='ignore')
# with open(input1, 'r') as read_x:
#     with open(input2,'r') as read_y:
#         x_reader = csv.reader(read_x)
#         y_reader=csv.reader(read_y)
#         # x_lines = (line.encode('ascii') for line in x_file)
#         # y_lines = (line.encode('ascii') for line in y_file)
x_reader=csv.reader(x_file,delimiter=',',quotechar='"',dialect=csv.excel)#,encoding='utf-8')
y_reader=csv.reader(y_file,delimiter=',',quotechar='"',dialect=csv.excel)#,encoding='utf-8')
#         # UnicodeReader
#         # y_reader.encode('utf-8')
dict_x={key:[] for key in range(3,8)}
dict_y={key:[] for key in range(3,8)}
count=0
for xline, yline in zip(x_reader,y_reader):
    count+=1
    # print(yline)
    if(count>2):
        #temp_x,temp_y=[],[]
        for i in range(3,8):
            # if(not xline[i]=='Invalid' and not yline[i]=='Invalid'):
            if(xline[i]=='CN'):
                dict_x[i].append(-1)
                #temp_x.append(-2)
            elif (xline[i] == 'PN'):
                dict_x[i].append(-1)
                #temp_x.append(-1)
            elif (xline[i] == 'Unknown'):
                dict_x[i].append(0)
                #temp_x.append(0)
            elif (xline[i] == 'PY'):
                dict_x[i].append(1)
                #temp_x.append(1)
            elif (xline[i] == 'CY'):
                dict_x[i].append(1)
                #temp_x.append(2)
            elif(xline[i] == 'Invalid'):
                # print("invalid")
                dict_x[i].append(0)
                #temp_x.append(-10)

            if(yline[i]=='CN'):
                dict_y[i].append(-1)
                #temp_y.append(-2)
            elif (yline[i] == 'PN'):
                dict_y[i].append(-1)
                # temp_y.append(-1)
            elif (yline[i] == 'Unknown'):
                dict_y[i].append(0)
                # temp_y.append(0)
            elif (yline[i] == 'PY'):
                dict_y[i].append(1)
                # temp_y.append(1)
            elif (yline[i] == 'CY'):
                dict_y[i].append(1)
                # temp_y.append(2)
            elif (yline[i] == 'Invalid'):
                # print("invalid")
                dict_y[i].append(0)
            else:
                if(not yline[i] == ''):
                    print(yline[0])
                # temp_y.append(-10)
        # print(xline,yline)
# x=[-2,-1,0,1,2]
# y=[-1,-1,0,2,1]
for j in range(3,8):
    # print(dict_x[j])
    # print(dict_y[j])
    print(len(dict_x[j]))
    print(len(dict_y[j]))
    # print
    print("Pearson:"+str(scipy.stats.pearsonr(dict_x[j],dict_y[j])))
    print(cohen_kappa_score(dict_x[j],dict_y[j]))
    def dist(label1, label2):
        return abs(label1-label2)
    taskdata=[[0,str(i),int(dict_x[j][i])] for i in range(0,len(dict_x[j]))]+[[1,str(i),int(dict_y[j][i])] for i in range(0,len(dict_y[j]))]
    ratingtask = agreement.AnnotationTask(data=taskdata, distance=dist)
    # ratingtask = agreement.AnnotationTask(data=taskdata, distance=binary_distance)
    # agreement.AnnotationTask
    # print("kappa " +str(ratingtask.kappa()))
    # print("fleiss " + str(ratingtask.multi_kappa()))
    print("alpha " +str(ratingtask.alpha()))
# print("scotts " + str(ratingtask.pi()))