import serial
import time
import requests

SERIAL_PORT = "COM3"
SERIAL_BAUD = 9600

current_temp = "0"
counter = 0
status = "0"


def rTemperature(currentTemp):
    try:
        rTemp = requests.post('http://ec2-35-158-176-134.eu-central-1.compute.amazonaws.com/temperature',
                              json={'temperature': currentTemp})
        print(rTemp.status_code)

    except requests.exceptions.MissingSchema:
        print("Invalid URL")


def rLights():
    rLights = requests.get('http://ec2-35-158-176-134.eu-central-1.compute.amazonaws.com/lights/1')
    print(rLights.status_code)
    data = rLights.json()

    return data


while True:
    
    ser = serial.Serial(SERIAL_PORT, SERIAL_BAUD, timeout=0, write_timeout=0)
    time.sleep(2)
    print("Connected to SerialPort: " + str(SERIAL_PORT) + ", baud rate: " + str(SERIAL_BAUD))

    

    while True:
        read_serial = ser.readline().decode('utf-8')  # Removing b, \r, \n from the line

        if read_serial[:12] == "Temperature1":
            current_temp = read_serial[14:]
            current_temp = current_temp.rstrip()
            

        if counter == 4:
            rTemperature(current_temp)
            status = rLights()
            counter = 0
            time.sleep(0.5)
        else:
            status = rLights()
            counter = counter + 1
            time.sleep(0.5)
            
        ser.write(status[0]['lightStatus'].encode())

        if read_serial[:6] == "lights":
            current_lights = read_serial[8:]
            print(current_lights)

        time.sleep(0.5)
