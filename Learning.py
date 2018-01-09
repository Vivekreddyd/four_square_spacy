
# coding: utf-8

# In[122]:


import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.dummy import DummyClassifier
# from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
import os
import Feature_Extraction
from sklearn.feature_extraction import DictVectorizer

# In[150]:


# df=pd.DataFrame()
# files_list=[]
# path='/home/vivek/Desktop/Thesis/Vivek/eduardoblanco-Vivek/Notebooks/Adjudicated/'
# for input_file in os.listdir(path):
#     adj_file=pd.read_csv(path+input_file,header=None,names=['Tweet_ID','Loc','Tweet','bgt_A1','bgt_A2','bgt_Ad','bgt_R','blt_A1','blt_A2','blt_Ad','blt_R','dur_A1','dur_A2','dur_Ad','dur_R','alt_A1','alt_A2','alt_Ad','alt_R','agt_A1','agt_A2','agt_Ad','agt_R'],skiprows=3)
#     files_list.append(adj_file)
# df=pd.concat(files_list)
# df.count()
# print(df.shape)
#
#
# # list_tags=['bgt_Ad','blt_Ad','dur_Ad','alt_Ad','agt_Ad']
# # for i in list_tags:
# #     print(i)
# # df.columns
# #     df_temp=pd.DataFrame(df[i].iloc[::4])
# # #     df_temp.isin(['NaN']).any(axis=1)
# # #     df_temp[i].isnull()
# #     df_temp.head()
# # df_temp=df[['Tweet_ID','agt_Ad']].iloc[::4]
# # # df_temp=pd.DataFrame(df['agt_Ad'].iloc[::4])
# # df_temp[df_temp.isnull().any(axis=1)]
# # df_test.head()
# # df_temp.isnull()
# # df_temp.tail()
#     # print(df_bgt['bgt_Ad'].value_counts())
# #     print(df_temp[i].value_counts())
# # print()
# # print(df_bgt.iloc[303])
# # print(df_bgt.head())
#
# # In[16]:
#
#
# df1=pd.DataFrame(df.iloc[::4,5::4])
# df2=pd.DataFrame(df['Tweet'].iloc[::4])
# # df1.append(df2)
# df3=pd.concat([df2,df1],axis=1)
# print(df3.tail())
# # df1.loc[:,'Tweet'] = pd.Series(df['Tweet'].iloc[::4], index=df1.index)
# # print(df['Tweet'].iloc[::4])
# # print(df1.head())
#
#
# # Below code is to split the dataset into training and test set. But the below code splits by shuffling the dataset, there is no option split the dataset without shuffling
#
# # In[17]:
#
#
# # for i in ['bgt_Ad','blt_Ad','dur_Ad','alt_Ad','agt_Ad']:
# #     x_train,x_test,y_train,y_test=train_test_split(df3['Tweet'].str.len(),df3[i],test_size=0.2,shuffle=False, stratify=None)
# #     print(x_train)
#
#
# # In[18]:
#
#
# # print(len(df3.index))
#
#
# # In[19]:
#
#
# train_split=abs(len(df3.index)*0.8)
# test_split=len(df3.index)-train_split
# df4=df3.head(int(train_split))
# df5=df3.tail(int(test_split))
# print(df4.shape)
# print(df5.shape)
# #FIXME use train_test_split from sklearn
#
# # print(df4.to_dict('records'))
# # print(df4.set_index('Tweet').to_dict('records'))
# df6=pd.DataFrame(df4['Tweet'].str.len())
# df7=pd.DataFrame(df5['Tweet'].str.len())
# print(df6.shape)
# print(df7.shape)
# # print(df6.as_matrix())

X,Y=Feature_Extraction.Extract_Features()
# print(X.shape,Y.shape)
# print("X Values")
# print(X.head())

# X['tweet_time'] = X['tweet_time'].cat.codes
# X['loc_spacy'] = X['loc_spacy'].cat.codes
# X['tweet_verb'] = X['tweet_verb'].cat.codes
# X['tweet_verb_tag']=X['tweet_verb_tag'].cat.codes

# print(X.head())

X=X.fillna(0)
# print(X.dtypes)
# print(Y.dtypes)
# #
# print(X.iloc[:,4:6])
# print ()

