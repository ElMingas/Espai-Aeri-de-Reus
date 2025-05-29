from graph import *
from airspace import *

from ctypes import windll
from functools import partial
from PIL import Image, ImageTk
from tkinter import filedialog
import tkinter as tk
import pygame
import pyautogui

'''El programa principal'''
def create_interactive_interface(graph, root, nodes_file):
    # Configuración HiDPI (Windows)
    config_root_window(root)  # Config de la ventana principal
    control_frame, graph_frame = setup_ui(root) #Setup ui

    visualizer = InteractiveGraph(graph_frame, graph, 'full', nodes_file)
    setup_control (control_frame, visualizer, root)   #Setup controles
def config_root_window(a1):
    """Configura la ventana principal"""
    a1.title("Visualización de grafo")
    resolution = a1.maxsize()
    width, height = resolution
    a1.geometry(f"{int(width)}x{int(height)}")
def setup_ui(root):
    """Crea y configura los frames principales de la interfaz"""
    # Frame para controles
    control_frame = tk.Frame(root, padx=10, pady=10)
    control_frame.pack(side="top", fill="x")

    # Frame para el gráfico
    graph_frame = tk.Frame(root, bg='white')
    graph_frame.pack(side="top", fill="both", expand=True)

    return control_frame, graph_frame
def setup_control (frame, v, root):
    pyglet.font.add_file("Minecraft.ttf")
    font_name = "Minecraft"

    tk.Button(frame, text = 'Back', font=font_name, command=lambda: return_to_main(root)).pack(side="left")

    modos = [
        ("Main Graph", 'full'),
        ("Neighbors only", 'solonodo'),
        ("Paths from a node", 'paths')
    ]
    # Todos los botones en el frame del grafo
    for text, modo in modos:
        tk.Button(
            frame,
            text=text,
            command=partial(change_mode, modo, v),
            width=15,
            height=2,
            bg='#4CAF50',
            fg='white',
            font=(font_name, 12)
        ).pack(side="left", padx=5)

    # Slider para el volumen de musica
    volume_slider = ttk.Scale(frame, from_=0, to=100, orient='horizontal',
                             command=set_volume)
    volume_slider.set(35)  # Volumen inicial
    volume_slider.pack(side="right", padx=3)
    lbl_volumen = tk.Label(frame, text="🔈", font=('arial', 17))
    lbl_volumen.pack(side="right", anchor='center')

    # Mostrar la ventana para indicar los controles
    tk.Button(
        frame,
        text='💡',
        bg = '#FFEF00',
        command=lambda: how_to_controls(v),
        font=('Arial', 12)
    ).pack(side="right", padx=5)
    tk.Button(
        frame,
        text='F. extras',
        bg='#FFEF00',
        command=f_extras,
        font=('Arial', 12)
    ).pack(side="right", padx=5)
def setup_audio():
    pygame.mixer.init()
    try:
        pygame.mixer.music.load("C418 - Wet Hands - Minecraft Volume Alpha [mukiMaOSLEs].mp3")
        pygame.mixer.music.set_volume(0.35)
        pygame.mixer.music.play(loops=-1)
    except pygame.error as e:
        print(f"Error al cargar/reproducir audio: {e}")
def set_volume(value):
    """Ajustar volumen según el slider (0-100)"""
    pygame.mixer.music.set_volume(float(value) / 100)
def change_mode(new_mode, v):
    v.mode = new_mode
    v.update_display()
def creategraph(selec):
    AddNavPoint(selec)
    AddNavSegment(selec)

    g_data = Airspace(NavPoint_lict, NavSegment_list, Airport_list)

    return g_data
def on_close(a1):
    pygame.mixer.music.fadeout(500)
    a1.after(510, a1.destroy)


'''Menu principal'''
def return_to_main(root):
    pygame.mixer.music.fadeout(500)
    for widget in root.winfo_children():
        widget.destroy()

    # Volver a crear el menú principal
    create_main_menu(root)
