# art-apex
PCBs and software for ART's APEX rocket

# Contents

1. [Hardware](#Hardware)
2. [Software architecture](#SoftwareArchitecture)
3. [Next Steps](#NextSteps)

## Hardware

The flight computer for Apex consists of the following components:

1. [Tiny2040](https://shop.pimoroni.com/products/tiny-2040) microcontroller - for controlling each of the components
2. [BNO085](https://learn.adafruit.com/adafruit-9-dof-orientation-imu-fusion-breakout-bno085) 9DoF IMU - for recording and fusing flight data
3. [DPS310](https://www.infineon.com/cms/en/product/sensor/pressure-sensors/pressure-sensors-for-iot/dps310/) barometer - for recording altitude information
4. [Sim800L](https://nettigo.eu/products/sim800l-gsm-grps-module) GPRS/GSM module - for communication between the flight computer and ground team
5. [Adafruit mini GPS PA1010D](https://www.adafruit.com/product/4415) GPS module - for recovery
6. 3.7V 200maH LiPo battery - for powering the system
7. A 104 decibel speaker - for recovery

The Tiny2040 is connected to the BNO085, DPS310 and PA1010D via an I2C connection using GPIO pins 26 and 27. The Tiny2040 is connected to the Sim800L module via a UART connection using GPIO pins 4 and 5.

The SIM8000L **must** be isolated when the Tiny2040 is connected to USB, or else it will be fried.

## Software

The filesystem on board the Tiny2040 will look like this:
```
📦src
 ┣ 📂lib
 ┃ ┣ 📂adafruit_bno08x
 ┃ ┃ ┣ 📜debug.py
 ┃ ┃ ┣ 📜i2c.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂adafruit_bus_device
 ┃ ┃ ┣ 📜i2c_device.mpy
 ┃ ┃ ┣ 📜spi_device.mpy
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📂adafruit_register
 ┃ ┃ ┣ 📜i2c_bcd_alarm.mpy
 ┃ ┃ ┣ 📜i2c_bcd_datetime.mpy
 ┃ ┃ ┣ 📜i2c_bit.mpy
 ┃ ┃ ┣ 📜i2c_bits.mpy
 ┃ ┃ ┣ 📜i2c_struct.mpy
 ┃ ┃ ┣ 📜i2c_struct_array.mpy
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📜adafruit_dps310.mpy
 ┃ ┗ 📜adafruit_gps.py
 ┣ 📜boot.py
 ┣ 📜code.py
 ┣ 📜gps.py
 ┣ 📜led.py
 ┣ 📜phone.number
 ┣ 📜sensors.py
 ┣ 📜sms.py
 ┣ 📜speaker.py
 ┗ 📜state_machine.py
```

All folders inside the lib directory are libraries required for the Tiny2040 to interact with components. None of these files should be changed, except for lib/adafruit_bno08x/\_\_init__.py, where `_DEFAULT_REPORT_INTERVAL` should be set to 35ms. **Pro tip: don't lower this if you want to launch**.

`boot.py` runs right after the Tiny2040 boots up. Its sole purpose is to grant write permission to the Tiny2040. Due to the implementation of CircuitPython's filesystem either a laptop or the Tiny2040, can write to the Tiny2040's filesystem, so this ensures that the Tiny2040 has this permission.

`code.py` runs the main code of the AAS. It essentially runs through the state machine defined in `state_machine.py`.

`gps.py`, `led.py`, `sensors.py`, `speaker.py` and `sms.py` are [adapters](https://www.tutorialspoint.com/design_pattern/adapter_pattern.htm) around the peripherals discussed above. The adapter pattern is used to decouple the rest of the code from the specifics of these devices.

`state_machine.py` contains the bulk of the flight logic. It describes a (linear) [finite state machine](https://en.wikipedia.org/wiki/Finite-state_machine) with 5 states.

1. Diagnostic - initialises sensors and sends initial messages
2. Calibration - calibrates the BNO085 as described [here](https://www.ceva-dsp.com/wp-content/uploads/2019/10/BNO080_085-Datasheet.pdf) on page 39
3. Preflight - sleeps until the launch command is sent.
4. Flight - records 5 minutes of flight data, and sends data to the telemetry service.
5. Postflight - sends the rocket's location/plays the siren when asked. Also plays the siren once every 30 seconds.

The Flight stage is the most involved, so a brief explanation of its code can be found below.

```py
def run(self):
    i = 0
    led.colour(255, 0, 0)

    #Problem:
    #Sim module will need long (50ms+) waits to work
    #But we can't afford that in a single threaded environment
    #Solution:
    #Use pkt_wait to provide the sleeps
    pkt_wait = 1
    pkt = bytearray(sensors.data_size * 4)
    self._sms.connect()

    while i < self._flight_time:
        pkt_wait -= 1
        i += 1
        start = millis()
        data = self._sensors.get()
        for reading in data:
            self._sensor_storage.write(struct.pack("f", reading))

        if pkt_wait == 0:
            pkt[0:4] = struct.pack("f", data[0]) #time
            for j in range(4):
                pkt[4*j:4*(j+1)] = struct.pack("f", data[j+4])
            
            pkt[20:24] = struct.pack("f", data[10]) #altitude
            pkt_wait = self._sms.send_pkt(pkt)
        end = millis()
        sleep_ms(max(0, self._delay - (end - start)))

    self._sensor_storage.flush()
    self._sensor_storage.close()
    self._sms.disconnect()
    return postflight(self._sms, self._gps)
```

```py
led.colour(255, 0, 0)
```
First the Tiny2040's led is set to red to indicate flight.

```py
pkt_wait = 1
pkt = bytearray(sensors.data_size * 4)
self._sms.connect()
```
This code relates to the telemetry service. The Sim800L will connect to GPRS here (the internet) and send appropriate data via UDP. To save space, it will group several readings into a single packet.

```py
while i < self._flight_time:
    pkt_wait -= 1
    i += 1
    start = millis()
    data = self._sensors.get()
    for reading in data:
        self._sensor_storage.write(struct.pack("f", reading))

    if pkt_wait == 0:
        pkt[0:4] = struct.pack("f", data[0]) #time
        for j in range(4):
            pkt[4*j:4*(j+1)] = struct.pack("f", data[j+4])
        
        pkt[20:24] = struct.pack("f", data[10]) #altitude
        pkt_wait = self._sms.send_pkt(pkt)
    end = millis()
    sleep_ms(max(0, self._delay - (end - start)))
```

This is the main flight loop. It waits for `self._flight_time` readings to occur (assuming each reading takes at most `self._delay` ms).

```py
start = millis()
data = self._sensors.get()
for reading in data:
    self._sensor_storage.write(struct.pack("f", reading))
```
This code takes sensor readings, and records the time that they were taken, then writes them into a file. The values are stored as 32bit floating point numbers, to save space.
Note: the time recorded is milliseconds from the start.

```py
if pkt_wait == 0:
    pkt[0:4] = struct.pack("f", data[0]) #time
    for j in range(4):
        pkt[4*j:4*(j+1)] = struct.pack("f", data[j+4])
    
    pkt[20:24] = struct.pack("f", data[10]) #altitude
    pkt_wait = self._sms.send_pkt(pkt)
```
This adds the readings into the packet defined earlier, and if the packet is full it sends them.

The `pkt_wait` variable is used to solve a problem, which is that the Sim800l needs to wait around 200ms after it's sent a packet, before being able to send another one. However we can't perform this wait in the main loop, as that would lead to large delays in between recordings, so we define the `pkt_wait` variable to indicate whether we can send a packet. This allows us to use the main loop as a pseudo sleep (at the time of writing, the `uasynchio` library was not available).


```py
end = millis()
sleep_ms(max(0, self._delay - (end - start)))
```
This ensures that we always sleep for at least 50ms, regardless of how long different components take to work.

```py
self._sensor_storage.flush()
self._sensor_storage.close()
self._sms.disconnect()
return postflight(self._sms, self._gps)
```
Finally we flush the recordings, and close the file, then disconnect the Sim800L from GPRS and move on to the postflight stage. 

The end.
