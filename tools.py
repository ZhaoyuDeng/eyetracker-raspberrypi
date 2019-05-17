import cv2
import numpy
import socket


class Tools:
    def __init__(self):
        # 瞳孔位置线性映射到前置坐标参数
        self.x0 = 1437.719
        self.kx = -3.8632
        self.y0 = -841.1098
        self.ky = 6.2992
        # 手动测试调整偏移值
        self.offset_x = -50
        self.offset_y = 0

    # 瞳孔坐标映射到前置坐标 线性映射
    def coord_map(self, xc, yc):
        xm = self.kx * xc + self.x0 + self.offset_x
        ym = self.y0 + self.ky * yc + self.offset_y
        return [xm, ym]

    # 显示二值图像
    @staticmethod
    def show_bin_image(eye, bin_thresh):
        ret, thresh = cv2.threshold(eye, bin_thresh, 255, cv2.THRESH_BINARY)
        cv2.imshow('Camera', thresh)

    # 遍历获得矩阵长度最大值参数[坐标,起始坐标,长度]
    @staticmethod
    def get_max_index(array):
        (col, row) = array.shape
        if col == 0 or row == 0:
            return [0, 0, 0]
        length = 0
        index_max_length = 0
        for index in range(0, col):
            if array[index][2] > length:
                length = array[index][2]
                index_max_length = index
        loc = array[index_max_length][0]
        start = array[index_max_length][1]
        length = array[index_max_length][2]
        return [loc, start, length]

    # 把图片矩阵放到surface缓存
    @staticmethod
    def put_array(surface, array):
        bv = surface.get_view('0')
        bv.write(array.tostring())

    # 获取本地IP
    @staticmethod
    def get_host_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip
