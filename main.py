import datetime
import sys
import qrcode
import cv2


def generateQR(link):
    img = qrcode.make(link)
    x = datetime.datetime.now()
    img.save(x.strftime("%Y%m%d-%H-%M-%S_generatedQRcode")+".jpg")


def readQR(filename):
    d = cv2.QRCodeDetector()
    val, _, _ = d.detectAndDecode(cv2.imread("20220130-16-07-15_generatedQRcode.jpg"))
    print("Decoded text is: ", val)


if __name__ == '__main__':
    args = sys.argv
    print(args)
    if args[1] == "gen":
        generateQR(args[2:])
    else:
        readQR(args[2:])







