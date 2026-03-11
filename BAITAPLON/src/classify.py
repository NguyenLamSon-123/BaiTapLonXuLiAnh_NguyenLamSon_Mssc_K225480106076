import numpy as np

def classify_leaf(img):
    # Tính trung bình màu để phân biệt lá khỏe hay bệnh
    mean_color = np.mean(img, axis=(0,1))
    if mean_color[1] < 80:  # kênh xanh thấp -> lá úa/bệnh
        return "Bệnh: Vàng lá"
    else:
        return "Lá khỏe mạnh"