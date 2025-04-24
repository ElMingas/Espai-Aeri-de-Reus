from segment import *
from node import *

import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.patches import FancyArrowPatch
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from tkinter import messagebox
from collections import deque
from queue import PriorityQueue

class Graphs:
    def __init__(self):
        self.nodes = []
        self.segments = []

def addnode (g, n):
    if n not in g.nodes:
        g.nodes.append(n)
        return True and g
    return False and g

def addsegment (g, name, name_origin_node, name_destination_node):
    origin_node = None
    dest_node = None

    for n in g.nodes:
        if n.name == name_origin_node:
            origin_node = n
        if n.name == name_destination_node:
            dest_node = n

    # Revisar si se encuentran los dos nodos
    if origin_node is None or dest_node is None:
        return False

    # Crear el segmento
    segment_name = f"{name_origin_node}{name_destination_node}"
    new_segment = segment(segment_name, origin_node, dest_node)

    # Añadir a Gragh el nuevo segmento
    g.segments.append(new_segment)

    # Actualizar los vecinos
    addneighbor(origin_node, dest_node)

    return True

def getclosest(g, x, y):
    if not g.nodes: return None

    straw_node = node("STRAW", x, y)
    d = distance(straw_node, g.nodes[0])
    nearest = g.nodes[0]

    i = 1
    while i < len(g.nodes):
        pd = distance(straw_node, g.nodes[i])
        if pd < d:
            d = pd
            nearest = g.nodes[i]
            if d == 0:
                break
        i += 1
    return nearest

