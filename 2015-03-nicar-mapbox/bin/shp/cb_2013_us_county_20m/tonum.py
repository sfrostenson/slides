import json


# this opens and reads a json file
def read(filename):
    with open(filename) as f:
        d = json.load(f)
    return d


# this writes output as json.
def write(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)


# this writes json so it's hierarchial structure is preserved.
def pretty_write(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, sort_keys=True,
                  indent=4, separators=(',', ': '))

data = read('joined.geojson')
features = data['features']

for feature in features:
    if feature['properties']['unemploy_3'] is not None:
        feature['properties']['unemploy_3'] = float(feature['properties']['unemploy_3'])
    else:
        feature['properties']['unemploy_3'] = -99

pretty_write(data, 'unemployment.geojson')
