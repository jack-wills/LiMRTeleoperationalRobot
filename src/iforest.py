from sklearn.ensemble import IsolationForest
import pandas as pd
import numpy as np
import pickle
import requests 
import json 
import time 
import datetime

def sensor_data(is_fault):
        #reading input data files for ml model training 
        train_data = pd.read_csv("../Isolation_forest_OC_SVM/norm.csv")
        #reading outlier data points, outliers correspond to faults 
        outlier_data = pd.read_csv("../Isolation_forest_OC_SVM/outlier.csv")

        with open('model', 'rb') as file:
                saved_model = file.read()
        clf = pickle.loads(saved_model)

        y_pred_train=clf.predict(train_data)
        y_pred_outliers=clf.predict(outlier_data)
        ML_prediction=np.concatenate((y_pred_train[0:train_data.shape[0]],y_pred_outliers[0:outlier_data.shape[0]]), axis=0)

        #data that is uploaded to cloud 
        MMC1Vlc = np.array(pd.read_csv("../Isolation_forest_OC_SVM/MMC1Vlc.csv"))
        MMC1Vuc = np.array(pd.read_csv("../Isolation_forest_OC_SVM/MMC1Vuc.csv"))

        API_ENDPOINT = "https://bmgxwpyyd2.execute-api.us-east-1.amazonaws.com/prod/sensordata"

        size = MMC1Vlc.shape[0]

        while(1):
                if (is_fault.is_fault):
                        last_is_fault = is_fault.is_fault
                        start = train_data.shape[0]
                        end = size
                else:
                        last_is_fault = is_fault.is_fault
                        start = 0
                        end = train_data.shape[0]
                for index in range (start,end,1):
                        SMVlc=MMC1Vlc[index]
                        SMVuc=MMC1Vuc[index]
                        prediction=ML_prediction[index]
                        sensor1={"SM1Vlc":str(SMVlc[0]),"SM2Vlc":str(SMVlc[1]) ,"SM3Vlc": str(SMVlc[2]),"SM4Vlc": str(SMVlc[3]),"SM5Vlc":str(SMVlc[4]),
                                "SM6Vlc": str(SMVlc[5]) ,"SM7Vlc":str(SMVlc[6]) ,"SM8Vlc":str(SMVlc[7]) ,"SM9Vlc":str(SMVlc[8]) ,"SM10Vlc":str(SMVlc[9]) ,
                                "SM11Vlc": str(SMVlc[10]) ,"SM12Vlc":str(SMVlc[11]) ,"SM13Vlc":str(SMVlc[12]) ,"SM14Vlc":str(SMVlc[13]) ,"SM15Vlc":str(SMVlc[14]) ,
                                "SM16Vlc": str(SMVlc[15]) ,"SM17Vlc":str(SMVlc[16]) ,"SM18Vlc":str(SMVlc[17]) ,"SM19Vlc":str(SMVlc[18]) ,"SM20Vlc":str(SMVlc[19]) ,
                                "SM21Vlc": str(SMVlc[20]) ,"SM22Vlc":str(SMVlc[21]) ,"SM23Vlc":str(SMVlc[22]) ,"SM24Vlc":str(SMVlc[23]) ,
                                "ml_prediction": str(prediction)}
                        sensor2={"SM25Vlc":str(SMVlc[24]) ,"SM26Vlc": str(SMVlc[25]) ,"SM27Vlc":str(SMVlc[26]) ,"SM28Vlc":str(SMVlc[27]) ,"SM29Vlc":str(SMVlc[28]) ,
                                "SM30Vlc":str(SMVlc[29]),"SM25Vuc":str(SMVuc[24]) ,"SM26Vuc": str(SMVuc[25]) ,"SM27Vuc":str(SMVuc[26]) ,"SM28Vuc":str(SMVuc[27]) ,"SM29Vuc":str(SMVuc[28]) ,
                                "SM30Vuc":str(SMVuc[29])
                                }
                        sensor3={"SM1Vuc":str(SMVuc[0]),"SM2Vuc":str(SMVuc[1]) ,"SM3Vuc": str(SMVuc[2]),"SM4Vuc": str(SMVuc[3]),"SM5Vuc":str(SMVuc[4]),
                                "SM6Vuc": str(SMVuc[5]) ,"SM7Vuc":str(SMVuc[6]) ,"SM8Vuc":str(SMVuc[7]) ,"SM9Vuc":str(SMVuc[8]) ,"SM10Vuc":str(SMVuc[9]) ,
                                "SM11Vuc": str(SMVuc[10]) ,"SM12Vuc":str(SMVuc[11]) ,"SM13Vuc":str(SMVuc[12]) ,"SM14Vuc":str(SMVuc[13]) ,"SM15Vuc":str(SMVuc[14]) ,
                                "SM16Vuc": str(SMVuc[15]) ,"SM17Vuc":str(SMVuc[16]) ,"SM18Vuc":str(SMVuc[17]) ,"SM19Vuc":str(SMVuc[18]) ,"SM20Vuc":str(SMVuc[19]) ,
                                "SM21Vuc": str(SMVuc[20]) ,"SM22Vuc":str(SMVuc[21]) ,"SM23Vuc":str(SMVuc[22]) ,"SM24Vuc":str(SMVuc[23])
                                }
                        data1 = {'timestamp':"{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now()), 
                                'sensorValues': json.dumps(sensor1)
                                }
                        data2 = {'timestamp':"{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now()), 
                                'sensorValues': json.dumps(sensor2)
                                }
                        data3 = {'timestamp':"{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now()), 
                                'sensorValues': json.dumps(sensor3)
                                }
                        r1 = requests.post(url = API_ENDPOINT, json = data1) 
                        r2=  requests.post(url = API_ENDPOINT, json = data2) 
                        r3=  requests.post(url = API_ENDPOINT, json = data3) 
                        #print("Data returned =%s"%r1.text)
                        #print("Data returned =%s"%r2.text)
                        #print("Data returned =%s"%r3.text)
                        #print(index)
                        time.sleep(1)
                        if (is_fault.is_fault != last_is_fault):
                                break