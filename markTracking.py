#!/usr/bin/env python3

import time
import argparse
import sys

import numpy as np
import cv2

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

    while(True):
        ret, img = capture.read()

        # q を押すと終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--scan',
                        help="Scan capture devices", action="store_true")
    parser.add_argument('-c', '--capture-device',
                        type=int, default=DEFAULT_CAPTURE_DEVICE,
                        help="# of capture device"
                             " (default:{})".format(DEFAULT_CAPTURE_DEVICE))
    args = parser.parse_args(argv)

    if args.scan:
        cams = check_cameras()
        print("Available caputre devices:", cams)
    else:
        capture_display_cv(args)

if __name__ == "__main__":
    print("OpenCV version:", cv2.__version__)
    main(sys.argv[1:])
