#encoding: UTF-8
from PIL import Image
from random import randint

def pixelNumberToCoordinate(n, img):
    return (n%img.size[0], n//img.size[0])

def coordinateToPixelNumber(x, y, img):
    return y*img.size[0]+x

def setLSB(v, state):
    if state == "0":
        return v & 0b11111110
    elif state == "1":
        return v | 0b00000001
    else:
        print "invalide state: %s" % (state)
        return v

def write(data, pixel, nextP, img):
    """
    Write data in binary form.
    NextP is the pixel number.
    """
    pix = img.load()
    x, y = pixelNumberToCoordinate(nextP, img)
    l = len(data)
    # binari representation of next pixel x
    col = bin(x)[2:].zfill(l)
    # binari representation of next pixel y
    lin = bin(y)[2:].zfill(l)
    # binari representation of alpha value
    alpha = "x".zfill(l).replace("0","1").replace("x","0")

    for i in range(pixel, pixel+l):
        p = pix[pixelNumberToCoordinate(i, img)]
        if len(p) == 4:
            # With alpha channel
            pix[pixelNumberToCoordinate(i, img)] = (
            setLSB(p[0], data[i-pixel]),
            setLSB(p[1], col[i-pixel]),
            setLSB(p[2], lin[i-pixel]),
            p[3])
        else:
            # no alpha channel
            pix[pixelNumberToCoordinate(i, img)] = (
            setLSB(p[0], data[i-pixel]),
            setLSB(p[1], col[i-pixel]),
            setLSB(p[2], lin[i-pixel]))

def toBin(string):
    return ''.join(format(ord(x), 'b').zfill(8) for x in string)

def binToString(i):
    # only works with long binari strings and 8-bit ascii blocks
    if len(i) > 0:
        rest = len(i) % 8
        if rest != 0:
            i = i + "0"*(8-rest)
        n = int(i, 2)
        n = hex(n)[2:][:-1]
        if len(n) % 2 != 0:
            n = "0"+n
        return n.decode("hex")
    return ""

def chunkstring(string, length):
    return [string[0+i:length+i].ljust(length, "0") for i in range(0, len(string), length)]

def haveCommon(a, b):
    """
    Returns if 2 ranges have elements in commun.
    """
    return not (max(a) < min(b) or max(b) < min(a))

def canWrite(nextP, img, occupied, l):
    total = img.size[0]*img.size[1]
    if nextP + l > total:
        return False
    i = 0
    occ = False
    while not occ and i < len(occupied):
        actuel = (nextP, nextP+l)
        present = (occupied[i], occupied[i]+l)
        occ = haveCommon(actuel, present)
        i += 1
    return not occ

def chooseNextP(img, occupied, l):
    total = img.size[0]*img.size[1]
    r = randint(1, total)
    while not canWrite(r, img, occupied, l):
        r = randint(1, total)
    return r

def hide(data, imgName, outName, startingPixel=(0,0)):
    img = Image.open(imgName)
    BLOCKLEN = len(bin(max(img.size))[2:])
    OCCUPIED = []

    d = chunkstring(toBin(data),BLOCKLEN)
    n = len(d)
    # choisie le premier pixel
    pixel = coordinateToPixelNumber(startingPixel[0], startingPixel[1], img)
    if startingPixel == (0,0):
        pixel = chooseNextP(img, OCCUPIED, BLOCKLEN)
        startingPixel = pixelNumberToCoordinate(pixel, img)
    for i in range(n-1):
        # pointeur vers le suivant
        nextP = chooseNextP(img, OCCUPIED, BLOCKLEN)
        # print "%.2f %%" % ((float(i)/float(n))*100)
        write(d[i], pixel, nextP, img)
        OCCUPIED.append(pixel)
        # passage au suivant
        pixel = nextP
    # le dernier pointe sur rien
    write(d[-1], pixel, 0, img)
    img.save(outName)
    img.close()
    print "data starts at " + str(startingPixel)
    return startingPixel

sp = hide(message, "original.png", "out.png")
# sp = hide(message, "original.png", "out.png", (123, 98))
