import networkx as nx
import matplotlib.pyplot as plt
import ttkbootstrap as ttk
import searchingAlgorithm as sa
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from ttkbootstrap.constants import *
from dataStructure import *
from graphImage import *
import sys

class main_app(ttk.Frame):

    def __init__(self, master):
        # read city adjacencies and it's coordinates
        edges = pd.read_csv('coordinates.csv', names=['city', 'longitude', 'latitude'])
        with open("adjacencies.txt") as f:
            adjacencies = f.readlines()
            
        super().__init__(master, padding=(20, 10))
        self.pack(fill=BOTH, expand=YES)
        self.algorithm_items = ['Breadth First Search (BFS)', 'Depth First Search (DFS)', 'ID-DFS', 'Best First Search', 'A Star Algorithm']
        self.city_items = self.get_city_list()
        self.cities = weightedBidirectionalGraph(edges, adjacencies)

        # --- Create Form --- #
        
        # form header
        hdr_txt = "Searching Algorithm" 
        hdr = ttk.Label(master=self, text=hdr_txt, width=50)
        hdr.pack(fill=X, pady=10)

        # form entries
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)
        
        lbl = ttk.Label(master=container, text="Start City", width=10)
        lbl.pack(side=LEFT, padx=5)
        
        container_end = ttk.Frame(self)
        container_end.pack(fill=X, expand=YES, pady=5)
        
        lbl_end = ttk.Label(master=container_end, text="End City", width=10)
        lbl_end.pack(side=LEFT, padx=5)
        
        container_algorithm = ttk.Frame(self)
        container_algorithm.pack(fill=X, expand=YES, pady=5)
        
        lbl_algorithm = ttk.Label(master=container_algorithm, text="Algorithm", width=10)
        lbl_algorithm.pack(side=LEFT, padx=5)
        
        self.start_city_box = ttk.Combobox(container, bootstyle="info", values=self.city_items, state="readonly")
        self.start_city_box.pack(side=LEFT, padx=5, fill=X, expand=YES)
        self.start_city_box.current(0)
        
        self.end_city_box = ttk.Combobox(container_end, bootstyle="info", values=self.city_items, state="readonly")
        self.end_city_box.pack(side=LEFT, padx=5, fill=X, expand=YES)
        self.end_city_box.current(0)
        
        self.algorithm_box = ttk.Combobox(container_algorithm, bootstyle="info", values=self.algorithm_items, state="readonly")
        self.algorithm_box.pack(side=LEFT, padx=5, fill=X, expand=YES)
        self.algorithm_box.current(0)
        
        # form buttons
        container_btn = ttk.Frame(self)
        container_btn.pack(fill=X, expand=YES, pady=(15, 10))
        
        cnl_btn = ttk.Button(
            master=container_btn,
            text="View All Possible Path",
            command=self.getAllPossiblePath,
            bootstyle=INFO,
            width="auto",
        )
        cnl_btn.pack(side=RIGHT, padx=5)

        sub_btn = ttk.Button(
            master=container_btn,
            text="Find the Best Path",
            command=self.getNodePath,
            bootstyle=SUCCESS,
            width='auto',
        )
        sub_btn.pack(side=RIGHT, padx=5)
        sub_btn.focus_set()
        
        # result data
        container_1 = ttk.Frame(self)
        container_1.pack(fill=X, expand=YES, pady=5)
        
        lbl_1 = ttk.Label(master=container_1, text="Paths Found:", font="bold")
        lbl_1.pack(side=LEFT, padx=5)
        
        self.lbl_11 = ttk.Label(master=container_1, text="")
        self.lbl_11.pack(side=LEFT)
        
        container_2 = ttk.Frame(self)
        container_2.pack(fill=X, expand=YES, pady=5)
        
        lbl_2 = ttk.Label(master=container_2, text="Total Time (in seconds):", font="bold")
        lbl_2.pack(side=LEFT, padx=5)
        
        self.lbl_22 = ttk.Label(master=container_2, text="")
        self.lbl_22.pack(side=LEFT)
        
        container_3 = ttk.Frame(self)
        container_3.pack(fill=X, expand=YES, pady=5)
        
        lbl_3 = ttk.Label(master=container_3, text="Total Distance from start to end:", font="bold")
        lbl_3.pack(side=LEFT, padx=5)
        
        self.lbl_33 = ttk.Label(master=container_3, text="")
        self.lbl_33.pack(side=LEFT)
        
        container_4 = ttk.Frame(self)
        container_4.pack(fill=X, expand=YES, pady=5)
        
        lbl_4 = ttk.Label(master=container_4, text="Total Distance from node to node in euclidian:", font="bold")
        lbl_4.pack(side=LEFT, padx=5)
        
        self.lbl_44 = ttk.Label(master=container_4, text="")
        self.lbl_44.pack(side=LEFT, expand=YES)

    def create_form_entry(self, label, variable):
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)

        lbl = ttk.Label(master=container, text=label.title(), width=10)
        lbl.pack(side=LEFT, padx=5)

        ent = ttk.Entry(master=container, textvariable=variable)
        ent.pack(side=LEFT, padx=5, fill=X, expand=YES)

    def create_buttonbox(self):
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=(15, 10))
        
        cnl_btn = ttk.Button(
            master=container,
            text="View All Possible Path",
            command=self.on_cancel,
            bootstyle=INFO,
            width="auto",
        )
        cnl_btn.pack(side=RIGHT, padx=5)

        sub_btn = ttk.Button(
            master=container,
            text="Find the Best Path",
            command=self.on_submit,
            bootstyle=SUCCESS,
            width='auto',
        )
        sub_btn.pack(side=RIGHT, padx=5)
        sub_btn.focus_set()
    
    def create_combobox(self, label, variable, item_list):
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)
        
        lbl = ttk.Label(master=container, text=label.title(), width=10)
        lbl.pack(side=LEFT, padx=5)
        
        combo_box = ttk.Combobox(container, bootstyle="info", values=item_list, state="readonly")
        combo_box.pack(side=LEFT, padx=5, fill=X, expand=YES)
        combo_box.current(0)
    
    def create_checkbox(self, label, var_data):
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)
        
        check_button = ttk.Checkbutton(master=container, bootstyle="info, square-toggle", text=label, variable=var_data, onvalue=1, offvalue=0)
        check_button.pack(side=LEFT, padx=5, fill=X, expand=YES)
    
    def get_city_list(self):
        city_adjacencies = []
        with open("adjacencies.txt") as f:
            adjacencies = f.readlines()
        
        for i in adjacencies:
            city1, city2 = i.split()
            city_adjacencies.append(city1)
            city_adjacencies.append(city2)
        
        return sorted(list(set(city_adjacencies)))

    def getNodePath(self):
        node_path = sa.findPath(self.algorithm_box.get(), self.cities, self.start_city_box.get(), self.end_city_box.get())
        self.lbl_11.config(text = " -> ".join(node_path[0][::-1]))
        self.lbl_22.config(text = f"{node_path[2]} s")
        self.lbl_33.config(text = f"{node_path[1][0]} euclidian unit")
        self.lbl_44.config(text = f"{node_path[1][1]}")
        print(node_path[0])
        displayGraphImage(node_path[0])

    def getAllPossiblePath(self):
        displayAllNodesinGraph()
        
    def on_view_all_path(self):
        self.quit()
        
if __name__ == "__main__":
    # launch application
    app = ttk.Window("Azaria, Fairuz | 2023FS-COMP_SCI-461-0002", "superhero", resizable=(True, False))
    main_app(app)
    app.mainloop()
    
