import pandas as pd
import numpy as np
import pickle

#reading input data files for ml model training 
train_data = pd.read_excel("../Isolation_forest_OC_SVM/PQ_1.xlsx", usecols="B:E",skiprows=100002)
Vdc_1=pd.read_excel("../Isolation_forest_OC_SVM/Vdc_1.xlsx", usecols="B:C",skiprows=100002)
Vs_1=pd.read_excel("../Isolation_forest_OC_SVM/Vs_1.xlsx", usecols="B:D",skiprows=100002)
Idc_1=pd.read_excel("../Isolation_forest_OC_SVM/Idc_1.xlsx", usecols="B:C",skiprows=100002)
Is_1=pd.read_excel("../Isolation_forest_OC_SVM/Is_1.xlsx", usecols="B:D",skiprows=100002)
train_data=np.concatenate((train_data, Vdc_1,Vs_1,Idc_1,Is_1), axis=1)
train_data = pd.DataFrame(data=train_data)

#reading outlier data points, outliers correspond to faults 
outlier_data = pd.read_excel("../Isolation_forest_OC_SVM/PQ_4.xlsx", usecols="B:E",skiprows=100002)
Vdc_4=pd.read_excel("../Isolation_forest_OC_SVM/Vdc_4.xlsx", usecols="B:C",skiprows=100002)
Vs_4=pd.read_excel("../Isolation_forest_OC_SVM/Vs_4.xlsx", usecols="B:D",skiprows=100002)
Idc_4=pd.read_excel("../Isolation_forest_OC_SVM/Idc_4.xlsx", usecols="B:C",skiprows=100002)
Is_4=pd.read_excel("../Isolation_forest_OC_SVM/Is_4.xlsx", usecols="B:D",skiprows=100002)
outlier_data=np.concatenate((outlier_data, Vdc_4,Vs_4,Idc_4,Is_4), axis=1)
outlier_data = pd.DataFrame(data=outlier_data)

#training iForest 
from sklearn.ensemble import IsolationForest
rng = np.random.RandomState(42)
clf = IsolationForest(max_samples=10, random_state=rng, behaviour="new",contamination=0.01)
clf.fit(train_data)




text_file = open("model", "wb")
n = text_file.write(pickle.dumps(clf))
text_file.close()