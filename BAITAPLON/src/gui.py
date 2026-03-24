import tkinter as tk
from tkinter import messagebox
import cv2
import os
import numpy as np
from PIL import Image, ImageTk  # Thư viện mới để nhúng ảnh vào giao diện
from preprocess import preprocess_image
from segment import segment_leaf
from classify import classify_leaf

def imwrite_utf8(filename, img):
    # Hàm hỗ trợ lưu ảnh có đường dẫn Tiếng Việt
    ext = os.path.splitext(filename)[1]
    result, n = cv2.imencode(ext, img)
    if result:
        with open(filename, mode='wb') as f:
            n.tofile(f)

def run_gui():
    root = tk.Tk()
    root.title("Hệ Thống Nhận Diện Bệnh Lá - Tự Động")
    root.geometry("950x500") # Mở rộng cửa sổ cho đẹp để chứa 3 ảnh

    # --- KHUNG BÊN TRÁI: Danh sách file tự động ---
    frame_left = tk.Frame(root, width=250)
    frame_left.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    tk.Label(frame_left, text="📂 Danh sách ảnh trong CSDL:", font=("Arial", 10, "bold")).pack(anchor="w")
    
    scrollbar = tk.Scrollbar(frame_left)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    listbox = tk.Listbox(frame_left, yscrollcommand=scrollbar.set, width=35, font=("Arial", 10))
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=listbox.yview)

    # --- KHUNG BÊN PHẢI: Nút bấm, Kết quả & Khu vực hiển thị ảnh ---
    frame_right = tk.Frame(root)
    frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # 1. Khung chứa nút bấm và Kết quả chữ
    frame_controls = tk.Frame(frame_right)
    frame_controls.pack(fill=tk.X, pady=5)

    btn_process = tk.Button(frame_controls, text="▶ Kiểm tra ảnh đang chọn", 
                            font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", padx=15, pady=8)
    btn_process.pack(side=tk.LEFT, padx=10)

    lbl_result = tk.Label(frame_controls, text="Kết quả: (Chưa có)", font=("Arial", 14, "bold"))
    lbl_result.pack(side=tk.LEFT, padx=20)

    # 2. Khung chứa 3 hình ảnh
    frame_images = tk.Frame(frame_right)
    frame_images.pack(fill=tk.BOTH, expand=True, pady=15)

    # Khởi tạo 3 nhãn (Label) để dán ảnh vào
    lbl_img_original = tk.Label(frame_images, text="1. Ảnh gốc", compound=tk.TOP, font=("Arial", 10))
    lbl_img_original.pack(side=tk.LEFT, padx=5, expand=True)

    lbl_img_mask = tk.Label(frame_images, text="2. Mask Vùng Bệnh", compound=tk.TOP, font=("Arial", 10))
    lbl_img_mask.pack(side=tk.LEFT, padx=5, expand=True)

    lbl_img_result = tk.Label(frame_images, text="3. Kết quả (Tô đỏ bệnh)", compound=tk.TOP, font=("Arial", 10))
    lbl_img_result.pack(side=tk.LEFT, padx=5, expand=True)

    # --- CÁC HÀM XỬ LÝ LOGIC ---
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_folder = os.path.join(current_dir, "..", "data")
    file_paths = []

    def load_files():
        """Hàm tự động quét toàn bộ ảnh trong folder data"""
        if not os.path.exists(data_folder):
            listbox.insert(tk.END, "⚠️ Không tìm thấy folder 'data'")
            return
            
        for root_dir, dirs, files in os.walk(data_folder):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    full_path = os.path.join(root_dir, file)
                    file_paths.append(full_path)
                    rel_path = os.path.relpath(full_path, data_folder)
                    listbox.insert(tk.END, rel_path)

    def display_image_on_label(cv_img, label_widget, size=(200, 200)):
        """Hàm chuyển đổi ảnh từ OpenCV sang Tkinter và dán lên giao diện"""
        # Đổi hệ màu cho đúng chuẩn hiển thị
        if len(cv_img.shape) == 3:
            cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        else: # Nếu là ảnh đen trắng (mask)
            cv_img = cv2.cvtColor(cv_img, cv2.COLOR_GRAY2RGB)
            
        pil_img = Image.fromarray(cv_img)
        pil_img = pil_img.resize(size, Image.Resampling.LANCZOS) # Thu nhỏ lại cho vừa khung
        tk_img = ImageTk.PhotoImage(pil_img)
        
        # Gắn ảnh vào Label
        label_widget.config(image=tk_img)
        label_widget.image = tk_img # Phải lưu tham chiếu để ảnh không bị mất

    def process_selected_image():
        """Hàm xử lý khi bấm nút"""
        selected_indices = listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Nhắc nhở", "Vui lòng chọn 1 ảnh từ danh sách bên trái trước!")
            return
            
        index = selected_indices[0]
        file_path = file_paths[index]

        # Hiệu ứng báo đang xử lý
        lbl_result.config(text="Đang phân tích ảnh...", fg="blue")
        lbl_result.update() # Ép giao diện cập nhật ngay lập tức!

        # 1. Tiền xử lý
        img = preprocess_image(file_path)
        
        # 2. Phân đoạn
        processed_leaf, mask_healthy, mask_disease = segment_leaf(img)

        # 3. Phân loại
        result = classify_leaf(mask_healthy, mask_disease)

        # Cập nhật CHỮ kết quả
        if "Bệnh" in result:
            lbl_result.config(text=f"Kết quả: \n{result}", fg="red")
        else:
            lbl_result.config(text=f"Kết quả: \n{result}", fg="green")
        lbl_result.update()

        # Cập nhật 3 HÌNH ẢNH trực tiếp lên giao diện
        display_image_on_label(img, lbl_img_original)
        display_image_on_label(mask_disease, lbl_img_mask)
        display_image_on_label(processed_leaf, lbl_img_result)

        # Lưu ảnh minh chứng ẩn ở dưới nền
        results_dir = os.path.join(current_dir, "..", "results")
        os.makedirs(results_dir, exist_ok=True)
        base_name = os.path.basename(file_path)
        imwrite_utf8(os.path.join(results_dir, f"original_{base_name}"), img)
        imwrite_utf8(os.path.join(results_dir, f"highlighted_{base_name}"), processed_leaf)
        imwrite_utf8(os.path.join(results_dir, f"mask_{base_name}"), mask_disease)

    # Gán sự kiện cho nút bấm
    btn_process.config(command=process_selected_image)

    # Gọi hàm quét file ngay khi vừa khởi động giao diện
    load_files()

    root.mainloop()