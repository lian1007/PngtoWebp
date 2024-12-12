import os
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
import datetime
from PIL import Image

font_style = ("Microsoft JhengHei UI", 10)

# 設定時間限制為2025年10月
time_limit = datetime.datetime(2025, 10, 6)

# 取得當前時間
current_time = datetime.datetime.now()

# Global variables for input file and output directory
input_file = None
output_dir = None

def wherethefolder(event=None):  # event 參數設為可選
    global input_file, seq_name, long_name, output_folder
    if event:  # 如果是來自拖放事件，使用 event.data
        files = event.data
    else:  # 否則使用檔案對話框
        files = filedialog.askopenfilename(filetypes=[('All Supported Files', '.png')])
    if not files:  # 如果沒有選擇文件，則返回
        return
    
    output_folder = os.path.dirname(files)  # 獲取文件所在的資料夾
    Fullpath = files.split('/')  # 分割成多塊的序列
    long_name = Fullpath[-1]  # 完整的檔案名
    seq_name = long_name.split('.')[-2]
    input_file = files  # 設定輸入的圖片檔案路徑
    output_dir = output_folder  # 設定輸出的資料夾路徑
    show_longname.set(input_file)  # 顯示選取的檔案名
    print(seq_name)


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

def create_tooglescaling_sequence(input_file, output_dir, frame_rate=24):
    """
    根據指定的動畫生成縮放序列圖片，並保存為 PNG 格式。
    
    :param input_file: 輸入的 PNG 文件路徑
    :param output_dir: 輸出的文件夾路徑
    :param frame_rate: 每秒幀數（默認 24 fps）
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 加載圖片
    img = Image.open(input_file)
    width, height = img.size

    # 定義動畫的縮放關鍵幀
    keyframes = {
        0: 100,    # 0 秒，100%
        0.5: 91,   # 0.5 秒，91%
        1: 100     # 1 秒，100%
    }

    # 總幀數
    total_frames = int(1 * frame_rate)  # 1 秒的動畫

    # 計算每幀的縮放比例
    scale_values = []
    for frame in range(total_frames + 1):  # +1 確保最後一幀也包含
        time = frame / frame_rate

        # 根據時間設置縮放值
        if time < 0.5:
            scale = keyframes[0]  # 保持 100%
        elif time < 1:
            scale = keyframes[0.5]  # 突然變成 91%
        else:
            scale = keyframes[1]  # 突然回到 100%

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
    print(f"WebP 文件已生成：{output_file}")


def stop_webp_action():
    output_dir = os.path.join(output_folder, "scaled_frames")
    output_webp = os.path.join(output_folder, f"{seq_name}_animation.webp")
    create_tooglescaling_sequence(input_file, output_dir)  # 生成縮放序列
    convert_to_webp(output_dir, output_webp)  # 轉換為 WebP
    
def scale_webp_action():
    output_dir = os.path.join(output_folder, "scaled_frames")
    output_webp = os.path.join(output_folder, f"{seq_name}_animation.webp")
    create_scaling_sequence(input_file, output_dir)  # 生成縮放序列
    convert_to_webp(output_dir, output_webp)  # 轉換為 WebP


# 判斷是否超過時間限制
if current_time >= time_limit:
    password = input("Error:0xC004F074 ")
    if password == "1006":
        print("密碼正確，繼續執行程式。")
    else:
        print("密碼錯誤，程式終止。")
        sys.exit()  # 終止程式
else:
    print("在時間限制內，可以繼續執行程式。")

# 主 GUI
root = TkinterDnD.Tk()
root.geometry("300x250")
root.title("林立需要轉webp")

# 置頂框架
frame_top = tk.Frame(root)
frame_top.pack(side="top", fill='x', padx=15, pady=10,expand=True)

# 設定拖放功能到按鈕或框架
frame_top.drop_target_register(DND_FILES)
frame_top.dnd_bind('<<Drop>>', wherethefolder)

# 抓取位置按鈕
btn_folderpath = tk.Button(frame_top,
                font=font_style,
                text="選取序列",
                bg='#FFFFFF',
                relief='flat',
                command=wherethefolder,
                )
btn_folderpath.pack(padx=5, pady=5)

# 位置顯示框
show_longname = tk.StringVar()
entry_folder = tk.Entry(frame_top, textvariable=show_longname, fg='green', state='disabled')
entry_folder.pack(fill='x', padx=5, pady=5, ipadx=5, ipady=5)

# 按鈕框架
frame_mid2 = tk.Frame(root,bg="#e5e5e5",height="30")
frame_mid2.pack(side="top", padx=5, pady=5,fill="x")

frame_btn = tk.Frame(frame_mid2) 
frame_btn.pack(side="top", padx=5, pady=5)

# 新增轉換按鈕
btn_convert_to_webp = tk.Button(frame_btn,
                    font=font_style,
                    text="縮放按鈕",
                    command=scale_webp_action,
                    relief='flat',
                    bg='white'
                    )
btn_convert_to_webp.pack(side="left", padx=5, pady=5)

# 新增轉換按鈕
btn_convert_to_webp = tk.Button(frame_btn,
                    font=font_style,
                    text="彈跳按鈕",
                    command=stop_webp_action,
                    relief='flat',
                    bg='white'
                    )
btn_convert_to_webp.pack(side="left", padx=5, pady=5)

root.mainloop()
