import cv2
import numpy as np

def segment_leaf(img):
    # Chuyển sang không gian màu HSV để bóc tách màu dễ hơn
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 1. BẮT VÙNG LÁ KHỎE (Màu xanh lá)
    lower_green = np.array([25, 40, 40])
    upper_green = np.array([95, 255, 255])
    mask_healthy = cv2.inRange(hsv, lower_green, upper_green)
import cv2
import numpy as np

def segment_leaf(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 1. BẮT VÙNG LÁ (Xanh lá)
    lower_green = np.array([33, 40, 40])
    upper_green = np.array([95, 255, 255])
    mask_healthy = cv2.inRange(hsv, lower_green, upper_green)

    # 2. BẮT CHÍNH XÁC ĐỐM BỆNH (Nâu, Vàng, Đỏ)
    # Dải Hue từ 0 -> 33 tóm gọn các đốm màu nâu cháy
    # Giới hạn Value > 30 để BỎ QUA bóng râm đen thui dưới thảm cỏ
    lower_disease = np.array([0, 30, 30])
    upper_disease = np.array([33, 255, 255])
    mask_disease = cv2.inRange(hsv, lower_disease, upper_disease)

    # Lọc nhiễu
    kernel = np.ones((3,3), np.uint8)
    mask_healthy = cv2.morphologyEx(mask_healthy, cv2.MORPH_OPEN, kernel)
    mask_disease = cv2.morphologyEx(mask_disease, cv2.MORPH_OPEN, kernel)
    
    # MẸO: Phóng to mask đốm bệnh lên 1 chút để viền bao trọn vết bệnh
    mask_disease = cv2.dilate(mask_disease, kernel, iterations=1)

    # Tô màu đỏ rực lên vết bệnh
    processed_leaf = img.copy()
    processed_leaf[mask_disease > 0] = [0, 0, 255]

    return processed_leaf, mask_healthy, mask_disease
    # 2. BẮT VÙNG LÁ BỆNH (Vàng úa, Nâu, Đỏ, Đốm đen cháy)
    # - Dải Vàng/Nâu/Đỏ (Hue từ 0 đến 25)
    lower_yr = np.array([0, 30, 30])
    upper_yr = np.array([25, 255, 255])
    mask_yr = cv2.inRange(hsv, lower_yr, upper_yr)

    # - Dải Đốm tối màu (Bệnh thường làm lá cháy đen thẫm -> Độ sáng Value thấp)
    lower_dark = np.array([0, 0, 0])
    upper_dark = np.array([179, 255, 75]) # Value < 75 là vùng tối màu
    mask_dark = cv2.inRange(hsv, lower_dark, upper_dark)

    # Gộp tất cả các vùng bệnh lại thành 1 Mask chung
    mask_disease = cv2.bitwise_or(mask_yr, mask_dark)

    # Lọc nhiễu để xóa bớt các chấm trắng li ti trên mask
    kernel = np.ones((3,3), np.uint8)
    mask_healthy = cv2.morphologyEx(mask_healthy, cv2.MORPH_OPEN, kernel)
    mask_disease = cv2.morphologyEx(mask_disease, cv2.MORPH_OPEN, kernel)

    # MẸO LẤY ĐIỂM: Tô màu Đỏ (Red) đè lên vùng bị bệnh trên ảnh gốc cho trực quan
    processed_leaf = img.copy()
    processed_leaf[mask_disease > 0] = [0, 0, 255] # BGR: 255 đỏ

    # Trả về ảnh đã tô màu, và 2 mask để tính toán
    return processed_leaf, mask_healthy, mask_disease