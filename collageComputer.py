from PIL import Image, ImageChops
import colorEvaluator as colorEval
import getImages as imageColl
import config
import glob
import random

class CollageComputer(object):
    def __init__(self, baseImgPath):
        self.basePath = baseImgPath

    def tintImage(self, path, tint_color):
        image = Image.open(path)
        image = ImageChops.multiply(image, Image.new('RGB', image.size, tint_color))
        image.save(path)
        return path

    def stitchHorizontal(self, imgs, resPath):
        width, height = Image.open(imgs[0]).size
        res = Image.new('RGB', (width * len(imgs), height))

        offset = 0
        for img in imgs:
            tmp = Image.open(img)
            res.paste(tmp, (offset, 0))
            offset += width
        res.save(resPath)
        return resPath

    def stitchVertical(self, imgs, resPath):
        width, height = Image.open(imgs[0]).size
        res = Image.new('RGB', (width, height * len(imgs)))

        offset = 0
        for img in imgs:
            tmp = Image.open(img)
            res.paste(tmp, (0, offset))
            offset += height
        res.save(resPath)
        return resPath

    def assembleCollage(self, topics):
        ce = colorEval.ColorEvaluator(self.basePath, 30, 30)
        avgPixels = ce.getAveragePixelByRegion()
        ic = imageColl.ImageCollector(config.BING_KEY)
        imgList = []
        for topic in topics:
            imgList.extend(ic.run(topic, 100, "img/" + topic, 15, 15))
        rowCounter = 1
        rows = []
        imgCounter = 0
        # Rows
        for x in range(len(averagePixel)):
            tmpRow = []
            for tintColor in averagePixel[x]:
                path = self.tintImage(imgList[imgCounter], tintColor)
                tmpRow.append(path)
                imgCounter += 1
            rows.append(self.stitchHorizontal(tmpRow, "img/row" + str(rowCounter) + ".jpg"))
            rowCounter += 1
        self.stitchVertical(rows, "finalimage.jpg")

    def assembleFromPictures(self, dim1, dim2):
        imgList = glob.glob("img/*.jpg")
        random.shuffle(imgList)
        ic = imageColl.ImageCollector(config.BING_KEY)
        for img in imgList:
            ic.resizeImage(img, 40, 40)
        ce = colorEval.ColorEvaluator(self.basePath, 30, 30)
        avgPixels = ce.getAveragePixelByRegion()
        rowCounter = 1
        rows = []
        imgCounter = 0
        # Rows
        for x in range(len(avgPixels)):
            tmpRow = []
            for tintColor in avgPixels[x]:
                try:
                    path = self.tintImage(imgList[imgCounter], (int(tintColor[0]), int(tintColor[1]), int(tintColor[2])))
                except Exception as e:
                    path = imgList[imgCounter]
                    print "hit exception"
                tmpRow.append(path)
                imgCounter += 1
            rows.append(self.stitchHorizontal(tmpRow, "img/row" + str(rowCounter) + ".jpg"))
            rowCounter += 1
        self.stitchVertical(rows, "finalimage.jpg")



if __name__ == "__main__":
    #cc = CollageComputer("baseImage.jpeg")
    #cc.tintImage("img/spring1.jpg", (244, 119, 66))
    cc = CollageComputer("baseImage.jpeg")
    #topics = ["spring", "summer", "autumn", "winter", "beach", "park", "home", "fruit", "vegetable"]
    #cc.assembleCollage(topics)
    cc.assembleFromPictures(28, 28)