vect=DictVectorizer()
Y=Y.replace(to_replace='Invalid',value='Unknown')
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
# print (vect.fit_transform(X_test.iloc[:,4:6].to_dict('records')))
# print(vect.fit_transform(X.iloc[:,4:6].to_dict('records')))
# Y = Y.reshape(-1, 1)

# print(X_train.iloc[:,4:18])

# print(Y)
# print(Y['bgt_Ad'].astype(str).str.contains('Invalid'))
majority_baseline_output=open('majority_baseline_output.txt','w')
SVM_output=open('svm_output.txt','w')

for tag in ['bgt_Ad','blt_Ad','dur_Ad','alt_Ad','agt_Ad']:
#     feature_vector = DictVectorizer()
#     print(any(Y[tag]== 'Invalid'))
    Baseline = DummyClassifier(strategy="most_frequent")
#     Baseline.fit(df4.to_dict('records'), df4[tag])
    Baseline.fit(vect.fit_transform(X_train.iloc[:,4:23].to_dict('records')),Y_train[tag])
    majority_baseline_output.write("Majority baseline for " + tag+'\n')
    majority_baseline_output.write (classification_report(Y_test[tag],Baseline.predict(vect.fit_transform(X_test.iloc[:,4:23].to_dict('records'))))+'\n')
    majority_baseline_output.write('\n')

