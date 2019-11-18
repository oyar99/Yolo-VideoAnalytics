from tkinter import ttk
import tkinter as tk
import videocap
import PIL.Image as Image
import PIL.ImageTk as ImageTk

title = 'SISTEMA DE VIGILANCIA INTELIGENTE'
screen_size = '620x500'
background_color = '#f2f0f0'

#Crea la ventana principal
window = tk.Tk()
window.title(title)
window.config(background=background_color)
window.geometry(screen_size)

#Crea un controlador de pestanas
tab_control = ttk.Notebook(window)
tab_main = tk.Frame(tab_control)
tab_log = tk.Frame(tab_control)
tab_control.add(tab_main, text = 'Video')
tab_control.add(tab_log, text = 'Log de resultados')
tab_control.pack(expand = 1, fill = 'both')


#Configura la pestana del video
imageFrame = tk.Frame(tab_main, width=600, height=480)
imageFrame.grid(row=0, column=0, padx=10, pady=2)
video = tk.Label(imageFrame)
video.grid(row=0, column=0)

#Crea un objecto para capturar frames
video_capture = videocap.VideoCapture(0)
def get_frame():
    frame = video_capture.read()
    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image = img)
    video.imgtk = imgtk
    video.configure(image = imgtk)
    video.after(15, get_frame)

get_frame()
window.mainloop()