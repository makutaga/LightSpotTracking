#!/usr/bin/env python3

import cv2

IMFILE = 'sea.png'

img = cv2.imread(IMFILE)

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.imshow(f'Original : {IMFILE}', img)
cv2.imshow(f'GRAY : {IMFILE}', img_gray)
cv2.waitKey(0)
cv2.destroyAllWindows()
