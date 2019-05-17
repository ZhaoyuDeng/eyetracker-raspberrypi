# 检测瞳孔坐标方法
# 邓昭宇 11月9日
import sys
import os
import cv2
import numpy
from tools import Tools


class PupilDet:
    def __init__(self):
        self.tools = Tools()
        # 图片分辨率: 宽480 x 长640
        self.res = [480, 640]
        # 人工调节瞳孔可能出现范围 [x,y,w,h]
        self.roi_x = 100
        self.roi_y = 120
        self.roi_w = 350
        self.roi_h = 240
        # 比较的最长线段最小阈值
        self.max_len_thresh = 10
        # 灰度图转二值图阈值
        self.bin_thresh = 30
        # 十字光标大小
        self.cross_size = 40

    def pupil_detect(self, eye_bgr):
        # 选择图片
        # for im_order in range(1, 12):
            # print(os.getcwd())
            # 读取图片BGR矩阵
            # eye_bgr = cv2.imread('./PupilSample/' + str(im_order) + '.jpg', )
        # 由于眼部摄像头已经设为灰度图，因此直接抽取一层
        eye = eye_bgr  # [:, :, 0]
        # 截取roi矩阵（瞳孔可能出现范围）
        eye_roi_gray = eye[self.roi_y:self.roi_y + self.roi_h, self.roi_x: self.roi_x + self.roi_w]
        # 仅用于测试显示的图片
        # eye_show = eye_bgr[self.roi_y:self.roi_y + self.roi_h, self.roi_x: self.roi_x + self.roi_w]
        # 设置阈值获得突出瞳孔的二值图
        eye_roi = eye_roi_gray < self.bin_thresh
        # 显示二值图(方法缺陷，无法使用eyeBin)
        # tools.show_bin_image(eye_roi_gray, bin_thresh)

        # 初始化[y坐标, x起始坐标, 长度]
        stat_h = numpy.zeros((self.roi_h, 3), dtype=int)
        # 扫描横向最长连续线段位置与长度
        for h in range(0, self.roi_h):
            # 前一项为0标志位
            is_fore0 = True
            # 用作选择最大值的比较临时变量
            tmp_max_len = self.max_len_thresh
            start_x = 0
            for w in range(0, self.roi_w):
                if eye_roi[h][w] and is_fore0:
                    start_x = w
                    is_fore0 = False
                elif not eye_roi[h][w] and not is_fore0:
                    is_fore0 = True
                    length = w - start_x
                    if length > tmp_max_len:
                        # 比较最终获得此行最长线段
                        stat_h[h][:] = [h, start_x, length]

        # 获得矩阵长度最大值参数[坐标,起始坐标,长度]
        [index_h, start_w, len_h] = self.tools.get_max_index(stat_h)

        # 扫描纵向最长连续线段位置与长度
        #
        scan_start_x = start_w
        max_len_h = len_h
        # 初始化[x坐标, y起始坐标, 长度]
        stat_w = numpy.zeros((max_len_h, 3), dtype=int)
        for w in range(0, max_len_h):
            # 前一项为0标志位
            is_fore0 = True
            # 用作选择最大值的比较临时变量
            tmp_max_len = self.max_len_thresh
            start_y = 0
            for h in range(0, self.roi_h):
                if eye_roi[h][w + scan_start_x] and is_fore0:
                    start_y = h
                    is_fore0 = False
                elif not eye_roi[h][w + scan_start_x] and not is_fore0:
                    is_fore0 = True
                    length = h - start_y
                    if length > tmp_max_len:
                        # 比较最终获得此行最长线段
                        stat_w[w][:] = [w, start_y, length]

        # 获得矩阵长度最大值参数[坐标,起始坐标,长度]
        [index_w, start_h, len_w] = self.tools.get_max_index(stat_w)
        # index_w = index_w+scan_start_x

        # 显示参考最长线段位置
        # cv2.line(eye_show, (start_w, index_h), (start_w+len_h, index_h), (255, 0, 0), 1)
        # cv2.line(eye_show, (index_w, start_h), (index_w, start_h+len_w), (255, 0, 0), 1)

        # 标志出检测所得瞳孔位置
        cross_x = start_w + len_h // 2
        cross_y = start_h + len_w // 2
        # 十字光标大小
        # cross_size = 40
        # cv2.line(eye_show, (cross_x - cross_size // 2, cross_y), (cross_x + cross_size // 2, cross_y), (0, 0, 255), 2)
        # cv2.line(eye_show, (cross_x, cross_y - cross_size // 2), (cross_x, cross_y + cross_size // 2), (0, 0, 255), 2)
        # tools.show_bin_image(eye_show, bin_thresh)
        if cross_x == 0 and cross_y == 0:
            [cross_x, cross_y] = [-self.roi_x, -self.roi_y]
        return [cross_x, cross_y]


