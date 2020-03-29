import requests
import datetime
import json

def uploadImage(imageX, imageY, imageZ, rotation):
    data = {"timestamp": datetime.datetime.now().isoformat(),
            "imageX": imageX,
            "imageY": imageY,
            "imageZ": imageZ,
            "rotation": rotation } 

    url = "http://bmgxwpyyd2.execute-api.us-east-1.amazonaws.com/prod/uploadimage"

    http_response = requests.post(url, json=data)


    url = json.loads(http_response.text)["URL"]

    http_response = requests.put(url, data=open('./test.png', 'rb'))
    print(http_response.text)

def main():
    print("Hello World!")

if __name__ == "__main__":
    main()
