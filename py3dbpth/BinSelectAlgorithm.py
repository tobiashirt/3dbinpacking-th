# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 17:43:44 2021

@author: Tobias Hirt
"""

from .Bin import Bin

from .FakeSkyline import FakeSkyline 

class BinSelectAlgorithm:
    
    def __init__(self, packer):
        
        self.bin_select_algorithm = packer.bin_select_algorithm
        self.bin_select_dimension = packer.bin_select_dimension

        algo_dict = {
            "fake_skyline": FakeSkyline(packer),
            #"shelf": Sheet(packer),
            #"maximal_rectangle": MaximalRectangle(packer),
            #"skyline": Skyline(packer),
            }
        
        dim_dict = {
            "-": Bin.get_volume, #RandomFunction
            "volume": Bin.get_remaining_volume_item,
            "aspect_ratio": Bin.get_aspect_ratio_diff,
            "longest_side": Bin.get_longest_side_diff
            } 

        f_algo = algo_dict[packer.packing_algorithm] 
        f_dim = dim_dict[packer.bin_select_dimension]
    
        if self.bin_select_algorithm == "first_fit":           
            
            while packer.items_to_pack: #Danger of infinite number of iterations
                packer.add_empty_bin_from_type()
                for item in packer.items_to_pack:
                    item_packed = False
                    for bin in packer.bins_to_use:
                        if f_algo.pack_virtual_to_bin(bin, item): #returns true if Item i can be packed into Bin j
                            item_packed = True
                            break
                    if item_packed == True:
                        break
                    
        elif self.bin_select_algorithm == "best_fit":   

            while packer.items_to_pack: #Danger of infinite number of iterations
                packer.add_empty_bin_from_type()
                for item in packer.items_to_pack:
                    item_packed = False
                    packer.bins_to_use.sort(key=lambda bin: f_dim(bin,item))
                    for b in packer.bins_to_use:
                        if f_algo.pack_virtual_to_bin(b, item): #returns true if Item i can be packed into Bin j
                            item_packed = True
                            break
                    if item_packed == True:
                        break

        elif self.bin_select_algorithm == "worst_fit":

            while packer.items_to_pack: #Danger of infinite number of iterations
                packer.add_empty_bin_from_type()    
                for item in packer.items_to_pack:
                    item_packed = False
                    packer.bins_to_use.sort(key=lambda bin: f_dim(bin,item), reverse=True)
                    for b in packer.bins_to_use:
                        if f_algo.pack_virtual_to_bin(b, item): #returns true if Item i can be packed into Bin j
                            item_packed = True
                            break
                    if item_packed == True:
                        break
        
        packer.bins.sort(key=lambda bin: bin.index)
        