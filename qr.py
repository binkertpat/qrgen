import datetime
import sys
import qrcode
import cv2
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
import os


def generateQR(datas, titel=None, fillcolor="black", bgcolor="white", roundPixel=None):
    """
    Generate a QR-Codes

    Parameters:
        datas (str): to encoding datas
        titel (str): name of the generate file
        fillcolor (str): color of the pixels (black, white, red, ...)
        bgcolor (str): backgroundcolor (black, white, red, ...)
        roundPixel (str): rounded rectangles in QR-Code (set a random character)

    Returns:
        generatedQRCode (jpg): have a look in ./generatedQRCodes
    """

    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=16,
        border=4,
    )
    qr.add_data(datas)
    qr.make(fit=True)

    if roundPixel is None:
        img = qr.make_image(fill_color=fillcolor, back_color=bgcolor)
    else:
        img = qr.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer(), fill_color=fillcolor,
                            back_color=bgcolor)

    datetimenow = datetime.datetime.now()
    if titel is not None:
        img.save("generatedQRcodes/" + titel + ".jpg")
        print("Generated QR-Codes saved in generatedQRcodes as: " + titel + ".jpg")
    else:
        img.save(datetimenow.strftime("generatedQRcodes/%Y%m%d-%H-%M-%S_generatedQRcode") + ".jpg")
        print("Generated QR-Codes saved in generatedQRcodes as: " + datetimenow.strftime("%Y%m%d-%H-%M-%S_generatedQRcode") + ".jpg")


def readQR(directoryName="readQR"):
    """
    read QR-Codes from files

    Parameters:
        directoryName (str): set directory with given QR-Codes

    Returns:
        datas (str): print decoded datas to console
    """

    filesToRead = os.listdir(directoryName)
    absoluteFilePaths = []
    for file in filesToRead:
        absoluteFilePaths.append(os.path.abspath(directoryName + "/" + file))

    for file in absoluteFilePaths:
        img = cv2.imread(file)
        detector = cv2.QRCodeDetector()
        data, boundingbox, _ = detector.detectAndDecode(img)
        if boundingbox is not None:
            print("Read QR-Code saved in " + file + ".\nDecoded QR-Code datas:\n" + data)
            n_lines = len(boundingbox[0])
            for i in range(0, n_lines):
                point1 = (int(boundingbox[0][i][0]), int(boundingbox[0][i][1]))
                point2 = (int(boundingbox[0][(i + 1) % n_lines][0]), int(boundingbox[0][(i + 1) % n_lines][1]))
                cv2.line(img, point1, point2, color=(0, 0, 255), thickness=5)
            cv2.imshow("QR-Code saved in " + file, img)
            if cv2.waitKey(1) == ord(" "):
                break
            cv2.waitKey(0)
            cv2.destroyAllWindows()


def liveCapturingQR(args=None):
    """
    read QR-Codes live via webcam

    Returns:
        datas (str): print decoded datas to console
        img (img): show webcam live image with marked detected qr-code
    """

    VideoCaputuringDevice = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()

    tempDecodedDatas = ""
    while True:
        _, img = VideoCaputuringDevice.read()
        data, boundingbox, _ = detector.detectAndDecode(img)
        if boundingbox is not None:
            # display the image with lines
            n_lines = len(boundingbox[0])
            for i in range(0, n_lines):
                p1 = (int(boundingbox[0][i][0]), int(boundingbox[0][i][1]))
                p2 = (int(boundingbox[0][(i + 1) % n_lines][0]), int(boundingbox[0][(i + 1) % n_lines][1]))
                cv2.line(img, p1, p2, color=(0, 0, 255), thickness=5)
            if data:
                if data != tempDecodedDatas:
                    tempDecodedDatas = data
                    print("Success! QR-Code detected and read. Decoded datas: \n", data)

        cv2.imshow("QR-Code capturing", img)
        if cv2.waitKey(1) == ord(" "):
            break
    VideoCaputuringDevice.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    args = sys.argv

    if args[1] == "gen":
        generateQR(*args[2:])
    elif args[1] == "read":
        readQR(*args[2:])
    elif args[1] == "live":
        liveCapturingQR(*args[2:])
