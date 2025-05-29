from airspace import *
from paths import *
from kml_graph import *
from kml_path import *
from kml_neighbors import *

import tkinter as tk
import pyglet

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter.ttk import Combobox
from functools import partial
from tkinter import ttk

'''class Graphs:
    def __init__(self):
        self.nodes = []
        self.segments = []'''

def addnode (g, n):
    if n not in g.nodes:
        g.nodes.append(n)
        return True and g
    return False and g
def addsegment (g, name_origin_node, name_destination_node):
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

    # Coste
    cost = distance(origin_node, dest_node) * 100

    # Crear el segmento
    new_segment = NavSegment(origin_node, dest_node, cost)
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
    def __init__(self, a1, graph, mode, file):
        self.a1 = a1
        self.graph = graph
        self.mode = mode
        self.file = file
        #self.minecraft_font = font.Font(file="Minecraft.ttf", size=10)

        '''Initialize UI attributes'''
        self.control_frame = None
        self.toolbar_frame = None
        self.controls_frame = None
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
        #Comun lbl
        self.lbl_google = None
        self.btn_save_graph = None
        # Mode full
        self.lbl_selec = None
        self.node_selec = None
        self.cmb_selec = None
        self.btn_add_node = None
        self.btn_add_segment = None
        self.btn_see_full_g = None
        # Mode solo nodo
        self.btn_see_neighbors = None
        # Mode paths
        self.lbl_origin = None
        self.cmb_origin = None
        self.lbl_destination = None
        self.cmb_destination = None
        self.btn_confirm = None
        self.btn_reachability_in_Gearth = None
        self.btn_see_path_in_Gearth = None
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
        self.update_display()
    '''Graph general'''
    def setup_ui(self):
        """La interfaz de usuario"""
        # Frame para controles
        self.control_frame = tk.Frame(self.a1, padx=10, pady=3)
        self.control_frame.pack(side="top", fill="x")

        # Frame para los controles debajo del toolbar
        self.controls_frame = tk.Frame(self.control_frame)
        self.controls_frame.pack(side="left", fill="y")

        # Frame dedicado para el toolbar
        self.toolbar_frame = tk.Frame(self.control_frame, padx=50)
        self.toolbar_frame.pack(side="left", fill="y")

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
        self.fig = Figure(figsize=(8, 6), dpi=80)
        self.ax = self.fig.add_subplot(111)
        self.fig.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.97)

        self.canvas = FigureCanvasTkAgg(self.fig, master = self.graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Barra de herramientas
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbar_frame)
        self.toolbar.update()

        #Eventos interactivos
        self.canvas.mpl_connect('button_press_event', self.on_node_click)
        self.canvas.mpl_connect('scroll_event', self.on_scroll)
    def setup_controls(self):
        # Variables
        self.node_selec = tk.StringVar()
        self.node_origin = tk.StringVar()
        self.node_destination = tk.StringVar()
        self.if_cost = tk.IntVar(value=1)
        self.if_node_name = tk.IntVar(value=1)

        pyglet.font.add_file("Minecraft.ttf")
        font_name = "Minecraft"

        '''Comunes'''
        self.cb_cost =tk.Checkbutton(
            self.controls_frame,
            variable=self.if_cost,
            text="Cost",
            onvalue=1,
            offvalue=0,
            command=lambda: self.update_display(),
            font = (font_name, 11)
        )
        self.cb_cost.pack(side="right", padx=5)

        self.cb_node_name = tk.Checkbutton(
            self.controls_frame,
            variable=self.if_node_name,
            text="Node name",
            onvalue=1,
            offvalue=0,
            command=lambda: self.update_display(),
            font=(font_name, 11)
        )
        self.cb_node_name.pack(side="right", padx=5)

        '''Modo full'''
        self.lbl_selec = tk.Label(self.controls_frame, text="Select a node:", font=(font_name, 10))
        self.cmb_selec = Combobox(
            self.controls_frame,
            textvariable=self.node_selec,
            width=15,
            font=(font_name, 10),
            values=[],
        )
        self.btn_add_node = tk.Button(
            self.controls_frame,
            text="Add node",
            command=self.crear_nodo,
            font=font_name,
            width=15
        )
        self.btn_add_segment = tk.Button(
            self.controls_frame,
            text="Add segment",
            command=self.crear_segmento,
            font=font_name,
            width=15
        )
        self.lbl_google = tk.Label(self.controls_frame, text="G.Earth:", font=(font_name, 11))
        self.btn_see_full_g = tk.Button(
            self.controls_frame,
            text="Full Graph",
            fg="white",
            relief="groove",
            font=font_name,
            command=lambda: txt_to_kml(NavPoint_lict, NavSegment_list, 'nav_point.kml'),
            width=15,
            bg = "#4285F4",
        )
        self.btn_save_graph = tk.Button(
            self.controls_frame,
            text="Save graph",
            font=font_name,
            command=self.guardar_grafo,
            width=15
        )

        # Inicialmente activo
        self.btn_add_node.pack(side="left", padx=5)
        self.btn_add_segment.pack(side="left", padx=5)
        #self.btn_save_graph.pack(side="left", padx=10)
        '''Modo solo nodo'''
        self.btn_see_neighbors = tk.Button(
            self.controls_frame,
            text="Neighbors",
            width=16,
            bg="#4285F4",
            fg="white",
            relief="groove",
            font=(font_name, 10),
            command=lambda: txt_to_kml_neighbors(self.selected_node, 'nav_neighbors.kml')
        )

        '''Modo 'paths'''
        self.lbl_origin = tk.Label(self.controls_frame, text="Node origin:", font=(font_name, 10))
        self.cmb_origin = Combobox(
            self.controls_frame,
            textvariable=self.node_origin,
            width=15,
            font=(font_name, 10),
            values=[]
        )
        self.lbl_destination = tk.Label(self.controls_frame, text="Node destination:", font=(font_name, 10))
        self.cmb_destination = Combobox(
            self.controls_frame,
            textvariable=self.node_destination,
            width=15,
            font=(font_name, 10),
            values=[]
        )
        self.btn_confirm = tk.Button(
            self.controls_frame,
            text="Confirm",
            width=15,
            font=(font_name, 10),
            command=lambda: self.paths.optimal_path(
                self.node_origin.get(),
                self.node_destination.get()
            )
        )
        self.btn_reachability_in_Gearth = tk.Button(
            self.controls_frame,
            text="All the paths",
            width=16,
            bg="#4285F4",
            fg="white",
            relief="groove",
            font=(font_name, 10),
            command=lambda: generate_reachability_kml(self.paths.all_reachable_nodes,
                                                      self.paths.all_possible_paths,
                                                      'nav_points_reach.kml',
                                                      'nav_segs_reach.kml')
        )
        self.btn_see_path_in_Gearth = tk.Button(
            self.controls_frame,
            text="Optimal path",
            width=16,
            bg="#4285F4",
            fg="white",
            relief="groove",
            font=(font_name, 10),
            command=lambda: txt_to_kml_path(self.paths.opt_path, 'opt_path.kml')
        )

        '''Menú flotante (delete/origen/destino)'''
        self.menu_buttons = []
        seleccion = [("Set as origin", 'origin'), ("Set as destination", 'destination')]
        for text, selec in seleccion:
            btn = tk.Button(
                self.menu_frame,
                text=text,
                font=font_name,
                command=partial(self.set_node_role, selec)
            )
            self.menu_buttons.append(btn)
        btn2 = tk.Button(
                self.menu_frame,
                text='Delete',
                font=font_name,
                command=lambda: self.delete_node()
        )
        self.menu_buttons.append(btn2)
        btn3 = tk.Button(
            self.menu_frame,
            text='Modify',
            font=font_name,
            command=lambda: self.modify_node()
        )
        self.menu_buttons.append(btn3)
    def setup_combobox_events(self):
        # modo full
        self.cmb_selec.bind("<<ComboboxSelected>>",
                            lambda e: self.combobox_selection('selec'))
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
        self.ax.set_xlabel("Longitude")
        self.ax.set_ylabel("Latitude")
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

        self.menu_frame.place_forget()
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

        dx = current_seg.destination.x - current_seg.origin.x
        dy = current_seg.destination.y - current_seg.origin.y

        self.ax.arrow(current_seg.origin.x, current_seg.origin.y,
                      dx, dy, length_includes_head=True,
                      head_width=0.03, head_length=0.1,
                      fc=color, ec=color, alpha=alpha, linewidth=linewidth)

        if self.if_cost.get():
            mid_x = (current_seg.origin.x + current_seg.destination.x) / 2
            mid_y = (current_seg.origin.y + current_seg.destination.y) / 2
            self.ax.text(mid_x, mid_y, f"{current_seg.cost:.1f}",
                         color='darkred' if color == '#ef5b1c' else 'black',
                         clip_on=True, fontsize=6.5, ha='center', va='center',
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
                transform=self.ax.transData, clip_on=True
            )

        if color == '#f8c675': # nodos naranjas
            size = 8
        elif color == 'blue': #nodo seleccionado
            size = 9
        elif color == 'green' or color == '#FFA500': #nodos vecinos o nodos del camino opt
            size = 7
        elif color == '#0047AB': #nodo destino
            size = 9
        else: # nodos grises
            size = 5
        self.ax.plot(current_n.x, current_n.y, 'o', markersize=size,
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
        self.cmb_selec['values'] = [n.name for n in self.graph.nodes]
        self.cmb_origin['values'] = [n.name for n in self.graph.nodes]
        self.cmb_destination['values'] = [n.name for n in self.graph.nodes]

        if not self.selected_node:
            self.cmb_origin.set('')
            self.cmb_selec.set('')
        else:
            self.cmb_origin.set(self.selected_node.name)
        self.cmb_destination.set('')

        """Mostrar/Ocultar botones según el modo"""
        mode_widgets = {
            'full': [self.btn_save_graph, self.lbl_selec, self.cmb_selec,
                     self.btn_add_node, self.btn_add_segment,
                     self.lbl_google, self.btn_see_full_g],
            'paths': [self.lbl_origin, self.cmb_origin,
                      self.lbl_destination, self.cmb_destination,
                      self.btn_confirm, self.lbl_google,
                      self.btn_reachability_in_Gearth, self.btn_see_path_in_Gearth],
            'solonodo': [self.lbl_selec, self.cmb_selec,
                         self.lbl_google, self.btn_see_neighbors]
        }

        for widget_list in mode_widgets.values():
            for widget in widget_list:
                widget.pack_forget()

        for widget in mode_widgets.get(self.mode, []):
            widget.pack(side="left", padx=5)

        menu_widgets = {
            'full': [self.menu_buttons[3], self.menu_buttons[2]],
            'paths': [self.menu_buttons[0], self.menu_buttons[1]]
        }

        for w_list in menu_widgets.values():
            for widget in w_list:
                widget.pack_forget()

        for widget in menu_widgets.get(self.mode, []):
            widget.pack(side="left")
    def on_node_click(self, event):
        '''if event.inaxes != self.ax:
            return

        for n in self.graph.nodes:
            if ((n.x - event.xdata) ** 2 + (n.y - event.ydata) ** 2) < 0.00025:
                if event.dblclick and event.button == 1:
                    self.selected_node = n
                    if self.mode in ['full', 'solonodo']:
                        self.plot_node_neighbors(n)
                    elif self.mode == 'paths':
                        self.paths.plot_node_paths(n)
                    self.node_origin.set(n.name)  # Actualizar el menú
                    # self.node_destination.set(' ')
                    self.menu_frame.place_forget()
                    break
                elif event.button == 3 and self.mode in ('paths', 'full'):
                    clicked_node = n
                    if clicked_node:
                        self.current_clicked_node = clicked_node
                        self.show_float_menu(event, clicked_node)
                        break
            elif (event.button == 1 or event.button == 3) and self.mode in ('paths', 'full'):
                if self.current_clicked_node is None:
                    self.menu_frame.place_forget()'''
        if event.inaxes != self.ax:
            return

        clicked_node = None
        for n in self.graph.nodes:
            if ((n.x - event.xdata) ** 2 + (n.y - event.ydata) ** 2) < 0.00008:
                clicked_node = n
                break

        if not clicked_node:
            self.menu_frame.place_forget()
            self.current_clicked_node = None
            return

        # Para nodo cliqueado
        if event.dblclick and event.button == 1:
            self.selected_node = clicked_node
            if self.mode in ['full', 'solonodo']:
                self.plot_node_neighbors(clicked_node)
            elif self.mode == 'paths':
                self.paths.plot_node_paths(clicked_node)
            self.node_origin.set(clicked_node.name)
            self.menu_frame.place_forget()
        elif event.button == 3 and self.mode in ('paths', 'full'):
            self.current_clicked_node = clicked_node
            self.show_float_menu(event, clicked_node)
    def on_scroll(self, event):
        base_scale = 2
        ax = self.fig.gca()  # Obtener el eje actual

        # Obtener límites actuales
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()

        # Posición del ratón
        xdata = event.xdata
        ydata = event.ydata

        if event.button == 'up':
            new_xlim = [xdata - (xdata - xlim[0]) / base_scale,
                        xdata + (xlim[1] - xdata) / base_scale]
            new_ylim = [ydata - (ydata - ylim[0]) / base_scale,
                        ydata + (ylim[1] - ydata) / base_scale]
        elif event.button == 'down':
            new_xlim = [xdata - (xdata - xlim[0]) * base_scale,
                        xdata + (xlim[1] - xdata) * base_scale]
            new_ylim = [ydata - (ydata - ylim[0]) * base_scale,
                        ydata + (ylim[1] - ydata) * base_scale]
        else:
            return

        # Aplicar nuevos límites
        ax.set_xlim(new_xlim)
        ax.set_ylim(new_ylim)
        self.canvas.draw_idle()
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
            self.menu_frame.place_forget()
            return

        if role == 'origin':
            self.selected_node = self.current_clicked_node
            self.node_origin.set(self.current_clicked_node.name)
            self.paths.plot_node_paths(self.current_clicked_node)
        elif role == 'destination':
            self.node_destination.set(self.current_clicked_node.name)
        # Ocultar el menú después de la selección
        self.menu_frame.place_forget()
    def combobox_selection(self, combobox_type):
        for n in self.graph.nodes:
            if combobox_type == 'origin':
                origin_name = self.node_origin.get()
                if n.name == origin_name:
                    self.paths.plot_node_paths(n)
            elif combobox_type == 'selec':
                selec_name = self.node_selec.get()
                if n.name == selec_name:
                    self.plot_node_neighbors(n)
    '''Añadir elementos'''
    def crear_segmento(self):
        pyglet.font.add_file("Minecraft.ttf")
        font_name = "Minecraft"

        sub_seg = tk.Toplevel()
        sub_seg.title("Add segment")
        sub_seg.geometry("600x350+600+500")
        sub_seg.transient(self.a1)

        # Variables para los campos
        origen = tk.StringVar()
        destino = tk.StringVar()

        def confirmar():
            try:
                # Validar datos
                nombre_origen = origen.get().strip()
                nombre_destino = destino.get().strip()

                if not nombre_origen or not nombre_destino:
                    messagebox.showerror("Error", "All fields are required")
                    return

                # Verificar si los nodos existen
                origen_existe = any(n.name == nombre_origen for n in self.graph.nodes)
                destino_existe = any(n.name == nombre_destino for n in self.graph.nodes)

                if not origen_existe or not destino_existe:
                    messagebox.showerror("Error", "nodes not found")
                    return

                # Verificar si el segmento ya existe
                '''seg_existe = any(s.name == nombre_segmento for s in self.graph.segments)
                if seg_existe:
                    messagebox.showerror("Error", "There is already a segment with this name")
                    return'''

                #Segmento existente con nombre distinto
                for s in self.graph.segments:
                    if s.origin.name == nombre_origen and s.destination.name == nombre_destino:
                            messagebox.showerror("Error", f"Existed segment with name: {s.name}")
                            return

                # Añadir el nuevo segmento
                if addsegment(self.graph, nombre_origen, nombre_destino):
                    messagebox.showinfo("Success", "Segment added successfully")
                    self.plot_full_graph()  # Actualizar el gráfico
                    sub_seg.destroy()
                else:
                    messagebox.showerror("Error", "Segment could not be added")

            except Exception as e:
                messagebox.showerror("Error", f"error: {str(e)}")

        # Usar OptionMenu para seleccionar nodos existentes
        tk.Label(sub_seg, text="Origin:", font=(font_name, 15)).place(x=30, y=80)
        Combobox(
            sub_seg,
            textvariable=origen,
            font=(font_name, 15),
            values=[n.name for n in self.graph.nodes]
        ).place(x=200, y=75, width=180)

        tk.Label(sub_seg, text="Destination:", font=(font_name, 15)).place(x=30, y=130)
        Combobox(
            sub_seg,
            textvariable=destino,
            font=(font_name, 15),
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
            font=(font_name, 12),
            bg="#4CAF50",
            fg="white"
        ).pack(side="left",padx = (10, 10), pady =5)

        tk.Button(
            btn_frame,
            text="Cancel",
            command=sub_seg.destroy,
            width=12,
            height=2,
            font=(font_name, 12),
            bg="#F44336",
            fg="white"
        ).pack(side="left", pady =5)

        # Añadir lista de nodos disponibles
        texto = tk.Text(sub_seg, width=40, height=3, wrap='word')
        texto.pack(side='left',pady=(270,0),padx=10, fill='x', expand=False)

        # Crear una Scrollbar y asociarla al Text
        scrollbar = tk.Scrollbar(sub_seg, command=texto.yview)
        scrollbar.pack(side='right', fill='y')

        texto.config(yscrollcommand=scrollbar.set)
        nodos_text = ", ".join([n.name for n in self.graph.nodes])
        texto.insert("1.0", nodos_text)
        texto.config(state="disabled", font=font_name)

        '''tk.Label(sub_seg, text="Available nodes:", font=('Arial', 10)).place(x=30, y=270)
        nodos_text = " ".join([n.name for n in self.graph.nodes])
        tk.Label(sub_seg, text=nodos_text, font=('Arial', 10)).place(x=30, y=300)'''
    def crear_nodo(self):
        pyglet.font.add_file("Minecraft.ttf")
        font_name = "Minecraft"

        sub_nodo = tk.Toplevel()
        sub_nodo.title("Add node")
        sub_nodo.geometry("600x400+600+500")
        sub_nodo.transient(self.a1)

        # Variables para los campos
        numero = tk.StringVar()
        nombre = tk.StringVar()
        posx = tk.StringVar()
        posy = tk.StringVar()

        def confirmar():
            try:
                # Validar datos
                numero_nodo = numero.get().strip()
                nombre_nodo = nombre.get().strip()
                x = posx.get().strip()
                y = posy.get().strip()

                if not nombre_nodo or not x or not y or not numero_nodo:
                    messagebox.showerror("Error", "All fields are required")
                    return

                # Verificar si el nodo ya existe
                if any(n.name == nombre_nodo for n in self.graph.nodes):
                    messagebox.showerror("Error", "A node with this name already exists")
                    return
                if any(n.number == numero_nodo for n in self.graph.nodes):
                    messagebox.showerror("Error", "A node with this ID already exists")
                    return

                numero_nodo = int(numero_nodo)
                x = float(x)
                y = float(y)
                # Crear y añadir el nuevo nodo
                nuevo_nodo = NavPoint(numero_nodo, nombre_nodo, y, x)
                if addnode(self.graph, nuevo_nodo):
                    messagebox.showinfo("Éxito", "Node added successfully")
                    self.plot_full_graph()  # Actualizar el gráfico
                    sub_nodo.destroy()
                else:
                    messagebox.showerror("Error", "Node could not be added")

            except Exception as e:
                messagebox.showerror("Error", f"error: {str(e)}")

        # Interfaz de usuario
        tk.Label(sub_nodo, text="ID:", font=(font_name, 15)).place(x=30, y=20)
        tk.Entry(sub_nodo, textvariable=numero, font=(font_name, 15)).place(x=200, y=20)

        tk.Label(sub_nodo, text="Name:", font=(font_name, 15)).place(x=30, y=70)
        tk.Entry(sub_nodo, textvariable=nombre, font=(font_name, 15)).place(x=200, y=70)

        tk.Label(sub_nodo, text="Longitude:", font=(font_name, 15)).place(x=30, y=120)
        tk.Entry(sub_nodo, textvariable=posx, font=(font_name, 15)).place(x=200, y=120)

        tk.Label(sub_nodo, text="Latitude:", font=(font_name, 15)).place(x=30, y=170)
        tk.Entry(sub_nodo, textvariable=posy, font=(font_name, 15)).place(x=200, y=170)

        # Botones
        btn_frame = tk.Frame(sub_nodo)
        btn_frame.place(x=50, y=250, width=300)

        tk.Button(
            btn_frame,
            text="Confirm",
            command=confirmar,
            width=10,
            height = 2,
            font=(font_name, 12),
            bg="#4CAF50",
            fg="white"
        ).pack(side="left",padx = (10, 20))

        tk.Button(
            btn_frame,
            text="Cancel",
            command=sub_nodo.destroy,
            width=10,
            height=2,
            font=(font_name, 12),
            bg="#F44336",
            fg="white"
        ).pack(side="left")
    def delete_node(self):
        if not self.current_clicked_node:
            return

        for s in list(self.graph.segments):
            if self.current_clicked_node == s.origin or self.current_clicked_node == s.destination:
                self.graph.segments.remove(s)
        self.graph.nodes.remove(self.current_clicked_node)

        self.update_display()
        # Ocultar el menú después de la selección
        self.menu_frame.place_forget()
    def guardar_grafo(self):
        # Guardar nodos
        file_nodos = filedialog.asksaveasfilename(
            title="Guardar nodos como...",
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt")]
        )
        if file_nodos:
            with open(file_nodos, "w", encoding="utf-8") as file:
                for n in self.graph.nodes:
                    file.write(f"{n.number} {n.name} {n.y} {n.x}\n")

        # Guardar segmentos
        file_segmentos = filedialog.asksaveasfilename(
            title="Guardar segmentos como...",
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt")]
        )
        if file_segmentos:
            with open(file_segmentos, "w", encoding="utf-8") as file:
                for s in self.graph.segments:
                    file.write(f"{s.origin.number} {s.destination.number} {s.cost}\n")

        # Guardar aeropuertos
        file_aeropuertos = filedialog.asksaveasfilename(
            title="Guardar aeropuertos como...",
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt")]
        )
        if file_aeropuertos:
            with open(file_aeropuertos, "w", encoding="utf-8") as file:
                for a in Airport_list:
                    file.write(a.name)
                    for b in a.sid:
                        file.write(b)
                    for c in a.star:
                        file.write(c)

    def modify_node(self):
        pyglet.font.add_file("Minecraft.ttf")
        font_name = "Minecraft.ttf"

        self.menu_frame.place_forget()
        print (self.current_clicked_node)

        sub2_nodo = tk.Toplevel()
        sub2_nodo.title("Modify Node")
        sub2_nodo.geometry("600x400+600+500")
        sub2_nodo.transient(self.a1)

        # Variables para los campos (pre-llenadas con los valores actuales)
        numero = tk.StringVar(value=self.current_clicked_node.number)
        nombre = tk.StringVar(value=self.current_clicked_node.name)
        posx = tk.StringVar(value=str(self.current_clicked_node.x))
        posy = tk.StringVar(value=str(self.current_clicked_node.y))

        def confirmar():
            try:
                # Validar datos
                numero_nodo = int(numero.get().strip())
                nombre_nodo = nombre.get().strip()
                x = float(posx.get().strip())
                y = float(posy.get().strip())

                # Verificar si el nuevo nombre/ID ya existe (excepto para el nodo actual)
                for n in self.graph.nodes:
                    if n != self.current_clicked_node:  # Ignorar el nodo que estamos modificando
                        if n.name == nombre_nodo:
                            messagebox.showerror("Error", "A node with this name already exists")
                            return
                        if n.number == numero_nodo:
                            messagebox.showerror("Error", "A node with this ID already exists")
                            return

                # Actualizar el nodo
                self.current_clicked_node.number = numero_nodo
                self.current_clicked_node.name = nombre_nodo
                self.current_clicked_node.x = x
                self.current_clicked_node.y = y

                messagebox.showinfo("Success", "Node modified successfully")
                self.plot_full_graph()  # Actualizar el gráfico
                sub2_nodo.destroy()

            except ValueError:
                messagebox.showerror("Error", "Invalid coordinates (must be numbers)")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

        # Interfaz de usuario
        tk.Label(sub2_nodo, text="ID:", font=(font_name, 15)).place(x=30, y=20)
        tk.Entry(sub2_nodo, textvariable=numero, font=(font_name, 13)).place(x=200, y=20)

        tk.Label(sub2_nodo, text="Name:", font=(font_name, 15)).place(x=30, y=70)
        tk.Entry(sub2_nodo, textvariable=nombre, font=(font_name, 13)).place(x=200, y=70)

        tk.Label(sub2_nodo, text="Longitude:", font=(font_name, 15)).place(x=30, y=120)
        tk.Entry(sub2_nodo, textvariable=posx, font=(font_name, 13)).place(x=200, y=120)

        tk.Label(sub2_nodo, text="Latitude:", font=(font_name, 15)).place(x=30, y=170)
        tk.Entry(sub2_nodo, textvariable=posy, font=(font_name, 13)).place(x=200, y=170)

        # Botones
        btn_frame = tk.Frame(sub2_nodo)
        btn_frame.place(x=50, y=250, width=300)

        tk.Button(
            btn_frame,
            text="Confirm",
            command=confirmar,
            width=10,
            height=2,
            font=(font_name, 12),
            bg="#4CAF50",
            fg="white"
        ).pack(side="left", padx=(10, 20))

        tk.Button(
            btn_frame,
            text="Cancel",
            command=sub2_nodo.destroy,
            width=10,
            height=2,
            font=(font_name, 12),
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



