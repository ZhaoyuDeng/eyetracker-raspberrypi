# 获取视频流检测瞳孔坐标
# 邓昭宇 11月29日
import sys
import os
import cv2
import numpy
from tools import Tools
from pupildet import PupilDet
import pygame
import pygame.camera
from pygame.locals import *
import socket
import time
from multiprocessing import Process


def main():
    pygame.init()
    tools = Tools()
    pupil_det = PupilDet()

    # 设置Socket参数 [接收端IP，端口，缓冲容量]
    host = tools.get_host_ip()
    port = 9999
    buff_size = 65535

    # 创建Socket监听连接
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print('Waiting')
    server.bind((host, port))

    # 创建窗口,设置分辨率,窗口标题
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('VideoStream -- Isaac CP')

    while True:
        # 帧率测试
        # since = time.time()
        # 获取每帧，并解码
        data, address = server.recvfrom(buff_size)
        # 不知准确作用，问鹏飞
        # if len(data) == 1 and data[0] == 1:
        #     server.close()
        #     pygame.quit()
        #     exit(0)
        # 图片解码
        data = bytearray(data)
        data = numpy.array(data)
        frame = cv2.imdecode(data, 1)  # 解码并窗口显示

        # 把图片矩阵格式从BGR转为BGRA格式&灰度图
        disp_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        detect_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 检测瞳孔的ROI坐标
        [pupil_x, pupil_y] = pupil_det.pupil_detect(detect_frame)
        # 非ROI的坐标补偿
        pupil_x += pupil_det.roi_x
        pupil_y += pupil_det.roi_y
        # 把图片矩阵放到surface缓存
        tools.put_array(screen, disp_frame)
        # 画出瞳孔标定十字
        pygame.draw.line(screen, (255, 0, 0), (pupil_x - pupil_det.cross_size // 2, pupil_y),
                         (pupil_x + pupil_det.cross_size // 2, pupil_y), 1)
        pygame.draw.line(screen, (255, 0, 0), (pupil_x, pupil_y - pupil_det.cross_size // 2),
                         (pupil_x, pupil_y + pupil_det.cross_size // 2), 1)
        # 将缓存图片加载在窗口上
        pygame.display.flip()
        pygame.display.update()
        # 检查退出程序事件
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                server.close()
                sys.exit(0)

        # 帧率测试
        # elapse = time.time() - since
        # print(1/elapse)


if __name__ == "__main__":
    main()

