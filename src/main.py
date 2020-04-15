import requests
import datetime
import json
import threading
import time
import socket
import pyaudio

import astar
import iforest

url_prefix = "http://bmgxwpyyd2.execute-api.us-east-1.amazonaws.com/prod/"

class IsFault:
   def __init__(self):
       self.is_fault = False

   def fault(self):
       self.is_fault = True
   def no_fault(self):
       self.is_fault = False

def main():
    audioThread = threading.Thread(target=audioThreadFunction, daemon=True)
    audioThread.start()

    is_fault = IsFault()
    sensorDataThread = threading.Thread(target=iforest.sensor_data, args=(is_fault,), daemon=True)
    sensorDataThread.start()

    url = url_prefix + "sensordata"
    maze = [[1 for j in range(100)] for i in range(100)]

    for x in range(100):
        for y in range(100):
            if(31 <= x <= 39 or 70 <= x <= 77 or 55 <= y <= 64 or 25 <= y <= 34):
                maze[x][y] = 0
    
    lastGoToX = 0
    lastGoToY = 0
    currentX = 0
    currentY = 0
    pathFollowThread = 0

    response_cloud = requests.get(url)
    sensorValues = json.loads(response_cloud.json()['sensorValues'])
    
    lastDroneImageX = sensorValues['droneImageX']
    lastDroneImageY = sensorValues['droneImageY']
    lastDroneImageZ = sensorValues['droneImageZ']
    lastDroneImageRot = sensorValues['droneImageRot']
    while 1:
        response_cloud = requests.get(url)

        sensorValues = json.loads(response_cloud.json()['sensorValues'])

        currentX = round(translate(float(sensorValues['robotCoordX']), -5.0, 8.0, 1.0, 100.0))
        currentY = round(translate(float(sensorValues['robotCoordY']), 3.0, 13.0, 1.0, 100.0))
        goToX = round(translate(float(sensorValues['robotGoToX']), -5.0, 8.0, 1.0, 100.0))
        goToY = round(translate(float(sensorValues['robotGoToY']), 3.0, 13.0, 1.0, 100.0))

        if ((currentX != goToX or currentY != goToY) and (lastGoToX != goToX or lastGoToY != goToY)):
            if (pathFollowThread != 0 and pathFollowThread.is_alive()):
                pathFollowThread.stop = True
                while(pathFollowThread.is_alive()):
                    time.sleep(0.01)
            lastGoToX = goToX
            lastGoToY = goToY
            start = (currentX, currentY)
            end = (goToX, goToY)

            path = astar.astar(maze, start, end)
            print(path)

            pathFollowThread = threading.Thread(target=pathFollowFunction, args=(path,))
            pathFollowThread.start()
        
        droneImageX = sensorValues['droneImageX']
        droneImageY = sensorValues['droneImageY']
        droneImageZ = sensorValues['droneImageZ']
        droneImageRot = sensorValues['droneImageRot']
        if (lastDroneImageX != droneImageX or lastDroneImageY != droneImageY or lastDroneImageZ != droneImageZ or lastDroneImageRot != droneImageRot):
            print("uploading image")
            lastDroneImageX = droneImageX
            lastDroneImageY = droneImageY
            lastDroneImageZ = droneImageZ
            lastDroneImageRot = droneImageRot
            uploadImage(droneImageX, droneImageY, droneImageZ, droneImageRot)

        if (sensorValues['isFault'] == "1"):
            is_fault.fault()
        else:
            is_fault.no_fault()
        time.sleep(1)

def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)

def pathFollowFunction(path):
    t = threading.currentThread()
    url = url_prefix + "sensordata"
    for i in range(len(path)-1):
        if (i%3 != 0):
            continue
        coord = path[i]
        if (getattr(t, "stop", False)):
            print("stopping")
            return
        print(coord)
        coord_current_X = translate(coord[0], 1.0, 100.0, -5.0, 8.0)
        coord_current_Y = translate(coord[1], 1.0, 100.0, 3.0, 13.0)
        
        coords = {"robotCoordX": str(coord_current_X),
                  "robotCoordY": str(coord_current_Y)}
        
        data = {
            "timestamp": "{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now()),
            "sensorValues": json.dumps(coords)
        }

        requests.post(url, json=data)

    coord = path[-1]
    print(coord)
    coord_current_X = translate(coord[0], 1.0, 100.0, -5.0, 8.0)
    coord_current_Y = translate(coord[1], 1.0, 100.0, 3.0, 13.0)
    
    coords = {"robotCoordX": str(coord_current_X),
                "robotCoordY": str(coord_current_Y)}
    
    data = {
        "timestamp": "{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now()),
        "sensorValues": json.dumps(coords)
    }

    requests.post(url, json=data)


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

def audioThreadFunction():
    while 1:
        url = url_prefix + "audio"
        timeout = True
        while (timeout):
            data = {"linkID": "1",
                    "sender": True } 

            ip = "0.0.0.0"
            timeout = False
            while (ip == "0.0.0.0"):
                http_response = requests.post(url, json=data)
                ip = json.loads(http_response.text)["ip"]
                time.sleep(1)

            print(ip)
            port = json.loads(http_response.text)["port"]

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)

            try:
                s.connect((ip, port))
            except socket.timeout:
                print("No Audio Reciever")
                data = {"linkID": "1",
                        "sender": True,
                        "port": port,
                        "ip": ip,
                        "invalid": True } 

                http_response = requests.post(url, json=data)
                timeout = True
            except socket.error:
                print("No Audio Reciever")
                data = {"linkID": "1",
                        "sender": True,
                        "port": port,
                        "ip": ip,
                        "invalid": True } 

                http_response = requests.post(url, json=data)
                timeout = True
            s.settimeout(None)

        FORMAT = pyaudio.paFloat32
        CHANNELS = 1
        RATE = 44100*2
        CHUNK = 2048
        
        audio = pyaudio.PyAudio()

        for i in range(audio.get_device_count()):
            dev = audio.get_device_info_by_index(i)
            input_chn = dev.get('maxInputChannels', 0)
            if input_chn > 0:
                name = dev.get('name')
                rate = dev.get('defaultSampleRate')
                print("Index {i}: {name} (Max Channels {input_chn}, Default @ {rate} Hz)".format(
                    i=i, name=name, input_chn=input_chn, rate=int(rate)

                ))
        
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK,
                        input_device_index=0)

        try:
            while 1:
                s.send(stream.read(CHUNK, exception_on_overflow=False))
        except BrokenPipeError:
            stream.stop_stream()
            stream.close()
            audio.terminate()

if __name__ == "__main__":
    main()