tuned_parameters = [
        {'kernel': ['rbf'], 'gamma': [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8], 'C': [1, 10, 100, 1000]},
        {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]

#Feature set

for feature in range(0,3):
    for tag in ['bgt_Ad','blt_Ad','dur_Ad','alt_Ad','agt_Ad']:
    #     feature_vector = DictVectorizer()
    #     Baseline = DummyClassifier(strategy="most_frequent")
    #     Baseline.fit(df4.to_dict('records'), df4[tag])
    #     Baseline.fit(df6.as_matrix(),df4[tag])
    #     print ("Majority baseline for " + tag)
    #     print (classification_report(df5[tag],Baseline.predict(df7.as_matrix())))
        if(feature==0):
            svm_classifier = GridSearchCV(SVC(), tuned_parameters, scoring='f1_weighted',cv=5,n_jobs=8)
            svm_classifier.fit(vect.fit_transform(X_train.iloc[:,4:7].to_dict('records')),Y_train[tag])
            SVM_output.write("SVM with Location features with fine grained labels" + tag+'\n')
            SVM_output.write(classification_report(Y_train[tag], svm_classifier.predict(vect.transform(X_train.iloc[:, 4:7].to_dict('records')))) + '\n')
            SVM_output.write(classification_report(Y_test[tag], svm_classifier.predict(vect.transform(X_test.iloc[:,4:7].to_dict('records'))))+'\n')
        elif (feature == 1):
            svm_classifier = GridSearchCV(SVC(), tuned_parameters, scoring='f1_weighted', cv=5, n_jobs=8)
            svm_classifier.fit(vect.fit_transform(X_train.iloc[:, 4:13].to_dict('records')), Y_train[tag])
            SVM_output.write("SVM with location and pronoun features with fine grained labels" + tag+'\n')
            SVM_output.write(classification_report(Y_train[tag], svm_classifier.predict(vect.transform(X_train.iloc[:, 4:13].to_dict('records')))) + '\n')
            SVM_output.write(classification_report(Y_test[tag], svm_classifier.predict(vect.transform(X_test.iloc[:, 4:13].to_dict('records'))))+'\n')
        elif (feature == 2):
            svm_classifier = GridSearchCV(SVC(), tuned_parameters, scoring='f1_weighted', cv=5, n_jobs=8)
            svm_classifier.fit(vect.fit_transform(X_train.iloc[:, 4:23].to_dict('records')), Y_train[tag])
            SVM_output.write("SVM with location, pronoun and other features with fine grained labels" + tag+'\n')
            SVM_output.write(classification_report(Y_train[tag], svm_classifier.predict(vect.transform(X_train.iloc[:, 4:23].to_dict('records')))) + '\n')
            SVM_output.write(classification_report(Y_test[tag], svm_classifier.predict(vect.transform(X_test.iloc[:, 4:23].to_dict('records'))))+'\n')

Y_train = Y_train.replace(to_replace=['CY','PY'], value='Yes')
Y_test = Y_test.replace(to_replace=['CY','PY'], value='Yes')
Y_train = Y_train.replace(to_replace=['CN','PN'], value='No')
Y_test = Y_test.replace(to_replace=['CN','PN'], value='No')
# print(Y['dur_Ad'].astype(str).str.contains('CY'))
# print(Y['dur_Ad'].astype(str).str.contains('PY'))
# print(Y['dur_Ad'].astype(str).str.contains('CN'))
# print(Y['dur_Ad'].astype(str).str.contains('PN'))
# X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
for tag in ['bgt_Ad','blt_Ad','dur_Ad','alt_Ad','agt_Ad']:
#     feature_vector = DictVectorizer()
#     print(any(Y[tag]== 'Invalid'))
    Baseline = DummyClassifier(strategy="most_frequent")
#     Baseline.fit(df4.to_dict('records'), df4[tag])
    Baseline.fit(vect.fit_transform(X_train.iloc[:,4:23].to_dict('records')),Y_train[tag])
    majority_baseline_output.write("Majority baseline for " + tag+'\n')
    majority_baseline_output.write (classification_report(Y_test[tag],Baseline.predict(vect.fit_transform(X_test.iloc[:,4:23].to_dict('records'))))+'\n')
    majority_baseline_output.write('\n')


for feature in range(0,3):
    for tag in ['bgt_Ad','blt_Ad','dur_Ad','alt_Ad','agt_Ad']:
    #     feature_vector = DictVectorizer()
    #     Baseline = DummyClassifier(strategy="most_frequent")
    #     Baseline.fit(df4.to_dict('records'), df4[tag])
    #     Baseline.fit(df6.as_matrix(),df4[tag])
    #     print ("Majority baseline for " + tag)
    #     print (classification_report(df5[tag],Baseline.predict(df7.as_matrix())))
        if(feature==0):
            svm_classifier = GridSearchCV(SVC(), tuned_parameters, scoring='f1_weighted',cv=5,n_jobs=8)
            svm_classifier.fit(vect.fit_transform(X_train.iloc[:,4:7].to_dict('records')),Y_train[tag])
            SVM_output.write("SVM with Location features with coarse grained labels" + tag+'\n')
            SVM_output.write(classification_report(Y_test[tag], svm_classifier.predict(vect.transform(X_test.iloc[:,4:7].to_dict('records'))))+'\n')
        elif (feature == 1):
            svm_classifier = GridSearchCV(SVC(), tuned_parameters, scoring='f1_weighted', cv=5, n_jobs=8)
            svm_classifier.fit(vect.fit_transform(X_train.iloc[:, 4:13].to_dict('records')), Y_train[tag])
            SVM_output.write("SVM with location and pronoun features with coarse grained labels" + tag+'\n')
            SVM_output.write(classification_report(Y_test[tag], svm_classifier.predict(vect.transform(X_test.iloc[:, 4:13].to_dict('records'))))+'\n')
        elif (feature == 2):
            svm_classifier = GridSearchCV(SVC(), tuned_parameters, scoring='f1_weighted', cv=5, n_jobs=8)
            svm_classifier.fit(vect.fit_transform(X_train.iloc[:, 4:23].to_dict('records')), Y_train[tag])
            SVM_output.write("SVM with location, pronoun and other features with coarse grained labels" + tag+'\n')
            SVM_output.write(classification_report(Y_test[tag], svm_classifier.predict(vect.transform(X_test.iloc[:, 4:23].to_dict('records'))))+'\n')
            # elif (feature == 3):
        #     svm_classifier = GridSearchCV(SVC(), tuned_parameters, scoring='f1_weighted', cv=5, n_jobs=8)
        #     svm_classifier.fit(vect.fit_transform(X_train.iloc[:, 4:19].to_dict('records')), Y_train[tag])
        #     print("SVM with features for " + tag)
        #     print(classification_report(Y_test[tag], svm_classifier.predict(vect.transform(X_test.iloc[:, 4:19].to_dict('records')))))



