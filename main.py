import sys

import qrcode


def generateQR(args):
    link, filename = args
    img = qrcode.make(link)
    img.save(filename)


def readQR(filename):
    pass


if __name__ == '__main__':
    args = sys.argv[1:]

    if args[1] == "gen":
        generateQR(args)
    else:
        readQR(args)







