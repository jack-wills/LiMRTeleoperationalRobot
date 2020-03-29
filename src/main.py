import requests
import datetime
import json
import threading
import time
import socket
import pyaudio

url_prefix = "http://bmgxwpyyd2.execute-api.us-east-1.amazonaws.com/prod/"

def main():
    audioThread = threading.Thread(target=audioThreadFunction, args=(1,))
    audioThread.start()

    while 1:
        print("hello world")

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
