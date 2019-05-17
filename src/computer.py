# -*- coding: UTF-8 -*-
import socket
import cv2
import struct
import numpy
import threading


class Camera_Connect_Object(object):
    def __init__(self):
        target=input("请输入目标树莓派ip地址")
        TargetIP = (target, 2333)
        self.TargetIP = TargetIP
        self.resolution = (640, 480)
        self.src = 888 + 15
        self.interval = 0
        self.img_fps = 15
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect(self.TargetIP)
        #self.Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.Server.bind(self.TargetIP)
        #self.Server.listen(5)

    def RT_Image(self):
        #self.client, self.addr = self.Server.accept()
        #self.name = self.addr[0] + " Camera"
        #print(self.name)
        while True:
            # time.sleep(0.3)  # sleep for 0.3 seconds
            tempdata = self.server.recv(8)
            if len(tempdata) == 0:
                print("+1")
                continue
            info = struct.unpack('lhh', tempdata)
            buf_size = int(info[0])

            if buf_size:
                try:
                    self.buf = b""
                    self.temp_buf = self.buf
                    while buf_size:
                        self.temp_buf = self.server.recv(buf_size)
                        buf_size -= len(self.temp_buf)
                        self.buf += self.temp_buf
                    data = numpy.fromstring(self.buf, dtype='uint8')

                    self.image = cv2.imdecode(data, 1)
                    #cv2.imshow(self.name, self.image)
                    cv2.imshow("Image", self.image)

                except Exception as e:
                    print(e.args)
                    pass
                finally:
                    if cv2.waitKey(10) == 27:
                        self.server.close()
                        cv2.destroyAllWindows()
                        break

    def Get_data(self):
        showThread = threading.Thread(target=self.RT_Image)
        showThread.start()
        showThread.join()


if __name__ == '__main__':
    camera = Camera_Connect_Object()
    camera.Get_data()