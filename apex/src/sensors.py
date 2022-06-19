from time import monotonic_ns
import struct
from adafruit_dps310.advanced import DPS310, Mode, Rate, SampleCount
import board
from busio import I2C
from adafruit_bno08x.i2c import BNO08X_I2C

from adafruit_bno08x import (
    BNO_REPORT_ACCELEROMETER,
    BNO_REPORT_GYROSCOPE,
    BNO_REPORT_MAGNETOMETER,
    BNO_REPORT_LINEAR_ACCELERATION,
    BNO_REPORT_GEOMAGNETIC_ROTATION_VECTOR,
    BNO_REPORT_ROTATION_VECTOR
)

#Data structure:
# Time: uint32
# Acceleration: (float32, float32, float32)
# Gyroscope: (float32, float32, float32)
# Magnetometer: (float32, float32, float32)
# Linear acceleration: (float32, float32, float32)
# Geomagnetic rotation vector: (float32, float32, float32, float32)
# Rotation vector: (float32, float32, float32, float32)
# Pressure: float32
# Temperature: float32

_DATA_SIZE = 23 * 4

class Sensors:
    _bytes = bytearray(_DATA_SIZE)

    def __init__(self) -> None:
        i2c = I2C(sda=board.SDA1, scl=board.SCL1) #type: ignore
        self._dps = DPS310(i2c)
        self._dps.reset()
        self._dps.pressure_oversample_count = SampleCount.COUNT_2 #type: ignore
        self._dps.pressure_rate = Rate.RATE_16_HZ #type: ignore
        self._dps.temperature_oversample_count = SampleCount.COUNT_16 #type: ignore
        self._dps.temperature_rate = Rate.RATE_16_HZ #type: ignore
        self._dps.mode = Mode.CONT_PRESTEMP #type: ignore
      
        self._dps.initialize()
        self._dps.wait_pressure_ready()
        self._dps.wait_temperature_ready()

        self._bno = BNO08X_I2C(i2c)
        self._bno.initialize()
        self._bno.enable_feature(BNO_REPORT_ACCELEROMETER)
        self._bno.enable_feature(BNO_REPORT_GYROSCOPE)
        self._bno.enable_feature(BNO_REPORT_MAGNETOMETER)
        self._bno.enable_feature(BNO_REPORT_LINEAR_ACCELERATION)
        self._bno.enable_feature(BNO_REPORT_GEOMAGNETIC_ROTATION_VECTOR)
        self._bno.enable_feature(BNO_REPORT_ROTATION_VECTOR)

    def calibrate(self):
        self._bno.begin_calibration()

    def packData(self) -> bytearray:
        now = monotonic_ns() // 1_000_000 #To ms
        acceleration = self._bno.acceleration
        gyroscope = self._bno.gyro
        magnetometer = self._bno.magnetic
        linear_acceleration = self._bno.linear_acceleration
        geomagnetic_rotation_vector = self._bno.geomagnetic_quaternion
        rotation_vector = self._bno.quaternion
        pressure = self._dps.pressure
        temperature = self._dps.temperature

        struct.pack_into("I", self._bytes, 0, now)
        struct.pack_into("fff", self._bytes, 4, *acceleration)
        struct.pack_into("fff", self._bytes, 16, *gyroscope)
        struct.pack_into("fff", self._bytes, 28, *magnetometer)
        struct.pack_into("fff", self._bytes, 40, *linear_acceleration)
        struct.pack_into("ffff", self._bytes, 52, *geomagnetic_rotation_vector)
        struct.pack_into("ffff", self._bytes, 68, *rotation_vector)
        struct.pack_into("f", self._bytes, 84, pressure)
        struct.pack_into("f", self._bytes, 88, temperature)

        return self._bytes
