#ВАЖНО! Изменить модуль для работы с файлами из веб-панели
import pandas as pd
from utils.const_data import *

def load_raw_fish_data():
    #Необработанные данные о выловленной рыбе
    raw_fish_data = pd.read_csv(DATA_PATH + "Ext2.csv", sep=",", parse_dates=['date_vsd'])
    raw_fish_data.loc[raw_fish_data['unit'] == 'тонна', 'volume'] *= 1000
    raw_fish_data.drop(columns=['unit'], inplace=True)
    return raw_fish_data

def load_raw_ship_data():
    #Необработанные данные о судне
    raw_ship_data = pd.read_csv(DATA_PATH + "Ext.csv", sep=",", parse_dates=['date_fishery'])
    raw_ship_data.drop(columns=['numPart'], inplace=True)
    return raw_ship_data

def load_merged_data():
    #Обьединение данных
    raw_ship_data = load_raw_ship_data()
    raw_fish_data = load_raw_fish_data()
    merged_data = merge_raw_data(raw_fish_data, raw_ship_data)
    return merged_data

def merge_raw_data(raw_fish_data: pd.DataFrame, raw_ship_data: pd.DataFrame):
    merged_data = pd.merge(raw_ship_data, raw_fish_data)
    return merged_data


