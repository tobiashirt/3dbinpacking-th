# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 16:11:57 2021

@author: Tobias Hirt
"""

class Tub:
    def __init__(self, name, items, index=None):
        self.name = name
        self.index = index
        self.weight = 0
        self.items = items
        for i in items:
            i.in_tub = self.index
            self.weight += i.weight
            
    def string(self):
        item_string = ""
        for i in self.items:
            item_string += i.index + ","
        return "Tub %s-%s: " % (self.index, self.name) + item_string
    
    def add_item(self, item):
        self.weight += item.weight
        item.in_tub = self.index
        return self.items.append(item)