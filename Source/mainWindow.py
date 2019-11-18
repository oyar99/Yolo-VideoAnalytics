from tkinter import ttk
import tkinter as tk
import videocap
import FrameAnalyzer
import cv2
import PIL.Image as Image
import PIL.ImageTk as ImageTk

#String usadas en la interfaz
title = 'SISTEMA DE VIGILANCIA INTELIGENTE'
screen_size = '620x500'
background_color = '#f2f0f0'
icon_path = 'Assets\\logo.ico'
text_tab_main = 'Video'
text_tab_log = 'Log de resultados'

#Datos de la red neuronal
algorithm_path = 'yolo\\yolov3.cfg'
trained_model_path = 'yolo\\yolov3.weights'
classes = ['person']
confidence_limit = 0.9

#Crea la ventana principal
window = tk.Tk()
window.title(title)
window.iconbitmap(icon_path)
window.resizable(False, False)
window.config(background=background_color)
window.geometry(screen_size)

#Crea un controlador de pestanas
tab_control = ttk.Notebook(window)
tab_main = tk.Frame(tab_control)
tab_log = tk.Frame(tab_control)
tab_control.add(tab_main, text = text_tab_main)
tab_control.add(tab_log, text = text_tab_log)
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
    frame_analyzer = FrameAnalyzer.FrameAnalyzer(algorithm_path, trained_model_path, classes, confidence_limit)
    frame_analyzer.set_video_source(frame)
    if not frame_analyzer.is_running():
        frame = frame_analyzer.run()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image = img)
    video.imgtk = imgtk
    video.configure(image = imgtk)
    video.after(10, get_frame)

get_frame()
window.mainloop()