import tkinter as tk
from tkinter import filedialog
import cv2
import os
from preprocess import preprocess_image
from segment import segment_leaf
from classify import classify_leaf

def run_gui():
    root = tk.Tk()
    root.title("Leaf Disease Detection")

    def open_image():
        # Chọn ảnh đầu vào
        file_path = filedialog.askopenfilename()
        if not file_path:
            return

        # Tiền xử lý và phân đoạn (trả về ảnh lá + mask)
        img = preprocess_image(file_path)
        seg, mask = segment_leaf(img)

        # Phân loại
        result = classify_leaf(seg)

        # Hiển thị ảnh gốc, mask và ảnh lá đã tách nền
        cv2.imshow("Ảnh gốc", img)
        cv2.imshow("Leaf Mask", mask)
        cv2.imshow("Processed Leaf", seg)
        print("Kết quả:", result)

        # Lưu cả 3 ảnh vào thư mục results
        base_name = os.path.basename(file_path)  # ví dụ: leaf1.jpg
        save_original = os.path.join("results", f"original_{base_name}")
        save_seg = os.path.join("results", f"result_{base_name}")
        save_mask = os.path.join("results", f"mask_{base_name}")

        cv2.imwrite(save_original, img)
        cv2.imwrite(save_seg, seg)
        cv2.imwrite(save_mask, mask)

        print(f"Ảnh gốc đã lưu tại: {save_original}")
        print(f"Ảnh kết quả đã lưu tại: {save_seg}")
        print(f"Mask đã lưu tại: {save_mask}")

    btn = tk.Button(root, text="Chọn ảnh lá", command=open_image)
    btn.pack()
    root.mainloop()