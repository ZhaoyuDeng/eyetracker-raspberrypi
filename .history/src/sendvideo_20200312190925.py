import cv2
import socket
from multiprocessing import Process
# 视频流发送
# 王鹏飞 11月27日
# 邓昭宇 12月4日
# 端口：眼动 999； 前置1000


class SendVideo:
    def __init__(self):
        self.host = '192.168.1.102'
        self.port = {'eye_cam': 9999, 'front_cam': 10000}
        self.cam = {'eye_cam': 0, 'front_cam': 1}

    def send_video(self, name):
        # 建立UDP连接
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.connect((self.host, self.port[name]))
        # 获取摄像头
        cap = cv2.VideoCapture(self.cam[name])
        try:
            print('Sending: ' + name)
            while True:
                ret, frame = cap.read()  # 读取视频帧
                if ret is False:
                    continue
                ret, img_encode = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])  # 编码图像并通过UDP发送出去
                server.sendall(img_encode)
        except Exception as e:
            print("Error: " + str(e))


if __name__ == "__main__":
    sv = SendVideo()
    eye_proc = Process(target=sv.send_video, args=('eye_cam',))
    front_proc = Process(target=sv.send_video, args=('front_cam',))
    eye_proc.start()
    front_proc.start()
