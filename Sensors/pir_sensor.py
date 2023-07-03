# -*- coding: utf-8 -*-

import wiringpi

wiringpi.wiringPiSetup()

PIR_PIN = 5

# PIR_PIN을 입력으로 설정
wiringpi.pinMode(PIR_PIN, wiringpi.INPUT)


def read_pir_sensor():
    if wiringpi.digitalRead(PIR_PIN):
        return 1  # PIR 센서 감지 여부에 따라 값을 반환 (1 또는 0)
    else:
        return 0
