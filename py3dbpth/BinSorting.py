# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 10:55:05 2021

@author: Tobias Hirt
"""

from .Bin import Bin

class BinSorting:
    
    def __init__(self,packer):
        
        self.string = packer.bin_sorting
        self.decreasing = None
        if self.string.startswith("D"):
            self.decreasing = True
        elif self.string.startswith("A"):
            self.decreasing = False

        self.dimension = self.string[1:]
        self.sort(packer.bins_to_use)
    
    def string(self):
        return self.string
    
    def sort(self,bins):
        
        bin_sort_dict = {
            "LS": Bin.get_longest_side,
            "AR": Bin.get_aspect_ratio,
            "VOL": Bin.get_volume
            }

        x = bin_sort_dict[self.dimension]
        bins.sort(key=lambda bin: x(bin), reverse=self.decreasing)
        return bins