import serial
import serial.tools.list_ports
import time

list_port = serial.tools.list_ports.comports()
ser = serial.Serial(list_port[0].device, 9600)
ser.write(b'NR')
time.sleep(1)
while 1:
    ser.write(f"V{0.02};{0.02}R\n".encode())
    print("coucou")