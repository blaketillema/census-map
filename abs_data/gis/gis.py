import pandas as pd


AUS = pd.read_pickle('abs_data/gis/aus/aus.pkl.xz').dropna(subset=['geometry'])
# SA1 = pd.read_pickle('abs_data/gis/sa1/sa1.pkl.xz').dropna(subset=['geometry']).astype({'STE_CODE21': int, 'SA1_CODE21': 'int64'})
SA2 = pd.read_pickle('abs_data/gis/sa2/sa2.pkl.xz').dropna(subset=['geometry']).astype({'STE_CODE21': int, 'SA2_CODE21': int})
SA3 = pd.read_pickle('abs_data/gis/sa3/sa3.pkl.xz').dropna(subset=['geometry']).astype({'STE_CODE21': int, 'SA3_CODE21': int})
SA4 = pd.read_pickle('abs_data/gis/sa4/sa4.pkl.xz').dropna(subset=['geometry']).astype({'STE_CODE21': int, 'SA4_CODE21': int})
STE = pd.read_pickle('abs_data/gis/ste/ste.pkl.xz').dropna(subset=['geometry']).astype({'STE_CODE21': int})
CED = pd.read_pickle('abs_data/gis/ced/ced.pkl.xz').dropna(subset=['geometry']).astype({'STE_CODE21': int})
SAL = pd.read_pickle('abs_data/gis/sal/sal.pkl.xz').dropna(subset=['geometry']).astype({'STE_CODE21': int})