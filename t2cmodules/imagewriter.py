from PIL import Image
from PIL import ImageFile
import os
from bs4 import BeautifulSoup


ImageFile.LOAD_TRUNCATED_IMAGES = True

osname = os.uname()[0]


def writeToFile(directory, filename, imginfo, keywords, cw, ch, opfile):
    if osname == 'Windows':
        openfolder = directory + '\\results\\'
    else:
        openfolder = directory + '/results/'
    if not os.path.exists(openfolder):
        os.makedirs(openfolder)

    if opfile == 'html':
        writeToHTML(imginfo, openfolder, filename, keywords)
    else:
        writeToJPG(imginfo, openfolder, filename, keywords, cw, ch)


def writeToHTML(imginfo, openfolder, filename, nouns):
    html = """
            <html>
            <head>
            <title>Photo layout</title>
            </head>
            <body>
            <p>
            """
    img = ''
    for name in imginfo:
        (nm, ((width, height), (x1, y1))) = imginfo[name]
        for index, n in enumerate(nouns):
            n = ''.join(x for x in n)
            if n == nm:
                break
        positions = "position:absolute;top:" + str(y1) + ";left:" + str(x1) + \
                    ";width:" + str(width) + ";height:" + str(height)
        img = img + "<img style=" + positions + " src=" + name + "></img>"

    html = html + img + """</html>"""
    soup = BeautifulSoup(html, 'html.parser')

    if filename != '':
        with open(openfolder + filename.split('.txt')[0] + '.html', 'w') as f:
            f.write(str(soup.prettify('utf-8')))
        print("The collage is saved in " + openfolder + filename.split('.txt')[0] + ".html")
    else:
        with open(openfolder + 'collage.html', 'w') as f:
            f.write(str(soup.prettify('utf-8')))
        print("The collage is saved in " + openfolder + "collage.html")


def writeToJPG(imginfo, openfolder, filename, nouns, canvasw, canvash):
    canvas = Image.new('RGB', (canvasw, canvash))
    for name in imginfo:
        (nm, ((width, height), (x1, y1))) = imginfo[name]
        im = Image.open(name)
        im = im.resize((width, height), Image.ANTIALIAS)
        canvas.paste(im, (x1, y1))

        for index, n in enumerate(nouns):
            n = ''.join(x for x in n)
            if n == nm:
                break

    if filename != '':
        canvas.save(openfolder + filename.split('.txt')[0] + '.jpg')
        print("The collage is saved in " + openfolder + filename.split('.txt')[0] + ".jpg\n")
    else:
        canvas.save(openfolder + 'collage.jpg')
        print("The collage is saved in " + openfolder + "collage.jpg\n")
