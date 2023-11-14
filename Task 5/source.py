import cv2
import tkinter as tk

def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    features = classifier.detectMultiScale(gray_img, scaleFactor, minNeighbors)
    cords = []
    for (x, y, w, h) in features:
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        cv2.putText(img, text, (x, y - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 1, cv2.LINE_AA)
        cords = [x, y, w, h]
    return cords, img


def detect(img,faceCascade):
    color = {"blue": (255, 0, 0), "red": (0, 0, 255), "green": (0, 255, 0)}
    cords, img = draw_boundary(img, faceCascade, 1.2, 10, color['green'], "Human")
    return img


faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

vc = cv2.VideoCapture(0)
while True:
    _, img = vc.read()
    img=detect(img,faceCascade)
    cv2.imshow("face detection", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
vc.release()
cv2.destroyAllWindows()
