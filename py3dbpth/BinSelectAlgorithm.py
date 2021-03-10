# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 17:43:44 2021

@author: Tobias Hirt
"""

from .Bin import Bin

#from .ShelfSheet import Shelf
#from .ShelfSheet import Sheet
from .FakeSkyline import FakeSkyline 

class BinSelectAlgorithm:
    
    def __init__(self, packer):
        
        self.bin_select_algorithm = packer.bin_select_algorithm
        self.bin_select_dimension = packer.bin_select_dimension
        
        dim_dict = {
            "volume": Bin.get_remaining_volume_item,
            "aspect_ratio": Bin.get_aspect_ratio_diff
            }        

        algo_dict = {
            "fake_skyline": FakeSkyline(packer),
            #"shelf": Sheet(packer),
            #"maximal_rectangle": MaximalRectangle(packer),
            #"skyline": Skyline(packer),
            }

        f_dim = dim_dict[packer.bin_select_dimension]
        f_algo = algo_dict[packer.packing_algorithm]        
        
        if self.bin_select_algorithm == "first_fit":          
            # äußere Schleife -> "quick & dirty" workaround
            # während schleife läuft werden dynamisch elemente aus der
            # "SchleifenIterationenbestimmenden" Liste entfernt  
            
            for qd in range(0,len(packer.items_to_pack)):
                for item in packer.items_to_pack:
                    for bin in packer.bins:
                        if f_algo.pack_to_bin(bin, item): #returns true if Item i can be packed into Bin j
                            break
                    
        elif self.bin_select_algorithm == "best_fit":
            # äußere Schleife -> "quick & dirty" workaround
            # während schleife läuft werden dynamisch elemente aus der
            # "SchleifenIterationenbestimmenden" Liste entfernt    

            #while packer.items_to_pack: #Danger of infinite number of iterations
            for qd in range(0,len(packer.items_to_pack)):
                for item in packer.items_to_pack:
                    item_packed = False
                    packer.bins.sort(key=lambda bin: f_dim(bin,item))
                    for b in packer.bins:
                        if f_algo.pack_to_bin(b, item): #returns true if Item i can be packed into Bin j
                            item_packed = True
                            break
                    if item_packed == True:
                        break

        elif self.bin_select_algorithm == "worst_fit":
            # äußere Schleife -> "quick & dirty" workaround
            # während schleife läuft werden dynamisch elemente aus der
            # "SchleifenIterationenbestimmenden" Liste entfernt

            #while packer.items_to_pack: #Danger of infinite number of iterations
            for qd in range(0,len(packer.items_to_pack)):
                for item in packer.items_to_pack:
                    item_packed = False
                    packer.bins.sort(key=lambda bin: f_dim(bin,item), reverse=True)
                    for b in packer.bins:
                        if f_algo.pack_to_bin(b, item): #returns true if Item i can be packed into Bin j
                            item_packed = True
                            break
                    if item_packed == True:
                        break
        
        packer.bins.sort(key=lambda bin: bin.index)
        packer.assignment_matrix=packer.assignment_matrix.astype(int)  
        packer.get_active_bins()
        