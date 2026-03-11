import cv2
import numpy as np

def segment_leaf(img):
    # Chuyển sang HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Dải màu lá (xanh, vàng, úa, đỏ đốm)
    ranges = [
        (np.array([25, 40, 40]), np.array([95, 255, 255])),   # xanh lá
        (np.array([15, 40, 40]), np.array([35, 255, 255])),   # vàng úa
        (np.array([0, 40, 40]),  np.array([15, 255, 255])),   # đỏ/đốm bệnh
    ]

    # Kết hợp mask
    mask_total = None
    for lower, upper in ranges:
        mask = cv2.inRange(hsv, lower, upper)
        mask_total = mask if mask_total is None else cv2.bitwise_or(mask_total, mask)

    # Lọc nhiễu
    kernel = np.ones((5,5), np.uint8)
    mask_total = cv2.morphologyEx(mask_total, cv2.MORPH_CLOSE, kernel)
    mask_total = cv2.morphologyEx(mask_total, cv2.MORPH_OPEN, kernel)

    # Áp dụng mask để giữ lại lá (nền đen)
    leaf_only = cv2.bitwise_and(img, img, mask=mask_total)

    return leaf_only, mask_total