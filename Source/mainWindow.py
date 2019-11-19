from tkinter import ttk
import tkinter as tk
import videocap
import FrameAnalyzer
import cv2
import PIL.Image as Image
import PIL.ImageTk as ImageTk

'''Variables'''

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
#Valores fijos de la interfaz
video_width = 600
video_height = 480
vide_x_pad = 10
video_y_pad = 2
update_frame_rate = 10
#Datos de la red neuronal
algorithm_path = 'yolo\\yolov2-tiny.cfg'
trained_model_path = 'yolo\\yolov2-tiny.weights'
classes = ['person']
confidence_limit = 0.75


'''Entry point'''


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
tab_control.pack(expand = 1, fill = tk.BOTH)


#Configura la pestana del video
imageFrame = tk.Frame(tab_main, width=video_width, height=video_height)
imageFrame.grid(row=0, column=0, padx=vide_x_pad, pady=video_y_pad)
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

def get_frame():
    frame = video_capture.read()
    global frame_analyzer
    frame_analyzer.set_video_source(frame)
    if not frame_analyzer.isAlive():
        if frame_analyzer.con > confidence_limit:
            text.insert(tk.END, log % frame_analyzer.con)
        text.see(tk.END)
        frame_analyzer = FrameAnalyzer.FrameAnalyzer(algorithm_path, trained_model_path, classes, confidence_limit)
        frame_analyzer.set_video_source(frame)
        frame_analyzer.start()
      
    frame = frame_analyzer.draw_detection(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image = img)
    video.imgtk = imgtk
    video.configure(image = imgtk)
    video.after(update_frame_rate, get_frame)

get_frame()
window.mainloop()