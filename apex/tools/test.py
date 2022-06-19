import time
import board
import busio
import pwmio
from math import sin
import adafruit_dps310
import adafruit_gps
from adafruit_bno08x import BNO_REPORT_ACCELEROMETER, BNO_REPORT_GYROSCOPE, BNO_REPORT_MAGNETOMETER, BNO_REPORT_ROTATION_VECTOR
from adafruit_bno08x.i2c import BNO08X_I2C
import rtc

rled = pwmio.PWMOut(board.LED_R, frequency=440)
gled = pwmio.PWMOut(board.LED_G, frequency=440)
bled = pwmio.PWMOut(board.LED_B, frequency=440)

# speaker = pwmio.PWMOut(board.GP7, frequency = 440)
# speaker.duty_cycle = 65535

# Turn off
rduty = 65535
gduty = 65535
bduty = 65535
rled.duty_cycle = rduty
gled.duty_cycle = gduty
bled.duty_cycle = bduty
f = 0.1

def LED(r,g,b):
    rduty = int(65535 -(65535 * r/255))
    gduty = int(65535 -(65535 * g/255))
    bduty = int(65535 -(65535 * b/255))
    rled.duty_cycle = rduty
    gled.duty_cycle = gduty
    bled.duty_cycle = bduty


# # initialise i2c
# print("Initialising I2C")
# LED(255, 255, 255)
# i2c = busio.I2C(scl=board.GP27, sda=board.GP26, frequency=100000, timeout=100000)  # uses board.SCL and board.SDA
# time.sleep(2)

# #initialise boards
# print("Initialising BARO")
# LED(255, 0, 0)
# dps310 = adafruit_dps310.DPS310(i2c)
# time.sleep(2)

# print("Initialising GPS")
# LED(0, 0, 255)
# gps = adafruit_gps.GPS_GtopI2C(i2c)
# time.sleep(1)
# gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
# time.sleep(1)
# gps.send_command(b"PMTK220,1000")
# time.sleep(1)
# print("Set GPS as time source")
# rtc.set_time_source(gps)
# the_rtc = rtc.RTC()

# def _format_datetime(datetime):
#     return "{:02}/{:02}/{} {:02}:{:02}:{:02}".format(
#         datetime.tm_mon,
#         datetime.tm_mday,
#         datetime.tm_year,
#         datetime.tm_hour,
#         datetime.tm_min,
#         datetime.tm_sec,
#     )

# print("Initialising BNO")
# LED(0, 20, 0)
# bno = BNO08X_I2C(i2c)
# time.sleep(1)
# print("Enabling Acc")
# LED(0, 40, 0)
# bno.enable_feature(BNO_REPORT_ACCELEROMETER)
# time.sleep(1)
# print("Enabling Gyro")
# LED(0, 80, 0)
# bno.enable_feature(BNO_REPORT_GYROSCOPE)
# time.sleep(1)
# print("Enabling Magnet")
# LED(0, 160, 0)
# bno.enable_feature(BNO_REPORT_MAGNETOMETER)
# time.sleep(1)
# print("Enabling Rotation")
# LED(0, 255, 0)
# bno.enable_feature(BNO_REPORT_ROTATION_VECTOR)
# time.sleep(1)

# last_print = time.monotonic()
# gps.update()

# while True:
#     print("Temperature = %.2f *C" % dps310.temperature)
#     print("Pressure = %.5f Pa" % (dps310.pressure*100))
#     print("")

#     print("Acceleration:")
#     accel_x, accel_y, accel_z = bno.acceleration  # pylint:disable=no-member
#     print("X: %0.6f  Y: %0.6f Z: %0.6f  m/s^2" % (accel_x, accel_y, accel_z))

#     print("Rotation Vector Quaternion:")
#     quat_i, quat_j, quat_k, quat_real = bno.quaternion  # pylint:disable=no-member
#     print("I: %0.6f  J: %0.6f K: %0.6f  Real: %0.6f" % (quat_i, quat_j, quat_k, quat_real))
#     print("")

#     current = time.monotonic()
#     if current - last_print >= 1.0:
#         last_print = current
        
#         if not gps.has_fix:
#             # Try again if we don't have a fix yet.
#             print("Waiting for fix...")
#             # if not gps.timestamp_utc:
#             #     print("No time data from GPS yet")
#             #     print("RTC timestamp: {}".format(_format_datetime(the_rtc.datetime)))
#             #     continue
#             # # Time & date from GPS informations
#             # print("Fix timestamp: {}".format(_format_datetime(gps.timestamp_utc)))

#             # # Time & date from internal RTC
#             # print("RTC timestamp: {}".format(_format_datetime(the_rtc.datetime)))

#             # # Time & date from time.localtime() function
#             # local_time = time.localtime()

#             # print("Local time: {}".format(_format_datetime(local_time)))
#             continue
#         # We have a fix! (gps.has_fix is true)
#         # Print out details about the fix like location, date, etc.
#         print("=" * 40)  # Print a separator line.
#         print(
#             "Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}".format(
#                 gps.timestamp_utc.tm_mon,  # Grab parts of the time from the
#                 gps.timestamp_utc.tm_mday,  # struct_time object that holds
#                 gps.timestamp_utc.tm_year,  # the fix time.  Note you might
#                 gps.timestamp_utc.tm_hour,  # not get all data like year, day,
#                 gps.timestamp_utc.tm_min,  # month!
#                 gps.timestamp_utc.tm_sec,
#             )
#         )
#         print("Latitude: {0:.6f} degrees".format(gps.latitude))
#         print("Longitude: {0:.6f} degrees".format(gps.longitude))
#         print("Fix quality: {}".format(gps.fix_quality))
#         # Some attributes beyond latitude, longitude and timestamp are optional
#         # and might not be present.  Check if they're None before trying to use!
#         if gps.satellites is not None:
#             print("# satellites: {}".format(gps.satellites))
#         if gps.altitude_m is not None:
#             print("Altitude: {} meters".format(gps.altitude_m))
#         if gps.speed_knots is not None:
#             print("Speed: {} knots".format(gps.speed_knots))
#         if gps.track_angle_deg is not None:
#             print("Track angle: {} degrees".format(gps.track_angle_deg))
#         if gps.horizontal_dilution is not None:
#             print("Horizontal dilution: {}".format(gps.horizontal_dilution))
#         if gps.height_geoid is not None:
#             print("Height geo ID: {} meters".format(gps.height_geoid))

#     # for i in range(255):
#     #     r = sin(f*i)*127 + 128
#     #     g = sin((f*i)+2)*127 + 128
#     #     b = sin((f*i)+4)*127 + 128
#     #     LED(r, g, b)
#     #     #print(r, g, b)
#     #     time.sleep(0.01)

#     for j in range(0, 250, 50):
#         gps.update()
#         for i in range(j, j+50):
#             r = sin(f*i)*127 + 128
#             g = sin((f*i)+2)*127 + 128
#             b = sin((f*i)+4)*127 + 128
#             LED(r, g, b)
#             #print(r, g, b)
#             time.sleep(0.005)
#     #time.sleep(1.0)

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

def send_msg(self, msg: str):
    send("AT+CMGF=1") # Text message mode
    send("AT+CMGS=\"{OWNER_NUMBER}\"")
    send(msg)
    sim.write(bytes(chr(26)))

print("Checking Connection")
send("at")
print("Getting SIM number")
send("at+ccid")
print("Check registration")
send("at+creg?")
print("Check inout voltage")
send("at+cbc")
