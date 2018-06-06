import argparse
import os

import t2cmodules.imageretriever as imageretriever
import t2cmodules.layoutoptimizer as layoutoptimizer
import t2cmodules.textanalyzer as textanalyzer
import t2cmodules.imagewriter as imagewriter
import t2cmodules.imageemphasis as imageemphasis

# Default command-line parameters
parser = argparse.ArgumentParser(description='This library converts a given paragraph '
                                             'of text into an equivalent image illustration, '
                                             'represented as a collage of images. It also gives '
                                             'the user the option of creating a collage of '
                                             'images from a folder containing a set of images.')
parser.add_argument('-i', default=["collection"], choices=['text', 'collection'], nargs=1,
                    help='Interactiveness:'
                         'Choose if text needs to be converted to a collage of images'
                         'or a folder containing images needs to be represented as a collage.'
                         'Default: collection')
parser.add_argument('-d', nargs=1,
                    help='Absolute path of folder containing text input (if text to '
                         'collage is chosen) or folder containing images (if image collection'
                         'to collage is chosen)')
parser.add_argument('-cw', default=1920, type=int, nargs=1,
                    help='Width of canvas. Default: 1920')
parser.add_argument('-ch', default=1080, type=int, nargs=1,
                    help='Height of canvas. Default: 1080')
parser.add_argument('-e', default='random', choices=['random', 'auto', 'user'], nargs=1,
                    help='Importance estimator for the images in the collage. The'
                         'importance assigned, will help the library decide the scale of '
                         'each image. Default: Random')
parser.add_argument('-b', default=3, type=int, nargs=1,
                    help='Beta: Space between images in the collage (in pixels).'
                         'Default: 3')
parser.add_argument('-GA', default=[500, 60, 0.6, 0.02, 0.15], type=float, nargs=5,
                    help='GA parameters - number of iterations, population size,'
                         'crossover probability, mutation probability, lambda (fitness'
                         'function parameter - lam).'
                         'Default: Number of generations - 500,'
                         ' Population size - 10, Crossover probability - 0.7,'
                         ' Mutation probability - 0.2, Lambda (fitness component'
                         'trade-off factor) - 0.15')
parser.add_argument('-f', default=["html"], choices=['jpg', 'html'], nargs=1,
                    help='Output file:'
                         'Choose if the collage needs to be saved as HTML and JPG')

'''
    text2collage API
'''


def text2collage(option='collection', d='', cw=1920, ch=1080, beta=3, imp='random', GA=[500, 60, 0.6, 0.02, 0.15], opfile='html'):
    """

    :param option: generate collage from text or a collection of images
    :param d: directory that contains the text or the collection of images
    :param cw: width of the collage
    :param ch: height of the collage
    :param beta: inter-image space
    :param imp: emphasis factor for images
    :param GA: Genetic Algorithm parameters
    :return: GA's fitness value
    """
    foldername = os.path.abspath(d)
    osname = os.uname()[0]
    if not foldername:
        print("A directory of text or image files is required")
        exit(0)
    emphasis = {}

    keywords = []
    if option == 'text':
        for filename in os.listdir(foldername):
            if filename.endswith('.txt'):
                print ("\nConverting "+filename+" to an illustration")
                if osname == 'Windows':
                    openfile = foldername + '\\' + filename
                else:
                    openfile = foldername + '/' + filename
                f = open(openfile, 'r')
                text = f.read().encode().decode('ascii', 'ignore')
                f.close()

                (keywords, tags), scores = textanalyzer.TextAnalyzer().main(text)

                imagelist = imageretriever.ImageRetrieval().main(keywords, tags, foldername)

                if imp == 'user':
                    filename = input("Enter the absolute path to the file containing image emphasis values: ")
                    emphasis = imageemphasis.emphasisFromFile(filename)
                elif imp == 'auto':
                    emphasis = imageemphasis.emphasisFromText(scores, imagelist)

                fitness, imginfo = layoutoptimizer.Environment().main(keywords, filename, foldername, canvasw, canvash, beta, GAparams, emphasis)

                imagewriter.writeToFile(foldername, filename, imginfo, keywords, cw, ch, opfile)

    elif option == 'collection':
        if imp == 'user':
            filename = input("Enter the absolute path to the file containing image emphasis values: ")
            emphasis = imageemphasis.emphasisFromFile(filename)
        fitness, imginfo = layoutoptimizer.Environment().main([], '', foldername, cw, ch, beta, GA, emphasis)

        imagewriter.writeToFile(foldername, '', imginfo, keywords, cw, ch, opfile)


if __name__ == "__main__":
    try:
        args = vars(parser.parse_args())
        canvasw = args['cw'][0] if isinstance(args['cw'], list) else args['cw']
        canvash = args['ch'][0] if isinstance(args['ch'], list) else args['ch']
        beta = args['b'][0] if isinstance(args['b'], list) else args['b']
        imp = args['e'][0] if isinstance(args['e'], list) else args['e']
        GAparams = args['GA']
        GAparams[:2] = map(int, GAparams[:2])
        option = args['i'][0]
        opfile = args['f'][0]

        foldername = os.path.abspath(args['d'][0])

        text2collage(option, args['d'][0], canvasw, canvash, beta, imp, GAparams, opfile)
    except Exception as e:
        print(e)
