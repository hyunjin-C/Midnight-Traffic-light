# -*- coding: utf-8 -*-

import threading
import subprocess


def run_segment_count():
    subprocess.run(['python', 'pir_sensor_1.py'])


def run_sensor_test():
    subprocess.run(['python', 'sensor_test_2.py'])


# 스레드 생성 및 실행
segment_count_thread = threading.Thread(target=run_segment_count)
sensor_test_thread = threading.Thread(target=run_sensor_test)

segment_count_thread.start()
sensor_test_thread.start()

# 스레드 종료 대기
segment_count_thread.join()
sensor_test_thread.join()
