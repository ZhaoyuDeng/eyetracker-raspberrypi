import pygame
import pygame.camera
from pygame.locals import *
#加载相应模块


def main():
            
    pygame.init()
    pygame.camera.init()
    # 创建一个640*480的屏幕
    screen=pygame.display.set_mode((640,480),0,32)
    # 调用USB摄像头
    camera = pygame.camera.Camera('/dev/video0',(640,480))
    #开启摄像头
    camera.start()                                       
    while True:
        #缓存图片
        image = camera.get_image()
        #将缓存图片加载在屏幕上
        screen.blit(image,(0,0))
        #屏幕刷新，覆盖上一张图片
        pygame.display.update()                         
        for event in pygame.event.get():
            #退出程序
            if event.type == QUIT:
                camera.stop()
                pygame.quit()
                sys.exit()
                                                                                                                                                        
#主函数
if __name__=="__main__":                                 
    main()

