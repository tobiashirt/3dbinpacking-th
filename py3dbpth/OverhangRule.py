# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 21:24:34 2021

@author: Tobias Hirt
"""

from .auxiliary_methods import rect_overlap

class OverhangRule:
    
    def __init__(self, max_overhang_ratio: float = 0.0, min_mounted_corners: int = 4):
        
        self.max_overhang_ratio = max_overhang_ratio
        self.min_mounted_corners = min_mounted_corners
        
    def get_overhang(self, bin, item, position):
        
        item.position=position
        contact_area = 0
        if item.position[2]==0:
            return 0
        
        for i in bin.items:
            if i != item:
                contact_with_item = 0
                
                if item.position[2] == i.position[2] + i.get_dimension()[2]:
                    contact_with_item = rect_overlap(item, i, 0, 1)
                    
                contact_area += contact_with_item
            else:
                continue
            
        return (item.get_dimension()[0]*item.get_dimension()[1]) - contact_area
    
    def get_relative_overhang(self, bin, item, position):
        return self.get_overhang(bin, item, position)/(item.get_dimension()[0]*item.get_dimension()[1])
    
    def get_number_of_mounted_corners(self, bin, item, position):
        
        item.position = position
        n_points = 0
        
        for i in bin.items:
            if item.position[2] == i.position[2] + i.get_dimension()[2]:
                if i.position[0] <= item.position[0] <= i.position[0] + i.get_dimension()[0]:
                    if i.position[1] <= item.position[1] <= i.position[1] + i.get_dimension()[1]:
                        n_points += 1
                if i.position[0] <= item.position[0] + item.get_dimension()[0] <= i.position[0] + i.get_dimension()[0]:
                    if i.position[1] <= item.position[1] <= i.position[1] + i.get_dimension()[1]:
                        n_points += 1
                if i.position[0] <= item.position[0] <= i.position[0] + i.get_dimension()[0]:
                    if i.position[1] <= item.position[1] + item.get_dimension()[1] <= i.position[1] + i.get_dimension()[1]:
                        n_points += 1
                if i.position[0] <= item.position[0] + item.get_dimension()[0] <= i.position[0] + i.get_dimension()[0]:
                    if i.position[1] <= item.position[1] + item.get_dimension()[1] <= i.position[1] + i.get_dimension()[1]:
                        n_points += 1
        
        return n_points
    
    def check_rule(self, bin, item, position):
                
        check_threshold = False
        check_points = False
        
        if item.position[2]==0:
            return True
        
        if self.get_relative_overhang(bin, item, position) <= self.max_overhang_ratio:
            check_threshold = True
        
        if self.get_number_of_mounted_corners(bin, item, position) >= self.min_mounted_corners:
            check_points = True
        
        return check_threshold and check_points