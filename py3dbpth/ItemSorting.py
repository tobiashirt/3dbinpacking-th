# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 09:43:39 2021

@author: Tobias Hirt
"""

from .Item import Item

class ItemSorting:
    
    def __init__(self,packer):
        
        self.string=packer.item_sorting
        self.decreasing = None
        if self.string.startswith("D"):
            self.decreasing = True
        elif self.string.startswith("A"):
            self.decreasing = False

        self.dimension = self.string[1:]
        self.sort(packer.items_to_pack)
        
    def string(self):
        return self.string
    
    def sort(self,items):
        
        item_sort_dict = {
            "W": Item.get_width,
            "H": Item.get_height,
            "D": Item.get_depth,
            "LS": Item.get_longest_side,
            "SS": Item.get_shortest_side,
            "MSD": Item.get_max_side_diff,
            "MSR": Item.get_max_side_ratio,
            "WHA": Item.get_wh_area,
            "WDA": Item.get_wd_area,
            "HDA": Item.get_hd_area,
            "LA": Item.get_largest_area,
            "SA": Item.get_smallest_area,
            "MAD": Item.get_max_area_diff,
            "MAR": Item.get_max_area_ratio,
            "SFA": Item.get_surface_area,
            "AR": Item.get_aspect_ratio,
            "VOL": Item.get_volume,
            "DEN": Item.get_density
            }

        x = item_sort_dict[self.dimension]
        items.sort(key=lambda item: x(item), reverse=self.decreasing)
        return items