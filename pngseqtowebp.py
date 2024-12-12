import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
import datetime, time, sys
import shutil

font_style = ("Microsoft JhengHei UI", 10)
time_limit = datetime.datetime(2025, 10, 6)
current_time = datetime.datetime.now()

drag_name = ""  # 初始化為空字串

def safe_compress():
    value = crf.get()
    if 20 <= value <= 50:
        crf_spinbox.config(fg="#FF4848")
    elif 75 <= value <= 100:
        crf_spinbox.config(fg="green")
    else:
        crf_spinbox.config(fg="black")

    
def wherethefolder(event=None):
    global input_name, seq_name, drag_name, output_folder
    if event:
        files = event.data.strip("{}")  # 去除大括號
    else:
        files = filedialog.askopenfilename(filetypes=[('All Supported Files', '*.png;*.jpg;*.mp4')])
    if not files:
        return
    
    output_folder = os.path.dirname(files)
    Fullpath = files.split('/')
    drag_name = Fullpath[-1]

    show_longname.set(drag_name)
    if drag_name.endswith(".png") or drag_name.endswith(".jpg"):
        if "_" not in drag_name:
            # 如果沒有底線，顯示錯誤訊息並清空顯示欄位
            messagebox.showerror("錯誤", "檔案名稱中沒有底線，請重新選擇檔案。")
            show_longname.set("")  # 清空 entry_folder 顯示的檔案名稱
            return  # 結束函數，不執行後續代碼
        else:  
            seq_name = drag_name.split('_')[-2]
            input_name = f"{seq_name}_%05d.{drag_name.split('.')[-1]}"

    elif drag_name.endswith(".mp4"):
        seq_name = drag_name.split('.')[-2]
        input_name = drag_name
    else:
        messagebox.showinfo('Error', '選取輸入值出現錯誤')

def convert_to_webp():

    if not drag_name:
        messagebox.showerror("錯誤", "無序列圖檔，請選擇檔案後再嘗試。")
        return
    
    output_filename = f"{seq_name}.webp"
    fps_value = fps.get()
    cps_value = crf.get()
    fps_str = f"fps={fps_value}"

    command = [
        'ffmpeg',
        '-i', input_name, 
        '-r', str(fps_value),
        '-quality', str(cps_value),
        '-y',
        '-loop', '0',
        output_filename
    ]

    os.chdir(output_folder)
    subprocess.run(command, check=True)
    parent_folder = os.path.dirname(output_folder)
    output_path = os.path.join(output_folder, output_filename)
    new_output_path = os.path.join(parent_folder, output_filename)
    
    shutil.move(output_path, new_output_path)
    messagebox.showinfo('Successful', '轉檔並移動檔案成功！')

if current_time >= time_limit:
    password = input("Error:0xC004F074 ")
    if password == "1006":
        print("密碼正確，繼續執行程式。")
    else:
        print("密碼錯誤，程式終止。")
        sys.exit()
else:
    print("在時間限制內，可以繼續執行程式。")

root = TkinterDnD.Tk()
root.geometry("380x280+400+200")
root.title("林立需要轉webp")
        
frame_top = tk.Frame(root)
frame_top.pack(side="top",fill="x", expand=True, padx=15, pady=10)
frame_top.drop_target_register(DND_FILES)
frame_top.dnd_bind('<<Drop>>', wherethefolder)

btn_folderpath = tk.Button(
    frame_top, font=font_style, text="選取序列", bg='#FFFFFF', relief='flat', command=wherethefolder)
btn_folderpath.pack(padx=5, pady=5)

show_longname = tk.StringVar()
entry_folder = tk.Entry(frame_top, textvariable=show_longname, fg='green', state='disabled')
entry_folder.pack(fill='x', padx=10, pady=5, ipadx=5, ipady=5)

frame_mid = tk.Frame(root)
frame_mid.pack(side="top", padx=5, pady=5)

fps_label = tk.Label(frame_mid, text="FPS(-r) :", font=font_style)
fps_label.pack(side="left", padx=5, pady=5)

fps = tk.StringVar(value="24")
fps_spinbox = tk.Spinbox(frame_mid, from_=8, to=30, increment=2, font=font_style, width=5, textvariable=fps)
fps_spinbox.pack(side="left", padx=5, pady=5)

frame_crf = tk.Frame(root)
frame_crf.pack(side="top", padx=5, pady=5)

crf_label = tk.Label(frame_crf, text="Compress(-q:v) :", font=font_style)
crf_label.pack(side="left", padx=5, pady=5)

crf = tk.IntVar(value=90)
crf_spinbox = tk.Spinbox(frame_crf, from_=25, to=100, increment=5, textvariable=crf, command=safe_compress, font=font_style, width=5)
crf_spinbox.pack(side="left", padx=5, pady=5)
safe_compress()

frame_mid2 = tk.Frame(root)
frame_mid2.pack(side="top",fill="x", expand=True, padx=15, pady=15)

btn_convert_to_webp = tk.Button(
    frame_mid2, font=font_style, text="轉換為WEBP", command=convert_to_webp, relief='flat', bg='white',height=3
)
btn_convert_to_webp.pack(side="top", fill="both", expand=True, padx=5, pady=5)

root.mainloop()
