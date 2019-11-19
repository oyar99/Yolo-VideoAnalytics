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

'''Variables'''
button_text = STOP
stop = False

'''Entry point'''


#Creates the root component of the GUI
window = tk.Tk()
window.title(TITLE)
window.iconbitmap(ICON_PATH)
window.resizable(False, False)
window.config(background=BACKGROUND_COLOR)
window.geometry(SCREEN_SIZE)

#Creates a tab controller
tab_control = ttk.Notebook(window)
tab_main = tk.Frame(tab_control)
tab_log = tk.Frame(tab_control)
tab_log.config(background=TERMINAL_COLOR)
tab_control.add(tab_main, text = TEXT_TAB_MAIN)
tab_control.add(tab_log, text = TEXT_TAB_LOG)
tab_control.pack(expand = 1, fill = tk.BOTH)


#Configures the video tab 
imageFrame = tk.Frame(tab_main, width=VIDEO_WIDTH, height=VIDEO_HEIGHT)
imageFrame.grid(row=0, column=0, padx=VIDEO_X_PAD, pady=VIDEO_Y_PAD)
video = tk.Label(imageFrame)
video.grid(row=0, column=0)

#Creates an object to handle video capture
video_capture = videocap.VideoCapture(DEFAULT_CAMERA)
frame_analyzer = FrameAnalyzer.FrameAnalyzer(ALGORITHM_PATH, TRAINED_MODEL_PATH, CLASSES, CONFIDENCE_LIMIT)

#Button action
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
text.config(bg=TERMINAL_COLOR, fg=BACKGROUND_COLOR)
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
        text.insert(tk.END, FRAME_TEXT_BEGIN)
        if not frame_analyzer.isAlive():
            if frame_analyzer.con > CONFIDENCE_LIMIT:
                contents = text.get(BEGIN, tk.END)
                if contents is not None:
                    if len(contents) > MAX_TEXT_SIZE:
                        text.delete(BEGIN, tk.END)
                text.insert(tk.END, LOG % frame_analyzer.con)
            text.see(tk.END)
            frame_analyzer = FrameAnalyzer.FrameAnalyzer(ALGORITHM_PATH, TRAINED_MODEL_PATH, CLASSES, CONFIDENCE_LIMIT)
            frame_analyzer.set_video_source(frame)
            frame_analyzer.start()
        text.insert(tk.END, FRAME_TEXT_END)
    button_stop[TEXT] = button_text
    frame = frame_analyzer.draw_detection(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image = img)
    video.imgtk = imgtk
    video.configure(image = imgtk)
    video.after(UPDATE_FRAME_RATE, get_frame)

#Main Loop
get_frame()
window.mainloop()