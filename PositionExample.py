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
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import math
import os

#%%
#Number of Aufträge is determined and for every Auftrag a dataframe is created
orderData = pd.read_excel(r'Packstückpositionen_11-29012021_VGruppen.xlsx', '11-29012021', header=2)

orderNumbers = orderData['LieferID'].drop_duplicates()
orderNumbers = orderNumbers.reset_index(drop=True)

packer = Packer()

#All orders are packed after each other

orders = []

#for o in range(0, len(orderNumbers.index)):
for o in range(0, 11):
#for o in range(452, 454):
    
    currentOrderData = orderData.loc[orderData['LieferID']==orderNumbers.iloc[o]]
    currentOrderData = currentOrderData.reset_index(drop=True)
    
    current_order = Order("Order_"+str(orderNumbers.iloc[o]),orderNumbers.iloc[o],
                          str(currentOrderData.iat[0,2]), None)
    
    packagePieceNumbers = currentOrderData['PackstückID']
    packagePiecePositionNumbers = currentOrderData['PSPosID']
    positionNumbers = packagePieceNumbers
    for pN in range(0,len(packagePieceNumbers.index)):
        positionNumbers[pN] = str(positionNumbers[pN])+str(packagePiecePositionNumbers.iloc[pN])
    
    tub_id = 0
    order_positions = []

    for pN in range(0,len(positionNumbers)):
        
        if str(currentOrderData.iat[pN,1])=="nein":
            pos_split = True
        else:
            pos_split = False
        
        current_order_position = OrderPosition("Pos_"+str(currentOrderData.iat[pN,4]),
                                               str(positionNumbers[pN]), currentOrderData.iat[pN,5], 
                                               None, pos_split, order = current_order)
        
        tubs = []
        
        #"Palette"
        if currentOrderData.iat[pN,15] == "Palette":
            anzahl_grpae_in_wanne = currentOrderData.iat[pN,18]
            wannen_mit_grpae = 1
        else:
            anzahl_grpae_in_wanne = currentOrderData.iat[pN,15]
            wannen_mit_grpae = math.ceil(currentOrderData.iat[pN,25])
        
        #GRPAE
        counter_GRPAE = currentOrderData.iat[pN,18]
        
        for t in range(0, wannen_mit_grpae):
            
            current_tub = Tub("Tub_GRPAE_"+str(tub_id)+"_"+str(currentOrderData.iat[pN,3]), tub_id, None,
                              order_position = current_order_position, order = current_order)
            tub_id += 1
            
            items=[]
            for i in range(0,min(anzahl_grpae_in_wanne, counter_GRPAE)):
                current_item = Item("GRPAE_"+str(currentOrderData.iat[pN,4])+"_"+str(i), str(currentOrderData.iat[pN,3]),
                                    int(currentOrderData.iat[pN,20]), int(currentOrderData.iat[pN,19]),
                                    int(currentOrderData.iat[pN,21]), int(currentOrderData.iat[pN,22]),
                                    tub = current_tub, order_position = current_order_position, 
                                    order = current_order)
                items.append(current_item)
                counter_GRPAE -= 1
            
            current_tub.add_items(items)
            tubs.append(current_tub)
            
        #STPAE
        current_tub = Tub("Tub_STPAE_"+str(tub_id)+"_"+str(currentOrderData.iat[pN,3]), tub_id, None)
        tub_id += 1
        items=[]
        for i in range(0,int(currentOrderData.iat[pN,26])):
            
            items.append(Item("STPAE_"+str(currentOrderData.iat[pN,4])+"_"+str(i),str(currentOrderData.iat[pN,3]),
                         int(currentOrderData.iat[pN,28]),int(currentOrderData.iat[pN,27]),int(currentOrderData.iat[pN,29]),
                         int(currentOrderData.iat[pN,30]), tub = current_tub, 
                         order_position = current_order_position, order = current_order))
        
        current_tub.add_items(items)
        tubs.append(current_tub)
        
        current_order_position.add_tubs(tubs)
        order_positions.append(current_order_position)        
        
    current_order.add_order_positions(order_positions)
    orders.append(current_order)

stammdatenBins = pd.read_excel (r'Inputdaten.xlsx', 'Stammdaten Bins')

#Add all available kind of bins 
for i in range(0,len(stammdatenBins.index)-1):
    packer.add_bin_type(Bin(stammdatenBins.iat[i+1,1], str(stammdatenBins.iat[i+1,1]), 
                            int(stammdatenBins.iat[i+1,11]), int(stammdatenBins.iat[i+1,10]), 
                            int(stammdatenBins.iat[i+1,12]), int(stammdatenBins.iat[i+1,14]),
                            #max_overhang_ratio = 0.4, min_mounted_corners = 4
                            )) 
    
packer.set_packing_approach(packing_algorithm="fake_skyline", packing_heuristic="bottom_left", 
                bin_select_algorithm="best_fit", bin_select_dimension="volume", 
                item_sorting="-", bin_sorting="-")

print("Pack_Orders")
packer.pack(orders)

    
#%%
overhang = ""
#overhang = "Overhang_0.4_4_"
folder_path = r''+overhang+str(packer.bin_select_algorithm)+str(packer.bin_select_dimension)+str(packer.packing_algorithm)+str(packer.packing_heuristic)+str(packer.item_sorting)+str(packer.bin_sorting)

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

print(packer)
for b in packer.bins:
    fig = plt.figure()
    b.plot_bin(figure=fig)
    fig.savefig(folder_path+"/Bin"+str(b.index))

packer_properties = [["Bin Sorting", packer.bin_sorting],["Item Sorting", packer.item_sorting],
                     ["Bin Select Algorithm", packer.bin_select_algorithm],
                     ["Bin Select Dimension", packer.bin_select_dimension],
                     ["Packing Algorithm", packer.packing_algorithm],
                     ["Packing Heuristic", packer.packing_heuristic]]
df_properties = pd.DataFrame(packer_properties, columns = ['Component', 'Value'])

perf_columns = ["Total"]
performances = [["", packer.get_bins_volume(), packer.get_bins_remaining_volume()]]
for b in packer.bins:
    perf_columns.append(str(b.index))
    performances.append([b.type, b.get_volume(), b.get_remaining_volume()])
performances = np.array(performances).T.tolist()
df_performance = pd.DataFrame(performances, index = ["Type","Bin Volume","Remaining Volume"], columns = perf_columns)

df_items_bins = pd.DataFrame(packer.item_bin_assignment_matrix)
df_bins_orders = pd.DataFrame(packer.bin_order_assignment_matrix)

df_item_sequences = pd.DataFrame(packer.item_sequences)
df_tub_sequences = pd.DataFrame(packer.tub_sequences)

with pd.ExcelWriter(folder_path+"/Results.xlsx") as writer:
    
    df_properties.to_excel(writer, sheet_name="Packer_Properties")
    df_performance.to_excel(writer, sheet_name="Performance in m^3")
    df_items_bins.to_excel(writer, sheet_name="Item_Bin")
    df_bins_orders.to_excel(writer, sheet_name="Bin_Order")
    df_item_sequences.to_excel(writer, sheet_name="Item_Sequence")
    df_tub_sequences.to_excel(writer, sheet_name="Tub_Sequence")
