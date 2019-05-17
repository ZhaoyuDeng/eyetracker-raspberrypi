# -*- coding: UTF-8 -*-
import socket
import struct
import time
import cv2
import numpy
import array
import fcntl  #此包为linux环境下特有，Windows环境下安装需要走一些歪门邪道

#linux环境下获取本机的局域网IP地址
def get_ip_address():
    #先获取所有网络接口
    SIOCGIFCONF = 0x8912
    SIOCGIFADDR = 0x8915
    BYTES = 4096
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    names = array.array('B',b'\0' * BYTES)
    bytelen = struct.unpack('iL', fcntl.ioctl(sck.fileno(), SIOCGIFCONF, struct.pack('iL', BYTES, names.buffer_info()[0])))[0]
    namestr = names.tostring()
    ifaces = [namestr[i:i+32].split('\0', 1)[0] for i in range(0, bytelen, 32)]

    #再获取每个接口的IP地址
    iplist = []
    for ifname in ifaces:
        ip = socket.inet_ntoa(fcntl.ioctl(sck.fileno(),SIOCGIFADDR,struct.pack('256s',ifname[:15]))[20:24])
        iplist.append(ifname+':'+ip)
    return iplist

class Config(object):
    def __init__(self):
        #调用函数获得本机局域网ip地址
        host = str(get_ip_address()[-1]).split(':')[-1]
        print("树莓派局域网ip地址为："+host)
        #本机ip地址以及传输端口
        self.TargetIP = (host, 2333)
        #设置传输图像分辨率
        self.resolution = (640, 480)  # 分辨率
        self.img_fps = 15  # each second send pictures
        #创建socket
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #socket绑定本地ip地址以及端口
        self.server.bind(self.TargetIP)
        #设置最大连接数目为5
        self.server.listen(5)
        #等待IP进行连接
        self.client, self.addr = self.server.accept()
        self.img = ''
        self.img_data = ''

    def RT_Image(self):
        #调用摄像头
        camera = cv2.VideoCapture(0)
        #cv2.IMWRITE_JPEG_QUALITY表示的是图像的质量,设置低质量，可以降低传输的压力，但图片质量会下降
        img_param = [int(cv2.IMWRITE_JPEG_QUALITY), self.img_fps]

        while True:
            time.sleep(0.1)  # sleep for 0.1 seconds

            #读取摄像头内容
            _, self.img = camera.read()

            #利用先前设置的分辨率对摄像头读取的图片内容进行缩放
            self.img = cv2.resize(self.img, self.resolution)

            #将图片内容进行编码为流数据
            _, img_encode = cv2.imencode('.jpg', self.img, img_param)

            #对流数据建立矩阵
            img_code = numpy.array(img_encode)

            self.img_data = img_code.tostring()  # bytes data
            try:
                #pack(fmt, v1, v2, ...)     按照给定的格式(fmt)，把数据封装成字符串(实际上是类似于c结构体的字节流)

                packet = struct.pack(b'lhh', len(self.img_data), self.resolution[0],
                                     self.resolution[1])
                #发送数据
                self.client.send(packet)
                self.client.send(self.img_data)

            except Exception as e:
                print(e.args)
                camera.release()
                return


if __name__ == '__main__':
    config = Config()
    config.RT_Image()
