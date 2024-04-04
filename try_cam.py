import cv2


def camera():
    captured = False
    cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    # cv2.namedWindow("capture")
    ret, frame = cam.read()
    cv2.imwrite("capture.png", frame)
    cam.release()
    cv2.destroyAllWindows()
    return captured

camera()