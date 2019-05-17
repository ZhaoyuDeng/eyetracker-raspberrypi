import cv2
import socket
# 视频流发送
# 王鹏飞 11月27日
# 邓昭宇 12月4日


def send_video():
    cap = cv2.VideoCapture(0)
    host = '192.168.1.102'  # '192.168.191.1'
    port = 9999
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.connect((host, port))

    try:
        print('Sending')
        while True:
            ret, frame = cap.read()  # 读取视频帧
            if ret is False:
                continue
            ret, img_encode = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])  # 编码图像并通过UDP发送出去
            server.sendall(img_encode)
    except Exception as e:
        print("Error:" + e)


if __name__ == "__main__":
    send_video()
