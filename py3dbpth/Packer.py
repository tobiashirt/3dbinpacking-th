from .constants import Axis

from .BinSorting import BinSorting
from .ItemSorting import ItemSorting
from .BinSelectAlgorithm import BinSelectAlgorithm
from .FakeSkyline import FakeSkyline

import copy
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

START_POSITION = [0, 0, 0]

class Packer:
    def __init__(self):
        
        self.bin_sorting = None
        self.item_sorting = None
        self.bin_select_algorithm = None
        self.bin_select_dimension = None
        self.packing_algorithm = None
        self.packing_heuristic = None
        
        self.bin_types = []
        self.bins = []
        self.bin_index = 0
        self.total_bins = 0
        
        self.orders = []
        self.order_index = 0
        self.total_orders = 0
        
        self.order_positions = []
        self.order_position_index = 0
        self.total_order_positions = 0
        
        self.tubs = []
        self.tub_index = 0
        self.total_tubs = 0
        
        self.items = []
        self.item_index = 0
        self.total_items = 0
        
        #per order
        self.items_to_pack = []
        self.bins_to_use = []
        
        self.item_sequences = []
        self.tub_sequences = []
        self.item_bin_assignment_matrix = np.zeros(shape=(1,1))
        self.bin_order_assignment_matrix = np.chararray(shape=(1,1), itemsize=3)
        self.utilization = 1.0

    def add_bin(self, bin):
        self.total_bins = len(self.bins) + 1
        bin.index = len(self.bins)
        return self.bins.append(bin)
    
    def add_bin_type(self, bin):
        return self.bin_types.append(bin)
    
    def add_bins_to_use(self, bin):
        return self.bins_to_use.append(bin)
    
    def add_empty_bin_from_type(self):
        if len(self.get_empty_bins()) != len(self.bin_types):
            for bt in self.bin_types:
                for eb in self.get_empty_bins():
                    if bt.type != eb.type:
                        #print("add_empty_bin_from_type: "+str(bt.type))
                        return self.add_bins_to_use(copy.deepcopy(bt))
        else:
            return self.bins
    
    def get_bins_volume(self):
        bins_volume = 0
        for b in self.bins:
            bins_volume += b.get_volume()
        return bins_volume
    
    def get_bins_remaining_volume(self):
        bins_remaining_volume = 0
        for b in self.bins:
            bins_remaining_volume += b.get_remaining_volume()
        return bins_remaining_volume
    
    def get_utilization(self):
        self.utilization = self.get_bins_remaining_volume()/self.get_bins_volume()
        return (self.get_bins_volume()-self.get_bins_remaining_volume())/self.get_bins_volume()
    
    def get_empty_bins(self):
        empty_bins = list()
        for j in self.bins_to_use:
            if not j.items:
                empty_bins.append(j)
        return empty_bins
        
    def get_active_bins(self):
        active_bins = list()
        for j in self.bins_to_use:
            if j.items:
                active_bins.append(j)
        return active_bins
    
    def get_active_bins_volume(self):
        active_bins_volume = 0
        for b in self.get_active_bins():
            active_bins_volume += b.get_volume()
        return active_bins_volume
    
    def add_orders(self, orders):
        for o in orders:
            self.add_order(o)
        return
    
    # Main Way to add things to pack
    def add_order(self, order):
        self.total_orders = len(self.orders) + 1
        order.index = len(self.orders)
        for op in order.order_positions:
            self.add_order_position(op)
        for t in order.tubs:
            self.add_tub(t)
        for i in order.items:
            self.add_item(i)
        return self.orders.append(order)
    
    def add_order_position(self, order_position):
        self.total_order_positions = len(self.order_positions) + 1
        order_position.index = len(self.order_positions)
        return self.order_positions.append(order_position)
    
    def add_tub(self, tub):
        self.total_tubs = len(self.tubs) + 1
        tub.index = len(self.tubs)
        return self.tubs.append(tub)

    def add_item(self, item):
        self.total_items = len(self.items) + 1
        item.index = len(self.items)
        return self.items.append(item)
    
    def get_remaining_items(self):
        result = ""
        for i in self.items_to_pack:
            result += str(i.index)+","
        result = result[:-1]
        return result
    
    def objective_value(self): 
        result = 0
        for j in self.get_active_bins():
            result += j.get_volume()
            for i in j.items:
                result = result - i.get_volume()
        return result
    
    def __str__(self):        
        result = "Bin_Select_Algo: "+str(self.bin_select_algorithm)+" | Bin_Select_Dim: "+str(self.bin_select_dimension)+" | Packing Algorithm: "+str(self.packing_algorithm)+" | Packing Heuristic: "+str(self.packing_heuristic)+" | Bin_Sorting: "+str(self.bin_sorting)+" | Item_Sorting: "+str(self.item_sorting)
        result = result + "\n V_bins: "+str(self.get_bins_volume())+" | V_remaining: "+str(self.get_bins_remaining_volume())
         
        return result
    
    def plot_packing(self):
        
        n = math.floor(math.sqrt(self.total_bins))
        m = math.ceil(math.sqrt(self.total_bins))
        
        while n*m < self.total_bins:
            m += 1
        
        fig, axes = plt.subplots(n,m, figsize=(m*6,n*6))
        
        for k in range(n):
            for l in range(m):
        # for l in range(3):
                axes[k,l].axis('off')
            # axes[l].axis('off')

        fig.suptitle("Bin_Select_Algo: "+str(self.bin_select_algorithm)+
                     " | Bin_Select_Dim: "+str(self.bin_select_dimension)+
                     "\n | Packing Algorithm: "+str(self.packing_algorithm)+
                     " | Packing Heuristic: "+str(self.packing_heuristic)+
                     "\n | Bin_Sorting: "+str(self.bin_sorting)+
                     " | Item_Sorting: "+str(self.item_sorting)+"\n\n"+
                     "V_bins: "+str(self.get_bins_volume())+" | V_remaining: "+str(self.get_bins_remaining_volume())+
                     " | V_a_bins: "+str(self.get_active_bins_volume())+" | Objective: "+str(self.objective_value())+
                     " | Remaining Items: "+self.get_remaining_items()+"\n\n")
        
        for j in self.bins:
            for k in range(n):
                for l in range(m):
            # for l in range(3):
                    axes[k,l]=fig.add_subplot(n,m,j.index+1, projection='3d')
                    j.plot_bin(axes[k,l])
                # axes[l]=fig.add_subplot(1,3,j.index+1, projection='3d')
                # j.plot_bin(axes[l])
                    
        plt.tight_layout()
        plt.show()

        return
    
    def set_packing_approach(self,
                             bin_select_algorithm: str = "first_fit", bin_select_dimension: str = "volume", 
                             packing_algorithm: str = "fake_skyline", packing_heuristic: str = "bottom_left", 
                             bin_sorting: str = "-", item_sorting: str = "-"):
                
        self.bin_sorting = bin_sorting
        self.item_sorting = item_sorting
        self.bin_select_algorithm = bin_select_algorithm
        self.bin_select_dimension = bin_select_dimension
        self.packing_algorithm = packing_algorithm
        self.packing_heuristic = packing_heuristic

    def pack_items(self, items):
        self.items_to_pack = copy.copy(items)
        self.bins_to_use = copy.deepcopy(self.bin_types)
        
        # Bin Sortierung
        if self.bin_sorting != "-":
            BinSorting(self)
        
        # Item Sortierung
        if self.item_sorting != "-":
            ItemSorting(self)
        
        # BinSelect Algorithmus
        BinSelectAlgorithm(self)

    def pack_order(self, order):
        
        for b in self.bin_types:
            if b.type in order.allowed_PM:
                self.bins_to_use.append(copy.deepcopy(b))
        
        # Bin Sortierung
        if self.bin_sorting != "-":
            BinSorting(self)
        
        self.items_to_pack = copy.copy(order.items)
        # Item Sortierung
        if self.item_sorting != "-":
            ItemSorting(self)
        
        # BinSelect Algorithmus
        BinSelectAlgorithm(self)
        
        for b in self.get_active_bins():
            self.add_bin(b)
            self.item_sequences.append([])
            self.item_sequences[b.index].extend(b.item_sequence)
            self.tub_sequences.append([])
            self.tub_sequences[b.index].extend(b.tub_sequence)
        
        order.finish_order(self.get_active_bins())
        self.reset_for_next_order()
        
    def reset_for_next_order(self):
        # self.order_positions = []
        # self.order_position_index = 0
        # self.tubs = []
        # self.tub_index = 0
        self.bins_to_use = []

    def pack(self, orders = [], items = []):   
        
        print("Packing Orders")
        for o in orders:
            print(o.name)
            self.add_order(o)
            self.pack_order(o)
        
        if items:
            print("packing NonOrder Items")
            self.pack_items(items)
            
        print("Create Assignment Matrices")
        self.item_bin_assignment_matrix = np.zeros(shape=(len(self.bins),len(self.items)))
        for b in self.bins:
            for i in b.items:
                self.item_bin_assignment_matrix[b.index,i.index]=1
        self.item_bin_assignment_matrix = self.item_bin_assignment_matrix.astype(int)
        
        self.bin_order_assignment_matrix = np.chararray(shape=(len(self.orders),len(self.bins)), itemsize=3)
        for o in self.orders:
            for b in self.bins:
                if b.items[0].order == o:
                    self.bin_order_assignment_matrix[o.index, b.index] = str(b.type)
                else:
                    self.bin_order_assignment_matrix[o.index, b.index] = "   "
                    
        self.utilization = self.get_utilization()
