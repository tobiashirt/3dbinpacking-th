# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 15:59:27 2021

@author: Tobias Hirt
"""

from .constants import RotationType
from .auxiliary_methods import rect_overlap
from .auxiliary_methods import distance_L2

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

from .constants import Axis

START_POSITION = [0, 0, 0]


class Item:
    def __init__(self, name: str, article_id: str, width: int, depth: int, height: int, weight:int, tub = None, order_position = None, order = None):
        self.name = name
        self.article_id = article_id
        self.tub = tub
        self.order_position = order_position
        self.order = order
        self.index = 0
        self.width = width
        self.depth = depth
        self.height = height
        self.weight = weight
        self.rotation_type = 0
        self.position = START_POSITION

    def string(self):
        return "Item %s / %s - %s (%sx%sx%s, weight: %s) pos(%s) rot(%s) vol(%s)" % (
            self. index, self.name, self.article_id, self.width, self.depth, self.height, self.weight,
            self.position, self.rotation_type, self.get_volume()
        )
    
    def get_width(self): #W
        return self.get_dimension()[0]
    
    def get_depth(self): #D
        return self.get_dimension()[1]

    def get_height(self): #H
        return self.get_dimension()[2]
    
    def get_longest_side(self): #LS
        return max(self.get_dimension())
    
    def get_shortest_side(self): #SS
        return min(self.get_dimension())
    
    def get_max_side_diff(self): #MSD
        return self.get_longest_side()-self.get_shortest_side()
    
    def get_max_side_ratio(self): #MSR
        return self.get_longest_side()/self.get_shortest_side()
    
    def get_wh_area(self): #WHA
        return self.get_dimension()[0]*self.get_dimension()[2]
    
    def get_wd_area(self): #WDA
        return self.get_dimension()[0]*self.get_dimension()[1]
    
    def get_hd_area(self): #HDA
        return self.get_dimension()[2]*self.get_dimension()[1]
    
    def get_largest_area(self): #LA
        return max(self.get_wh_area(),self.get_wd_area(),self.get_hd_area())
    
    def get_smallest_area(self): #SA
        return min(self.get_wh_area(),self.get_wd_area(),self.get_hd_area())
    
    def get_max_area_diff(self): #MAD
        return self.get_largest_area()-self.get_smallest_area()
    
    def get_max_area_ratio(self): #MAR
        return self.get_largest_area()/self.get_smallest_area()
    
    def get_surface_area(self): #SFA
        return 2*(self.get_wh_area()+self.get_wd_area()+self.get_hd_area())
    
    def get_volume(self): #VOL
        return self.width * self.height * self.depth
    
    def get_density(self): #DEN
        return self.weight / self.get_volume()
    
    def get_aspect_ratio(self): #AR
        return ((self.get_width()/self.get_longest_side())*(self.get_height()/self.get_longest_side())*(self.get_depth()/self.get_longest_side()))

    # TODO: In Bin auslagern
    def contact_area(self, bin, position):
        contact_area = 0
        self.position=position
        
        # Kontaktfläche mit Bin berechnen
        if self.position[0]==0: # linke Seite
             contact_area += self.get_dimension()[1]*self.get_dimension()[2]
        if self.position[0]+self.get_dimension()[0]==bin.width: # rechte Seite
            contact_area += self.get_dimension()[1]*self.get_dimension()[2]
        if self.position[1]==0: # vordere Seite
            contact_area += self.get_dimension()[0]*self.get_dimension()[2]
        if self.position[1]+self.get_dimension()[1]==bin.depth: # hintere Seite
            contact_area += self.get_dimension()[0]*self.get_dimension()[2]
        if self.position[2]==0: # NUR Boden
            contact_area += self.get_dimension()[0]*self.get_dimension()[1]    
        
        # Kontaktfläche mit Bin Items berechnen
        for item in bin.items:
            if self != item:
                contact_with_item = 0
                
                if self.position[0] == item.position[0] + int(item.get_dimension()[0]) or self.position[0]+int(self.get_dimension()[0]) == item.position[0]: #linke oder rechte Seite
                    contact_with_item = rect_overlap(self, item,1,2)
                elif self.position[1] == item.position[1] + int(item.get_dimension()[1]) or self.position[1]+int(self.get_dimension()[1]) == item.position[1]: #vorne oder hinten
                    contact_with_item = rect_overlap(self, item,0,2)
                elif self.position[2] == item.position[2] + item.get_dimension()[2] or self.position[2]+int(self.get_dimension()[2]) == item.position[2]: #unten oder oben
                    contact_with_item = rect_overlap(self, item,0,1)
                else:
                    contact_with_item = 0
                    
                contact_area += contact_with_item
            else:
                continue
        return contact_area
    
    # TODO: In Bin auslagern
    def get_max_contact_point(self, bin):
        
        memory_contact_area = 0
        max_contact_area = 0
        max_contact_r = 0
        max_contact_xyz = [0,0,0]
        
        # TODO: Effizienter machen... Nicht mit for-Schleifen durchgehen, sondern 
        # Menge zu untersuchender bzw. sinnvoller Punkte über Eckpunkte der Items etc. bestimmen
        for r in range(0,6):
            self.rotation_type=r
            for x in range(0,1+bin.width-self.get_dimension()[0]):
                for y in range(0,1+bin.depth-self.get_dimension()[1]):
                    for z in range(0,1+bin.height-self.get_dimension()[2]):
                        memory_contact_area = self.contact_area(bin,[x,y,z])
                        if max_contact_area < memory_contact_area:
                            if bin.put_item(self,[x,y,z],False):
                                max_contact_area = memory_contact_area
                                max_contact_xyz = [x,y,z]
                                max_contact_r = r
        self.position=START_POSITION
        self.rotation_type=max_contact_r
        return max_contact_xyz
    
    # TODO: In Bin auslagern
    def get_min_distance_to_bottom_corner(self, bin, position):
        
        item_bottom_corners = [position,[position[0]+self.get_dimension()[0], position[1], position[2]],
                               [position[0], position[1]+self.get_dimension()[1], position[2]],
                               [position[0]+self.get_dimension()[0], position[1]+self.get_dimension()[1], position[2]]]
        bin_bottom_corners = [[0,0,0],[bin.width,0,0],[0,bin.depth,0],[bin.width,bin.depth,0]]
        
        d = distance_L2([0,0,0],[bin.width/2,bin.depth/2,bin.height])
        
        for ic in item_bottom_corners:
            for bc in bin_bottom_corners:
                if distance_L2(ic, bc) < d:
                    d = distance_L2(ic, bc)
        
        return d
    
    # TODO: In Bin auslagern
    def get_most_cornerlike_point(self, bin):
        
        cornerlike_xyz = [bin.width/2,bin.depth/2,bin.height]
        cornerlike_r = 0
        
        max_x = 1+bin.width-self.get_dimension()[0]
        max_y = 1+bin.depth-self.get_dimension()[1]
        
        # TODO: Effizienter machen... Nicht mit for-Schleifen durchgehen, sondern 
        # Menge zu untersuchender bzw. sinnvoller Punkte über Eckpunkte der Items etc. bestimmen
        if bin.items:
            max_z = max((i.position[2]+i.get_dimension()[2]) for i in bin.items)
        else:
            max_z = 1
        
        for r in range(0,6):
            self.rotation_type=r
            for x in range(0,max_x):
                for y in range(0,max_y):
                    for z in range(0,max_z):
                        if bin.put_item(self,[x,y,z],False):
                            if self.get_min_distance_to_bottom_corner(bin, [x,y,z]) < self.get_min_distance_to_bottom_corner(bin, cornerlike_xyz):
                                cornerlike_xyz = [x,y,z]
                                cornerlike_r = r
                                
        self.position=START_POSITION
        self.rotation_type=cornerlike_r
                
        return cornerlike_xyz
    
    def set_position_corner(self, x, y, z, corner: int = 0):
        if corner == 0:
            self.position = [x,y,z]
        elif corner == 1:
            self.position = [x-self.width,y,z]
        elif corner == 2:
            self.position = [x,y-self.depth,z]
        elif corner == 3:
            self.position = [x-self.width,y-self.depth,z]
        elif corner == 4:
            self.position = [x,y,z-self.height]
        elif corner == 5:
            self.position = [x-self.width,y,z-self.height]
        elif corner == 6:
            self.position = [x,y-self.depth,z-self.height]
        elif corner == 7:
            self.position = [x-self.width,y-self.depth,z-self.height]
        
    
    def get_dimension(self):
        if self.rotation_type == RotationType.RT_WDH:
            dimension = [self.width, self.depth, self.height]
        elif self.rotation_type == RotationType.RT_WHD:
            dimension = [self.width, self.height, self.depth]
        elif self.rotation_type == RotationType.RT_DHW:
            dimension = [self.depth, self.height, self.width]
        elif self.rotation_type == RotationType.RT_DWH:
            dimension = [self.depth, self.width, self.height]
        elif self.rotation_type == RotationType.RT_HWD:
            dimension = [self.height, self.width, self.depth]
        elif self.rotation_type == RotationType.RT_HDW:
            dimension = [self.height, self.depth, self.width]
        else:
            dimension = []

        return dimension