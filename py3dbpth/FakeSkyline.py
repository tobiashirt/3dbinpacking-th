# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 15:42:48 2021

@author: Tobias Hirt
"""

from .constants import Axis

START_POSITION = [0, 0, 0]

class FakeSkyline:
    def __init__(self, packer):
        self.packer = packer
    
    def pack_single_to_bin(self, bin, item):
        
        # --- BOTTOM-LEFT ---
        if self.packer.packing_heuristic == "bottom_left":  
        
            fitted = False    
            
            if not bin.items: #Falls Bin leer ist -> put_item an [0,0,0]
                response = bin.put_item(item, START_POSITION, True) #Boolean Wert von "fit"
                if response:
                    bin.items.append(item)
                    self.packer.items_to_pack.remove(item)                        
                    bin.item_sequence.append(item.index)
                return response
    
            for axis in range(0, 3): #0=WIDTH, 1=HEIGHT, 2=DEPTH
                items_in_bin = bin.items
    
                for ib in items_in_bin: #Bestimmung möglicher Pivot Punkte
                    pivot = [0, 0, 0]
                    w, d, h = ib.get_dimension()
                    if axis == Axis.WIDTH:
                        pivot = [ib.position[0] + w, ib.position[1], ib.position[2]]
                    elif axis == Axis.DEPTH:
                        pivot = [ib.position[0], ib.position[1] + d, ib.position[2]]
                    elif axis == Axis.HEIGHT:
                        pivot = [ib.position[0], ib.position[1], ib.position[2] + h]
    
                    if bin.put_item(item, pivot, True):
                        fitted = True
                        bin.items.append(item)
                        self.packer.items_to_pack.remove(item)
                        bin.item_sequence.append(item.index)
                        break
                if fitted:
                    break
            
            return fitted
        
        # --- MAX CONTACT ---
        elif self.packer.packing_heuristic == "max_contact":
            fitted = False    
            
            if bin.put_item(item,item.get_max_contact_point(bin), False): #Boolean Wert von "fit"
                bin.items.append(item)
                self.packer.items_to_pack.remove(item)                        
                bin.item_sequence.append(item.index)
                fitted=True
            return fitted
        
        # --- CORNER ---
        elif self.packer.packing_heuristic == "corner":
            fitted = False    
            
            if bin.put_item(item,item.get_most_cornerlike_point(bin), False): #Boolean Wert von "fit"
                bin.items.append(item)
                self.packer.items_to_pack.remove(item)                        
                bin.item_sequence.append(item.index)
                fitted=True
            return fitted    
    
    def pack_virtual_to_bin(self, bin, item):
        
        virt_items = []
        
        # TODO
        # Hier könnten "gut gruppier-/stapelbare" Items als Virtuelles Item zusammengefügt werden
        
        if item.order != None and not item.order.order_split:
            virt_items = item.order.items
            
        elif item.order_position != None and not item.order_position.position_split:
            virt_items = item.order_position.items
        
        elif item.tub != None and not item.tub.tub_split:
            virt_items = item.tub.items
            
        else:
            virt_items = item
        
        fitted_virt_item = True
        for i in virt_items:
            fitted_virt_item = fitted_virt_item and self.pack_single_to_bin(bin, i)
            if fitted_virt_item:
                continue
            else:
                for i in virt_items:
                    if i in bin.items:
                        self.remove_from_bin(bin, i)
                break
        
        if fitted_virt_item:
            s = set()
            for i in virt_items:
                s.add(i.tub.index)
            bin.tub_sequence.extend(list(s))
        
        return fitted_virt_item
    
    def remove_from_bin(self, bin, item):
        item.rotation_type = 0
        item.position = START_POSITION
        bin.items.remove(item)
        self.packer.items_to_pack.insert(0, item)
        bin.item_sequence.remove(item.index)
        return