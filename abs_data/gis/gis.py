import pandas as pd


AUS = pd.read_pickle('abs_data/gis/aus/aus.pkl.xz').dropna(subset=['geometry'])
SA1 = pd.read_pickle('abs_data/gis/sa1/sa1.pkl.xz').dropna(subset=['geometry'])
SA2 = pd.read_pickle('abs_data/gis/sa2/sa2.pkl.xz').dropna(subset=['geometry'])
SA3 = pd.read_pickle('abs_data/gis/sa3/sa3.pkl.xz').dropna(subset=['geometry'])
SA4 = pd.read_pickle('abs_data/gis/sa4/sa4.pkl.xz').dropna(subset=['geometry'])
STE = pd.read_pickle('abs_data/gis/ste/ste.pkl.xz').dropna(subset=['geometry'])