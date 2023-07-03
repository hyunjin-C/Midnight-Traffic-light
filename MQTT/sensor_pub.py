# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
from pir_sensor import read_pir_sensor
import time

# MQTT 클라이언트 생성
client = mqtt.Client()

# MQTT 브로커에 연결되었을 때 호출되는 콜백 함수


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("MQTT broker connected.")
    else:
        print("MQTT broker not connected. code:", rc)


# MQTT 브로커에 연결
broker_address = "localhost"
broker_port = 1883  # MQTT 브로커의 포트
client.connect(broker_address, broker_port, 60)

# PIR 센서 값을 읽고 MQTT로 publish하는 함수


def publish_pir_sensor_value():
    new_sensor_value = read_pir_sensor()  # PIR 센서 값을 읽어옴

    if new_sensor_value is not None:  # 값이 반환되었을 때만 변수에 할당
        pir_sensor_value = new_sensor_value
        print("pir_sensor_value: ", pir_sensor_value)
        # PIR 센서 값을 MQTT로 publish
        pir_topic = "sensors/pir"
        if (pir_sensor_value == 1):
            client.publish(pir_topic, pir_sensor_value, qos=2)
            time.sleep(46)
        else:
            client.publish(pir_topic, pir_sensor_value, qos=2)


def on_publish(client, userdata, mid):
    print("Message published successfully")


# MQTT 클라이언트 실행
client.on_connect = on_connect
client.on_publish = on_publish

client.loop_start()

# 일정 간격으로 PIR 센서 값을 publish
while True:
    publish_pir_sensor_value()
    time.sleep(1)
