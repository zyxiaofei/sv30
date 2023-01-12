import datetime

import cv2


class camera:
    instance = None

    # def __new__(cls, *args, **kwargs):
    #     # 1.判断类属性是否为空对象，若为空说明第一个对象还没被创建
    #     if cls.instance is None:
    #         # 2.对第一个对象没有被创建，我们应该调用父类的方法，为第一个对象分配空间
    #         cls.instance = super().__new__(cls)
    #     # 3.把类属性中保存的对象引用返回给python的解释器
    #     return cls.instance

    def __init__(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        print('cap实例化', datetime.datetime.now())

    def get_size(self):
        size = (int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        return size

    def read(self):
        success, frame = self.cap.read()
        return success, frame

    def release(self):
        self.cap.release()
