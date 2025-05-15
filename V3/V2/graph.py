from segment import *
from paths import *

import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.patches import FancyArrowPatch
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from tkinter import messagebox
from tkinter.ttk import Combobox
from functools import partial
from tkinter import ttk

class Graphs:
    def __init__(self):
        self.nodes = []
        self.segments = []

def addnode (g, n):
    if n not in g.nodes:
        g.nodes.append(n)
        return True and g
    return False and g
def addsegment (g, seg_name, name_origin_node, name_destination_node):
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
    new_segment = Segment(segment_name, origin_node, dest_node)

    # Añadir a Gragh el nuevo segmento
    g.segments.append(new_segment)

    # Actualizar los vecinos
    addneighbor(origin_node, dest_node)

    return True
def getclosest(g, x, y):
    if not g.nodes: return None

    straw_node = Node("STRAW", x, y)
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

        '''Initialize UI attributes'''
        self.control_frame = None
        self.graph_frame = None
        self.menu_frame = None
        self.fig = None
        self.ax = None

        '''Initialize control widgets'''
        #Preferencias
        self.if_cost = None
        self.cb_cost = None
        self.if_node_name = None
        self.cb_node_name = None
        # Targets nodes
        self.selected_node = None
        self.node_origin= None
        self.node_destination = None
        # Mode full
        self.btn_add_node = None
        self.btn_add_segment = None
        # Mode paths
        self.lbl_origin = None
        self.cmb_origin = None
        self.lbl_destination = None
        self.cmb_destination = None
        self.btn_confirm = None
        # Float menu
        self.menu_buttons = None
        self.lbl_cost = None

        '''Initialize graph elements'''
        self.canvas = None
        self.toolbar = None

        '''Initialize event elements'''
        self.current_clicked_node = None

        # Configurar la estructura principal
        self.setup_ui()

        # referenciados en Paths (POSICIONA DESPUES DE TODAS LAS INICIACIONES DE ATRIBUTOS)
        self.paths = Paths(
            graph=self.graph,
            ax=self.ax,
            control_frame=self.control_frame,
            drawing={
                'draw_node': self.draw_node,
                'draw_segment': self.draw_segment,
                'finish_plot': self.finish_plot
            }
        )

        # Dibujar el grafo
        self.plot_full_graph()
    '''Graph general'''
    def setup_ui(self):
        """La interfaz de usuario"""
        # Frame para controles
        self.control_frame = tk.Frame(self.a1, padx=10, pady=20)
        self.control_frame.pack(side="top", fill="x")

        # Frame para el gráfico
        self.graph_frame = tk.Frame(self.a1)
        self.graph_frame.pack(side="top", fill="both", expand=True)

        # Frame para el menu flotante en el modo 'paths'
        self.menu_frame = tk.Frame(self.graph_frame)
        self.menu_frame.place_forget() # Inicialmente oculto

        # Botones de control
        #self.create_controls()
        self.setup_controls()
        self.setup_combobox_events()

        # Configurar el área del gráfico
        self.setup_graph_area()
    def setup_graph_area(self):
        """Configura el área del gráfico matplotlib"""
        self.fig = Figure(dpi=80)
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master = self.graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Barra de herramientas
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.graph_frame)
        self.toolbar.update()

        #Eventos interactivos
        self.canvas.mpl_connect('button_press_event', self.on_node_click)
        '''self.canvas.get_tk_widget().bind("<Button-1>",
                                         lambda e: self.menu_frame.place_forget())'''
    def setup_controls(self):
        # Variables
        self.node_origin = tk.StringVar()
        self.node_destination = tk.StringVar()
        self.if_cost = tk.IntVar(value=1)
        self.if_node_name = tk.IntVar(value=1)

        '''Comunes'''
        self.cb_cost =tk.Checkbutton(
            self.control_frame,
            variable=self.if_cost,
            text="Cost",
            onvalue=1,
            offvalue=0,
            command=lambda: self.update_display(),
            font=('Segoe UI', 12)
        )
        self.cb_cost.pack(side="right", padx=5)

        self.cb_node_name = tk.Checkbutton(
            self.control_frame,
            variable=self.if_node_name,
            text="Node name",
            onvalue=1,
            offvalue=0,
            command=lambda: self.update_display(),
            font=('Segoe UI', 12)
        )
        self.cb_node_name.pack(side="right", padx=5)

        '''Modo full'''
        self.btn_add_node = tk.Button(
            self.control_frame,
            text="Add node",
            command=self.crear_nodo,
            width=15
        )
        self.btn_add_segment = tk.Button(
            self.control_frame,
            text="Add segment",
            command=self.crear_segmento,
            width=15
        )
        # Inicialmente activo
        self.btn_add_node.pack(side="left", padx=5)
        self.btn_add_segment.pack(side="left", padx=10)

        '''Modo 'paths'''
        self.lbl_origin = tk.Label(self.control_frame, text="Node origin:", font=('arial', 10))
        self.cmb_origin = Combobox(
            self.control_frame,
            textvariable=self.node_origin,
            width=15,
            font=('Arial', 10),
            values=[]
        )
        self.lbl_destination = tk.Label(self.control_frame, text="Node destination:", font=('arial', 10))
        self.cmb_destination = Combobox(
            self.control_frame,
            textvariable=self.node_destination,
            width=15,
            font=('Arial', 10),
            values=[]
        )
        self.btn_confirm = tk.Button(
            self.control_frame,
            text="Confirm",
            width=15,
            font=('Arial', 10),
            command=lambda: self.paths.optimal_path(
                self.node_origin.get(),
                self.node_destination.get()
            )
        )
        '''self.lbl_cost = tk.Label(self.control_frame, font=('arial', 10))
        self.btn_confirm = tk.Button(
            self.control_frame,
            text="Confirm",
            width=15,
            font=('Arial', 10),
            command=lambda: (
                self.lbl_cost.config(
                    text=f"Total cost: {self.paths.optimal_path(self.node_origin.get(), self.node_destination.get())[1]}"
                )
            )
        )'''

        # Menú flotante (origen/destino)
        self.menu_buttons = []
        seleccion = [("Set as origin", 'origin'), ("Set as destination", 'destination')]
        for text, selec in seleccion:
            btn = tk.Button(
                self.menu_frame,
                text=text,
                command=partial(self.set_node_role, selec)
            )
            btn.pack(side='left')
            self.menu_buttons.append(btn)
    def setup_combobox_events(self):
        # modo paths
        # Combobox de origen
        self.cmb_origin.bind("<<ComboboxSelected>>",
                             lambda e: self.combobox_selection('origin'))

        # Combobox de destino
        self.cmb_destination.bind("<<ComboboxSelected>>",
                                  lambda e: self.combobox_selection('destination'))
    def plot_full_graph(self):
        """Dibuja el grafo completo sin resaltados"""
        self.ax.clear()
        self.selected_node = None

        #Dibujar todos los segmentos
        if self.mode == 'full':
            for seg in self.graph.segments:
                self.draw_segment(seg)

        #Dibujar todos los nodos
        for n in self.graph.nodes:
            self.draw_node(n, '#f8c675')

        if self.mode == 'full':
            self.finish_plot("Complete Graph Visualization")
        elif self.mode == 'solonodo':
            self.finish_plot("Visualization of nodes and their neighbors")
        elif self.mode == 'paths':
            self.finish_plot("Path Visualization")
    def finish_plot(self, title):
        self.ax.set_title(title)
        self.ax.set_xlabel("Coordenada X")
        self.ax.set_ylabel("Coordenada Y")
        self.ax.grid(True, linestyle='--', alpha=0.3)
        #self.ax.axis('equal')
        self.ax.set_aspect('equal', adjustable='box')
        self.canvas.draw()
    def update_display(self):
        if self.mode == 'full':
            self.plot_full_graph()
        elif self.mode == 'solonodo':
            self.plot_node_neighbors(self.selected_node) if self.selected_node else self.plot_full_graph()
        elif self.mode == 'paths':
            self.paths.plot_node_paths(self.selected_node) if self.selected_node else self.plot_full_graph()

        self.show_controls()
    '''Estetica'''
    def draw_segment(self, current_seg, color='#37873b'):
        if color == '#FFD700':
            linewidth = 1.7
            alpha = 1
        elif color == '#ef5b1c':
            linewidth = 1.1
            alpha = 0.56
        else:
            linewidth = 0.65
            alpha = 0.56

        arrow = FancyArrowPatch(
            (current_seg.origin.x, current_seg.origin.y),
            (current_seg.destination.x, current_seg.destination.y),
            arrowstyle='->',
            mutation_scale=15,
            color=color,
            linewidth=linewidth,
            alpha=alpha
        )
        self.ax.add_patch(arrow)

        # Etiqueta de costo
        if self.if_cost.get():
            mid_x = (current_seg.origin.x + current_seg.destination.x) / 2
            mid_y = (current_seg.origin.y + current_seg.destination.y) / 2
            self.ax.text(mid_x, mid_y, f"{current_seg.cost:.1f}",
                         color='darkred' if color == '#ef5b1c' else 'black',
                         fontsize=6.5, ha='center', va='center',
                         bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=1))
    def draw_node(self, current_n=None, color=None):
        if current_n is None and color is None:
            for n in self.graph.nodes:
                self.if_node_name_visible(n)
        else:
            self.if_node_name_visible(current_n, color)
    def if_node_name_visible(self, current_n, color=None):
        offset_pixels = 0.1
        offset_data = offset_pixels / self.ax.figure.dpi  # Convertir píxeles a pulgadas
        if self.if_node_name.get():
            self.ax.text(
                current_n.x, current_n.y + offset_data, current_n.name,
                fontsize=8, ha='center', va='center',
                transform=self.ax.transData
            )
        self.ax.plot(current_n.x, current_n.y, 'o', markersize=8,
                     markerfacecolor=color, markeredgecolor = None,
                     pickradius=5)
    def highlight_selected_node(self, selected_node=None):
        """Resalta el nodo seleccionado en el menú"""
        if selected_node is not None:
            node_name = selected_node
        else:
            node_name = self.node_origin.get()

        if not node_name:
            return
        for n in self.graph.nodes:
            if n.name == node_name:
                if self.mode == 'paths':
                    self.paths.plot_node_paths(n)
                    break
                else:
                    self.plot_node_neighbors(n)
    def plot_node_neighbors(self, sel_n):
        """Resalta un nodo y sus conexiones"""
        self.ax.clear()
        self.selected_node = sel_n

        # Dibujar todos los segmentos
        if self.mode == 'full':
            for seg in self.graph.segments:
                if seg.origin == sel_n or seg.destination == sel_n:
                    self.draw_segment(seg, '#ef5b1c')
        elif self.mode == 'solonodo':
            for seg in self.graph.segments:
                if seg.origin == sel_n:
                    color = '#ef5b1c'
                    self.draw_segment(seg, color)

        # Dibujar todos los nodos
        for n in self.graph.nodes:
            if n == sel_n:
                self.draw_node(n, 'blue')
            elif n in sel_n.neighbors:
                self.draw_node(n, 'green')
            else:
                self.draw_node(n, 'lightgray')
        if self.mode == 'full':
            self.finish_plot(f"Node: {sel_n.name}")
        elif self.mode == 'solonodo':
            self.finish_plot(f"Node: {sel_n.name} and its neighbors")
    '''Controles'''
    def show_controls(self):
        self.cmb_origin['values'] = [n.name for n in self.graph.nodes]
        self.cmb_destination['values'] = [n.name for n in self.graph.nodes]

        self.cmb_origin.set('')
        self.cmb_destination.set('')

        """Mostrar/Ocultar botones según el modo"""
        mode_widgets = {
            'full': [self.btn_add_node, self.btn_add_segment],
            'paths': [self.lbl_origin, self.cmb_origin,
                      self.lbl_destination, self.cmb_destination,
                      self.btn_confirm],
            'solonodo': []
        }

        for widget_list in mode_widgets.values():
            for widget in widget_list:
                widget.pack_forget()

        for widget in mode_widgets.get(self.mode, []):
            widget.pack(side="left", padx=5)

        self.menu_frame.place_forget() if self.mode != 'paths' else None
    def on_node_click(self, event):
        if event.inaxes != self.ax:
            return

        for n in self.graph.nodes:
            if ((n.x - event.xdata) ** 2 + (n.y - event.ydata) ** 2) < 0.0005:
                if event.dblclick and event.button == 1:
                    if self.mode in ['full', 'solonodo']:
                        self.plot_node_neighbors(n)
                    elif self.mode == 'paths':
                        self.paths.plot_node_paths(n)
                    self.node_origin.set(n.name)  # Actualizar el menú
                    # self.node_destination.set(' ')
                    self.menu_frame.place_forget()
                    break
                elif event.button == 3 and self.mode == 'paths':
                    clicked_node = n
                    if clicked_node:
                        self.current_clicked_node = clicked_node
                        self.show_float_menu(event, clicked_node)
                        break
    def show_float_menu(self, event, current_node):
        """Muestra el menú contextual en la posición del clic"""
        canvas_widget = self.canvas.get_tk_widget()

        x_frame = event.x + canvas_widget.winfo_x()
        y_frame = canvas_widget.winfo_height() - event.y + canvas_widget.winfo_y()  # Invertir Y

        offset = 15
        x_pos = x_frame + offset
        y_pos = y_frame - 3*offset

        self.menu_frame.place(x=x_pos, y=y_pos)
        self.menu_frame.lift()
    def set_node_role(self, role):
        """Establece el nodo como origen o destino según el parámetro role"""
        if not self.current_clicked_node:
            return

        if role == 'origin':
            self.node_origin.set(self.current_clicked_node.name)
            self.paths.plot_node_paths(self.current_clicked_node)
        elif role == 'destination':
            self.node_destination.set(self.current_clicked_node.name)
            '''self.draw_node(self.current_clicked_node, '#0047AB')
            self.canvas.draw_idle()'''

        # Ocultar el menú después de la selección
        self.menu_frame.place_forget()
    def combobox_selection(self, combobox_type):
        for n in self.graph.nodes:
            if combobox_type == 'origin':
                origin_name = self.node_origin.get()
                if n.name == origin_name:
                    self.paths.plot_node_paths(n)
            '''elif combobox_type == 'destination':
                dest_name = self.node_destination.get()
                if n.name == node_name:
                    self.draw_node(n, '#0047AB')'''

        '''if self.node_origin.get() and self.node_destination.get():
            self.optimal_path(origin_name, dest_name)'''
    '''Añadir elementos'''
    def crear_segmento(self):
        sub_seg = tk.Toplevel()
        sub_seg.title("Add segment")
        sub_seg.geometry("600x350+600+500")
        sub_seg.transient(self.a1)

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

                #Segmento existente con nombre distinto
                for s in self.graph.segments:
                    if s.origin.name == nombre_origen and s.destination.name == nombre_destino:
                            messagebox.showerror("Error", f"Existed segment with name: {s.name}")
                            return

                # Añadir el nuevo segmento
                if addsegment(self.graph, nombre_segmento, nombre_origen, nombre_destino):
                    messagebox.showinfo("Success", "Segment added successfully")
                    self.plot_full_graph()  # Actualizar el gráfico
                    sub_seg.destroy()
                else:
                    messagebox.showerror("Error", "Segment could not be added")

            except Exception as e:
                messagebox.showerror("Error", f"error: {str(e)}")

        # Interfaz de usuario
        tk.Label(sub_seg, text="Name:", font=('Arial', 15)).place(x=30, y=30)
        tk.Entry(sub_seg, textvariable=nombre, font=('Arial', 15)).place(x=140, y=30)

        # Usar OptionMenu para seleccionar nodos existentes
        tk.Label(sub_seg, text="Origin:", font=('Arial', 15)).place(x=30, y=80)
        Combobox(
            sub_seg,
            textvariable=origen,
            font=('Arial', 15),
            values=[n.name for n in self.graph.nodes]
        ).place(x=200, y=75, width=180)

        tk.Label(sub_seg, text="Destination:", font=('Arial', 15)).place(x=30, y=130)
        Combobox(
            sub_seg,
            textvariable=destino,
            font=('Arial', 15),
            values=[n.name for n in self.graph.nodes]
        ).place(x=200, y=125, width=180)

        '''destino_menu = Combobox(sub_seg, textvariable=destino, values=[n.name for n in self.graph.nodes])
        destino_menu.config(font=('Arial', 15))
        destino_menu.place(x=200, y=125, width=180)'''

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
        ).pack(side="left",padx = (10, 10), pady =5)

        tk.Button(
            btn_frame,
            text="Cancel",
            command=sub_seg.destroy,
            width=12,
            height=2,
            font=('Arial', 12),
            bg="#F44336",
            fg="white"
        ).pack(side="left", pady =5)

        # Añadir lista de nodos disponibles
        tk.Label(sub_seg, text="Available nodes:", font=('Arial', 10)).place(x=30, y=270)
        nodos_text = " ".join([n.name for n in self.graph.nodes])
        tk.Label(sub_seg, text=nodos_text, font=('Arial', 10)).place(x=30, y=300)
    def crear_nodo(self):
        sub_nodo = tk.Toplevel()
        sub_nodo.title("Add node")
        sub_nodo.geometry("600x300+600+500")
        sub_nodo.transient(self.a1)

        # Variables para los campos
        nombre = tk.StringVar()
        posx = tk.StringVar()
        posy = tk.StringVar()

        def confirmar():
            try:
                # Validar datos
                nombre_nodo = nombre.get().strip()
                x = posx.get().strip()
                y = posy.get().strip()

                if not nombre_nodo or not x or not y:
                    messagebox.showerror("Error", "All fields are required")
                    return

                # Verificar si el nodo ya existe
                if any(n.name == nombre_nodo for n in self.graph.nodes):
                    messagebox.showerror("Error", "A node with this name already exists")
                    return

                x = float(x)
                y = float(y)
                # Crear y añadir el nuevo nodo
                nuevo_nodo = Node(nombre_nodo, x, y)
                if addnode(self.graph, nuevo_nodo):
                    messagebox.showinfo("Éxito", "Node added successfully")
                    self.plot_full_graph()  # Actualizar el gráfico
                    sub_nodo.destroy()
                else:
                    messagebox.showerror("Error", "Node could not be added")

            except Exception as e:
                messagebox.showerror("Error", f"error: {str(e)}")

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

    '''def nodos_con_mas_de_dos_nodos(self):
        encontrado = 0

        for n in self.graph.nodes:
            if len(n.neighbors) >= 2:
                self.draw_node(n, 'blue')
                encontrado += 1

        node_label = tk.Label(self.control_frame, text=encontrado)
        node_label.pack(side="left", padx=5)

        self.canvas.draw()'''
