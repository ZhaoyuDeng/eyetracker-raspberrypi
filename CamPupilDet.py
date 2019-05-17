# 视频流检测瞳孔坐标
# 邓昭宇 11月9日
import sys
import os
import cv2
import numpy
from tools import Tools
from pupildet import PupilDet
import pygame
import pygame.camera
from pygame.locals import *


def main():
    pygame.init()
    tools = Tools()
    pudet = PupilDet()
    # 获取摄像头
    cap = cv2.VideoCapture(0)
    if not cv2.VideoCapture.isOpened(cap):
        print('Device not found')
        pygame.quit()
        sys.exit(0)
    # 创建窗口,设置分辨率,窗口标题
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('VideoStream -- Isaac CP')

    while True:
        # 读取每帧视频
        grab_success = cap.grab()
        if grab_success:
            ret_success, frame = cap.retrieve()
            if not ret_success:
                continue
        else:
            print('Frame dropped')
            pygame.quit()
            cap.release()
            sys.exit(0)
        # 把图片矩阵格式从BGR转为BGRA格式&灰度图
        disp_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        detect_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 检测瞳孔的ROI坐标
        [pupil_x, pupil_y] = pudet.pupil_detect(detect_frame)
        # 非ROI的坐标补偿
        pupil_x += pudet.roi_x
        pupil_y += pudet.roi_y
        # 把图片矩阵放到surface缓存
        tools.put_array(screen, disp_frame)
        # 画出瞳孔标定十字
        pygame.draw.line(screen, (0, 0, 255), (pupil_x - pudet.cross_size // 2, pupil_y),
                         (pupil_x + pudet.cross_size // 2, pupil_y), 1)
        pygame.draw.line(screen, (0, 0, 255), (pupil_x, pupil_y - pudet.cross_size // 2),
                         (pupil_x, pupil_y + pudet.cross_size // 2), 1)
        # 将缓存图片加载在窗口上
        pygame.display.flip()
        pygame.display.update()
        # 检查退出程序事件
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                cap.release()
                sys.exit(0)


if __name__ == "__main__":
    main()

