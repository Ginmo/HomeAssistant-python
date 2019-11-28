import serial
import time
import requests


SERIAL_PORT = "COM12"
SERIAL_BAUD = 9600


def rTemperature(currentTemp):
    try:
        rTemp = requests.post('http://ec2-35-158-176-134.eu-central-1.compute.amazonaws.com/temperature', json={'temperature': currentTemp})
        print (rTemp.status_code)

    except requests.exceptions.MissingSchema:
        print("Invalid URL")
    finally:
        time.sleep(5)

def rLights():
    rLights = requests.get('http://ec2-35-158-176-134.eu-central-1.compute.amazonaws.com/lights/1')
    print(rLights.status_code)
    data = rLights.json()

    ser.write(data[0]['lightStatus'])
    time.sleep(1)



while True:
    try:
        SERIAL_PORT = input("SerialPort: ")
        SERIAL_BAUD = input("Baud Rate: ")
        ser = serial.Serial(SERIAL_PORT, SERIAL_BAUD)
        time.sleep(2)
        print("Connected to SerialPort: " + str(SERIAL_PORT) + ", baud rate: " + str(SERIAL_BAUD))

        while True:
            read_serial = ser.readline().decode('utf-8') # Removing b, \r, \n from the line

            if read_serial[:12] == "Temperature1":
                current_temp = read_serial[14:]
                #print("Data from SerialPort: " + current_temp)
                rTemperature(current_temp)

            rLights()
                
                

    except:
        print("Check connections.")