import requests
import datetime
import json
url_prefix = "http://bmgxwpyyd2.execute-api.us-east-1.amazonaws.com/prod/"
API_ENDPOINT = "https://bmgxwpyyd2.execute-api.us-east-1.amazonaws.com/prod/sensordata"
def uploadImage(imageX, imageY, imageZ, rotation):
    data = {"timestamp": datetime.datetime.now().isoformat(),
            "imageX": imageX,
            "imageY": imageY,
            "imageZ": imageZ,
            "rotation": rotation } 

    url = url_prefix + "uploadimage"

    http_response = requests.post(url, json=data)


    url = json.loads(http_response.text)["URL"]

    http_response = requests.put(url, data=open('./test.jpeg', 'rb'))
    print(http_response.text)

#uploadImage(4,2,1,45)

def uploadData():

    sensor1={}
    print(sensor1)
    for i in range(25,55):
        sensor1["SM" + str(i) + "Vuc"] = str("20")
    print(sensor1)
    data1 = {'timestamp':"{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now()), 
            'sensorValues': json.dumps(sensor1)
            }
    print(json.dumps(data1))
    r1 = requests.post(url = API_ENDPOINT, json = data1) 
    print(r1.text)
uploadData()