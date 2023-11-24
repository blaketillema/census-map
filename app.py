import time

from flask import Flask, render_template, request

# from abs_data.data import metadata
from abs_data.gis import SA1, SA2


app = Flask(__name__)

levels = {
    'SA1': SA1,
    'SA2': SA2
}

states = {
    'NSW': 1, 'VIC': 2, 'QLD': 3,  'SA': 4,
    'WA': 5,  'TAS': 6,  'NT': 7, 'ACT': 8,
}

@app.route('/')
def index():
    return render_template('index.html', states=states.keys(), levels=levels.keys())

@app.route('/data')
def data():
    state_list = request.args.getlist('states')
    level = request.args.get('level')

    if level not in levels:
        return "{} not a valid level {{}}".format(level, levels.keys()), 400
    
    for state in state_list:
        if state not in states:
            return "{} not a valid state {{}}".format(state, states.keys()), 400
    
    return get_geojson(level, state_list)


def get_geojson(level: str, state_list: list[str]):

    start = time.time()
    requested_map = levels[level.upper()]

    if state_list:
        out = requested_map[requested_map['STE_CODE21'].isin([str(states[state]) for state in state_list])].to_json()
    else:
        out = requested_map.to_json()

    print(f'time to return {time.time() - start}')
    return out


if __name__ == '__main__':
    app.run()