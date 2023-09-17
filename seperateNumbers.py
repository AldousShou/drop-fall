import numpy as np

def fillNumber(imgt, point):
    dirct = [-1, -1, -1, 0, -1, 1, 0, -1, 0, 1, 1, -1, 1, 0, 1, 1]
    h, w = len(imgt), len(imgt[0])
    q = [point]
    side = [point[0], point[0], point[1], point[1]]
    while q:
        t = q.pop()
        if imgt[t[0]][t[1]] == 0:
            continue
        imgt[t[0]][t[1]] = 0
        side[0] = min(side[0], t[0])
        side[1] = max(side[1], t[0])
        side[2] = min(side[2], t[1])
        side[3] = max(side[3], t[1])
        for i in range(0, 8, 2):
            x, y = t[0] + dirct[i], t[1] + dirct[i + 1]
            if imgt[x][y] != 0:
                q.append([x, y])
    if (side[1] - side[0]) * (side[3] - side[2]) < 1024:
        side = []
    if side:
        side = [side[0] - 1, side[1] + 1, side[2] - 1, side[3] + 1]
    return side

def separateNumbers(img):
    h, w, c = img.shape
    step = w // 150
    imgt = np.sum(img, axis=2)
    side = []
    for i in range(0, h, step):
        for j in range(0, w, step):
            if imgt[i][j] != 0:
                newside = fillNumber(imgt, [i, j])
                if newside:
                    side.append(newside)
    return side

def quickSeparateNumbers(img):
    h, w = len(img), len(img[0])
    step = w >> 8 if w > 256 else 1
    imgt = [[img[i][j] for j in range(0, w, step)] for i in range(0, h, step)]
    side = []
    newh, neww = h // step, w // step
    for i in range(newh):
        for j in range(neww):
            if imgt[i][j] != 0:
                newside = fillNumber(imgt, [i, j])
                if newside:
                    side.append([i * step for i in newside])
    imgList = []
    for each in side:
        imgList.append([[img[i][j] for j in range(each[2], each[3] + 1)] for i in range(each[0], each[1] + 1)])
    return imgList
