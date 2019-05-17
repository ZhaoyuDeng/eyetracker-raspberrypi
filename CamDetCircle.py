import sys
import pygame
import pygame.camera
from pygame.locals import *
import cv2
import numpy


# 加载相应模块


# 把图片矩阵放到surface缓存
def put_array(surface, array):
    bv = surface.get_view('0')
    bv.write(array.tostring())


def main():
    pygame.init()
    # 使用opencv自带的VideoCapture，0表示第一个摄像头
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
            print('Frame droped')
            continue
        # 把图片矩阵格式从BGR转为BGRA格式&灰度图
        disp_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        detect_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 中值滤波,很消耗资源
        # detect_frame = cv2.medianBlur(detect_frame, 5)
        # 把图片矩阵放到surface缓存
        put_array(screen, disp_frame)
        try:
            # 圆检测
            [circles] = cv2.HoughCircles(detect_frame, cv2.HOUGH_GRADIENT, 3, 50, param1=100, param2=100, minRadius=10,
                                         maxRadius=100)
            circles = numpy.uint16(numpy.around(circles))
            # 把检测到的圆显示出来
            print(circles, end='\n\n')
            for circle in circles[0:1]:
                pygame.draw.circle(screen, [255, 0, 0], [circle[0], circle[1]], circle[2], 2)
        except Exception as e:
            # 报告错误
            print(e)
        finally:
            # 将缓存图片加载在屏幕上
            pygame.display.update()
            # 检查事件
            for event in pygame.event.get():
                # 退出程序
                if event.type == QUIT:
                    pygame.quit()
                    cap.release()
                    sys.exit(0)


# # 主函数
# if __name__ == "__main__":
main()
