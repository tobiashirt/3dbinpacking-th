from .constants import Axis

from .BinSorting import BinSorting
from .ItemSorting import ItemSorting
from .BinSelectAlgorithm import BinSelectAlgorithm
from .FakeSkyline import FakeSkyline

import copy
import math
import numpy as np
import matplotlib.pyplot as plt

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
        
        self.bins = []
        self.bin_index = 0
        self.total_bins = 0
        
        self.orders = []
        self.order_index = 0
        self.total_orders = 0
        
        self.tubs = []
        self.tub_index = 0
        self.total_tubs = 0
        
        self.items = []
        self.item_index = 0
        self.total_items = 0
        
        self.items_to_pack = []
        self.unpacked_items = []
        
        self.sequence = []
        self.assignment_matrix = np.zeros(shape=(1,1))

    def add_bin(self, bin):
        self.total_bins = len(self.bins) + 1
        bin.index = len(self.bins)
        return self.bins.append(bin)
    
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
    
    def get_active_bins(self):
        active_bins = list()
        for j in self.bins:
            if j.items:
                active_bins.append(j)
        return active_bins
    
    def get_active_bins_volume(self):
        active_bins_volume = 0
        for b in self.get_active_bins():
            active_bins_volume += b.get_volume()
        return active_bins_volume
    
    def add_order(self, order):
        self.total_orders = len(self.orders) + 1
        order.index = len(self.orders)
        for t in order.tubs:
            self.add_tub(t)
        for i in order.items:
            self.add_item(i)
        return self.orders.append(order)
    
    def add_tub(self, tub):
        self.total_tubs = len(self.tubs) + 1
        tub.index = len(self.tubs)
        for i in tub.items:
            i.in_tub=tub.index
        for i in tub.items:
            self.add_item(i)
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
        print("Bin_Select_Algo: "+str(self.bin_select_algorithm)+
              " | Bin_Select_Dim: "+str(self.bin_select_dimension)+
              " | Packing Algorithm: "+str(self.packing_algorithm)+
              " | Packing Heuristic: "+str(self.packing_heuristic)+
              " | Bin_Sorting: "+str(self.bin_sorting)+
              " | Item_Sorting: "+str(self.item_sorting))
        print("V_bins: "+str(self.get_bins_volume())+" | V_remaining: "+str(self.get_bins_remaining_volume())+
              " | V_a_bins: "+str(self.get_active_bins_volume())+" | Objective: "+str(self.objective_value()))
        print(self.assignment_matrix)
        print("Remaining Items: "+self.get_remaining_items())
        return ""
    
    def plot_packing(self):
        
        n = math.floor(math.sqrt(self.total_bins))
        m = math.ceil(math.sqrt(self.total_bins))
        
        while n*m < self.total_bins:
            m += 1
        
        fig, axes = plt.subplots(n,m, figsize=(m*6,n*6))
        # fig, axes = plt.subplots(1,3, figsize=(15,6))
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

    def pack(
        self, bin_select_algorithm = "first_fit", bin_select_dimension = "volume", packing_algorithm = "fake_skyline",  
        packing_heuristic="bottom_left", bin_sorting="-", item_sorting="-"):
                
        self.items_to_pack = copy.copy(self.items)
        
        self.bin_sorting = bin_sorting
        self.item_sorting = item_sorting
        self.bin_select_algorithm = bin_select_algorithm
        self.bin_select_dimension = bin_select_dimension
        self.packing_algorithm = packing_algorithm
        self.packing_heuristic = packing_heuristic
        
        self.assignment_matrix = np.zeros(shape=(len(self.bins),len(self.items)))
        
        for bin in self.bins:
            self.sequence.append([])
        
        # Bin Sortierung
        if bin_sorting != "-":
            BinSorting(self)
        
        # Item Sortierung
        if item_sorting != "-":
            ItemSorting(self)
        
        # BinSelect Algorithmus
        BinSelectAlgorithm(self)
        
        # Packalgorithmus mit spezifischer Packheuristik wird vom BinSelectAlgorithm aufgerufen
        # TODO: 3D Shelf implementieren
        
