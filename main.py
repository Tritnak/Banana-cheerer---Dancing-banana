import tkinter as tk
from tkinter import Canvas
import ctypes # Hacer click detras del lienzo

class Banana:
    def __init__(self, scene, x=0, y=0):
        self.scene = scene
        # Intentar cargar más frames por si hay más de 3 disponibles
        self.frames = []
        try:
            i = 0
            while True:
                frame = tk.PhotoImage(file='banana-cheerer.gif', format=f'gif -index {i}')
                self.frames.append(frame)
                i += 1
        except tk.TclError:
            pass  # Se detiene cuando no puede cargar más frames
        
        self.frame_index = 0
        self.frames = [frame.subsample(3) for frame in self.frames]  # Cambia el tamaño del plátano
        self.imageRef = scene.canvas.create_image(x, y, image=self.frames[0])
        self.animate()

    def animate(self):
        # Cambiar el frame actual
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.scene.canvas.itemconfig(self.imageRef, image=self.frames[self.frame_index])
        # Volver a llamar este método después de 100 ms para crear el efecto de animación
        self.scene.canvas.after(100, self.animate)

class Scene:
    def __init__(self, window: tk):
        self.screen_width = window.winfo_screenwidth()
        self.screen_height = window.winfo_screenheight()
        self.canvas = Canvas(
            window, 
            width=self.screen_width,
            height=self.screen_height, 
            highlightthickness=0,  
            bg='green'
        )
        self.canvas.pack()
        self.bananas = list()
    
    def new_banana(self, x, y):
        banana = Banana(self, x, y)
        self.bananas.append(banana)

class Game:
    def __init__(self):
        self.window = self.create_window()
        self.apply_click_through(self.window)
        self.scene = Scene(self.window)
    
    def create_window(self):
        window = tk.Tk()
        window.wm_attributes("-topmost", True)
        window.attributes("-fullscreen", True)
        window.overrideredirect(True)
        # Trasparencia
        window.attributes('-transparentcolor', 'green')
        window.config(bg='green')
        return window
    
    def apply_click_through(self, window):
        # Constantes API windows
        WS_EX_TRANSPARENT = 0x00000020
        WS_EX_LAYERED = 0x00080000
        GWL_EXSTYLE = -20
        
        # Obtener el identificador de ventana (HWND)
        hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
        # Obtener los estilos actuales de la ventana
        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        # Establecer nuevo estilo
        style = style | WS_EX_TRANSPARENT | WS_EX_LAYERED
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
        
    def start(self):
        self.window.mainloop()

game = Game()
game.scene.new_banana(100, 100)
game.start()
