import pandas as pd
import pickle
import numpy as np
norm_size = 50
outlier_size = 10

train_data = pd.read_excel("../Isolation_forest_OC_SVM/PQ_1.xlsx", usecols="B:E",skiprows=100002, nrows=norm_size)
Vdc_1=pd.read_excel("../Isolation_forest_OC_SVM/Vdc_1.xlsx", usecols="B:C",skiprows=100002, nrows=norm_size)
Vs_1=pd.read_excel("../Isolation_forest_OC_SVM/Vs_1.xlsx", usecols="B:D",skiprows=100002, nrows=norm_size)
Idc_1=pd.read_excel("../Isolation_forest_OC_SVM/Idc_1.xlsx", usecols="B:C",skiprows=100002, nrows=norm_size)
Is_1=pd.read_excel("../Isolation_forest_OC_SVM/Is_1.xlsx", usecols="B:D",skiprows=100002, nrows=norm_size)
train_data=np.concatenate((train_data, Vdc_1,Vs_1,Idc_1,Is_1), axis=1)
train_data = pd.DataFrame(data=train_data)

train_data.to_csv("../Isolation_forest_OC_SVM/norm.csv", index=False)

outlier_data = pd.read_excel("../Isolation_forest_OC_SVM/PQ_4.xlsx", usecols="B:E",skiprows=100002,nrows=outlier_size)
Vdc_4=pd.read_excel("../Isolation_forest_OC_SVM/Vdc_4.xlsx", usecols="B:C",skiprows=100002,nrows=outlier_size)
Vs_4=pd.read_excel("../Isolation_forest_OC_SVM/Vs_4.xlsx", usecols="B:D",skiprows=100002,nrows=outlier_size)
Idc_4=pd.read_excel("../Isolation_forest_OC_SVM/Idc_4.xlsx", usecols="B:C",skiprows=100002,nrows=outlier_size)
Is_4=pd.read_excel("../Isolation_forest_OC_SVM/Is_4.xlsx", usecols="B:D",skiprows=100002,nrows=outlier_size)
outlier_data=np.concatenate((outlier_data, Vdc_4,Vs_4,Idc_4,Is_4), axis=1)
outlier_data = pd.DataFrame(data=outlier_data)

outlier_data.to_csv("../Isolation_forest_OC_SVM/outlier.csv", index=False)


MMC1Vlc_1=pd.read_excel("../Isolation_forest_OC_SVM/MMC1Vlc_1.xlsx", usecols="B:AE",skiprows=100002, nrows=norm_size)
MMC1Vlc_4 =pd.read_excel("../Isolation_forest_OC_SVM/MMC1Vlc_4.xlsx", usecols="B:AE",skiprows=100002,nrows=outlier_size)
MMC1Vlc=np.concatenate((MMC1Vlc_1,MMC1Vlc_4), axis=0)
MMC1Vlc_data = pd.DataFrame(data=MMC1Vlc)

MMC1Vlc_data.to_csv("../Isolation_forest_OC_SVM/MMC1Vlc.csv", index=False)
MMC1Vuc_1=pd.read_excel("../Isolation_forest_OC_SVM/MMC1Vuc_1.xlsx", usecols="B:AE",skiprows=100002,nrows=norm_size)
MMC1Vuc_4=pd.read_excel("../Isolation_forest_OC_SVM/MMC1Vuc_4.xlsx", usecols="B:AE",skiprows=100002,nrows=outlier_size)
MMC1Vuc=np.concatenate((MMC1Vuc_1,MMC1Vuc_4), axis=0)
MMC1Vuc_data = pd.DataFrame(data=MMC1Vuc)

MMC1Vuc_data.to_csv("../Isolation_forest_OC_SVM/MMC1Vuc.csv", index=False)