def create_main_menu(root):
    pyglet.font.add_file("Minecraft.ttf")
    font_name = "Minecraft"

    """Crea el menú principal en la ventana existente"""
    frame = tk.Frame(root)
    frame.pack(expand=True, fill='both')

    # Configurar imagen de fondo
    resolution = root.maxsize()
    width, height = resolution
    image = Image.open("MC_avion.png")
    image = image.resize((width, height), Image.LANCZOS)
    bg_image = ImageTk.PhotoImage(image)

    background_label = tk.Label(frame, image=bg_image, compound="center")
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    background_label.image = bg_image  # Mantener referencia
    background_label.lower()

    tk.Button(frame, command=lambda: start_program(root, 'ECAC'),
              text='Europe',width=25,font=(font_name, 16, "bold"),bg="#E0E0E0",fg="#212121"
            ).pack(pady=(int(height/2), 5))
    tk.Button(frame, command=lambda: start_program(root, 'Spain'),
              text='Spain',width=25,font=(font_name, 16, "bold"),bg="#E0E0E0",fg="#212121"
            ).pack(pady=5)
    tk.Button(frame, command=lambda: start_program(root, 'Catalonia'),
              text='Catalonia',width=25,font=(font_name, 16, "bold"),bg="#E0E0E0",fg="#212121"
              ).pack(pady=5)
    tk.Button(frame, command=lambda: start_program(root, 'Empty'),
              text='Empty', width=17, font=(font_name, 11),bg="#E0E0E0",fg="#212121"
              ).pack(pady=5)
    tk.Button(frame, command=lambda: start_program(root, 'Load'),
              text='Load', width=17, font=(font_name, 11),bg="#E0E0E0",fg="#212121"
              ).pack(pady=5)

    tk.Button(frame, command=show_picture,
              text='Foto grupo',width=25,font=("arial", 16),bg="#E0E0E0",fg="#212121"
              ).pack(pady=(35, 5))
    tk.Button(frame, command=lambda: on_close(root),
              text='Exit', width=25, font=(font_name, 16),bg="#E0E0E0",fg="#212121"
              ).pack(pady=(0, 5))
    #tk.Button(frame, command=lambda: on_close(root), text='🌐', width=3, height=1, font=("", 20)).place(x=945, y=1145)

    setup_audio()
def start_program(a1, selection):
    '''for widget in a1.winfo_children():
        widget.destroy()
    g = creategraph(selection)

    f = None
    if selection == 'ECAC':
        f = 'ECAC/ECAC_nav.txt'
    elif selection == 'Spain':
        f = 'Spain/Spain_nav.txt'
    elif selection == 'Catalonia':
        f = 'catalonia/catalonia_nav.txt'
    create_interactive_interface(g, a1, f)'''
    try:
        for widget in a1.winfo_children():
            widget.destroy()

        if selection == 'Load':
            file_nav_points = filedialog.askopenfilename(title="Selecciona el archivo de nodos (NavPoints)",
                                                         filetypes=[("text", "*.txt")])
            if not file_nav_points:
                create_main_menu(a1)
                return
            file_nav_segments = filedialog.askopenfilename(title="Selecciona el archivo de segmentos (NavSegments)",
                                                           filetypes=[("text", "*.txt")])
            if not file_nav_segments:
                create_main_menu(a1)
                return
            file_nav_airports = filedialog.askopenfilename(title="Selecciona el archivo de aeropuertos (NavAirports)",
                                                           filetypes=[("text", "*.txt")])
            if not file_nav_airports:
                create_main_menu(a1)
                return

            # Vacía las listas antes de cargar
            NavPoint_lict.clear()
            NavSegment_list.clear()
            Airport_list.clear()

            AddNavPoint(file_nav_points)
            AddNavAirport(file_nav_airports)
            AddNavSegment(file_nav_segments)

            g = Airspace(NavPoint_lict, NavSegment_list, Airport_list)
            create_interactive_interface(g, a1, file_nav_points)
        elif selection == 'Empty':
            NavPoint_lict.clear()
            NavSegment_list.clear()
            Airport_list.clear()

            f = None

            g = Airspace(NavPoint_lict, NavSegment_list, Airport_list)
            create_interactive_interface(g, a1, f)
        else:
            g = creategraph(selection)
            f = None
            if selection == 'ECAC':
                f = 'ECAC/ECAC_nav.txt'
            elif selection == 'Spain':
                f = 'Spain/Spain_nav.txt'
            elif selection == 'Catalonia':
                f = 'catalonia/catalonia_nav.txt'
            create_interactive_interface(g, a1, f)
    except Exception as e:
        return_to_main(a1)
        messagebox.showerror("Error", f"error: {str('Illo, que loh ah puehsto mal, preguntale a tu padre xhaval ')}")
