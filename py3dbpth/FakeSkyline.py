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
    
    def pack_to_bin(self, bin, item, tub_item=False):
        
        if item.in_tub != None and not tub_item:

            tub_items = self.packer.tubs[item.in_tub-1].items
            fitted_tub = True
                
            for i in tub_items:
                fitted_tub = fitted_tub and self.pack_to_bin(bin, i, True)
                if fitted_tub:
                    continue
                else:
                    for i in tub_items:
                        if i in bin.items:
                            self.remove_from_bin(bin, i)
                    break
            return fitted_tub
                    
        else:
            # --- BOTTOM-LEFT ---
            if self.packer.packing_heuristic == "bottom_left":  
            
                fitted = False    
                
                if not bin.items: #Falls Bin leer ist -> put_item an [0,0,0]
                    response = bin.put_item(item, START_POSITION, True) #Boolean Wert von "fit"
                    if response:
                        bin.items.append(item)
                        self.packer.items_to_pack.remove(item)                        
                        bin.sequence.append(item.index)
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
                            bin.sequence.append(item.index)
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
                    bin.sequence.append(item.index)
                    fitted=True
                return fitted
            
            # --- CORNER ---
            elif self.packer.packing_heuristic == "corner":
                fitted = False    
                
                if bin.put_item(item,item.get_most_cornerlike_point(bin), False): #Boolean Wert von "fit"
                    bin.items.append(item)
                    self.packer.items_to_pack.remove(item)                        
                    bin.sequence.append(item.index)
                    fitted=True
                return fitted
    
    def remove_from_bin(self, bin, item):
        item.rotation_type = 0
        item.position = START_POSITION
        bin.items.remove(item)
        self.packer.items_to_pack.insert(0, item)
        bin.sequence.remove(item.index)
        return