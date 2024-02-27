import os
import pandas as pd
import re


table_names = pd.read_excel(
    'abs_data/data/metadata/Metadata_2021_PEP_DataPack_R1_R2.xlsx',
    sheet_name='Table Number, Name, Population',
    skiprows=9,
    usecols=[0, 1],
    index_col=0
)

def short_to_long(idx):
    table, subgroup = idx[:3], idx[3:4]
    replacement = table_names.loc[table, 'Table name']
    if subgroup:
        return '{} ({})'.format(replacement, subgroup)
    return replacement

column_metadata = pd.read_excel(
    'abs_data/data/metadata/Metadata_2021_PEP_DataPack_R1_R2.xlsx', 
    sheet_name='Cell Descriptor Info', 
    skiprows=10,
    usecols=['Short', 'Long', 'DataPack file'],
    index_col=[2, 0]
).rename(index=short_to_long, level=0)

AUS = {
    short_to_long(re.match(r'2021Census_(?P<table>P\d{2}\w{0,1})_AUS_AUS\.csv', file).group('table'))
    :
    pd.read_csv(os.path.join('abs_data/data/data/AUS', file))
    for file in os.listdir('abs_data/data/data/AUS')
}

SA1 = {
    short_to_long(re.match(r'2021Census_(?P<table>P\d{2}\w{0,1})_AUST_SA1\.csv', file).group('table'))
    :
    pd.read_csv(os.path.join('abs_data/data/data/SA1/AUS', file))
    for file in os.listdir('abs_data/data/data/SA1/AUS')
}

SA2 = {
    short_to_long(re.match(r'2021Census_(?P<table>P\d{2}\w{0,1})_AUST_SA2\.csv', file).group('table'))
    :
    pd.read_csv(os.path.join('abs_data/data/data/SA2/AUS', file))
    for file in os.listdir('abs_data/data/data/SA2/AUS')
}

SA3 = {
    short_to_long(re.match(r'2021Census_(?P<table>P\d{2}\w{0,1})_AUST_SA3\.csv', file).group('table'))
    :
    pd.read_csv(os.path.join('abs_data/data/data/SA3/AUS', file))
    for file in os.listdir('abs_data/data/data/SA3/AUS')
}

SA4 = {
    short_to_long(re.match(r'2021Census_(?P<table>P\d{2}\w{0,1})_AUST_SA4\.csv', file).group('table'))
    :
    pd.read_csv(os.path.join('abs_data/data/data/SA4/AUS', file))
    for file in os.listdir('abs_data/data/data/SA4/AUS')
}

STE = {
    short_to_long(re.match(r'2021Census_(?P<table>P\d{2}\w{0,1})_AUST_STE\.csv', file).group('table'))
    :
    pd.read_csv(os.path.join('abs_data/data/data/STE/AUS', file))
    for file in os.listdir('abs_data/data/data/STE/AUS')
}

CED = {
    short_to_long(re.match(r'2021Census_(?P<table>P\d{2}\w{0,1})_AUST_CED\.csv', file).group('table'))
    :
    pd.read_csv(os.path.join('abs_data/data/data/CED/AUS', file))
    for file in os.listdir('abs_data/data/data/CED/AUS')
}
for table in CED:
    CED[table]['CED_CODE_2021'].replace('CED', '', inplace=True, regex=True)


SAL = {
    short_to_long(re.match(r'2021Census_(?P<table>P\d{2}\w{0,1})_AUST_SAL\.csv', file).group('table'))
    :
    pd.read_csv(os.path.join('abs_data/data/data/SAL/AUS', file))
    for file in os.listdir('abs_data/data/data/SAL/AUS')
}
for table in SAL:
    SAL[table]['SAL_CODE_2021'].replace('SAL', '', inplace=True, regex=True)