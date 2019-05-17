# 检测瞳孔坐标
# 邓昭宇 10月27日(Matlab) 11月7日(Python)
import sys
import os
import cv2
import numpy
from tools import Tools


def main():
    tools = Tools()
    # 图片分辨率: 宽480 x 长640
    res = [480, 640]
    # 人工调节瞳孔可能出现范围 [x,y,w,h]
    roi_x = 100
    roi_y = 120
    roi_w = 350
    roi_h = 240
    # 比较的最长线段最小阈值
    max_len_thresh = 10
    # 灰度图转二值图阈值
    bin_thresh = 30
    # 选择图片
    # im_order = 9
    for im_order in range(1, 12):
        # print(os.getcwd())
        # 读取图片BGR矩阵
        eye_bgr = cv2.imread('./PupilSample/' + str(im_order) + '.jpg', )
        # 由于眼部摄像头已经设为灰度图，因此直接抽取一层
        eye = eye_bgr[:, :, 0]
        # 截取roi矩阵（瞳孔可能出现范围）
        eye_roi_gray = eye[roi_y:roi_y + roi_h, roi_x: roi_x + roi_w]
        # 仅用于测试显示的图片
        eye_show = eye_bgr[roi_y:roi_y + roi_h, roi_x: roi_x + roi_w]
        # 设置阈值获得突出瞳孔的二值图
        eye_roi = eye_roi_gray < bin_thresh
        # 显示二值图(方法缺陷，无法使用eyeBin)
        # tools.show_bin_image(eye_roi_gray, bin_thresh)

        # 扫描横向最长连续线段位置与长度
        # 初始化[y坐标, x起始坐标, 长度]
        stat_h = numpy.zeros((roi_h, 3), dtype=int)
        for h in range(0, roi_h):
            # 前一项为0标志位
            is_fore0 = True
            # 用作选择最大值的比较临时变量
            tmp_max_len = max_len_thresh
            start_x = 0
            for w in range(0, roi_w):
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
        [index_h, start_w, len_h] = tools.get_max_index(stat_h)

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
            tmp_max_len = max_len_thresh
            start_y = 0
            for h in range(0, roi_h):
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
        [index_w, start_h, len_w] = tools.get_max_index(stat_w)
        index_w = index_w+scan_start_x

        # 显示参考最长线段位置
        cv2.line(eye_show, (start_w, index_h), (start_w+len_h, index_h), (255, 0, 0), 1)
        cv2.line(eye_show, (index_w, start_h), (index_w, start_h+len_w), (255, 0, 0), 1)
        # 标志出检测所得瞳孔位置
        # 十字光标大小
        cross_x = start_w+len_h//2
        cross_y = start_h+len_w//2
        cross_size = 40
        cv2.line(eye_show, (cross_x-cross_size//2, cross_y), (cross_x+cross_size//2, cross_y), (0, 0, 255), 2)
        cv2.line(eye_show, (cross_x, cross_y-cross_size//2), (cross_x, cross_y+cross_size//2), (0, 0, 255), 2)
        tools.show_bin_image(eye_show, bin_thresh)

        # 等待按键下一步
        while True:
            # 检测n键是否被按下
            if cv2.waitKey(1) & 0xFF == ord('n'):
                break

    # 等待按键退出程序
    while True:
        # 检测q键是否被按下
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # 关闭窗口
            cv2.destroyAllWindows()
            sys.exit()


if __name__ == "__main__":
    main()