def main_menu():
    # Configuración HiDPI (Windows)
    # windll.shcore.SetProcessDpiAwareness(1)
    root = tk.Tk()
    resolution = root.maxsize()
    width, height = resolution

    # Formula inventada para que los widgets del interfaz pueda
    # adapta a cualquier resulocion de pantalla
    scale_multiplier = float((width*height)/(width+height)) / 500

    try:
        # Obtener la escala de la pantalla (Windows/macOS/Linux)
        scale_factor = pyautogui.screenshot().size[0] / pyautogui.size().width
    except:
        scale_factor = 1.0

    root.tk.call('tk', 'scaling', scale_factor * scale_multiplier)
    config_root_window(root)  # Config de la ventana principal
    setup_audio()             # Setup audio

    create_main_menu(root)

    root.protocol("WM_DELETE_WINDOW", lambda: on_close(root))
    root.mainloop()
def show_picture():
    window = tk.Toplevel()

    photo_normal = tk.PhotoImage(file="Serio.png")
    photo_hover = tk.PhotoImage(file="Fotaco.png")

    hover_button = tk.Button(window, image=photo_normal, borderwidth=0)

    def on_enter(e):
        hover_button.config(image=photo_hover)

    def on_leave(e):
        hover_button.config(image=photo_normal)

    hover_button.bind("<Enter>", on_enter)
    hover_button.bind("<Leave>", on_leave)
    hover_button.pack()
def how_to_controls(v):
    pyglet.font.add_file("Minecraft.ttf")
    font_name = "Minecraft"

    sub_control = tk.Toplevel()
    texto = tk.Text(sub_control, width=40, height=10, wrap='word')
    texto.pack(side='left', fill='both', expand=True)

    # Crear una Scrollbar y asociarla al Text
    scrollbar = tk.Scrollbar(sub_control, command=texto.yview)
    scrollbar.pack(side='right', fill='y')

    modo = {
        'full': '--Main graph--'
                '\nUPON A NODE:'
                '\nDouble left click: select a node'
                '\nRight click: open the menu'
                '\nANYWHERE:'
                '\nUse scroll to zoom in or zoom out'
                '\nUse the toolbar to move the graph'
                '\n(a simbol of arrows, yes, that one)'
                '\n\nPlease if the graph does not appears entirely in your screen, '
                'pulse "Maximize" two times to re-scale the window'
                '\n\nPlease if the clicks are not responding, zoom in to the node you want to '
                'select and try again'
                '\n\nTo maximize the performance of the program, '
                'please disable the name and cost of the graph and enable them when is necessary',
        'solonodo': '--Neighbors only--'
                    '\nUPON A NODE:'
                    '\nDouble left click: select a node'
                    '\nANYWHERE:'
                    '\nUse scroll to zoom in or zoom out'
                    '\nUse the toolbar to move the graph'
                    '\n(a simbol of arrows, yes, that one)',
        'paths': '--Paths from a node--'
                '\nUPON A NODE:'
                 '\nDouble left click: set a origin node (You can also use the input box)'
                 '\nRight click: open the menu'
                 '\nANYWHERE:'
                 '\nUse scroll to zoom in or zoom out'
                 '\nUse the toolbar to move the graph'
                 '\n(a simbol of arrows, yes, that one)'
    }
    texto.config(yscrollcommand=scrollbar.set)
    texto.insert("1.0", modo[v.mode])
    texto.config(state="disabled", font=(font_name, 15))

def f_extras():
    pyglet.font.add_file("Minecraft.ttf")
    font_name = "Minecraft"

    sub_control = tk.Toplevel()
    texto = tk.Text(sub_control, width=40, height=10, wrap='word')
    texto.pack(side='left', fill='both', expand=True)

    # Crear una Scrollbar y asociarla al Text
    scrollbar = tk.Scrollbar(sub_control, command=texto.yview)
    scrollbar.pack(side='right', fill='y')

    texto.config(yscrollcommand=scrollbar.set)
    texto.insert("1.0",
                 'FUNCIONALIDADES EXTRAS:'
                        '\n- Musica de fondo'
                        '\n- Crear tu propio grafo'
                        '\n- E/D nombres y costes'
                        '\n- Foto grupo, pasa el raton encima y veras'
                        '\n- Poder modificar un nodo sus datos sin tener que eliminarlo',
                        )
    texto.config(state="disabled", font=(font_name, 15))

if __name__ == "__main__":
    print("Probando el grafo...")
    main_menu()