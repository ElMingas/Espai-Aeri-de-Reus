from graph import *
from ctypes import windll

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
    root.geometry(f"{int(width/2)}x{int(height/2)}")

    # Frame para controles
    control_frame = tk.Frame(root, padx=10, pady=10)
    control_frame.pack(side="top", fill="x")

    # Frame para el gráfico
    graph_frame = tk.Frame(root, bg='white')
    graph_frame.pack(side="top", fill="both", expand=True)

    display_graph_in_frame(graph_frame, g, 'full')

    # Botones
    plot_button = tk.Button(
        control_frame,
        text="Main Graph",
        command=lambda: display_graph_in_frame(graph_frame, g, 'full'),
        width=15,
        height=2,
        bg='#4CAF50',
        fg='white',
        font=('Arial', 12)
    )
    plot_button.pack(side="left", padx=5)

    plot_button = tk.Button(
        control_frame,
        text="Nodes only",
        command=lambda: display_graph_in_frame(graph_frame, g, 'solonodo'),
        width=15,
        height=2,
        bg='#4CAF50',
        fg='white',
        font=('Arial', 12)
    )
    plot_button.pack(side="left", padx=5)

    plot_button = tk.Button(
        control_frame,
        text="Paths from a node",
        command=lambda: display_graph_in_frame(graph_frame, g, 'paths'),
        width=15,
        height=2,
        bg='#4CAF50',
        fg='white',
        font=('Arial', 12)
    )
    plot_button.pack(side="left", padx=5)

    root.mainloop()

def display_graph_in_frame(parent_frame, g, mode):
    # Limpiar el frame si ya tenía contenido
    for widget in parent_frame.winfo_children():
        widget.destroy()

    # Crear el visualizador interactivo dentro del frame
    InteractiveGraph(parent_frame, g, mode)