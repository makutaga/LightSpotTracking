#!/usr/bin/env python3

'''
カメラなどの動画キャプチャデバイスから画像を取り込み，
リアルタイムで画像処理をするサンプル

「Pythonでカメラを制御する【研究用】- Qiita」
https://qiita.com/opto-line/items/7ade854c26a50a485159

を元にコード追加
'''

import time
import argparse
import sys

import numpy as np
import cv2

DEFAULT_CAPTURE_DEVICE = 0
DEFAULT_KERNEL_SIZE = 10


def check_cameras():
    ''' 接続されたカメラのチェック

    OpenCV はカメラデバイスを番号で指定するが，
    何番が接続されているのかを調べる関数が用意されていない．
    0番から9番まで順に cv2.read() で確かめている

    Return Value
    ------------
    available_cameras: list
        使用可能なカメラ番号のリスト
    '''
    available_cameras = []

    for cnum in range(0, 10):
        print(f"Check camera {cnum} -----")
        cap = cv2.VideoCapture(cnum)
        ret, frame = cap.read()
        if ret is True:
            print("OK")
            available_cameras.append(cnum)
            frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            frame_fps = cap.get(cv2.CAP_PROP_FPS)
            print(f"frame size: {frame_width} x {frame_height}")
            print(f"frame per second: {frame_fps}")

        else:
            print("Nop")
    return available_cameras


def capture_display_cv(args):
    '''カメラ画像をキャプチャして画像処理し，画面に表示

    Parameters
    ----------
    camera_num : int
        カメラの番号
    '''
    font = cv2.FONT_HERSHEY_SIMPLEX  # 情報表示用のフォント
    capture = cv2.VideoCapture(args.capture_device)  # キャプチャデバイスの指定

    # デバイスのフレームサイズを取得
    # その他 cv2.CAP_PROP_FPS など多数のpropertyがある．
    # OpenCVのマニュアル参照
    cap_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    cap_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap_fps = int(capture.get(cv2.CAP_PROP_FPS))
    image_size = (int(cap_width * args.resize_factor),
                  int(cap_height * args.resize_factor))
    print(f"frame width:{cap_width} height:{cap_height} fps:{cap_fps}")
    tick_pre = time.time()
    while(True):
        # 画像取得
        ret, img = capture.read()

        # resize the window 今は未使用
        img = cv2.resize(img, image_size)

        # 白黒画像の生成
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # ぼかし画像の生成
        img_blur = cv2.blur(img_gray, (args.kernel_size, args.kernel_size))

        # 処理する画像の指定
        img_process = img_blur

        # 表示用の画像の指定
        if args.show_gray is True:
            img_draw = img_process
        else:
            img_draw = img

        # print(img_gray.shape)

        # 各x/y 位置毎の最大値
        sum_on_x = np.max(img_process, axis=0)
        sum_on_y = np.max(img_process, axis=1)

        # x/y の最大値の最大値
        max_on_x = np.max(sum_on_x)
        max_on_y = np.max(sum_on_y)

        # x/y の最大値のインデックス
        # max_x_idx = np.argmax(sum_on_x)
        # max_y_idx = np.argmax(sum_on_y)
        idx_max = img_process.argmax()
        max_xy_idx = (idx_max % image_size[0], int(idx_max / image_size[0]))

        # グラフ表示用の座標の計算
        pts_sum_x = np.zeros((sum_on_x.shape[0], 2), dtype=int)
        pts_sum_x[:, 0] = np.arange(sum_on_x.shape[0])
        pts_sum_x[:, 1] = sum_on_y.shape[0] - sum_on_x / max_on_x * 100

        pts_sum_y = np.zeros((sum_on_y.shape[0], 2), dtype=int)
        pts_sum_y[:, 0] = sum_on_y / max_on_y * 100
        pts_sum_y[:, 1] = np.arange(sum_on_y.shape[0])

        # cv2.circle(img_draw, (max_x_idx, max_y_idx), 10, (255, 255, 0))
        cv2.circle(img_draw, (max_xy_idx[0], max_xy_idx[1]), 10, (0, 128, 0))
        cv2.polylines(img_draw, [pts_sum_x], False, (255, 0, 0))
        cv2.polylines(img_draw, [pts_sum_y], False, (0, 0, 255))

        # fpsの計算
        tick = time.time()
        fps = 1.0 / (tick - tick_pre)
        tick_pre = tick
        info = f"x:{max_xy_idx[0]:4d} y:{max_xy_idx[1]:4d}  {fps:.2f} fps"
        cv2.putText(img_draw, info, (11, 21), font, 0.5, (0, 0, 0))
        cv2.putText(img_draw, info, (10, 20), font, 0.5, (0, 255, 255))

        cv2.imshow('Image', img_draw)

        # q を押すと終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()


def main(argv):
    '''main'''
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
    parser.add_argument('-k', '--kernel-size',
                        type=int, default=DEFAULT_KERNEL_SIZE,
                        help="blurring kernel size for cv2.blur()"
                             " (default:{})".format(DEFAULT_KERNEL_SIZE))
    parser.add_argument('-g', '--show-gray',
                        help="Show internal gray image", action="store_true")
    parser.add_argument('--dry',
                        help='Dry run', action="store_true")
    args = parser.parse_args(argv)
    if args.scan:
        cams = check_cameras()
        print("Available caputre devices:", cams)
    else:
        print(f"capture device:{args.capture_device}")
        if args.dry is not True:
            capture_display_cv(args)


if __name__ == "__main__":
    print("OpenCV version:", cv2.__version__)
    main(sys.argv[1:])
