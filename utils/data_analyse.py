from warnings import simplefilter
simplefilter(action='ignore', category=FutureWarning)

from utils.second_db_parser import *
from utils.word_editor import *
from fuzzywuzzy import fuzz

import pandas as pd
import numpy as np
import datetime


class Analyzer:

    class RawAnalys:

        def get_null_volumes(merged_data: pd.DataFrame):
            return merged_data[merged_data['volume'] == 0]
        
        def get_product_list(merged_data: pd.DataFrame):
            product_list = merged_data[merged_data['id_fish'] == -1]
            return product_list
        
        def get_fish_list(merged_data: pd.DataFrame):
            fish_list = merged_data[merged_data['id_fish'] != -1]
            return fish_list
    
    class PlatAnalys:

        def get_plat_anomaly_count(merged_data: pd.DataFrame, id_plat: int,):
            data = Analyzer.CompareAnalys.get_product_and_fish(merged_data, id_plat)
            return len(data)

        def get_id_plat_list(merged_data: pd.DataFrame):
            plat_list = merged_data['id_Plat'].unique()
            return plat_list

        def get_id_plat_null_list(merged_data: pd.DataFrame):
            plat_null = Analyzer.RawAnalys.get_null_volumes(merged_data)['id_Plat'].unique()
            return plat_null
        
        def get_plat_null_records(id_plat: int, merged_data: pd.DataFrame):
            plat_null = Analyzer.RawAnalys.get_null_volumes(merged_data)
            plat_null_records = plat_null[plat_null['id_Plat'] == id_plat]
            return plat_null_records
        
        def get_plat_products(id_plat: int, merged_data: pd.DataFrame):
            products = Analyzer.RawAnalys.get_product_list(merged_data)
            plat_products = products[products['id_Plat'] == id_plat]
            return plat_products
        
        def get_plat_fish(id_plat: int, merged_data: pd.DataFrame):
            fish_list = Analyzer.RawAnalys.get_fish_list(merged_data)
            plat_fish = fish_list[fish_list['id_Plat'] == id_plat]
            return plat_fish
    
    class CompareAnalys:

        def get_product_and_fish(merged_data: pd.DataFrame, id_plat: int):
            generated_data = pd.DataFrame(data=None, columns=merged_data.columns, index=None)
            plat_data = merged_data[merged_data['id_Plat'] == id_plat]
            plat_products = Analyzer.RawAnalys.get_product_list(plat_data)
            plat_fish = Analyzer.RawAnalys.get_fish_list(plat_data)
            for i_prod, r_prod in plat_products.iterrows():
                for i_fish, r_fish in plat_fish.iterrows():
                    if int(fuzz.token_sort_ratio(r_prod['fish'], r_fish['fish'])) >= 70:
                        if abs(r_fish['date_fishery'] - r_prod['date_fishery']) <= datetime.timedelta(days=2):
                            volume_diff = r_prod['volume'] - r_fish['volume']
                            if volume_diff > 0:
                                if (abs(volume_diff) / r_prod['volume']) * 100 > 10:
                                    generated_data = generated_data.append(r_prod)
                                    generated_data['volume_diff'] = abs(volume_diff)
                            elif volume_diff < 0:
                                if (abs(volume_diff) / r_fish['volume']) * 100 > 10:
                                    generated_data = generated_data.append(r_fish)
                                    generated_data['volume_diff'] = abs(volume_diff)
            unique_vsd = generated_data['id_vsd'].unique()
            output_columns = {('id_ves', int), ('id_own', int),
                            ('date', str), ('id_vsd', int),
                            ('num_vsd', int), ('id_Plat', int),
                            ('Name_Plat', str), ('Region_Plat', str), 
                            ('fish', str), ('volume', int), ('volume_diff', int)}
            output_data = pd.DataFrame({k: pd.Series(dtype=t) for k, t in output_columns})
            output_data['date'] = output_data['date'].astype('datetime64')
            for i in unique_vsd:
                new_row = generated_data[generated_data['id_vsd'] == i].iloc[0]
                append_row_data = {'id_ves': new_row['id_ves'], 'id_own': new_row['id_own'],
                                    'date': new_row['date_fishery'], 'id_vsd': new_row['id_vsd'],
                                    'num_vsd': new_row['num_vsd'], 'id_Plat': new_row['id_Plat'],
                                    'Name_Plat': new_row['Name_Plat'], 'Region_Plat': new_row['Region_Plat'],
                                    'fish': new_row['fish'],'volume': new_row['volume'], 'volume_diff': new_row['volume_diff']}
                append_row = pd.Series(data=append_row_data, name='')
                output_data = output_data.append(append_row)
            return output_data
        
        def get_all_differences(merged_data: pd.DataFrame):
            plat_id_list = Analyzer.PlatAnalys.get_id_plat_list(merged_data)
            all_data = pd.DataFrame()
            for i in plat_id_list:
                output_data = Analyzer.CompareAnalys.get_product_and_fish(merged_data, i)
                all_data = all_data.append(output_data)
            return all_data

