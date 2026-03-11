import cv2

def preprocess_image(path):
    img = cv2.imread(path)
    img = cv2.resize(img, (256, 256))
    img = cv2.GaussianBlur(img, (5,5), 0)
    return img