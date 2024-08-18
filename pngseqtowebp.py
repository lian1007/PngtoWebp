import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

font_style = ("Microsoft JhengHei UI", 10)

def safe_compress():
    value = crf.get()
    if 20 <= value <= 50:
        crf_spinbox.config(fg="#FF4848")
    elif 75 <= value <= 100:
        crf_spinbox.config(fg="green")
    else:
        crf_spinbox.config(fg="black")

def used_color():
    if "_" in entry_folder.get():
        print('66')
    

def wherethefolder(): #抓取路徑位置

    global input_name,seq_name,long_name,output_folder
    files = filedialog.askopenfilename(filetypes=[('All Supported Files', '*.png;*.jpg;*.mp4')])
    output_folder = os.path.dirname(files)
    Fullpath = files.split('/')  #分割成多塊的序列
    long_name = Fullpath[-1] #完整名字

    if files.endswith(".png"):
        show_longname.set(long_name) #將文字方框設為完整名字
        seq_name = (long_name.split('_')[-2]) #將完整名字拆分為只有短名
        print (files,output_folder,seq_name)
        input_name = (seq_name + '_%05d.png')

    elif files.endswith(".jpg"):
        show_longname.set(long_name) #將文字方框設為完整名字
        seq_name = (long_name.split('_')[-2]) #將完整名字拆分為只有短名
        print (files,output_folder,seq_name)
        input_name = (seq_name + '_%05d.jpg')

    elif files.endswith(".mp4"):
        show_longname.set(long_name) #將文字方框設為完整名字
        seq_name = (long_name.split('.')[-2])
        print (files,output_folder,seq_name)
        input_name = long_name

    else:
        # 如果字符串中不包含特定的字，执行相关操作
        messagebox.showinfo('Error','圖片序列錯誤')

    
def convert_to_gif():
    
    output_filename =  (seq_name+'.webp') 
    fps_value = fps.get()
    cps_value = crf.get()
    fps_str = (f"\"fps={fps_value}\"")
    print(fps_str,input_name,output_filename,seq_name,long_name)

    # 使用 FFmpeg 轉換圖片序列為 GIF
    command = [
        'ffmpeg',
        '-i',input_name , 
        '-r',str(fps_value),
        '-q:v',str(cps_value),
        '-y',
        '-loop','0',
        output_filename
    ]

    os.chdir(output_folder)

    print (command)

    subprocess.run(command, check=True)

    os.startfile(output_folder)

    subprocess.Popen(['open', output_folder])

    messagebox.showinfo('Successful','轉檔成功!')

   
    
root = tk.Tk()
root.geometry("400x280")
root.title("林立很需要轉檔WEBP")

output_folder = tk.StringVar()

#置頂框架
frame_top = tk.Frame(root)
frame_top.pack(side="top",fill='x',padx=15,pady=10)

#抓取位置按鈕
btn_folderpath =tk.Button(frame_top,
                font=font_style,
                text="選取序列",
                bg='#FFFFFF',
                relief='flat',
                command=wherethefolder,
                )
btn_folderpath.pack(padx=5,pady=5)

#位置顯示框
show_longname = tk.StringVar()
entry_folder = tk.Entry(frame_top,textvariable=show_longname,fg='green',state='disabled')
entry_folder.pack(fill='x',padx=5,pady=5,ipadx=5,ipady=5)
used_color()

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

# 新增轉換為GIF的按鈕
btn_convert_to_gif = tk.Button(frame_mid2,
                    font=font_style,
                    text="轉換為WEBP",
                    command=convert_to_gif,
                    relief='flat',
                    bg='white'
                    ).pack(side="top", padx=5, pady=5)
root.mainloop()