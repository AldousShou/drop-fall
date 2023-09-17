import cv2
import numpy as np
import separateNumbers as sn

def openImg(name="res/img4.jpg"):
    orgimg = cv2.imread(name)
    assert orgimg is not None
    img = np.sum(orgimg, axis=2) < 50
    return img.astype(int)

def dfa(img):
    h, w = img.shape
    startw = int(w * 0.2)
    p = [h - 1, startw]
    l, r = startw, startw
    while p[0] != 0:
        img[p[0], p[1]] = 2
        p[0] -= 1
        value = img[p[0] - 1, p[1] - 1] * 10000 + img[p[0] - 1, p[1]] * 1000 + img[p[0] - 1, p[1] + 1] * 100 + \
                img[p[0], p[1] - 1] * 10 + img[p[0], p[1] + 1]
        if value == 11101:
            p[1] -= 2
        elif value == 1101:
            p[1] -= 1
        elif value == 11010:
            p[1] += 1
        elif value == 11110:
            p[1] += 2
        elif img[p[0], p[1] - 1] == 1 and img[p[0], p[1] + 1] == 1:
            p[1] -= 1
        if p[1] < l:
            l = p[1]
        elif p[1] > r:
            r = p[1]
    num1 = img[:, :r+1]
    num2 = img[:, l-1:]
    numList = [num1, num2]
    for i in range(2):
        t = numList[i]
        numShape = t.shape
        t = np.where(t == 0, 0, 255)
        padding1 = numShape[0] - numShape[1]
        padding2 = padding1 // 2
        padding1 -= padding2
        t = np.pad(t, ((0, 0), (padding1, padding2)), mode='constant', constant_values=0)
        t = t.astype(np.uint8)
        numList[i] = t
    num1 = cv2.resize(numList[0], (28, 28), interpolation=cv2.INTER_AREA)
    num2 = cv2.resize(numList[1], (28, 28), interpolation=cv2.INTER_AREA)
    thresholding(num1)
    thresholding(num2)
    return [num1, num2]

def thresholding(img):
    img[img >= 20] = 255
    img[img < 20] = 0

if __name__ == '__main__':
    img = openImg()
    numList = sn.quickSeparateNumbers(img)
    numList = dfa(numList[0])
    cv2.imwrite("result/num1.jpg", numList[0])
    cv2.imwrite("result/num2.jpg", numList[1])
    print("DONE")
