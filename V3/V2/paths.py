from node import *

from queue import PriorityQueue
from tkinter import messagebox
from collections import deque

class Paths:
    def __init__(self, graph, ax, control_frame, drawing):
        self.graph = graph
        self.ax = ax
        self.control_frame = control_frame

        #referencias de InteractiveGraph
        self.draw_node = drawing['draw_node']
        self.draw_segment = drawing['draw_segment']
        self.finish_plot = drawing['finish_plot']

        self.lbl_cost = None

    def optimal_path(self, origin_name, destination_name):
        origin_node = None
        destination_node = None

        for n in self.graph.nodes:
            if n.name == origin_name:
                origin_node = n
            if n.name == destination_name:
                destination_node = n

        if not origin_node or not destination_node:
            messagebox.showerror("Error", "Nodes not found")
            return None

        frontier = PriorityQueue()
        frontier.put((0, origin_node))  # (prioridad, nodo)
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

        total_cost = cost_so_far.get(destination_node, float('inf'))
        print(path, total_cost)

        if total_cost != float('inf'):
            path_segments = []
            i = 0
            while i < len(path) - 1:
                segment1 = next(s for s in self.graph.segments
                                if s.origin == path[i] and s.destination == path[i + 1])
                path_segments.append(segment1)
                i += 1

            self.plot_node_paths(origin_node, destination_node, path_segments, path)
        else:
            messagebox.showerror("Error", "Path does not exist")

        return path,total_cost
    def plot_node_paths(self, origin_node, dest_node = None, opt_path = None, opt_node = None):
        # Inicializar listas mutables
        opt_path = [] if opt_path is None else opt_path
        opt_node = [] if opt_node is None else opt_node

        self.ax.clear()
        #self.selected_node = origin_node
        visited = set()
        contra_opt_path_segments = set()
        queue = deque([(origin_node, [origin_node])])

        #Dibujar los nodos
        for n in self.graph.nodes:
            if n in opt_node:
                    self.draw_node(n, '#FFA500')
            else:
                self.draw_node(n, 'lightgray')

        if dest_node:
            self.draw_node(dest_node, '#0047AB')
        self.draw_node(origin_node, 'blue')

        #Dibujar los caminos
        while queue:
            current_node, path = queue.popleft()

            if current_node not in visited:
                visited.add(current_node)

                if (current_node != origin_node and
                        current_node != dest_node and
                        current_node not in opt_node):
                    self.draw_node(current_node, 'green')

                for seg in self.graph.segments:
                    for s in opt_path:
                        if s.origin == seg.destination and s.destination == seg.origin:
                            contra_opt_path_segments.add(seg)
                            continue

                    if seg in opt_path:
                        self.draw_segment(seg, '#FFD700')
                    elif (seg not in contra_opt_path_segments and
                            seg.origin == current_node and
                            seg.destination != current_node and
                            seg.destination != origin_node):
                        self.draw_segment(seg, 'red')

            for neighbor in current_node.neighbors:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))

        self.finish_plot('')