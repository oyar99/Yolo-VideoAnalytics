#CONSTANTS
#String used for GUI
title = 'SISTEMA DE VIGILANCIA INTELIGENTE'
screen_size = '620x500'
background_color = '#f2f0f0'
terminal_color = '#000000'
icon_path = 'Assets\\logo.ico'
text_tab_main = 'Video'
text_tab_log = 'Log de resultados'
log = 'Se ha detectado una persona con un nivel de confianza de: %s\n' 
frame_text_begin = 'INICIO_FRAME\n'
Frame_text_end = 'FINAL_FRAME\n'
BEGIN = '1.0'
TEXT = 'text'
STOP = 'Detener'
RESUME = 'Resumir'
button_text = STOP
#Other values used for GUI
video_width = 600
video_height = 480
vide_x_pad = 10
video_y_pad = 2
update_frame_rate = 10
max_text_size = 100000
#Neural network data
algorithm_path = 'yolo\\yolov2-tiny.cfg'
trained_model_path = 'yolo\\yolov2-tiny.weights'
classes = ['person']
confidence_limit = 0.75
#Video Capture
default_camera = 0
#Colors RGB
blue_color_bgr = (180, 75, 25)