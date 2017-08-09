import scipy
from scipy.stats.stats import pearsonr
from sklearn.metrics import cohen_kappa_score
from nltk import agreement
import csv
# from itertools import zip
# input1=input()
# input2=input()
input1='/home/vivek/Four_Square_tweets/Annotations/Batch4/Batch4_Vivek.csv'
input2='/home/vivek/Four_Square_tweets/Annotations/Batch4/Batch4_Alakananda2.csv'
x_file=open(input1,'r')
y_file=open(input2,'r')
x_reader=csv.reader(x_file,delimiter=',',quotechar='"')
y_reader=csv.reader(y_file,delimiter=',',quotechar='"')
# y_reader.encode('utf-8')
dict_x={key:[] for key in range(3,8)}
dict_y={key:[] for key in range(3,8)}
count=0
for xline, yline in zip(x_reader,y_reader):
    count+=1
    if(count>2):
        #temp_x,temp_y=[],[]
        for i in range(3,8):
            # if(not xline[i]=='Invalid' and not yline[i]=='Invalid'):
            if(xline[i]=='CN'):
                dict_x[i].append(-2)
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
                dict_x[i].append(2)
                #temp_x.append(2)
            elif(xline[i] == 'Invalid'):
                # print("invalid")
                dict_x[i].append(0)
                #temp_x.append(-10)

            if(yline[i]=='CN'):
                dict_y[i].append(-2)
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
                dict_y[i].append(2)
                # temp_y.append(2)
            elif (yline[i] == 'Invalid'):
                # print("invalid")
                dict_y[i].append(0)
                # temp_y.append(-10)
        # print(xline,yline)
# x=[-2,-1,0,1,2]
# y=[-1,-1,0,2,1]
for j in range(3,8):
    print(dict_x[j])
    print(dict_y[j])
    print(len(dict_x[j]))
    print(len(dict_y[j]))
    # print
    print("Pearson:"+str(scipy.stats.pearsonr(dict_x[j],dict_y[j])))
    # print(cohen_kappa_score(dict_x[j],dict_y[j]))

    taskdata=[[0,str(i),str(dict_x[j][i])] for i in range(0,len(dict_x[j]))]+[[1,str(i),str(dict_y[j][i])] for i in range(0,len(dict_y[j]))]
    ratingtask = agreement.AnnotationTask(data=taskdata)
    print("kappa " +str(ratingtask.kappa()))
    # print("fleiss " + str(ratingtask.multi_kappa()))
    print("alpha " +str(ratingtask.alpha()))
    # print("scotts " + str(ratingtask.pi()))