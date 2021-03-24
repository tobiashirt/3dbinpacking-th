# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 22:16:22 2021

@author: Tobias Hirt
"""

from .Item import Item

START_POSITION = [0, 0, 0]


class Order:
    def __init__(self, name: str, order_id: int, tubs, index=None):
        self.name = name
        self.order_id = order_id
        self.index = index
        self.tubs = []
        self.order_positions = []
        self.items = []
        
        for t in tubs:
            self.tubs.append(t)
            for op in t.order_positions:
                self.order_positions.append(op)
                self.items.extend(op.items)
        
    def string(self):
        item_string = ""
        for i in self.items:
            item_string += i.index + ","
        return "Order %s-%s: " % (self.order_id, self.name) + item_string
    
    def add_tub(self, name, order_id, order_positions, index):
        tub = Tub(name, order_id, order_positions, index)
        self.items.extend(tub.items)
        self.order_positions.extend(tub.order_positions)
        return self.tubs.append(tub)
      

class Tub:
    def __init__(self, name: str, tub_id: int, order_positions, index=None):
        self.name = name
        self.tub_id = tub_id
        self.index = index
        self.order_positions = order_positions
        
        self.items = []
        for o in self.order_positions:
            self.items.extend(o.items)
            
    def string(self):
        item_string = ""
        for i in self.items:
            item_string += i.index + ","
        return "Tub %s-%s: " % (self.index, self.name) + item_string
    
    def add_order_position(self, name, article_id, w, d, h, weight, amount, in_tub):
        order_pos = OrderPosition(name, article_id, w, d, h, weight, amount, in_tub)
        self.items.extend(order_pos.items)
        return self.order_positions.append(order_pos)


class OrderPosition:
    def __init__(self, name: str, article_id: int, width: int, depth: int, height: int, weight:int, amount: int = 1, in_tub: int=None, index=None):
        self.name = name
        self.article_id = article_id
        self.index = index
        self.amount = amount        
        
        self.items = []
        for i in range(self.amount):
            self.items.append(Item(name, article_id, width, depth, height, weight, in_tub))
        
    def string(self):
        return "Order Position  %s-%s: %s (%sx%sx%s) x %s" % (
            self.index, self.name, self.article_id, self.width, self.depth, self.height, self.amount
        )
        