import sys
import cv2
import numpy
from tools import Tools
from pupildet import PupilDet
import pygame
import pygame.camera
from pygame.locals import *
import socket
import time
from multiprocessing import Process, Pipe
# 邓昭宇 12月5日
# 通过局域网，获取眼部摄像头图像并检测瞳孔，获取前置摄像头图像并映射坐标


class RecvPupilDetMap:
    def __init__(self):
        pygame.init()
        self.tools = Tools()
        self.port_eye_cam = 9999
        self.port_front_cam = 10000
        self.buff_size = 65535
        # 设置Socket参数 [接收端IP，端口，缓冲容量]
        self.host = self.tools.get_host_ip()
        # 瞳孔检测坐标
        # pupil_det_x = 0
        # pupil_det_y = 0
        # 映射坐标圆半径
        self.radius = 20

    # 获取眼部摄像头图像并检测瞳孔
    def recv_pupil_det(self, eye_pipe):
        # 初始化瞳孔检测
        pupil_det = PupilDet()

        # 创建Socket监听连接
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind((self.host, self.port_eye_cam))
        print('Pupil Detect Processing')

        # 创建窗口,设置分辨率,窗口标题
        eye_screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption('EyeCamDet -- Isaac CP')

        while True:
            # 帧率测试
            # since = time.time()
            # 获取每帧，并解码
            data, address = server.recvfrom(self.buff_size)

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
            pupil_det_x = pupil_x + pupil_det.roi_x
            pupil_det_y = pupil_y + pupil_det.roi_y
            # 输出瞳孔坐标 ——测试校正用
            print([pupil_det_x, pupil_det_y])
            # 通过Pipe进程通信
            eye_pipe.send([pupil_det_x, pupil_det_y])
            # 把图片矩阵放到surface缓存
            self.tools.put_array(eye_screen, disp_frame)
            # 画出瞳孔标定十字
            pygame.draw.line(eye_screen, (255, 0, 0), (pupil_det_x - pupil_det.cross_size // 2, pupil_det_y),
                             (pupil_det_x + pupil_det.cross_size // 2, pupil_det_y), 1)
            pygame.draw.line(eye_screen, (255, 0, 0), (pupil_det_x, pupil_det_y - pupil_det.cross_size // 2),
                             (pupil_det_x, pupil_det_y + pupil_det.cross_size // 2), 1)
            # 将缓存图片加载在窗口上
            pygame.display.flip()
            pygame.display.update()
            # 检查退出程序事件
            for event in pygame.event.get():
                if event.type == QUIT:
                    eye_pipe.close()
                    pygame.quit()
                    server.close()
                    sys.exit(0)

            # 帧率测试
            # elapse = time.time() - since
            # print(1/elapse)

    # 获取前置摄像头图像并映射坐标
    def recv_front_map(self, front_pipe):
        # 创建Socket监听连接
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind((self.host, self.port_front_cam))
        print('Front Map Processing')

        # 创建窗口,设置分辨率,窗口标题
        front_screen = pygame.display.set_mode((640, 480))
        pygame.display.set_caption('FrontCam -- Isaac CP')

        while True:
            # 帧率测试
            # since = time.time()
            # 获取每帧，并解码
            data, address = server.recvfrom(self.buff_size)

            # 图片解码
            data = bytearray(data)
            data = numpy.array(data)
            frame = cv2.imdecode(data, 1)  # 解码并窗口显示

            # 把图片矩阵格式从BGR转为BGRA格式
            disp_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

            # 把图片矩阵放到surface缓存
            self.tools.put_array(front_screen, disp_frame)
            # 获取眼球标定坐标
            [pupil_det_x, pupil_det_y] = front_pipe.recv()
            # 瞳孔坐标映射到前置坐标
            [pupil_map_x, pupil_map_y] = self.tools.coord_map(pupil_det_x, pupil_det_y)

            # 画出映射标定圆
            pygame.draw.circle(front_screen, [255, 0, 0], [int(pupil_map_x), int(pupil_map_y)], self.radius, 2)

            # 将缓存图片加载在窗口上
            pygame.display.flip()
            pygame.display.update()
            # 检查退出程序事件
            for event in pygame.event.get():
                if event.type == QUIT:
                    front_pipe.close()
                    pygame.quit()
                    server.close()
                    sys.exit(0)

            # 帧率测试
            # elapse = time.time() - since
            # print(1/elapse)


if __name__ == "__main__":
    (eye_pipe, front_pipe) = Pipe()
    rpdm = RecvPupilDetMap()

    eye_recv_proc = Process(target=rpdm.recv_pupil_det, args=(eye_pipe,))
    front_recv_proc = Process(target=rpdm.recv_front_map, args=(front_pipe,))
    eye_recv_proc.start()
    front_recv_proc.start()
