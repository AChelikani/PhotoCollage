from PIL import Image

class ColorEvaluator(object):
    def __init__(self, path, xDim, yDim):
        self.path = path
        self.im = Image.open(path)
        self.pix = self.im.load()
        self.xPics = xDim
        self.yPics = yDim

    def getRGB(self, x, y):
        return self.pix[x,y]

    def getSize(self):
        return self.im.size

    def getRegionAverage(self, xStart, xInc, yStart, yInc):
        pixels = 0.0
        r = g = b = 0
        for x in range(xStart, xStart + xInc):
            for y in range(yStart, yStart + yInc):
                rt, gt, bt = self.getRGB(x, y)
                r += rt; g += gt; b += bt
                pixels += 1.0
        return (r/pixels, g/pixels, b/pixels)


    def getAveragePixelByRegion(self):
        xDim, yDim = self.getSize()
        # Assumes xDim divides xPics and yDim divides yPics
        xInc = xDim / self.xPics
        yInc = yDim / self.yPics
        avgPixels = [[(0, 0, 0) for x in range(self.xPics)] for y in range(self.yPics)]
        xCount = 0
        yCount = 0
        for x in range(0, xDim, xInc):
            for y in range(0, yDim, yInc):
                avgPixels[y/yInc][x/xInc] = self.getRegionAverage(x, xInc, y, yInc)
        return avgPixels

    def getAveragePixel(self):
        r = g = b = 0
        pixels = 0.0
        xDim, yDim = self.getSize()
        for x in range(xDim):
            for y in range(yDim):
                rt, gt, bt = self.getRGB(x, y)
                r += rt; g += gt; b += bt
                pixels += 1.0
        return (r/pixels, g/pixels, b/pixels)

    def getAllPixels(self):
        return self.pix



if __name__ == "__main__":
    ce = ColorEvaluator("baseImage.jpeg", 28, 28)
    res = ce.getAveragePixelByRegion()
    for item in res[0]:
        print map(int, item)
