import sys
import socket
import json

# Makefile arguments
api_key = sys.argv[1]
city = sys.argv[2]

# Information for socket
HOST = "api.openweathermap.org"   
PORT = 80
msg = "GET /data/2.5/weather?q={}&APPID={}&units=metric HTTP/1.1\r\nHost: {}\r\n\r\n".format(city, api_key, HOST)

# Connect to API server and send message
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sckt:
        sckt.connect((HOST, PORT))
        sckt.send(msg.encode())    
        data = sckt.recv(1024)
except Exception as error:
    print("API connection ERROR ({})".format(error))
    sys.exit(1)

# Decode and convert data into JSON
try:
    data = data.decode()
    data = data[data.find('{'):]
    data = json.loads(data)
except Exception as error:
    print("Data processing ERROR ({})".format(error))
    sys.exit(1)

# Print out the result
if data.get("cod") != 200:
    print("ERROR {}: {}".format(data["cod"], data["message"]))
    sys.exit(1)
else:
    print(city)
    print(data["weather"][0]["description"])
    
    if  data["main"].get("temp", -1) != -1:
        print("temp:{}°C".format(data["main"]["temp"]))
        
    if  data["main"].get("humidity", -1) != -1:
        print("humidity:{}%".format(data["main"]["humidity"]))
        
    if  data["main"].get("pressure", -1) != -1:
        print("pressure:{} hPa".format(data["main"]["pressure"]))
    
    if  data["wind"].get("speed", -1) != -1:
        print("wind-speed:{} km/h".format(data["wind"]["speed"]))

    if  data["wind"].get("deg", -1) != -1:
        print("wind-deg:{}".format(data["wind"]["deg"]))
