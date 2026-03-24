import numpy as np

def classify_leaf(mask_healthy, mask_disease):
    healthy_pixels = np.count_nonzero(mask_healthy)
    disease_pixels = np.count_nonzero(mask_disease)
    total_pixels = healthy_pixels + disease_pixels

    if total_pixels == 0:
        return "Lỗi: Không nhận diện được thực vật!"

    disease_ratio = (disease_pixels / total_pixels) * 100

    # Hạ ngưỡng xuống 1.2% để bù đắp cho việc bãi cỏ xanh phía sau quá to làm loãng tỉ lệ
    if disease_ratio > 1.2:  
        return f"Bệnh: Đốm nâu / Úa (Tỉ lệ: {disease_ratio:.1f}%)"
    else:
        return f"Lá khỏe mạnh (Tỉ lệ rủi ro: {disease_ratio:.1f}%)"