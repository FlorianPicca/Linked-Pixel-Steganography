#encoding: UTF-8
from PIL import Image
from random import randint

def pixelNumberToCoordinate(n, img):
    """
    Converts pixel number to coordinates.
    Ex: Image size is w=10, h=20
    The 23th pixel has coordinates of (3, 2).
    """
    return (n%img.size[0], n//img.size[0])

def coordinateToPixelNumber(x, y, img):
    """
    Converts coordinates to pixel number.
    Ex: Image size is w=10, h=20
    pixel (3, 2) is the 23th pixel.
    """
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
    Writes a block of data and pointer to the next pixel in binary format at a given pixel.

    @param data: Binary representation of a block of data.
    @type data: String

    @param pixel: Pixel number where the block starts.
    @type pixel: Int

    @param nextP: Pixel number to the next block of data.
    @type nextP: Int

    @param img: Image Object.
    @type img: Image
    """
    pix = img.load()
    x, y = pixelNumberToCoordinate(nextP, img)
    l = len(data)
    # binari representation of next pixel x
    col = bin(x)[2:].zfill(l)
    # binari representation of next pixel y
    lin = bin(y)[2:].zfill(l)

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

def chunkstring(string, length):
    return [string[0+i:length+i].ljust(length, "0") for i in range(0, len(string), length)]

def canWrite(nextP, img, occupied, l):
    """
    Checks if we can use this pixel to write data without overwriting previously written data.

    @param nextP: Pixel number to check.
    @type nextP: Int

    @param img: Image Object.
    @type img: Image

    @param occupied: List of pixels representing the start of a previously written block.
    @type occupied: List

    @param l: The length of a block.
    @type l: Int

    @returns: True if ok.
    @rtype: Boolean
    """
    total = img.size[0]*img.size[1]
    if nextP + l > total:
        return False
    i = 0
    occ = False
    while not occ and i < len(occupied):
        actuel = (nextP, nextP+l)
        present = (occupied[i], occupied[i]+l)
        # check if no elements in common
        occ = not (max(actuel) < min(present) or max(present) < min(actuel))
        i += 1
    return not occ

def chooseNextP(img, occupied, l):
    """
    Chooses the next pixel randomly while making sure it won't overwrite previously written data.

    @param img: Image Object.
    @type img: Image

    @param occupied: List of pixels representing the start of a previously written block.
    @type occupied: List

    @param l: The length of a block.
    @type l: Int

    @returns: The new pixel number.
    @rtype: Int
    """
    total = img.size[0]*img.size[1]
    r = randint(1, total)
    while not canWrite(r, img, occupied, l):
        r = randint(1, total)
    return r

def hide(data, imgName, outName, startingPixel=(0,0)):
    """
    Hides the string data in the image imgName and creates a new image containing the data outName.
    startingPixel is optional and will be choosed randomly if not specified.

    @param data: Data to hide.
    @type data: String

    @param imgName: Name of the original image.
    @type imgName: String

    @param outName: Name of the resulting image.
    @type outName: String

    @param startingPixel: Optional starting pixel coordinates.
    @type startingPixel: Tuple

    @returns: The starting pixel used.
    @rtype: Tuple
    """
    img = Image.open(imgName)
    BLOCKLEN = len(bin(max(img.size))[2:])
    OCCUPIED = []

    d = chunkstring(toBin(data),BLOCKLEN)
    n = len(d)
    # choose the first pixel
    pixel = coordinateToPixelNumber(startingPixel[0], startingPixel[1], img)
    if startingPixel == (0,0):
        pixel = chooseNextP(img, OCCUPIED, BLOCKLEN)
        startingPixel = pixelNumberToCoordinate(pixel, img)
    for i in range(n-1):
        # pointer to the next pixel
        nextP = chooseNextP(img, OCCUPIED, BLOCKLEN)
        write(d[i], pixel, nextP, img)
        OCCUPIED.append(pixel)
        # switch to next pixel
        pixel = nextP
    # last pointer towards NULL (0, 0)
    write(d[-1], pixel, 0, img)
    img.save(outName)
    img.close()
    return startingPixel

message = "Example data that can be hidden."
# Usage examples
print hide(message, "original.png", "out.png")
# print hide(message, "original.png", "out.png", (123, 98))
