import sys
import pygame
import pygame.camera
from pygame.locals import *
import cv2
import numpy
#加载相应模块


# 把图片矩阵放到surface缓存
def put_array(surface, array):          
    bv = surface.get_view('0')
    bv.write(array.tostring())

def main():
    pygame.init()
    # 使用opencv自带的VideoCapture，0表示第一个摄像头
    cap = cv2.VideoCapture(0)
    screen = pygame.display.set_mode((640,480))
    pygame.display.set_caption('VideoStream -- Isaac CP')
    while True:
        #读取每帧视频
        success,frame = cap.read()
        # 把图片矩阵格式从BGR转为BGRA
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2BGRA)
        # 把图片矩阵放到surface缓存
        put_array(screen, frame)
        #将缓存图片加载在屏幕上
        pygame.display.update()
        # 检查事件
        for event in pygame.event.get():
            #退出程序
            if event.type == QUIT:
                pygame.quit()
                cap.release()
                sys.exit(0)
                                                                                                                                                        
#主函数
if __name__=="__main__":                                 
    main()
