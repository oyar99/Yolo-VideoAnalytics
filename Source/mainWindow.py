from tkinter import ttk
import tkinter as tk
import videocap
import FrameAnalyzer
import cv2
import time
import PIL.Image as Image
import PIL.ImageTk as ImageTk

#CONSTANTES
#String usadas en la interfaz
title = 'SISTEMA DE VIGILANCIA INTELIGENTE'
screen_size = '620x500'
background_color = '#f2f0f0'
terminal_color = '#000000'
icon_path = 'Assets\\logo.ico'
text_tab_main = 'Video'
text_tab_log = 'Log de resultados'
log = 'Se ha detectado una persona con un nivel de confianza de: %s\n' 

#Datos de la red neuronal
algorithm_path = 'yolo\\yolov2-tiny.cfg'
trained_model_path = 'yolo\\yolov2-tiny.weights'
classes = ['person']
confidence_limit = 0.75

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
tab_log.config(background=terminal_color)
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
frame_analyzer = FrameAnalyzer.FrameAnalyzer(algorithm_path, trained_model_path, classes, confidence_limit)

#Configura la pestana del log de resultados
scroll = tk.Scrollbar(tab_log)
scroll.pack(side=tk.RIGHT, fill=tk.Y)
text = tk.Text(tab_log, wrap=tk.NONE, yscrollcommand=scroll.set)
text.config(bg=terminal_color, fg=background_color)
text.pack(side=tk.LEFT)

scroll.config(command=text.yview)

#benchmarking
start_time = time.time()

def get_frame():
    frame = video_capture.read()
    global frame_analyzer
    frame_analyzer.set_video_source(frame)
    if not frame_analyzer.isAlive():
        global start_time
        print("Time: " + str(time.time() - start_time))
        #text.insert(tk.END, "Time: %s\n" % str(time.time() - start_time))
        if frame_analyzer.con > confidence_limit:
            text.insert(tk.END, log % frame_analyzer.con)
        text.see(tk.END)
        frame_analyzer = FrameAnalyzer.FrameAnalyzer(algorithm_path, trained_model_path, classes, confidence_limit)
        frame_analyzer.set_video_source(frame)
        frame_analyzer.start()
        start_time = time.time()
      
    frame = frame_analyzer.draw_detection(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image = img)
    video.imgtk = imgtk
    video.configure(image = imgtk)
    video.after(10, get_frame)

get_frame()
window.mainloop()