class InteractiveGraph:
    def __init__(self, a1, graph, mode):
        self.a1 = a1
        self.graph = graph
        self.mode = mode
        self.selected_node = None

        # Configurar la estructura principal
        self.setup_ui(mode)

        # Dibujar el grafo
        if mode == 'full':
            self.plot_full_graph()
        elif mode == 'solonodo':
            self.plot_solo_nodos()
        elif mode == 'paths':
            self.plot_solo_nodos()

    def setup_ui(self, mode):
        """La interfaz de usuario"""
        # Frame para controles
        self.control_frame = tk.Frame(self.a1, padx=10, pady=10)
        self.control_frame.pack(side="top", fill="x")

        # Frame para el gráfico
        self.graph_frame = tk.Frame(self.a1)
        self.graph_frame.pack(side="top", fill="both", expand=True)

        # Botones de control
        self.create_controls(mode)

        # Configurar el área del gráfico
        self.setup_graph_area()

    def setup_graph_area(self):
        """Configura el área del gráfico matplotlib"""
        self.fig = Figure(dpi=90)
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master = self.graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Barra de herramientas
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.graph_frame)
        self.toolbar.update()

        #Eventos interactivos
        self.canvas.mpl_connect('button_press_event', self.on_node_click)

    def plot_full_graph(self):
        """Dibuja el grafo completo sin resaltados"""
        self.ax.clear()
        self.selected_node = None

        #Dibujar todos los segmentos
        for seg in self.graph.segments:
            self.draw_segment(seg)

        #Dibujar todos los nodos
        for node in self.graph.nodes:
            self.draw_node(node, 'orange')

        self.finish_plot("Visualización Completa del Grafo")

    def plot_solo_nodos(self):
        """Dibuja el grafo completo sin resaltados"""
        self.ax.clear()
        self.selected_node = None

        # Dibujar todos los nodos
        for node in self.graph.nodes:
            self.draw_node(node, 'orange')

        self.finish_plot("Visualización de solo los nodos")

    def plot_node_paths(self, node):
        self.ax.clear()
        self.selected_node = node
        visited = set()
        queue = deque([(node, [node])])

        #Dibujar los nodos
        for n in self.graph.nodes:
            self.draw_node(n, 'lightgray')

        self.draw_node(node, 'blue')

        #Dibujar los caminos
        while queue:
            current_node, path = queue.popleft()

            if current_node not in visited:
                visited.add(current_node)

                if current_node != node:
                    self.draw_node(current_node, 'green')

                for seg in self.graph.segments:
                    if (seg.origin == current_node and
                            seg.destination != current_node and
                            seg.destination != node):
                        color = 'red'
                        self.draw_segment(seg, color)

            for neighbor in current_node.neighbors:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))

        self.fig.canvas.draw()

    def optimal_path(self, origin_name, destination_name):
        origin_node = None
        destination_node = None

        for node in self.graph.nodes:
            if node.name == origin_name:
                origin_node = node
            if node.name == destination_name:
                destination_node = node

        frontier = PriorityQueue()
        frontier.put((0, origin_node))  #(prioridad, nodo)
        came_from = {origin_node: None}
        cost_so_far = {origin_node: 0}

        while not frontier.empty():
            _, current = frontier.get()

            if current == destination_node:
                break

            for neighbor in current.neighbors:
                new_cost = cost_so_far[current] + distance(current, neighbor)

                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + distance(neighbor, destination_node)
                    frontier.put((priority, neighbor))
                    came_from[neighbor] = current

        path = []
        current = destination_node
        while current is not None:
            path.append(current)
            current = came_from.get(current)
        path.reverse()

        path_segments = []
        i = 0
        while i < len(path) - 1:
            segment = next(s for s in self.graph.segments
                if s.origin == path[i] and s.destination == path[i + 1])
            path_segments.append(segment)
            i += 1

        self.draw_highlight_optimal_path(path_segments)

        #print (path, cost_so_far.get(destination_node, float('inf')))

        return path, cost_so_far.get(destination_node, float('inf'))

    def draw_highlight_optimal_path (self, path_segments):
        for segment in path_segments:
            arrow = FancyArrowPatch(
                (segment.origin.x, segment.origin.y),
                (segment.destination.x, segment.destination.y),
                arrowstyle='->',
                mutation_scale=15,
                color='yellow',
                linewidth=2,
                alpha=0.7
            )
            self.ax.add_patch(arrow)

            # Etiqueta de costo
            mid_x = (segment.origin.x + segment.destination.x) / 2
            mid_y = (segment.origin.y + segment.destination.y) / 2
            self.ax.text(mid_x, mid_y, f"{segment.cost:.1f}",
                         color='darkred',
                         fontsize=9, ha='center', va='center',
                         bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=1))

        self.canvas.draw_idle()

    def plot_node_neighbors(self, node):
        """Resalta un nodo y sus conexiones"""
        self.ax.clear()
        self.selected_node = node

        # Dibujar todos los segmentos
        if self.mode == 'full':
            for seg in self.graph.segments:
                color = 'red' if seg.origin == node or seg.destination == node else 'blue'
                self.draw_segment(seg, color)
        elif self.mode == 'solonodo':
            for seg in self.graph.segments:
                if seg.origin == node:
                    color = 'red'
                    self.draw_segment(seg, color)

        # Dibujar todos los nodos
        for n in self.graph.nodes:
            if n == node:
                self.draw_node(n, 'blue')
            elif n in node.neighbors:
                self.draw_node(n, 'green')
            else:
                self.draw_node(n, 'lightgray')
        if self.mode == 'full':
            self.finish_plot(f"Node: {node.name}")
        elif self.mode == 'solonodo':
            self.finish_plot(f"Node: {node.name} and its neighbors")

    def finish_plot(self, title):
        self.ax.set_title(title)
        self.ax.set_xlabel("Coordenada X")
        self.ax.set_ylabel("Coordenada Y")
        self.ax.grid(True, linestyle='--', alpha=0.3)
        self.ax.axis('equal')
        self.canvas.draw()

    def draw_segment(self, segment, color='blue'):
        arrow = FancyArrowPatch(
            (segment.origin.x, segment.origin.y),
            (segment.destination.x, segment.destination.y),
            arrowstyle='->',
            mutation_scale=15,
            color=color,
            linewidth=2 if color == 'red' else 1,
            alpha=0.7
        )
        self.ax.add_patch(arrow)

        # Etiqueta de costo
        mid_x = (segment.origin.x + segment.destination.x) / 2
        mid_y = (segment.origin.y + segment.destination.y) / 2
        self.ax.text(mid_x, mid_y, f"{segment.cost:.1f}",
                     color='darkred' if color == 'red' else 'black',
                     fontsize=9, ha='center', va='center',
                     bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=1))

    def draw_node(self, node, color):
        self.ax.plot(node.x, node.y, 'o', markersize=10,
                     markerfacecolor=color, markeredgecolor='black',
                     pickradius=5)
        self.ax.text(node.x, node.y + 0.37, node.name,
                     fontsize=12, ha='center', va='center')

    def create_controls(self, mode):
        # Variables
        self.node_origin = tk.StringVar()
        self.node_destination = tk.StringVar()

        """Botones"""
        '''tk.Button(
            self.control_frame,
            text="Mostrar Todo",
            command=self.plot_full_graph,
            width=15
        ).pack(side=tk.LEFT, padx=5)'''

        '''self.node_menu = tk.OptionMenu(
            self.control_frame,
            self.node_var,
            *[n.name for n in self.graph.nodes]
        )
        self.node_menu.pack(side=tk.LEFT, padx=5)'''

        tk.Button(
            self.control_frame,
            command=self.highlight_selected_node,
            width=15
        )

        if mode == 'full':
            tk.Button(
                self.control_frame,
                text="Add node",
                command=self.crear_nodo,
                width=15
            ).pack(side="left", padx=5)

            tk.Button(
                self.control_frame,
                text="Add segment",
                command=self.crear_segmento,
                width=15
            ).pack(side="left", padx=10)
        elif mode == 'paths':
            '''Create the menu'''
            #origin
            node_label = tk.Label(self.control_frame, text="Node origin:")
            node_label.pack(side="left", padx=5)

            self.node_menu = tk.OptionMenu(
                self.control_frame,
                self.node_origin,
                command=self.highlight_selected_node,
                *[n.name for n in self.graph.nodes]
            )
            self.node_menu.pack(side="left", padx=0)

            # Destination
            node_label = tk.Label(self.control_frame, text="Node destination:")
            node_label.pack(side="left", padx=5)

            self.node_menu = tk.OptionMenu(
                self.control_frame,
                self.node_destination,
                *[n.name for n in self.graph.nodes]
            )
            self.node_menu.pack(side="left", padx=0)

            self.confirm_button = tk.Button(
                self.control_frame,
                text="Confirm",
                state="disabled",  #Inicialmente deshabilitado
                width=15
            )
            self.confirm_button.pack(side="left", padx=10)

            if self.node_origin and self.node_destination:
                self.confirm_button.config(state="normal",
                                           command=lambda: self.optimal_path(
                                               self.node_origin.get(),
                                               self.node_destination.get()
                                           ))
            else:
                self.confirm_button.config(state="disabled")

    def highlight_selected_node(self, selected_value=None):
        """Resalta el nodo seleccionado en el menú"""
        if selected_value is not None:
            node_name = selected_value
        else:
            node_name = self.node_origin.get()

        if not node_name:
            return
        for node in self.graph.nodes:
            if node.name == node_name:
                if self.mode == 'paths':
                    self.plot_node_paths(node)
                    break
                else:
                    self.plot_node_neighbors(node)

    def on_node_click(self, event):
        if event.inaxes != self.ax:
            return

        for node in self.graph.nodes:
            # Verificar si el clic está cerca de un nodo
            if ((node.x - event.xdata) ** 2 + (node.y - event.ydata) ** 2) < 0.5:
                if self.mode == 'full' or self.mode == 'solonodo':
                    self.plot_node_neighbors(node)
                elif self.mode == 'paths':
                    self.plot_node_paths(node)
                self.node_origin.set(node.name)  #Actualizar el menú
                break

    def crear_segmento(self):
        sub_seg = tk.Toplevel()
        sub_seg.title("Add segment")
        sub_seg.geometry("400x300")

        # Variables para los campos
        nombre = tk.StringVar()
        origen = tk.StringVar()
        destino = tk.StringVar()

        def confirmar():
            try:
                # Validar datos
                nombre_segmento = nombre.get().strip()
                nombre_origen = origen.get().strip()
                nombre_destino = destino.get().strip()

                if not nombre_segmento or not nombre_origen or not nombre_destino:
                    messagebox.showerror("Error", "All fields are required")
                    return

                # Verificar si los nodos existen
                origen_existe = any(n.name == nombre_origen for n in self.graph.nodes)
                destino_existe = any(n.name == nombre_destino for n in self.graph.nodes)

                if not origen_existe or not destino_existe:
                    messagebox.showerror("Error", "nodes not found")
                    return

                # Verificar si el segmento ya existe
                seg_existe = any(s.name == nombre_segmento for s in self.graph.segments)
                if seg_existe:
                    messagebox.showerror("Error", "There is already a segment with this name")
                    return

                # Añadir el nuevo segmento
                if addsegment(self.graph, nombre_segmento, nombre_origen, nombre_destino):
                    messagebox.showinfo("Success", "Segment added successfully")
                    self.plot_full_graph()  # Actualizar el gráfico
                    sub_seg.destroy()
                else:
                    messagebox.showerror("Error", "The segment could not be added")

            except Exception as e:
                messagebox.showerror("Error", f"error: {str(e)}")

        # Interfaz de usuario
        tk.Label(sub_seg, text="Name:", font=('Arial', 15)).place(x=30, y=30)
        tk.Entry(sub_seg, textvariable=nombre, font=('Arial', 15)).place(x=125, y=30)

        # Usar OptionMenu para seleccionar nodos existentes
        tk.Label(sub_seg, text="Origin:", font=('Arial', 15)).place(x=30, y=80)
        origen_menu = tk.OptionMenu(sub_seg, origen, *[n.name for n in self.graph.nodes])
        origen_menu.config(font=('Arial', 15))
        origen_menu.place(x=125, y=75, width=180)

        tk.Label(sub_seg, text="Destination:", font=('Arial', 15)).place(x=30, y=130)
        destino_menu = tk.OptionMenu(sub_seg, destino, *[n.name for n in self.graph.nodes])
        destino_menu.config(font=('Arial', 15))
        destino_menu.place(x=125, y=125, width=180)

        # Botones
        btn_frame = tk.Frame(sub_seg)
        btn_frame.place(x=50, y=180, width=300)

        tk.Button(
            btn_frame,
            text="Confirm",
            command=confirmar,
            width=12,
            height=2,
            font=('Arial', 12),
            bg="#4CAF50",
            fg="white"
        ).pack(side="left", padx=10)

        tk.Button(
            btn_frame,
            text="Cancel",
            command=sub_seg.destroy,
            width=12,
            height=2,
            font=('Arial', 12),
            bg="#F44336",
            fg="white"
        ).pack(side="left", padx=10)

        # Añadir lista de nodos disponibles
        tk.Label(sub_seg, text="Available nodes:", font=('Arial', 10)).place(x=30, y=250)
        nodos_text = " ".join([n.name for n in self.graph.nodes])
        tk.Label(sub_seg, text=nodos_text, font=('Arial', 10)).place(x=30, y=270)

    def crear_nodo(self):
        sub_nodo = tk.Toplevel()
        sub_nodo.title("Add node")
        sub_nodo.geometry("600x300")

        # Variables para los campos
        nombre = tk.StringVar()
        posx = tk.StringVar()
        posy = tk.StringVar()

        def confirmar():
            try:
                # Validar datos
                nombre_nodo = nombre.get().strip()
                x = float(posx.get())
                y = float(posy.get())

                if not nombre_nodo or not x or not y:
                    messagebox.showerror("Error", "All fields are required")
                    return

                # Verificar si el nodo ya existe
                if any(n.name == nombre_nodo for n in self.graph.nodes):
                    messagebox.showerror("Error", "Ya existe un nodo con ese nombre")
                    return

                # Crear y añadir el nuevo nodo
                nuevo_nodo = node(nombre_nodo, x, y)
                if addnode(self.graph, nuevo_nodo):
                    messagebox.showinfo("Éxito", "Nodo añadido correctamente")
                    self.plot_full_graph()  # Actualizar el gráfico
                    sub_nodo.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo añadir el nodo")

            except ValueError:
                messagebox.showerror("Error", "Las coordenadas deben ser números válidos")

        # Interfaz de usuario
        tk.Label(sub_nodo, text="Name:", font=('Arial', 15)).place(x=30, y = 30)
        tk.Entry(sub_nodo, textvariable=nombre, font=('Arial', 15)).place(x=200, y = 30)

        tk.Label(sub_nodo, text="Position X:", font=('Arial', 15)).place(x=30, y=80)
        tk.Entry(sub_nodo, textvariable=posx, font=('Arial', 15)).place(x=200, y=80)

        tk.Label(sub_nodo, text="Position Y:", font=('Arial', 15)).place(x=30, y=130)
        tk.Entry(sub_nodo, textvariable=posy, font=('Arial', 15)).place(x=200,y=130)

        # Botones
        btn_frame = tk.Frame(sub_nodo)
        btn_frame.place(x=50, y=180, width=300)

        tk.Button(
            btn_frame,
            text="Confirm",
            command=confirmar,
            width=10,
            height = 2,
            font=('Arial', 12),
            bg="#4CAF50",
            fg="white"
        ).pack(side="left",padx = (10, 20))

        tk.Button(
            btn_frame,
            text="Cancel",
            command=sub_nodo.destroy,
            width=10,
            height=2,
            font=('Arial', 12),
            bg="#F44336",
            fg="white"
        ).pack(side="left")

