import sys,os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon
from shapely.ops import unary_union
from tqdm import tqdm
from rtree import index
import numpy as np
from matplotlib import pyplot as plt
import math

def main(CAR_file, state_name, year_tags):

    print('Uploading CAR...')

    shapefile = gpd.read_file(CAR_file)
    df = shapefile.to_crs(6933)
    pol_list = []
    for elem in list(df['geometry']):
        if elem.is_valid:
            pol_list.append(elem)
        else:
            pol_list.append(elem.buffer(0))
    idx_pol = index.Index()
    for pos, cell in enumerate(pol_list):
        idx_pol.insert(pos, cell.bounds)

    output = {}

    for i, year_tag in enumerate(year_tags):
        n_failures = 0
        
        print('Indexing deforestation data: '+year_tag)
        
        def_file = state_name+'_def_'+year_tag+'/'+state_name+'_def_'+year_tag+'.shp'
        shapefile = gpd.read_file(def_file)
        df_def = shapefile.to_crs(6933)
        def_list_prelim = list(df_def['geometry'])

        def_list = []
        for def_poly in def_list_prelim:
            if def_poly.is_valid:
                def_list.append(def_poly)
            else:
                def_list.append(def_poly.buffer(0))

        idx_def = index.Index()
        for pos, cell in enumerate(def_list):
            idx_def.insert(pos, cell.bounds)
            
        data = {}
        pol_ids = list(df['cod_imovel'])
        
        print('Calculating statistics: '+year_tag)

        for num, pol in enumerate(tqdm(pol_list)):
            
            
            # handle property overlaps
            candidate_overlaps = [pol_list[pos] for pos in idx_pol.intersection(pol.bounds)]
            overlaps = [poly for poly in candidate_overlaps if poly.intersects(pol) and not poly.equals(pol)]
            real_overlaps = [poly for poly in overlaps if poly.intersection(pol).area > 10000]
            num_overlaps = len(real_overlaps)
            overlap_union = unary_union(overlaps)
            overlap_region = overlap_union.intersection(pol)
            area_overlap = overlap_region.area

            try:
                # handle deforestation
                candidate_def = [def_list[pos] for pos in idx_def.intersection(pol.bounds)]
                overlap_def_pols = [def_pol for def_pol in candidate_def if overlap_region.intersects(def_pol)]
                overlap_def_union = unary_union(overlap_def_pols)
                overlap_def = overlap_def_union.intersection(overlap_region)
                area_overlap_def = overlap_def.area
                
                total_def = overlap_def_union.intersection(pol)
                area_total_def = total_def.area
            
            except:
                area_overlap_def = 0
                area_total_def = 0
                n_failures += 1

            
            # output
            data[pol_ids[num]] = {
                'prop_area': pol.area / 10000,
                'num_overlaps_1ha_buffer': num_overlaps,
                'area_overlap': area_overlap / 10000,
                'area_overlap_def': area_overlap_def / 10000,
                'area_total_def': area_total_def / 10000
            }
        print('Failures:', n_failures)
        output[year_tag] = data

    out = {}
    for cod_imovel in list(df['cod_imovel']):
        out[cod_imovel] = {}
        out[cod_imovel]['prop_area'] = output[year_tags[0]][cod_imovel]['prop_area']
        out[cod_imovel]['num_overlaps_1ha_buffer'] = output[year_tags[0]][cod_imovel]['num_overlaps_1ha_buffer']
        out[cod_imovel]['area_overlap'] = output[year_tags[0]][cod_imovel]['area_overlap']
        for year_tag in year_tags:
            out[cod_imovel]['area_overlap_def_'+year_tag] = output[year_tag][cod_imovel]['area_overlap_def']
            out[cod_imovel]['area_total_def_'+year_tag] = output[year_tag][cod_imovel]['area_total_def']
    df_out = pd.DataFrame.from_dict(out, orient='index')
    out_file = state_name+'_def_statistics.csv'
    df_out.to_csv(out_file)
    print('Finished. Saved to '+out_file)
    return 0

if __name__ == '__main__':
    args = sys.argv
    if len(sys.argv) < 4:
        print('Error. Please provide more arguments.')
    else:
        main(args[1], args[2], args[3:])