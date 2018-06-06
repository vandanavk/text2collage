from bs4 import BeautifulSoup
import urllib.request
import os
import json
import re
import string
import request


header = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
        }


class ImageRetrieval:
    def main(self, query, tags, directory):
        self.osname = os.uname()[0]
        if self.osname == 'Windows':
            openfolder = directory + '\\images'
        else:
            openfolder = directory + '/images'
        if not os.path.exists(openfolder):
            os.makedirs(openfolder)

        self.query = query
        self.tagset = tags
        self.directory = directory
        self.retrieveImages()


    def saveImages(self, sortedmatchingtag, qcopy, q):
        """
        Save the image with highest Keyword Overlap value
        :param sortedmatchingtag: image links of images sorted in decreasing order of Keyword Overlap value
        :param qcopy: copy of the query without spaces
        :param q: query keywords
        """
        if self.osname == 'Windows':
            openfolder = self.directory + "\\images\\"
        else:
            openfolder = self.directory + "/images/"
        for i, t in enumerate(sortedmatchingtag):
            try:
                raw_img = urllib.request.urlopen(t).read()
                f = open(openfolder + qcopy + ".jpg", 'wb')

                f.write(raw_img)
                f.close()
                print ("Saved image for " + q)
                break
            except Exception as e:
                continue

    def retrieveImages(self):
        """
        Retrieve images for query keywords of each sentence.
        Retrieve image tags and compare with sentence tags.
        Sort image links in decreasing order of keyword overlap value.
        Call saveImage
        """
        imageList = []
        for i, q in enumerate(self.query):
            matchingtags = {}
            querytag = []
            for tag in self.tagset[i]:
                for x in tag.split():
                    querytag.append(x.lower())
            if isinstance(q, list):
                qcopy = ''.join(x for x in q)
            else:
                qcopy = q.replace(' ', '')

            imageList.append(qcopy)

            if self.osname == 'Windows':
                openfolder = self.directory + "\\images\\" + qcopy
            else:
                openfolder = self.directory + "/images/" + qcopy
            if os.path.exists(openfolder + ".jpg"):
                continue
            if isinstance(q, list):
                q = '+'.join(x for x in q)
            else:
                q = q.replace(' ', '+')

            url = 'https://www.google.com/search?q=' + q + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg&safe=active&tbs=sur:fm'
            soup = BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url, headers=header)), 'html.parser')
            for a in soup.find_all("div", {"class": "rg_meta"}):
                link, Type, tags = json.loads(a.text)["ou"], json.loads(a.text)["ity"], json.loads(a.text)["s"]
                tags = re.sub('[' + string.punctuation + ']', '', tags)
                taglist = [x for x in tags.split()]
                commontag = [x.lower() for x in taglist if x.lower() in querytag]
                matchingtags[link] = len(commontag)

            sortedmatchingtag = sorted(matchingtags, key=matchingtags.get, reverse=True)
            self.saveImages(sortedmatchingtag, qcopy, q)
        return imageList
