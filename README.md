# SpotTracking

## cvcam.py

カメラなどの動画キャプチャデバイスからOpenCV経由で画像を取り込み，
リアルタイムで最も明るい点を探して表示するプログラム．

- Python 3.8.5
- opencv-python 4.4.0.42

で動作確認済み．OSは

- macOS Catalina (10.15.6)
- Windows 10

で動作確認済み．恐らく Ubuntu Linux でも動作可能．

素の Python では opencv-python はインストールされていないので，手動でインストールする必要がある．
pip を使う場合であれば，python （python3）が実行できるターミナルで

```
pip install opencv-python
```
を実行する．環境によっては ```pip``` の代わりに ```pip3``` を使わなければならないかもしれない．

### 使い方

コマンドラインツールなので python3 が実行できる端末で，```cvcam.py``` を実行する．
キャプチャに用いるデバイスの番号を指定しなければならない場合が多い．
以下はヘルプメッセージ

```
python3 cvcam.py -h
OpenCV version: 4.4.0
usage: cvcam.py [-h] [-s] [-r RESIZE_FACTOR] [-c CAPTURE_DEVICE] [-k KERNEL_SIZE] [-g] [--dry]

optional arguments:
  -h, --help            show this help message and exit
  -s, --scan            Scan capture devices
  -r RESIZE_FACTOR, --resize-factor RESIZE_FACTOR
                        Resize factor (default: 1)
  -c CAPTURE_DEVICE, --capture-device CAPTURE_DEVICE
                        # of capture device (default:0)
  -k KERNEL_SIZE, --kernel-size KERNEL_SIZE
                        blurring kernel size for cv2.blur() (default:10)
  -g, --show-gray       Show internal gray image
  --dry                 Dry run
```

各オプションの使用方法は以下の通り．

#### -s

キャプチャデバイスをスキャンする．
カメラなどのキャプチャデバイス接続後にこのオプションでデバイス番号を調べておく．
カメラの情報などを表示後にすぐに終了する．

#### -r RESIZE_FACTOR

```RESIZE_FACTOR``` にはキャプチャした画像のリサイズ倍率を指定する．例えば 0.5 で画像サイズは半分になる．

#### -c CAPTURE_DEVICE

キャプチャデバイスの番号を指定する．

#### -k KERNEL_SIZE

ぼかしフィルタのサイズを指定する．

#### -g

カラー元画像ではなく，画像処理に用いている白黒画像を表示する．

#### -dry

何もしない．キャプチャおよび画像表示をせずにすぐ終了．
