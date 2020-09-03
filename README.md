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
