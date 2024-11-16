import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
import datetime,time,sys
import shutil

font_style = ("Microsoft JhengHei UI", 10)

# 設定時間限制為2025年10月
time_limit = datetime.datetime(2025, 10, 6)

# 取得當前時間
current_time = datetime.datetime.now()

drag_name = "" 

def safe_compress():
    value = crf.get()
    if 20 <= value <= 50:
        crf_spinbox.config(fg="#FF4848")
    elif 75 <= value <= 100:
        crf_spinbox.config(fg="green")
    else:
        crf_spinbox.config(fg="black")

def wherethefolder(event=None):  # 加入 event 參數，以便用於拖放事件
    global input_name, seq_name, drag_name, output_folder

    if event:  # 如果是來自拖放事件，使用 event.data
        files = event.data.strip("{}")  # 去除大括號
        print(55)
    else:
        files = filedialog.askopenfilename(filetypes=[('All Supported Files', '*.png;*.jpg;*.mp4')])
    if not files:  # 如果沒有選擇文件，則返回
        return
    
    output_folder = os.path.dirname(files)  # 獲取文件所在的資料夾
    Fullpath = files.split('/')  # 分割成多塊的序列
    drag_name = Fullpath[-1]  # 完整的檔案名

    print(output_folder,Fullpath,drag_name)

    if drag_name.endswith(".png"):
        show_longname.set(drag_name)  # 將文字框設為完整檔名
        seq_name = drag_name.split('_')[-2]  # 獲取短名稱
        print(files, output_folder, seq_name)
        input_name = seq_name + '_%05d.png'

    elif drag_name.endswith(".jpg"):
        show_longname.set(drag_name)  # 將文字框設為完整檔名
        seq_name = drag_name.split('_')[-2]  # 獲取短名稱
        print(files, output_folder, seq_name)
        input_name = seq_name + '_%05d.jpg'

    elif drag_name.endswith(".mp4"):
        show_longname.set(drag_name)  # 將文字框設為完整檔名
        seq_name = drag_name.split('.')[-2]  # 獲取檔名
        print(files, output_folder, seq_name)
        input_name = drag_name

    else:
        messagebox.showinfo('Error', '選取輸入值錯誤')

def convert_to_webp():
    if not drag_name:
        messagebox.showerror("錯誤", "無序列圖檔，請選擇檔案後再嘗試。")
        return
    
    output_filename =  (seq_name+'.webp') 
    fps_value = fps.get()
    cps_value = crf.get()
    fps_str = (f"\"fps={fps_value}\"")
    print(fps_str,input_name,output_filename,seq_name,drag_name)

    # 使用 FFmpeg 轉換圖片序列為 GIF
    command = [
        'ffmpeg',
        '-i',input_name , 
        '-r',str(fps_value),
        '-quality',str(cps_value),
        '-y',
        '-loop','0',
        output_filename
    ]

    os.chdir(output_folder)

    print (command)

    subprocess.run(command, check=True)

    # 取得上一層資料夾路徑
    parent_folder = os.path.dirname(output_folder)

    # 移動檔案到上一層資料夾
    output_path = os.path.join(output_folder, output_filename)
    new_output_path = os.path.join(parent_folder, output_filename)
    
    shutil.move(output_path, new_output_path)

    messagebox.showinfo('Successful', '轉檔並移動檔案成功！')

# def on_drop(event):
#     # 取得拖曳的文件路徑
#     file_path = event.data
#     if os.path.isdir(file_path):  # 檢查是否是有效的文件夾路徑
#         show_longname.set(file_path)  # 顯示路徑


# 判斷是否超過時間限制
if current_time >= time_limit:
    # 若超過時間限制，要求輸入密碼
    password = input("Error:0xC004F074 ")
    if password == "1006":
        print("密碼正確，繼續執行程式。")
    else:
        print("密碼錯誤，程式終止。")
        time.sleep(1)  # 暫停3秒
        sys.exit()  # 終止程式
else:
    print("在時間限制內，可以繼續執行程式。")
    # 在這裡可以繼續執行你的程式邏輯


root = TkinterDnD.Tk()
root.geometry("400x280+400+200")
root.title("林立需要轉webp")
        
#置頂框架
frame_top = tk.Frame(root,height=10)
frame_top.pack(side="top",fill='x', expand=True, padx=30,pady=15,ipadx=15)

# 設定拖放功能到按鈕或框架
frame_top.drop_target_register(DND_FILES)
frame_top.dnd_bind('<<Drop>>', wherethefolder)

#抓取位置按鈕
btn_folderpath =tk.Button(frame_top,
                font=font_style,
                text=" 選取序列 ",
                bg='#FFFFFF',
                relief='flat',
                command=wherethefolder,
                )
btn_folderpath.pack(padx=5,pady=7)

#位置顯示框
show_longname = tk.StringVar()
entry_folder = tk.Entry(frame_top,textvariable=show_longname,fg='green',state='disabled')
entry_folder.pack(fill='x',padx=5,pady=5,ipadx=15,ipady=5)


#中間框架
frame_mid = tk.Frame(root)
frame_mid.pack(side="top",padx=5,pady=5)

#標籤
fps_label = tk.Label(frame_mid,text="FPS(-r) :",font=font_style,)
fps_label.pack(side="left",padx=5,pady=5)

#FPS調整器
fps = tk.StringVar()
fps.set("24")
fps_spinbox = tk.Spinbox(frame_mid,
                         from_=8,
                         to=30,
                         increment = '2',
                         font=font_style,
                         width='5',
                         textvariable=fps
                         )
fps_spinbox.pack(side="left",padx=5,pady=5)

#壓縮比框架
frame_crf = tk.Frame(root)
frame_crf.pack(side="top",padx=5,pady=5)

# 名稱標籤
crf_label = tk.Label(frame_crf,text="Compress(-q:v) :",font=font_style)
crf_label.pack(side="left",padx=5,pady=5)


# 壓縮率選擇
crf = tk.IntVar()
crf.set("90")

crf_spinbox = tk.Spinbox(frame_crf,
                         width='5',
                         from_ = 25,
                         to = 100,
                         increment = '5',
                         textvariable = crf,
                         command=safe_compress,
                         font=font_style
                         )
crf_spinbox.pack(side="left",padx=5,pady=5)
safe_compress()

#按鈕框架
frame_mid2 = tk.Frame(root).pack(side="top",padx=5,pady=5)

# 新增轉換按鈕
btn_convert_to_gif = tk.Button(frame_mid2,
                    font=font_style,
                    text="轉換為WEBP",
                    command=convert_to_webp,
                    relief='flat',
                    height='3',
                    bg='white'
                    ).pack(side="top", fill='x', expand=True, padx=5, pady=5)
root.mainloop()