import cv2
import numpy as np

def preprocess_image(path):
    # Đọc ảnh hỗ trợ đường dẫn chứa ký tự Tiếng Việt
    with open(path, "rb") as f:
        bytes_array = bytearray(f.read())
    np_array = np.asarray(bytes_array, dtype=np.uint8)
    img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    
    # Tiền xử lý
    img = cv2.resize(img, (256, 256))
    img = cv2.GaussianBlur(img, (5,5), 0)
    return img