import sys, getopt

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

poll_interval = imu.IMUGetPollInterval()
print("Recommended Poll Interval: %dmS\n" % poll_interval)

smoothed_rpm = 0
loop_counter = 0

while True:
  if imu.IMURead():
    data = imu.getIMUData()
    gyro = data["gyro"]
    rpm = math.degrees(gyro[2]) * 0.1666666667
    smoothed_rpm *= 0.992
    smoothed_rpm += rpm * 0.008
    loop_counter += 1
    if(loop_counter == 250)
        print("rpm: %f" % (smoothed_rpm))
        loop_counter = 0
    time.sleep(poll_interval*1.0/1000.0)

