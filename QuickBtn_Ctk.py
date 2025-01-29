import os
import sys
import subprocess
from tkinter import filedialog,messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
import tkinter as tk
import customtkinter as ctk
from PIL import Image
import shutil

ctk.set_appearance_mode("light")
font_style = ("Microsoft JhengHei", 12, "bold")

input_files = []  # 初始化空的檔案清單
output_folder = ""  # 初始化資料夾路徑


"""抓icon圖片用的"""
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        # 如果程序被打包，_MEIPASS 是打包后的临时文件夹路径
        return os.path.join(sys._MEIPASS, relative_path)
    else:
        # 未打包时，直接返回相对路径
        return os.path.join(os.path.abspath("."), relative_path)

"""操作結束後開啟資料夾"""
def open_folder():
    if os.path.exists(output_folder):
        os.startfile(output_folder)
    else:
        print("資料夾不存在")

def wherethefolder(event=None):  # event 參數設為可選
    global output_folder,input_files
    if event:  # 拖曳進來的文件
        files = event.data.strip('{}').split()  # 解析多個檔案
    else:  # 檔案對話框選擇多個圖片
        files = filedialog.askopenfilenames(filetypes=[('PNG Files', '*.png')])

    if not files:
        return
    
    output_folder = os.path.dirname(files[0])  # 以第一個檔案決定輸出資料夾
    input_files = list(files)  # 轉成清單存入

    # 只提取檔名（不含路徑）
    file_names = [os.path.basename(f) for f in input_files]
    
    # 顯示檔名，逗號分隔
    show_longname.set(" + ".join(file_names))  # 這裡改成 | 分隔
    print("選取的圖片:", file_names)

def ease_in_out(t):
    """ 緩入緩出的插值函數（Ease-In-Out） """
    return 3 * t**2 - 2 * t**3

def create_scaling_sequence(input_file, output_dir, frame_rate=24):
    """ 根據指定的動畫生成縮放序列圖片，並保存為 PNG 格式 """
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 加載圖片
    img = Image.open(input_file)
    width, height = img.size

    # 定義動畫的縮放關鍵幀
    keyframes = {
        0: 100,    # 0 秒，100%
        0.5: 92,   # 0.5 秒，92%
        1: 100     # 1 秒，100%
    }

    # 總幀數
    total_frames = int(1 * frame_rate)  # 1 秒的動畫

    # 計算每幀的縮放比例
    scale_values = []
    for frame in range(total_frames + 1):  # +1 確保最後一幀也包含
        time = frame / frame_rate

        # 根據時間插值計算縮放值
        if time <= 0.5:
            start_scale = keyframes[0]
            end_scale = keyframes[0.5]
            progress = time / 0.5
        else:
            start_scale = keyframes[0.5]
            end_scale = keyframes[1]
            progress = (time - 0.5) / 0.5

        # 使用緩入緩出曲線計算縮放比例
        eased_progress = ease_in_out(progress)
        scale = start_scale + (end_scale - start_scale) * eased_progress
        scale_values.append(scale)

    # 按照計算的縮放比例生成序列圖片
    for frame, scale in enumerate(scale_values):
        new_width = int(width * scale / 100)
        new_height = int(height * scale / 100)

        # 縮放圖片
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # 中心裁剪為原始大小
        crop_box = (
            (new_width - width) // 2,
            (new_height - height) // 2,
            (new_width + width) // 2,
            (new_height + height) // 2
        )
        cropped_img = resized_img.crop(crop_box)

        # 保存圖片
        output_file = os.path.join(output_dir, f"frame_{frame:03d}.png")
        cropped_img.save(output_file)
        print(f"Saved: {output_file}")

def create_tooglescaling_sequence(input_file, output_dir):
    """ 產生 8 張圖片的縮放動畫，100% → 91% → 100%，逐格突變 """
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 加載圖片
    img = Image.open(input_file)
    width, height = img.size

    # 8 幀的縮放比例
    keyframes = [100, 100, 100, 91, 91, 91, 91, 100]  # 逐格突變：100% → 91% → 100%

    # 生成圖片序列
    for frame, scale in enumerate(keyframes):
        new_width = int(width * scale / 100)
        new_height = int(height * scale / 100)

        # 縮放圖片
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # 中心裁剪為原始大小
        crop_box = (
            (new_width - width) // 2,
            (new_height - height) // 2,
            (new_width + width) // 2,
            (new_height + height) // 2
        )
        cropped_img = resized_img.crop(crop_box)

        # 儲存圖片
        output_file = os.path.join(output_dir, f"frame_{frame:03d}.png")
        cropped_img.save(output_file)
        print(f"Saved: {output_file}")

