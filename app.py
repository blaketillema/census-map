import pandas as pd

from flask import Flask, render_template, request
from geopandas import GeoDataFrame
from matplotlib import colormaps
from matplotlib.colors import Normalize
from typing import Literal

from abs_data.data import column_metadata, short_to_long
from abs_data import data
from abs_data import gis


app = Flask(__name__)


levels = {
    'AUS': {
        'map': gis.AUS,
        'data': data.AUS
    },
    'SA1': {
        'map': gis.SA1,
        'data': data.SA1
    },
    'SA2': {
        'map': gis.SA2,
        'data': data.SA2
    },
    'SA3': {
        'map': gis.SA3,
        'data': data.SA3
    },
    'SA4': {
        'map': gis.SA4,
        'data': data.SA4
    },
    'STE': {
        'map': gis.STE,
        'data': data.STE
    },
    'CED': {
        'map': gis.CED,
        'data': data.CED
    },
    'SAL': {
        'map': gis.SAL,
        'data': data.SAL
    }
}

states = {
    'NSW': 1, 'VIC': 2, 'QLD': 3,  'SA': 4,
    'WA': 5,  'TAS': 6,  'NT': 7, 'ACT': 8,
}

datapacks = column_metadata.groupby(level=0).apply(lambda x: x.droplevel(0).to_dict()['Long']).to_dict()


@app.route('/')
def index():
    return render_template(
        template_name_or_list='index.html', 
        states=states.keys(), 
        levels=levels.keys(), 
        datapacks=datapacks
    )


@app.route('/data')
def get_data():
    level = request.args.get('level', 'STE')

    if level not in levels:
        return "{} not a valid level {{}}".format(level, levels.keys()), 404
    
    state_list = request.args.getlist('states')
    
    for state in state_list:
        if state not in states:
            return "{} not a valid state {{}}".format(state, states.keys()), 404
    
    statistic = request.args.get('statistic')
    if statistic:
        table, field = ':'.join(statistic.split(':')[:-1]), statistic.split(':')[-1]
        if table not in datapacks:
            return "{} not a valid table name {{}}".format(table, datapacks.keys())
        if field not in datapacks[table]:
            return "{} not a valid field of {} {{}}".format(field, table, datapacks[table].keys())
    
    function = request.args.get('function')
    if function and function not in ['normalise', 'density']:
        return "{} not a valid function {{}}".format(function, ['normalise', 'density'])

    return get_geojson(level, state_list, statistic, function)


@app.route('/test')
def metadata():
    statistic = 'P01:Tot_P_M'
    table, field = ':'.join(statistic.split(':')[:-1]), statistic.split(':')[-1]
    requested_map = levels['AUS']['map']
    requested_df = levels['AUS']['data'][table]
    joined = requested_map.merge(
        requested_df, 
        left_on=requested_map.columns[0], 
        right_on=requested_df.columns[0]
    )[[*requested_map.columns, field]].rename(
        columns={
            field: datapacks[short_to_long(table)][field].replace('_', ' ')
        }
    )
    out = joined.to_json()
    return out


def get_geojson(level: str, state_list: list[str], statistic: str | None, function: Literal['normalise', 'density'] | None = None):

    requested_map: GeoDataFrame = levels[level.upper()]['map']
    columns = requested_map.columns.copy()

    if state_list and level != 'AUS':
        if statistic:
            table, field = ':'.join(statistic.split(':')[:-1]), statistic.split(':')[-1]
            requested_df = levels[level.upper()]['data'][table]
            out = requested_map[
                requested_map['STE_CODE21'].isin([states[state] for state in state_list])
            ].merge(
                requested_df, left_on=columns[0], right_on=requested_df.columns[0]
            )
        else:
            out = requested_map[
                requested_map['STE_CODE21'].isin([states[state] for state in state_list])
            ]
    else:
        if statistic:
            table, field = ':'.join(statistic.split(':')[:-1]), statistic.split(':')[-1]
            requested_df = levels[level.upper()]['data'][table]
            out = requested_map.merge(
                requested_df, left_on=columns[0], right_on=requested_df.columns[0]
            )
        else:
            out = requested_map
    
    if function == 'density':
        if state_list and level != 'AUS':
            out[field] /= requested_map[requested_map['STE_CODE21'].isin([states[state] for state in state_list])]['AREASQKM21']
        else:
            out[field] /= requested_map['AREASQKM21']

    column_mapper = {
        f'{level.upper()}_CODE21': 'code',
        f'{level.upper() if level.upper() != "SA1" else "SA2"}_NAME21': 'name',
    }
    colour_map = {}
    if statistic:
        column_mapper[field] = 'targetStatistic'
        min_stat, max_stat = min(out[field]), max(out[field])
        cmap = colormaps.get_cmap('plasma')
        norm = Normalize(min_stat, max_stat)
        normalised = out.set_index(f'{level.upper()}_CODE21')[field].map(norm)
        colours = normalised.map(cmap)
        colours_df = pd.merge(normalised, colours, left_index=True, right_index=True)
        colours_df.columns = ['norm', 'colour']
        colour_map = colours_df.to_dict(orient='index')


    return {'data': out.rename(columns=column_mapper).to_json(), 'colours': colour_map}


if __name__ == '__main__':
    app.run(debug=True)