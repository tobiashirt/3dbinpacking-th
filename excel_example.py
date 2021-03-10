# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 20:50:37 2021

@author: Tobias Hirt
"""

from py3dbpth import Packer
from py3dbpth import Bin
from py3dbpth import Tub
from py3dbpth import Item
from py3dbpth import Order
from openpyxl import Workbook
from openpyxl import load_workbook
import random
import pandas as pd


#Number of Aufträge is determined and for every Auftrag a dataframe is created
orderData = pd.read_excel (r'Inputdaten.xlsx', 'Artikel bereinigt')
#orderData = orderData.drop(columns=["ID"])
orderNumbers = orderData['Auftragsnummer'].drop_duplicates()
orderNumbers = orderNumbers.reset_index(drop=True)

#%%
orders = list()
packer = list()

#%%
#All orders are packed after each other

#for o in range(0, len(orderNumbers.index)):
for o in range(0, 1):
    print("Order: "+str(orderNumbers.iloc[o]))
    
    packer.append(Packer())
    orders.append(Order("Order_"+str(o), orderNumbers.iloc[o]))
    currentOrder = orderData.loc[orderData['Auftragsnummer']==orderNumbers.iloc[o]]
    
    tubNumbers = currentOrder['Wannen-ID'].drop_duplicates()
    tubNumbers = tubNumbers.reset_index(drop=True)
    
    #Iterate through all tubs of the same order
    for t in range(0, len(tubNumbers.index)):
        print("Tub: "+str(tubNumbers.iloc[t]))
        
        currentTub = currentOrder.loc[currentOrder['Wannen-ID']==tubNumbers.iloc[t]]
        currentTub = currentTub.reset_index(drop=True)

        tub_items = list()
        #Iterate through all kind of items in a tub
        for i in range(0, len(currentTub.index)):
            print("Item: "+str(currentTub.iat[i,3]))
            
            #Iterate through all items of the same kind
            for a in range(0, currentTub.iat[i,5]):
                tub_items.append(Item('tub' + str(t) + '_item_' + str(currentTub.iat[i,2]) + ': ' + str(currentTub.iat[i,3]), currentTub.iat[i,7], currentTub.iat[i,8], currentTub.iat[i,9], currentTub.iat[i,10]))
        
        tub1 = Tub('tub_' + str(t), tub_items)
        orders[o].add_tub(tub1)
        packer[o].add_tub(tub1)

    stammdatenBins = pd.read_excel (r'Inputdaten.xlsx', 'Stammdaten Bins')
    
    #TODO: Add bins dynamically or "enough from the start"
    #Add all available kind of bins 
    print("Add_Bins")
    #for i in range(0,len(stammdatenBins.index)-1):
    for i in range(0,1):
        packer[o].add_bin(Bin(stammdatenBins.iat[i+1,1], stammdatenBins.iat[i+1,11], stammdatenBins.iat[i+1,12], stammdatenBins.iat[i+1,13], stammdatenBins.iat[i+1,15])) 
    
#%%   
print("PackOrder: "+str(orderNumbers.iloc[0]))
packer[0].pack(packing_algorithm="fake_skyline", packing_heuristic="bottom_left", bin_select_algorithm="first_fit", bin_select_dimension="volume", item_sorting="DVOL", bin_sorting="DVOL")

#%%

for p in range(0,1):
    for j in packer[p].bins:
        j.plot_bin()
    #packer[p].plot_packing()