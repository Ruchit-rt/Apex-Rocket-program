import time
import busio
import board
import pwmio

rled = pwmio.PWMOut(board.LED_R, frequency=440)
gled = pwmio.PWMOut(board.LED_G, frequency=440)
bled = pwmio.PWMOut(board.LED_B, frequency=440)

with open("phone.number") as pno:
    num = pno.readline()

def LED(r,g,b):
    rduty = int(65535 -(65535 * r/255))
    gduty = int(65535 -(65535 * g/255))
    bduty = int(65535 -(65535 * b/255))
    rled.duty_cycle = rduty
    gled.duty_cycle = gduty
    bled.duty_cycle = bduty

print("Initialising SIM")
LED(255, 0, 0)
sim = busio.UART(baudrate = 9600, rx = board.GP5, tx = board.GP4)

def send(cmd: str) -> str:
    sim.write(bytes((cmd+"\r\n").encode("ascii")))
    time.sleep(0.05)
    resp = sim.read()
    if resp is None:
        print("No response")
        return "No response"
    print(resp.decode("ascii"))
    return resp.decode("ascii")

def send_msg(msg: str, num):
    send("AT+CMGF=1") # Text message mode
    send("AT+CMGS=\""+num+"\"")
    send(msg)
    sim.write(bytes(chr(26).encode("ascii")))

        
print("Checking Connection")
send("at")
print("Getting SIM number")
send("at+ccid")
print("Check registration")
send("at+creg?")
print("Check input voltage")
send("at+cbc")
print("sending message")


while True:
    inp = input("Command: ")
    if inp == "text":
        numin = input("number: ")
        if numin != "":
            num = numin
        msg = input("message: ")
        send_msg(msg, num)
    else:
        send(inp)
    time.sleep(1)
