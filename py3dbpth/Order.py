# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 22:16:22 2021

@author: Tobias Hirt
"""

from .Item import Item

START_POSITION = [0, 0, 0]


class Order:
    def __init__(self, name: str, order_id: int, allowed_PM: str, order_positions, order_split: bool = True, index=None):
        self.name = name
        self.order_id = order_id
        self.allowed_PM = allowed_PM
        self.index = index
        self.order_split = order_split
        self.order_positions = []
        self.tubs = []
        self.items = []
        
        self.bins = []
        self.utilization = 1.0
        
        if order_positions != None:
            for op in order_positions:
                self.order_positions.append(op)
                for t in op.tubs:
                    self.tubs.append(t)
                    self.items.extend(t.items)
        
    def string(self):
        item_string = ""
        for i in self.items:
            item_string += i.index + ","
        return "Order %s-%s: " % (self.order_id, self.name) + item_string

    def add_order_positions(self, order_positions):
        for op in order_positions:
            self.order_positions.append(op)
            for t in op.tubs:
                self.tubs.append(t)
                self.items.extend(t.items)
                
    def finish_order(self, bins):
        for b in bins:
            self.bins.append(b)
            
        self.utilization = (self.get_bins_volume()-self.get_bins_remaining_volume())/self.get_bins_volume()
        return True
    
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
        return self.utilization
          
class OrderPosition:
    def __init__(self, name: str, order_position_id: str, amount, tubs, position_split: bool = True, index=None, order=None):
        self.name = name
        self.order_position_id = order_position_id
        self.index = index
        self.amount = amount
        
        self.order = order
        self.position_split = position_split
        
        self.tubs = []
        self.items = []
        
        if tubs != None:
            for t in tubs:
                self.tubs.append(t)
                self.items.extend(t.items)
        
    def string(self):
        return "Order Position  %s-%s: %s x %s" % (
            self.index, self.name, self.article_id, self.amount)
        
    def add_tubs(self, tubs):
        for t in tubs:
            self.tubs.append(t)
            self.items.extend(t.items)

class Tub:
    def __init__(self, name: str, tub_id: int, items, tub_split: bool = False, index=None, order_position = None, order = None):
        self.name = name
        self.tub_id = tub_id
        self.index = index
        
        self.order = order
        self.order_position = order_position
        self.tub_split = tub_split
        
        self.items = []
        
        if items != None:
            self.items.extend(items)
            
    def string(self):
        item_string = ""
        for i in self.items:
            item_string += i.index + ","
        return "Tub %s-%s: " % (self.index, self.name) + item_string
    
    def add_items(self, items):
        self.items.extend(items)
