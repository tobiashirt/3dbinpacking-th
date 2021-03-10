# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 22:16:22 2021

@author: Tobias Hirt
"""

class Order:
    def __init__(self, name, index=None):
        self.name = name
        self.index = index
        self.items = []
        self.tubs = []
        
    def string(self):
        item_string = ""
        for i in self.items:
            item_string += i.index + ","
        return "Order %s-%s: " % (self.index, self.name) + item_string
    
    def add_item(self, item):
        return self.items.append(item)
    
    def add_tub(self, tub):
        return self.tubs.append(tub)