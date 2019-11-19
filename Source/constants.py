#CONSTANTS
#String used for GUI
TITLE = 'SISTEMA DE VIGILANCIA INTELIGENTE'
SCREEN_SIZE = '620x500'
BACKGROUND_COLOR = '#f2f0f0'
TERMINAL_COLOR = '#000000'
ICON_PATH = 'Assets\\logo.ico'
TEXT_TAB_MAIN= 'Video'
TEXT_TAB_LOG = 'Log de resultados'
LOG = 'Se ha detectado una persona con un nivel de confianza de: %s\n' 
FRAME_TEXT_BEGIN = 'INICIO_FRAME\n'
FRAME_TEXT_END = 'FINAL_FRAME\n'
BEGIN = '1.0'
TEXT = 'text'
STOP = 'Detener'
RESUME = 'Resumir'
#Other values used for GUI
VIDEO_WIDTH = 600
VIDEO_HEIGHT = 480
VIDEO_X_PAD = 10
VIDEO_Y_PAD = 2
UPDATE_FRAME_RATE = 10
MAX_TEXT_SIZE = 100000
#Neural network data
ALGORITHM_PATH = 'yolo\\yolov2-tiny.cfg'
TRAINED_MODEL_PATH = 'yolo\\yolov2-tiny.weights'
CLASSES = ['person']
CONFIDENCE_LIMIT = 0.75
#Video Capture
DEFAULT_CAMERA = 0
#Colors RGB
BLUE_COLOR_BGR = (180, 75, 25)