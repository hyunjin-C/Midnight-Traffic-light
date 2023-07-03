# -*- coding: utf-8 -*-

import time
import picamera
import picamera.array
import cv2

# 카메라 초기화
camera = picamera.PiCamera()

# 비디오 해상도 설정
camera.resolution = (640, 480)

# 녹화 시간(초)
record_time = 16

# 녹화 시작 시간
start_time = time.time()

# 프레임 속도 설정
camera.framerate = 30  # 30fps로 설정 (원하는 값으로 조정)

# 비디오 녹화 시작
camera.start_recording('output.h264')

# OpenCV 창 생성
cv2.namedWindow('Live Video')

# 실시간 비디오 녹화 및 사용자에게 보여주기
while True:
    # 프레임 읽기
    with picamera.array.PiRGBArray(camera) as stream:
        camera.capture(stream, 'bgr')
        frame = stream.array

    # 화면에 출력
    cv2.imshow('Live Video', frame)

    # 키 입력 처리
    key = cv2.waitKey(1)
    if (time.time() - start_time) > record_time:  # 녹화 시간이 지나면 종료
        break

# 비디오 녹화 중지
camera.stop_recording()

# 사용자가 보던 창 닫기
cv2.destroyAllWindows()
