import datetime
import sys
import qrcode
import cv2
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer


def generateQR(link, titel = None, fillcolor="black", bgcolor="white", roundPixel=None):
    errorcorrectionOptions = [qrcode.constants.ERROR_CORRECT_L, qrcode.constants.ERROR_CORRECT_M, qrcode.constants.ERROR_CORRECT_Q, qrcode.constants.ERROR_CORRECT_H]
    errorcorrection = errorcorrectionOptions[0]
    size = 2

    qr = qrcode.QRCode(
        version=size,
        error_correction=errorcorrection,
        box_size=16,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)

    if roundPixel is None:
        img = qr.make_image(fill_color=fillcolor, back_color=bgcolor)
    else:
        img = qr.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer(), fill_color=fillcolor, back_color=bgcolor)

    datetimenow = datetime.datetime.now()
    if titel is not None:
        img.save("generatedQRcodes/" + titel + ".jpg")
    else:
        img.save(datetimenow.strftime("generatedQRcodes/%Y%m%d-%H-%M-%S_generatedQRcode") + ".jpg")


def readQR(filename=None):
    img = cv2.imread("C:/Users/Patri/OneDrive/Dokumente/GitHub/qrgen/20220217-14-19-06_generatedQRcode.jpg")
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)
    print("data", data, "bbox", bbox)
    if bbox is not None:
        print(f"QRCode data:\n{data}")
        # display the image with lines
        # length of bounding box
        n_lines = len(bbox[0])

        for i in range(0, n_lines):
            point1 = (int(bbox[0][i][0]), int(bbox[0][i][1]))
            point2 = (int(bbox[0][(i+1) % n_lines][0]), int(bbox[0][(i+1) % n_lines][1]))
            cv2.line(img, point1, point2, color=(0, 0, 255), thickness=5)

        cv2.imshow("img", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def liveCapturingQR(args=None):
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    while True:
        _, img = cap.read()
        # detect and decode
        data, bbox, _ = detector.detectAndDecode(img)
        # check if there is a QRCode in the image
        if bbox is not None:
            # display the image with lines
            n_lines = len(bbox[0])
            for i in range(0, n_lines):
                point1 = (int(bbox[0][i][0]), int(bbox[0][i][1]))
                point2 = (int(bbox[0][(i + 1) % n_lines][0]), int(bbox[0][(i + 1) % n_lines][1]))
                cv2.line(img, point1, point2, color=(0, 0, 255), thickness=5)
            if data:
                print("[+] QR Code detected, data:", data)

        cv2.imshow("img", img)
        if cv2.waitKey(1) == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    args = sys.argv
    print(args)
    if args[1] == "gen":
        generateQR(*args[2:])
    elif args[1] == "read":
        readQR(*args[2:])
    elif args[1] == "live":
        liveCapturingQR(*args[2:])