def convert_to_webp_short(input_dir, output_file):
    """ 只將 3 張 PNG 圖片轉換為 WebP，FPS 設為 8 讓播放更順暢 """
    input_pattern = os.path.join(input_dir, "frame_%03d.png")
    command = [
        "ffmpeg",
        "-framerate", "8",   # FPS 設為 8，讓播放不卡頓
        "-i", input_pattern,  # 只輸入 3 張圖片
        "-y",
        "-loop", "0",         # WebP 循環播放（0 = 不循環）
        output_file           # 輸出的 WebP 檔案
    ]

    print("執行 FFmpeg 指令：", " ".join(command))
    subprocess.run(command, check=True)

def convert_to_webp(input_dir, output_file):
    """ 使用 FFmpeg 將 PNG 圖片序列轉換為 WebP 格式 """
    input_pattern = os.path.join(input_dir, "frame_%03d.png")
    command = [
        "ffmpeg",
        "-i", input_pattern,    # 輸入序列圖片
        "-y",                   # 覆蓋輸出文件
        "-r", "24",             # 幀率
        "-loop", "0",           # WebP 是否循環播放（0=不循環）
        output_file             # 輸出的 WebP 文件名
    ]

    print("執行 FFmpeg 指令：", " ".join(command))
    subprocess.run(command, check=True)
    
def scale_webp_action():
    if not input_files:
        messagebox.showerror("錯誤", "請先選擇檔案進行處理!")
        return

    for img in input_files:
        seq_name = os.path.splitext(os.path.basename(img))[0]  # 取得不含副檔名的檔名
        output_dir = os.path.join(output_folder, f"{seq_name}_frames")
        output_webp = os.path.join(output_folder, f"{seq_name}_btn.webp")

        create_scaling_sequence(img, output_dir)  
        convert_to_webp(output_dir, output_webp)  
        shutil.rmtree(output_dir)  # 刪除臨時檔案夾
        print(f"已轉換 {output_webp}")

    # 所有圖片轉換完畢後，彈出視窗通知
    messagebox.showinfo("完成", "所有圖片轉換已完成！")
    open_folder()

def stop_webp_action():
    # 檢查是否有選擇檔案
    if not input_files:
        messagebox.showerror("錯誤", "請先選擇檔案進行處理!")
        return
    
    for img in input_files:
        seq_name = os.path.splitext(os.path.basename(img))[0]
        output_dir = os.path.join(output_folder, f"{seq_name}_frames")
        output_webp = os.path.join(output_folder, f"{seq_name}_btn.webp")

        create_tooglescaling_sequence(img, output_dir)  # 產生 3 張縮放圖片
        convert_to_webp_short(output_dir, output_webp)  # 只輸出 3 幀的 WebP
        shutil.rmtree(output_dir)  # 刪除臨時檔案夾
        print(f"已轉換 {output_webp}")
            
    # 所有圖片轉換完畢後，彈出視窗通知
    messagebox.showinfo("完成", "所有圖片轉換已完成！")
    open_folder()

root = ctk.CTk()
root.geometry("300x220")
root.title(" 尼縮縮看阿")

# 修改背景色
root.configure(fg_color='#EDEDF2')

root_frame = ctk.CTkFrame(root, fg_color='#EDEDF2')
root_frame.pack(fill='x', padx=10, pady=10)

image_path = resource_path('Assets/open-folder.png')
photo = ctk.CTkImage(light_image=Image.open(image_path))

# 設置窗口圖標
root.iconbitmap("Assets/star.ico")

# 抓取位置按鈕
btn_folderpath = ctk.CTkButton(root_frame,
                font=font_style,
                text="選取資料夾位置",
                text_color="#191B1D",
                fg_color="#CEF409",
                hover_color="#DFF56D",
                image=photo,
                command=wherethefolder,
                height=35)
btn_folderpath.pack(padx=5, pady=15)

# 位置顯示框
show_longname = ctk.StringVar()  # 建立文字變數
show_longname.set('Filepath')  # 一開始設定沒有內容
entry_folder = ctk.CTkEntry(root_frame, textvariable=show_longname, border_width=0, text_color='#bdb5bc', font=("Calibri", 12))
entry_folder.pack(fill='x', padx=10, pady=5, ipadx=5, ipady=2)

frame_mid=ctk.CTkFrame(root,height=50,fg_color="#EDEDF2")
frame_mid.pack(side="top", padx=5, ipady=5)

# 執行按鈕
btn_pop = ctk.CTkButton(frame_mid,
                font=font_style,
                text="彈跳",
                text_color="#FFFFFF",
                fg_color="#1A1A1A",
                hover_color="#FF8AEB",
                command=stop_webp_action,
                width=70,height=35)
btn_pop.pack(side="left", padx=5, pady=5)

# 執行按鈕
btn_scale = ctk.CTkButton(frame_mid,
                font=font_style,
                text="縮放",
                text_color="#FFFFFF",
                fg_color="#1A1A1A",
                hover_color="#FF8AEB",
                command=scale_webp_action,
                width=70,height=35)
btn_scale.pack(side="left", padx=5, pady=5)

root.mainloop()
