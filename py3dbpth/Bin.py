# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 15:58:17 2021

@author: Tobias Hirt
"""

from .constants import RotationType
from .auxiliary_methods import intersect
from .OverhangRule import OverhangRule

import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

START_POSITION = [0, 0, 0]

class Bin:
    def __init__(self, name: str, t: str, width: int, depth: int, height: int, max_weight: int, max_overhang_ratio: float = 0.0, min_mounted_corners: int = 4, weight: int = 0):
        self.name = name
        self.type = t
        self.index = 0
        self.width = width
        self.depth = depth
        self.height = height
        self.weight = weight
        self.max_weight = max_weight
        self.items = []
        self.item_sequence = []
        self.tub_sequence = []
        self.overhangRule = OverhangRule(max_overhang_ratio, min_mounted_corners)

    def string(self):
        item_string = ""
        for i in self.items:
            item_string += i.index + ","
        return "Bin %s-%s: " % (self.index, self.name) + item_string

    def get_longest_side(self): #LS
        return max(self.width,self.depth,self.height)
    
    def get_longest_side_diff(self, item):
        return self.get_aspect_ratio()-item.get_aspect_ratio()

    def get_volume(self): #VOL
        return self.width * self.depth * self.height / (1000*1000*1000)
    
    def get_aspect_ratio(self) -> float: #AR
        return ((self.width/self.get_longest_side())*(self.depth/self.get_longest_side())*(self.height/self.get_longest_side()))
    
    def get_aspect_ratio_diff(self, item):
        min_aspect_ratio_diff = 10000
        rotation = 0
        for r in range(0,6):
            item.rotation=r
            if min_aspect_ratio_diff > abs(self.get_aspect_ratio()-item.get_aspect_ratio()):
                rotation = r
        item.rotation = rotation
        return abs(self.get_aspect_ratio()-item.get_aspect_ratio())
    
    def get_remaining_volume(self):
        items_volume = 0
        for i in self.items:
            items_volume += i.get_volume()
        return self.get_volume()-(items_volume/(1000*1000*1000))
    
    def get_remaining_volume_item(self, item):
        items_volume = 0
        for i in self.items:
            items_volume += i.get_volume()
        return self.get_volume()-items_volume-item.get_volume()

    def get_total_weight(self):
        total_weight = 0

        for item in self.items:
            total_weight += item.weight

        return total_weight

    def plot_bin(self, figure = None, axis = None):
        
        item_string = str(len(self.items))+" Items"
        
        if figure:
            fig = figure
        else:
            fig = plt.figure()
        
        if not axis:
            #fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
        else:
            ax = axis
        
        ax.set_title("Bin " + str(self.index) + " from " + self.type + " with " + item_string)
        
        Z = np.array([[0, 0, 0], 
                      [self.width, 0, 0], 
                      [0, self.depth, 0], 
                      [0, 0, self.height],
                      [self.width, self.depth, 0], 
                      [self.width,0, self.height], 
                      [0, self.depth, self.height], 
                      [self.width, self.depth, self.height]])
        ax.scatter3D(Z[:, 0], Z[:, 1], Z[:, 2])
        verts = [[Z[0],Z[1],Z[4],Z[2]],
             [Z[0],Z[3],Z[6],Z[2]], 
             [Z[0],Z[1],Z[5],Z[3]], 
             [Z[4],Z[2],Z[6],Z[7]], 
             [Z[4],Z[1],Z[5],Z[7]],
             [Z[5],Z[3],Z[6],Z[7]]]
        
        ax.add_collection3d(Poly3DCollection(verts, linewidths=1, edgecolors='r', alpha=.00))
        
        color_list = ['cyan','green','yellow','blue','purple']*5
        for c,item in zip(color_list,self.items):
            Z = np.array([[item.position[0], item.position[1], item.position[2]], 
                          [item.position[0]+item.get_dimension()[0], item.position[1], item.position[2]], 
                          [item.position[0], item.position[1]+item.get_dimension()[1], item.position[2]], 
                          [item.position[0], item.position[1], item.position[2]+item.get_dimension()[2]],
                          [item.position[0]+item.get_dimension()[0], item.position[1]+item.get_dimension()[1], item.position[2]], 
                          [item.position[0]+item.get_dimension()[0],item.position[1], item.position[2]+item.get_dimension()[2]], 
                          [item.position[0], item.position[1]+item.get_dimension()[1], item.position[2]+item.get_dimension()[2]], 
                          [item.position[0]+item.get_dimension()[0], item.position[1]+item.get_dimension()[1], item.position[2]+item.get_dimension()[2]]])
            ax.scatter3D(Z[:, 0], Z[:, 1], Z[:, 2])
            verts = [[Z[0],Z[1],Z[4],Z[2]],
                 [Z[0],Z[3],Z[6],Z[2]], 
                 [Z[0],Z[1],Z[5],Z[3]], 
                 [Z[4],Z[2],Z[6],Z[7]], 
                 [Z[4],Z[1],Z[5],Z[7]],
                 [Z[5],Z[3],Z[6],Z[7]]]

            ax.add_collection3d(Poly3DCollection(verts, facecolors=c, linewidths=1, edgecolors='r', alpha=.3))
            ax.text(float(item.position[0])+float(item.get_dimension()[0])/2, 
                    float(item.position[1]), 
                    float(item.position[2])+float(item.get_dimension()[2])/2, 
                    str(item.index))
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        
        if not axis:
            return ax
        
        else:
            #plt.show()
            return

    def put_item(self, item, pivot, rotate=True):

        fit = False
        valid_item_position = item.position #standardmäßig STARTING_POSITION [0,0,0]
        item.position = pivot #mögliche Pivotpunkte

        if rotate:
            for i in range(0, len(RotationType.ALL)):
                item.rotation_type = i
                dimension = item.get_dimension() #gibt Dimensionen je nach Rotationswert zurück
                
                if (self.width < pivot[0] + dimension[0] or self.depth < pivot[1] + dimension[1] or self.height < pivot[2] + dimension[2]):
                    continue
    
                fit = True #Item i passt "generell" in Bin j
    
                for current_item_in_bin in self.items:
                    if intersect(current_item_in_bin, item): 
                        fit = False 
                        break #Falls sich Items in Bin mit betrachtetem Item schneiden, nächste Rotation

                if not self.overhangRule.check_rule(self, item, pivot):
                    fit = False
                    break
    
                if fit:
                    if self.get_total_weight() + item.weight > self.max_weight:
                        fit = False
                        return fit #Falls zu schwer, hilft auch keine Rotation ^^
    
                if not fit:
                    item.position = valid_item_position
    
                return fit
    
            if not fit:
                item.position = valid_item_position
    
            return fit
        
        else:
            dimension = item.get_dimension() #gibt Dimensionen je nach Rotationswert zurück
            if ( #check ob Item nicht zu groß für Bin ist
                self.width >= pivot[0] + dimension[0] or self.height >= pivot[1] + dimension[1] or self.depth >= pivot[2] + dimension[2]):
                fit = True #Item i passt "generell" in Bin j

            for current_item_in_bin in self.items:
                if intersect(current_item_in_bin, item): 
                    fit = False
                    break

            if fit:
                if self.get_total_weight() + item.weight > self.max_weight:
                    fit = False
                    return fit #Falls zu schwer, hilft auch keine Rotation ^^

            if not fit:
                item.position = valid_item_position

            return fit

        if not fit:
            item.position = valid_item_position

        return fit
