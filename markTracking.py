#!/usr/bin/env python3

import time
import argparse
import sys

import numpy as np
import cv2

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

import cvcam

DEFAULT_CAPTURE_DEVICE = 0
DEFAULT_KERNEL_SIZE = 10


def capture_display_cv(args):
    '''カメラ画像をキャプチャして画像処理し，画面に表示

    Parameters
    ----------
    camera_num : int
        カメラの番号
    '''
    capture = cv2.VideoCapture(args.capture_device)  # キャプチャデバイスの指定

    try:
        while True:
            ret, img = capture.read()

            print(img.shape)
            # q を押すと終了
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        pass

    capture.release()
    cv2.destroyAllWindows()


class myImage():
    def __init__(self, args):
        self.capture_device_id = args.capture_device
        self.capture = cv2.VideoCapture(self.capture_device_id)
        self.cap_width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.cap_height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.cap_fps = int(self.capture.get(cv2.CAP_PROP_FPS))
        self.image_size = (int(self.cap_width * args.resize_factor),
                           int(self.cap_height * args.resize_factor))

    def getImage(self):
        ret, img = self.capture.read()
        img = cv2.resize(img, self.image_size)
        print(img.shape)
        return img

    def __del__(self):
        self.capture.release()
        # cv2.destroyAllWindows()


class MyWidget(QtGui.QMainWindow):
    def __init__(self, args, parent=None):
        super().__init__(parent)
        self.initUI()
        self.cam = myImage(args)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)

    def initUI(self):
        self.win = pg.GraphicsLayoutWidget()
        self.setCentralWidget(self.win)
        self.view = self.win.addViewBox()

        self.view.setAspectLocked(True)
        self.image_item = pg.ImageItem()
        self.view.addItem(self.image_item)

        self.view2 = self.win.addViewBox()
        self.view2.setAspectLocked(True)
        self.image_item2 = pg.ImageItem()
        self.view2.addItem(self.image_item2)

        self.show()

    def update(self):
        img = self.cam.getImage()
        # self.image_item.setImage(img)
        cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
        self.image_item.setOpts(axisOrder='row-major')
        self.image_item.setImage(np.flipud(img))

        imgYUV = cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
        imgY = imgYUV[:, :, 0]

        # edge = cv2.Laplacian(imgY, cv2.CV_64F)
        edge = cv2.Canny(imgY, 100, 200)

        self.image_item2.setOpts(axisOrder='row-major')
        self.image_item2.setImage(np.flipud(edge))


def main(argv):

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--scan',
                        help="Scan capture devices", action="store_true")
    parser.add_argument('-r', '--resize-factor',
                        type=float, default=1.0,
                        help="Resize factor (default: 1)")
    parser.add_argument('-c', '--capture-device',
                        type=int, default=DEFAULT_CAPTURE_DEVICE,
                        help="# of capture device"
                             " (default:{})".format(DEFAULT_CAPTURE_DEVICE))
    args = parser.parse_args(argv)

    if args.scan:
        cams = cvcam.check_cameras()
        print("Available caputre devices:", cams)
    else:
        app = QtGui.QApplication(argv)
        win = MyWidget(args)

        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PY_QTVERSION'):
            # QtGui.QApplication.instance().exec_()
            app.exec_()
            # capture_display_cv(args)


if __name__ == "__main__":
    print("OpenCV version:", cv2.__version__)
    main(sys.argv[1:])
