from sklearn.ensemble import IsolationForest
import pandas as pd
import numpy as np
import pickle
import requests 
import json 
import time 
import datetime

def sensor_data(is_fault, is_pause):
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
                if (not is_pause.is_pause):
                        for index in range (start,end,1):
                                SMVlc=MMC1Vlc[index]
                                SMVuc=MMC1Vuc[index]
                                prediction=ML_prediction[index]
                                sensor1 = {}
                                sensor2 = {}
                                sensor1["ml_prediction"] = str(prediction)
                                for i in range(0,24):
                                        sensor1["SM" + str(i+1) + "Vuc"] = str(SMVuc[i])
                                for i in range(0,25):
                                        sensor2["SM" + str(i+25) + "Vuc"] = str(SMVuc[i])
                                data1 = {'timestamp':"{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now()), 
                                        'sensorValues': json.dumps(sensor1)
                                        }
                                data2 = {'timestamp':"{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now()), 
                                        'sensorValues': json.dumps(sensor2)
                                        }
                                r1 = requests.post(url = API_ENDPOINT, json = data1) 
                                r2=  requests.post(url = API_ENDPOINT, json = data2) 
                                #r3=  requests.post(url = API_ENDPOINT, json = data3) 
                                print("Data returned =%s"%r1.text)
                                #print("Data returned =%s"%r2.text)
                                #print("Data returned =%s"%r3.text)
                                #print(index)
                                time.sleep(1)
                                if (is_pause.is_pause):
                                        break
                                if (is_fault.is_fault != last_is_fault):
                                        break