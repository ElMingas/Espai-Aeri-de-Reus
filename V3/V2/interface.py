from graph import *

from ctypes import windll
from functools import partial

def create_interactive_interface(g):
    # Configuración HiDPI (Windows)
    windll.shcore.SetProcessDpiAwareness(1)

    root = tk.Tk()

    # Configuración de la ventana
    root.title("Visualizacion de grafo")
    resolution = root.maxsize()
    width, height = resolution
    '''width = root.winfo_screenwidth()
    height = root.winfo_screenheight()'''
    root.geometry(f"{int(width/2)}x{int(height/2)}+500+400")
    #root.attributes('-topmost', False)

    # Frame para controles
    control_frame = tk.Frame(root, padx=10, pady=10)
    control_frame.pack(side="top", fill="x")

    # Frame para el gráfico
    graph_frame = tk.Frame(root, bg='white')
    graph_frame.pack(side="top", fill="both", expand=True)

    #display_graph_in_frame(graph_frame, g, 'full')
    visualizer = InteractiveGraph(graph_frame, g, 'full')

    modos = [
        ("Main Graph", 'full'),
        ("Nodes only", 'solonodo'),
        ("Paths from a node", 'paths')
    ]

    for text, modo in modos:
        tk.Button(
            control_frame,
            text=text,
            command=partial(change_mode,modo, visualizer),
            width=15,
            height=2,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 12)
        ).pack(side="left", padx=5)

    root.mainloop()

def change_mode(new_mode, v):
    v.mode = new_mode
    v.update_display()