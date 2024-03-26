import sys,os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon
from shapely.ops import unary_union
from shapely.validation import make_valid
from tqdm import tqdm
from rtree import index
import numpy as np
from matplotlib import pyplot as plt
import math

def main(CAR_file, LR_file, state_name, muni_name):

    print('Uploading CAR...')

    shapefile = gpd.read_file(CAR_file)
    df = shapefile.to_crs(6933)
    pol_list = []
    for elem in list(df['geometry']):
        if elem.is_valid:
            pol_list.append(elem)
        else:
            pol_list.append(make_valid(elem.buffer(0)))
    idx_pol = index.Index()
    for pos, cell in enumerate(pol_list):
        idx_pol.insert(pos, cell.bounds)

    munis = list(df[muni_name])

    output = {}

    n_failures = 0
    
    print('Indexing LR data')
    
    shapefile = gpd.read_file(LR_file)
    df_lr = shapefile.to_crs(6933)
    lr_list_prelim = list(df_lr['geometry'])

    lr_list = []
    for lr_poly in lr_list_prelim:
        lr_list.append(make_valid(lr_poly.buffer(0)))

    idx_lr = index.Index()
    for pos, cell in enumerate(lr_list):
        idx_lr.insert(pos, cell.bounds)
        
    data = {}
    pol_ids = list(df['cod_imovel'])
    
    print('Calculating statistics')

    for num, pol in enumerate(tqdm(pol_list)):
        
        # handle property overlaps
        candidate_overlaps = [pol_list[pos] for pos in idx_pol.intersection(pol.bounds)]
        overlaps = [poly for poly in candidate_overlaps if poly.intersects(pol) and not poly.equals(pol)]
        overlap_union = make_valid(unary_union(overlaps).buffer(0))
        overlap_region = make_valid(overlap_union.intersection(pol).buffer(0))
        area_overlap = overlap_region.area

        candidate_lr = [lr_list[pos] for pos in idx_lr.intersection(pol.bounds)]
        lr_pols = [lr_pol for lr_pol in candidate_lr if pol.intersects(lr_pol)]
        lr_union = make_valid(unary_union(lr_pols).buffer(0))

        overlap_lr = make_valid(lr_union.intersection(overlap_region).buffer(0))
        area_overlap_lr = overlap_lr.area

        total_lr = make_valid(lr_union.intersection(pol))
        area_total_lr = total_lr.area
        
        # output
        data[pol_ids[num]] = {
            'cod_ibge': munis[num],
            'state': state_name,
            'prop_area': pol.area / 10000,
            'area_overlap': area_overlap / 10000,
            'area_overlap_lr': area_overlap_lr / 10000,
            'area_total_lr': area_total_lr / 10000
        }
    print('Failures:', n_failures)
    output = data
    
    df_out = pd.DataFrame.from_dict(output, orient='index')
    out_file = state_name+'_LR_statistics_CS2.csv'
    df_out.to_csv(out_file)
    print('Finished. Saved to '+out_file)
    return 0

if __name__ == '__main__':
    args = sys.argv
    if len(sys.argv) < 4:
        print('Error. Please provide more arguments.')
    else:
        # ex.
        # python LR_statistics_CS.py CAR_file.shp LR_file.shp AC cod_muni
        main(args[1], args[2], args[3], args[4])