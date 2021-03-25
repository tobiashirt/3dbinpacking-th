# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 20:50:37 2021

@author: Tobias Hirt
"""

from py3dbpth import Packer
from py3dbpth import Bin
from py3dbpth import OverhangRule
from py3dbpth import Order
from py3dbpth.Order import OrderPosition
from py3dbpth.Order import Tub
from py3dbpth import Item
from openpyxl import Workbook
from openpyxl import load_workbook
import random
import pandas as pd
import math


#Number of Aufträge is determined and for every Auftrag a dataframe is created
orderData = pd.read_excel (r'Inputdaten.xlsx', 'Artikel bereinigt')
orderNumbers = orderData['Auftragsnummer'].drop_duplicates()
orderNumbers = orderNumbers.reset_index(drop=True)

#%%

packer = Packer()

#%%
#All orders are packed after each other

orders = []

for o in range(0, len(orderNumbers.index)):
#for o in range(0, 2):
    
    currentOrder = orderData.loc[orderData['Auftragsnummer']==orderNumbers.iloc[o]]
    
    tubNumbers = currentOrder['Wannen-ID'].drop_duplicates()
    tubNumbers = tubNumbers.reset_index(drop=True)
    
    tubs = []
    
    #Iterate through all tubs of the same order
    for t in range(0, len(tubNumbers.index)):
        
        currentTub = currentOrder.loc[currentOrder['Wannen-ID']==tubNumbers.iloc[t]]
        currentTub = currentTub.reset_index(drop=True)

        order_positions = []
        
        #Iterate through all order positions in a tub
        for op in range(0, len(currentTub.index)):
            
            order_positions.append(OrderPosition("OrderPos"+str(currentTub.iat[op,3]),currentTub.iat[op,2],
                                                 currentTub.iat[op,8], currentTub.iat[op,7], currentTub.iat[op,9], 
                                                 currentTub.iat[op,10], currentTub.iat[op,5], currentTub.iat[op,4]))
            
        tubs.append(Tub("Tub"+str(t), currentTub.iat[op,4], order_positions))
    
    orders.append(Order("Order"+str(orderNumbers.iloc[o]),orderNumbers.iloc[o],tubs))
    
stammdatenBins = pd.read_excel (r'Inputdaten.xlsx', 'Stammdaten Bins')

#Add all available kind of bins 

for i in range(0,len(stammdatenBins.index)-1):
    packer.add_bin_type(Bin(stammdatenBins.iat[i+1,1], "type"+str(stammdatenBins.iat[i+1,1]), stammdatenBins.iat[i+1,11], stammdatenBins.iat[i+1,10], stammdatenBins.iat[i+1,12], stammdatenBins.iat[i+1,14])) 
    
# for i in range(0,len(stammdatenBins.index)-1):
#         packers[5].add_bin_type(Bin(stammdatenBins.iat[i+1,1], "type"+str(stammdatenBins.iat[i+1,1]), stammdatenBins.iat[i+1,11], stammdatenBins.iat[i+1,10], stammdatenBins.iat[i+1,12], stammdatenBins.iat[i+1,14], 0.1,3)) 

# for i in range(0,len(stammdatenBins.index)-1):
#         packers[6].add_bin_type(Bin(stammdatenBins.iat[i+1,1], "type"+str(stammdatenBins.iat[i+1,1]), stammdatenBins.iat[i+1,11], stammdatenBins.iat[i+1,10], stammdatenBins.iat[i+1,12], stammdatenBins.iat[i+1,14], 0.4,4)) 

#%%

packer.set_packing_approach(packing_algorithm="fake_skyline", packing_heuristic="bottom_left", 
                bin_select_algorithm="first_fit", bin_select_dimension="-", 
                item_sorting="DVOL", bin_sorting="AVOL")

# packers[1].set_packing_approach(packing_algorithm="fake_skyline", packing_heuristic="bottom_left", 
#                 bin_select_algorithm="first_fit", bin_select_dimension="volume", 
#                 item_sorting="DVOL", bin_sorting="DVOL")

# packers[2].set_packing_approach(packing_algorithm="fake_skyline", packing_heuristic="bottom_left", 
#                 bin_select_algorithm="best_fit", bin_select_dimension="volume", 
#                 item_sorting="-", bin_sorting="-")

# packers[3].set_packing_approach(packing_algorithm="fake_skyline", packing_heuristic="bottom_left", 
#                 bin_select_algorithm="best_fit", bin_select_dimension="aspect_ratio", 
#                 item_sorting="DVOL", bin_sorting="DVOL")

# packers[4].set_packing_approach(packing_algorithm="fake_skyline", packing_heuristic="bottom_left", 
#                 bin_select_algorithm="best_fit", bin_select_dimension="longest_side", 
#                 item_sorting="DVOL", bin_sorting="DVOL")

# packers[5].set_packing_approach(packing_algorithm="fake_skyline", packing_heuristic="bottom_left", 
#                 bin_select_algorithm="first_fit", bin_select_dimension="volume", 
#                 item_sorting="DVOL", bin_sorting="DVOL")

# packers[6].set_packing_approach(packing_algorithm="fake_skyline", packing_heuristic="bottom_left", 
#                 bin_select_algorithm="first_fit", bin_select_dimension="volume", 
#                 item_sorting="DVOL", bin_sorting="DVOL")

print("Pack_Orders")
packer.pack(orders)

#%%
print(packer)
for j in packer.bins:
    j.plot_bin()
        
#%%
packer.bins[17].plot_bin()