import sys, mraa

sys.path.append('.')
import RTIMU
import os.path
import time
import math

SETTINGS_FILE = "RTIMULib"

print("Using settings file " + SETTINGS_FILE + ".ini")
if not os.path.exists(SETTINGS_FILE + ".ini"):
  print("Settings file does not exist, will be created")

s = RTIMU.Settings(SETTINGS_FILE)
imu = RTIMU.RTIMU(s)

print("IMU Name: " + imu.IMUName())

if (not imu.IMUInit()):
    print("IMU Init Failed")
    sys.exit(1)
else:
    print("IMU Init Succeeded")

# this is a good time to set any fusion parameters

imu.setSlerpPower(0.02)
imu.setGyroEnable(True)
imu.setAccelEnable(True)
imu.setCompassEnable(True)

smoothed_rpm = 0
flight_time = 0
#top_score = 0


uart = mraa.Uart(0)
uart.setBaudRate(9600)
uart.setMode(8, mraa.UART_PARITY_NONE, 1)
uart.setFlowcontrol(False, False)

uart.writeStr(chr(255))
print("sent: " + chr(255)) //i = 255

while True:
    if imu.IMURead():
        data = imu.getIMUData()
        gyro = data["gyro"]
        rpm = math.degrees(gyro[2]) * 0.1666666667
        smoothed_rpm *= 0.75
        smoothed_rpm += rpm * 0.25

        print("rpm: %f" % (smoothed_rpm))

        if flight_time == 0 and smoothed_rpm >= 5:
            flight_time = time.time()
        elif flight_time != 0 and smoothed_rpm < 5:
            flight_time = 0

        if smoothed_rpm >= 5:
            print("here")
            #uart.writeStr(chr(charmath.round(smoothed_rpm / 10, 0))
            #print("sent: " + chr(charmath.round(smoothed_rpm / 10, 0))
        else:
            uart.writeStr(chr(254))
            print("sent: " + chr(254)) //r = 254

        time.sleep(1)

