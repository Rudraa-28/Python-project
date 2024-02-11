import tkinter as tk
from tkinter import ttk

class TransportMapApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Transportation Network Map")

        self.canvas = tk.Canvas(self.master, width=400, height=400, background="white")
        self.canvas.pack(side=tk.LEFT)

        self.stations = {
            1: (100, 100),
            2: (200, 100),
            3: (300, 100),
            4: (100, 200),
            5: (200, 200),
            6: (300, 200),
            7: (100, 300),
            8: (200, 300),
            9: (300, 300),
            10: (200, 400),
        }

        self.connections = {
            1: [2, 4],
            2: [1, 3, 5, 6],
            3: [2, 7],
            4: [1, 8],
            5: [2, 9],
            6: [2, 9],
            7: [3],
            8: [4, 10],
            9: [5, 6, 10],
            10: [8, 9],
        }

        self.costs = {
            1: 2.50,
            2: 3.00,
            3: 2.75,
            4: 2.90,
            5: 3.20,
            6: 2.60,
            7: 3.10,
            8: 2.80,
            9: 3.30,
            10: 2.95,
        }

        self.speed = 30  # speed in km/h

        self.start_label = ttk.Label(self.master, text="From Station:")
        self.start_station_var = tk.StringVar()
        self.start_station_dropdown = ttk.Combobox(self.master, textvariable=self.start_station_var, values=list(map(str, self.stations.keys())))

        self.end_label = ttk.Label(self.master, text="To Station:")
        self.end_station_var = tk.StringVar()
        self.end_station_dropdown = ttk.Combobox(self.master, textvariable=self.end_station_var, values=list(map(str, self.stations.keys())))

        self.calculate_button = ttk.Button(self.master, text="Calculate Routes", command=self.calculate_routes)

        self.result_label = ttk.Label(self.master, text="Result will be displayed here.")
        self.route_frame = ttk.Frame(self.master)
        self.route_buttons = []

        self.start_label.pack(pady=5)
        self.start_station_dropdown.pack(pady=5)
        self.end_label.pack(pady=5)
        self.end_station_dropdown.pack(pady=5)
        self.calculate_button.pack(pady=10)
        self.result_label.pack(pady=10)
        self.route_frame.pack(side=tk.RIGHT, padx=10)

        self.draw_map()

    def draw_map(self):
        for station, (x, y) in self.stations.items():
            self.canvas.create_text(x, y, text=f"Station {station}", font=("Helvetica", 8), fill="black")
            self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, outline="black", fill="white")

        for station, connections in self.connections.items():
            x1, y1 = self.stations[station]
            for connected_station in connections:
                x2, y2 = self.stations[connected_station]
                cost = self.calculate_cost(station, connected_station)
                self.canvas.create_line(x1, y1, x2, y2, fill="lightgray", width=2)
                label_x, label_y = (x1 + x2) / 2, (y1 + y2) / 2
                self.canvas.create_text(label_x, label_y, text=f"{cost:.2f}£", font=("Helvetica", 8), fill="blue")

    def calculate_cost(self, from_station, to_station):
        return abs(self.costs[from_station] - self.costs[to_station])

    def highlight_route(self, route):
        self.canvas.delete("highlight")  # Remove previous highlighting

        for i in range(len(route) - 1):
            station1, station2 = route[i], route[i + 1]
            x1, y1 = self.stations[station1]
            x2, y2 = self.stations[station2]
            self.canvas.create_line(x1, y1, x2, y2, fill="red", width=2, tags="highlight")

    def calculate_routes(self):
        start_station = int(self.start_station_var.get())
        end_station = int(self.end_station_var.get())

        if start_station not in self.stations or end_station not in self.stations:
            self.result_label.config(text="Invalid station selection. Please choose valid stations.")
            return

        all_routes = self.find_all_routes(start_station, end_station)

        if not all_routes:
            self.result_label.config(text="No route found between the selected stations.")
            return

        self.display_all_routes(all_routes)

    def find_all_routes(self, start, end, visited=set(), path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if start not in self.connections:
            return []
        routes = []
        visited.add(start)
        for station in self.connections[start]:
            if station not in visited:
                new_routes = self.find_all_routes(station, end, visited.copy(), path)
                for r in new_routes:
                    routes.append(r)
        return routes

    def display_all_routes(self, all_routes):
        for widget in self.route_frame.winfo_children():
            widget.destroy()  # Clear previous route buttons

        result_text = "All possible routes:\n"
        for i, route in enumerate(all_routes, 1):
            route_str = " -> ".join([f"Station {station}" for station in route])
            cost = sum(self.calculate_cost(route[i], route[i + 1]) for i in range(len(route) - 1))
            result_text += f"{i}. {route_str} (Cost: {cost:.2f}£)\n"

            route_button = ttk.Button(self.route_frame, text=f"Go with Route {i}", command=lambda r=route: self.highlight_route(r))
            route_button.pack(pady=5)
            self.route_buttons.append(route_button)

        self.result_label.config(text=result_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = TransportMapApp(root)
    root.mainloop()
