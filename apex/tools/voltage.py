import time
import serial
import mouse
from random import randint

ser = serial.Serial("COM12", 9600)
text = ""

n = 1000

start = time.time()
for i in range(n):
    cc = str(ser.readline())[2:][:-5]
    l = str(time.time() - start) + ", " + cc + "\n"
    text += l
    print(l, i, n)
    mouse.move(randint(0, 500), randint(0, 500))

data = open("voltage.csv", "w")
data.write(text)
data.close()
