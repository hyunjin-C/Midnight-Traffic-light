# -*- coding: utf-8 -*-

import time
import wiringpi

PIN_TRIG = 12
PIN_ECHO = 14
RANGE_MAX = 200
RANGE_MIN = 0

PIN_TRIG_R = 16  # phy=16
PIN_ECHO_R = 20


wiringpi.wiringPiSetup()

count = 0
count_1 = 0
time = 0

def read_ultrasonic_sensor():
  wiringpi.pinMode(PIN_TRIG, 1)  # OUTPUT
  wiringpi.pinMode(PIN_ECHO, 0)  # INPUT
  
  wiringpi.pinMode(PIN_TRIG_R, 1)  # OUTPUT
  wiringpi.pinMode(PIN_ECHO_R, 0)  # INPUT
  
  while time <= 10:
      wiringpi.digitalWrite(PIN_TRIG, 0)  # LOW
      time.sleep(0.002)
      wiringpi.digitalWrite(PIN_TRIG, 1)  # HIGH
      time.sleep(0.02)
      wiringpi.digitalWrite(PIN_TRIG, 0)  # LOW
  
      while wiringpi.digitalRead(PIN_ECHO) == 0:
          start_time = time.time()
      while wiringpi.digitalRead(PIN_ECHO) == 1:
          end_time = time.time()
  
      duration = end_time - start_time
      distance = (duration * 34300) / 2
  
      if distance <= 15:
          count += 1
  
      wiringpi.digitalWrite(PIN_TRIG_R, 0)  # LOW
      time.sleep(0.002)
      wiringpi.digitalWrite(PIN_TRIG_R, 1)  # HIGH
      time.sleep(0.02)
      wiringpi.digitalWrite(PIN_TRIG_R, 0)  # LOW
  
      while wiringpi.digitalRead(PIN_ECHO_R) == 0:
          start_time_R = time.time()
      while wiringpi.digitalRead(PIN_ECHO_R) == 1:
          end_time_R = time.time()
  
      duration_R = end_time_R - start_time_R
      distance_R = (duration_R * 34300) / 2
  
      if distance_R <= 15:
          count_1 += 1
  
      time.sleep(0.3)
      time += 1
  
  if count >= 10 or count_1 >= 10:
      print("success")
      return 1
  else:
      print("fail")
      return 0
