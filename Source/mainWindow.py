#External modules
from tkinter import ttk
import tkinter as tk
import cv2
import PIL.Image as Image
import PIL.ImageTk as ImageTk

#custom modules
from constants import *
import videocap
import FrameAnalyzer


'''Entry point'''


#Creates the root component of the GUI
window = tk.Tk()
window.title(title)
window.iconbitmap(icon_path)
window.resizable(False, False)
window.config(background=background_color)
window.geometry(screen_size)

#Creates a tab controller
tab_control = ttk.Notebook(window)
tab_main = tk.Frame(tab_control)
tab_log = tk.Frame(tab_control)
tab_log.config(background=terminal_color)
tab_control.add(tab_main, text = text_tab_main)
tab_control.add(tab_log, text = text_tab_log)
tab_control.pack(expand = 1, fill = tk.BOTH)


#Configures the video tab 
imageFrame = tk.Frame(tab_main, width=video_width, height=video_height)
imageFrame.grid(row=0, column=0, padx=vide_x_pad, pady=video_y_pad)
video = tk.Label(imageFrame)
video.grid(row=0, column=0)

#Creates an object to handle video capture
video_capture = videocap.VideoCapture(default_camera)
frame_analyzer = FrameAnalyzer.FrameAnalyzer(algorithm_path, trained_model_path, classes, confidence_limit)

#Button action
stop = False
def clicked():
    global button_text
    global stop
    stop =  not stop
    if stop:
        button_text = RESUME
    else:
        button_text = STOP


#Configures the log tab
button_stop = tk.Button(tab_log, text=button_text, command=clicked)
button_stop.pack()
scroll = tk.Scrollbar(tab_log)
scroll.pack(side=tk.RIGHT, fill=tk.Y)
text = tk.Text(tab_log, wrap=tk.NONE, yscrollcommand=scroll.set)
text.config(bg=terminal_color, fg=background_color)
text.pack(side=tk.LEFT)
scroll.config(command=text.yview)



#Gets the camera frame periodically
def get_frame():
    '''Global variables'''
    global button_text
    global button_stop
    global frame_analyzer

    frame = video_capture.read()
    if frame is None:
        return None
    frame_analyzer.set_video_source(frame)
    if not stop:
        text.insert(tk.END, frame_text_begin)
        if not frame_analyzer.isAlive():
            if frame_analyzer.con > confidence_limit:
                contents = text.get(BEGIN, tk.END)
                if contents is not None:
                    if len(contents) > max_text_size:
                        text.delete(BEGIN, tk.END)
                text.insert(tk.END, log % frame_analyzer.con)
            text.see(tk.END)
            frame_analyzer = FrameAnalyzer.FrameAnalyzer(algorithm_path, trained_model_path, classes, confidence_limit)
            frame_analyzer.set_video_source(frame)
            frame_analyzer.start()
        text.insert(tk.END, Frame_text_end)

    button_stop[TEXT] = button_text
    frame = frame_analyzer.draw_detection(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image = img)
    video.imgtk = imgtk
    video.configure(image = imgtk)
    video.after(update_frame_rate, get_frame)

#Main Loop
get_frame()
window.mainloop()