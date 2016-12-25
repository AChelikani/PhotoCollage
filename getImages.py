import urllib, httplib, base64
import config
import json
from PIL import Image

class ImageCollector(object):
    def __init__(self, subKey):
        self.header = {
            # Request headers
            'Ocp-Apim-Subscription-Key': subKey,
        }

    def downloadImage(self, url, savePath):
        urllib.urlretrieve(url, savePath)
        return savePath

    def resizeImage(self, imgPath, dim1, dim2):
        image = Image.open(imgPath)
        image = image.resize((dim1, dim2), Image.ANTIALIAS)
        image.save(imgPath)

    def getImages(self, query, count):
        params = urllib.urlencode({
            'q': query,
            'count': count,
            'offset': '0',
            'mkt': 'en-us',
            'safeSearch': 'Moderate',
        })
        try:
            conn = httplib.HTTPSConnection('api.cognitive.microsoft.com')
            conn.request("GET", "/bing/v5.0/images/search?%s" % params, "{body}", self.header)
            response = conn.getresponse()
            data = response.read()
            conn.close()
            return data
        except Exception as e:
            print e

    def parseURL(self, resp):
        json_resp = json.loads(resp)
        urls = []
        for image in json_resp["value"]:
            urls.append((image["contentUrl"], image["width"], image["height"]))
        return urls

    def downloadAllAndResize(self, urls, dim1, dim2, pathBase):
        counter = 1
        for item in urls:
            url = item[0]
            path = self.downloadImage(url, pathBase + str(counter) + ".jpg")
            self.resizeImage(path, dim1, dim2)
            counter += 1

    def run(self, keyword, count, path, dim1, dim2):
        res = self.getImages(keyword, count)
        self.downloadAllAndResize(self.parseURL(res), dim1, dim2, path)



if __name__ == "__main__":
    ic = ImageCollector(config.BING_KEY)
    #path = ic.downloadImage("http://parade.com/wp-content/uploads/2014/03/Why-Do-Stars-All-Look-Almost-the-Same-Size-ftr.jpg", "stars.jpg")
    #ic.resizeImage(path, 100)
    ic.run("stars", 5, "img/stars", 100, 100)
