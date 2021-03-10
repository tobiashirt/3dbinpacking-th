from py3dbpth import Packer
from py3dbpth import Bin
from py3dbpth import Tub
from py3dbpth import Item

import random

packer = list()
for p in range(0,10): 
    packer.append(Packer())
    
    packer[p].add_bin(Bin('small-box', 50, 50, 50, 1000, 0.0,4))
    packer[p].add_bin(Bin('medium-box', 100, 100, 50, 1000, 0.0,4))
    packer[p].add_bin(Bin('large-box', 100, 100, 100, 1000, 0.0,4))
    packer[p].add_bin(Bin('s-box', 5, 5, 5, 1000, 0.0,4))
    
    packer[p].add_item(Item('90article_1', 100, 100, 90, 2))
    
    tub_items = list()
    for i in range(1,4):
        tub_items.append(Item('tub1_item_'+str(i), 50, 50, 40, 1))
    t1 = Tub("t1", tub_items)
    packer[p].add_tub(t1)
    
    for i in range(4,5):
        packer[p].add_item(Item('50article_1', 50, 50, 20, 1))
        packer[p].add_item(Item('50article_2', 50, 20, 50, 1))
    
    tub_items = list()
    for i in range(6,9):
        tub_items.append(Item('tub2_item_'+str(i), 50, 50, 10, 1))
    t1 = Tub("t2", tub_items)
    packer[p].add_tub(t1)
    
    for i in range(9,11):
        packer[p].add_item(Item('30article_'+str(i), 30, 30, 30, 1))
    
    tub_items = list()
    for i in range(11,14):
        tub_items.append(Item('tub3_item_'+str(i), 30, 20, 10, 1))
    t1 = Tub("t3", tub_items)
    packer[p].add_tub(t1)
    
    for i in range(14,16):
        packer[p].add_item(Item('10article_'+str(i), 15, 15, 15, 1))
        
    packer[p].add_item(Item('aspect_article', 20, 20, 10, 1))

    random.Random(0).shuffle(packer[p].items)    

#%%

packer[0].pack(packing_algorithm="fake_skyline", packing_heuristic="bottom_left", bin_select_algorithm="first_fit", bin_select_dimension="volume", item_sorting="DVOL", bin_sorting="DVOL")
packer[1].pack(packing_algorithm="fake_skyline", packing_heuristic="bottom_left", bin_select_algorithm="first_fit", bin_select_dimension="volume", item_sorting="DLA")

packer[2].pack(packing_algorithm="fake_skyline", packing_heuristic="bottom_left", bin_select_algorithm="best_fit", bin_select_dimension="volume", item_sorting="DVOL")
packer[3].pack(packing_algorithm="fake_skyline", packing_heuristic="bottom_left", bin_select_algorithm="best_fit", bin_select_dimension="aspect_ratio", item_sorting="DVOL")

packer[4].pack(packing_algorithm="fake_skyline", packing_heuristic="bottom_left", bin_select_algorithm="worst_fit", bin_select_dimension="volume", item_sorting="DVOL")
packer[5].pack(packing_algorithm="fake_skyline", packing_heuristic="bottom_left", bin_select_algorithm="worst_fit", bin_select_dimension="volume", item_sorting="AVOL")

packer[6].pack(packing_algorithm="fake_skyline", packing_heuristic="max_contact", bin_select_algorithm="first_fit", bin_select_dimension="volume", item_sorting="DVOL")
packer[7].pack(packing_algorithm="fake_skyline", packing_heuristic="max_contact", bin_select_algorithm="best_fit", bin_select_dimension="volume", item_sorting="DVOL")

packer[8].pack(packing_algorithm="fake_skyline", packing_heuristic="corner", bin_select_algorithm="first_fit", bin_select_dimension="volume", item_sorting="DVOL")
packer[9].pack(packing_algorithm="fake_skyline", packing_heuristic="corner", bin_select_algorithm="best_fit", bin_select_dimension="volume", item_sorting="DVOL")

#%%
for p in range(0,10):
    # for j in packer[p].bins:
    #     j.plot_bin()
    packer[p].plot_packing()