'''def reset_node_color(self, node):
    """Reset a node to its default color based on selection state"""
    if node == self.selected_node:
        self.draw_node(node, 'blue')  # Selected node color
    else:
        self.draw_node(node, 'orange')  # Default node color

def plot_node(g, name_origin):
    origin = None
    for node in g.nodes:
        if node.name == name_origin:
            origin = node
            break

    if not origin:
        return False

    fig, ax = plt.subplots(figsize=(10, 8))

    # Draw all segments first (background)
    for seg in g.segments:
        if seg.origin == origin:
            arrow_color = 'red'
            line_width = 2
            cost_color = 'darkred'
        else:
            arrow_color = 'black'
            line_width = 1.5
            cost_color = 'gray'

        # Check if segment connects to origin
        arrow = FancyArrowPatch(
            (seg.origin.x, seg.origin.y),
            (seg.destination.x, seg.destination.y),
            arrowstyle='->',
            mutation_scale=18 if arrow_color == 'red' else 10,
            color=arrow_color,
            linewidth=line_width,
            alpha=0.65 if arrow_color == 'red' else 0.2
        )
        ax.add_patch(arrow)

        mid_x = (seg.origin.x + seg.destination.x) / 2
        mid_y = (seg.origin.y + seg.destination.y) / 2
        ax.text(mid_x, mid_y, f"{seg.cost:.1f}",
                color=cost_color, fontsize=9, ha='center', va='center',
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=1))

    # Draw all nodes with appropriate colors
    for node in g.nodes:
        if node == origin:
            # Origin node (blue)
            color = 'blue'
            size = 9
        elif node in origin.neighbors:
            # Neighbor nodes (green)
            color = 'green'
            size = 7
        else:
            # Other nodes (gray)
            color = 'gray'
            size = 5

        ax.plot(node.x, node.y, 'o', markersize=size,
                markerfacecolor=color, markeredgecolor='black')

        # Node label
        ax.text(node.x, node.y + 0.3, node.name,
                fontsize=12, ha='center', va='center')

    plt.title(f"Node {name_origin} and its neighbors")
    plt.xlabel("X-coordinate")
    plt.ylabel("Y-coordinate")
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.axis('equal')
    plt.show()

    return True'''