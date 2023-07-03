# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt
import os
import subprocess
import time
import threading


# MQTT 메시지를 받았을 때 segment_count.c 실행
def execute_segment_count(payload):
    command = ['./segment_count', str(payload)]
    print("Executing C file with payload:", payload)
    start_time = time.time()  # C파일 실행 시작 시간 기록
    subprocess.run(command)
    end_time = time.time()  # C파일 실행 종료 시간 기록
    execution_time = end_time - start_time
    print("C file execution time:", execution_time, "seconds")

# 스레드를 통해 실행할 함수


def run_scripts(payload):
    # 스레드를 사용하여 segment_count.c 실행
    segment_count_thread = threading.Thread(
        target=execute_segment_count, args=(payload,))
    segment_count_thread.start()

    # camera_sensor.py 실행
    camera_sensor_command = ['python3', './camera_sensor.py']
    camera_sensor_start_time = time.time()
    subprocess.run(camera_sensor_command)
    camera_sensor_end_time = time.time()
    camera_sensor_execution_time = camera_sensor_end_time - camera_sensor_start_time
    print("camera_sensor.py execution time:",
          camera_sensor_execution_time, "s")

    # segment_count.c 스레드 종료 대기
    segment_count_thread.join()

# MQTT 브로커에 연결되었을 때 호출되는 콜백 함수


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("MQTT broker connected")
        client.subscribe(pir_topic)

    else:
        print("MQTT broker not connected. code:", rc)

# 메시지가 도착했을 때 호출되는 콜백 함수


def on_message(client, userdata, msg):
    payload = int(msg.payload)
    print("message:", msg.topic + " " + str(payload))
    if (payload == 1):
        run_scripts(payload)  # segment_count.c와 camera_sensor.py 실행
    elif (payload == 0):
        execute_segment_count(payload)
        return


#  MQTT 브로커 정보
# broker_address = "192.168.0.46"  # MQTT 브로커의 주소
broker_port = 1883  # MQTT 브로커의 포트
pir_topic = "sensors/pir"

# MQTT 클라이언트 생성
client = mqtt.Client()

# 연결 및 콜백 함수 설정
client.on_connect = on_connect
client.on_message = on_message

# MQTT 브로커에 연결
client.connect("localhost", broker_port, 60)

# 무게 센서 값을 전달받을 토픽 설정
# weight_topic = "sensors/weight"
# client.subscribe(weight_topic)

# MQTT 클라이언트 실행 (메시지 수신 대기)
client.loop_forever()
