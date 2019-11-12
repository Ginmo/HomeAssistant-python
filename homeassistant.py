import serial
import time
import mysql.connector
#connect to database
db_conn = mysql.connector.connect(
  host = "localhost",
  user = "root",
  passwd = "test",
  database = "test"
)

db_stmt = db_conn.cursor()

sql = "SELECT * FROM temperature"
db_stmt.execute(sql)
result = db_stmt.fetchone()
print("result: " + str(result))

SERIAL_PORT = "COM12"
SERIAL_BAUD = 9600

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
                print("Data from SerialPort: " + current_temp)
                sql = "UPDATE temperature SET currentTemperature =  %s WHERE idTemperature = %s"
                val = (current_temp, 1)
                db_stmt.execute(sql, val)
                db_conn.commit()
                print(db_stmt.rowcount, "record(s) affected")
    except:
        print("Check connections.")