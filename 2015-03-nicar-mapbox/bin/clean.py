import csv
import math


# this opens and reads a csv data as a list
# and is called in our read_as_dict function
def read(filename):
    data = []
    with open(filename, 'rU') as f:
        f = csv.reader(f)
        for row in f:
            data.append(row)

    return data


# this opens and reads csv data as a dict
def read_as_dict(filename):
    csv = read(filename)
    headers = csv.pop(0)
    data = list()
    for row in csv:
        d = dict()
        for index, header in enumerate(headers):
            d[header] = row[index]
        data.append(d)
    return data


# this writes output as a csv
def write(data, filename):
    with open(filename, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(data)


# function for finding the min/max & natural quantiles in our data.
def quantiles(l):
    all_indexes = sorted(l)
    # filter out '-99.0'
    filtered = filter(lambda a: a != -99.0, all_indexes)
    minimum = min(filtered)
    maximum = max(filtered)
    divisions = 5
    num_entries = len(l)
    division = int(math.ceil(num_entries / divisions))

    stops = list()
    for n in range(0, 5):
        stops.append(filtered[n * division])

    return minimum, maximum, stops


### STEP ONE: Read csv in as one list of lists of dictionaries.
### Next, clean data and build node.
data = read_as_dict('unemployment-no-headers.csv')

# next remove all state level data && PR data
# we're only interested in mapping US county data.
counties = list()

for row in data:
    if row['Cnty_FIPS'] == '000':
        continue
    if row['State'] == 'PR':
        continue
    else:
        counties.append(row)

# build node w/ unemployment 2013 data
node = list()

for row in counties:
    att = dict()
    att['FIPS'] = row['FIPS_Code']
    att['c'] = row['Area_name']
    att['s'] = row['State']
    att['rate'] = row['Unemployment_rate_2013']
    node.append(att)

# assign empty unemployment rates a value of -99.0
for row in node:
    if row['rate'] == ' ':
        row['rate'] = '-99.0'


# STEP TWO: Calculate quantiles.

# first, convert rate to float to find proper data breaks.
unemploy_rate = []

for row in node:
    rate = float(row['rate'])
    unemploy_rate.append(rate)

print quantiles(unemploy_rate)


# STEP THREE: Write node to file.
headers = ['FIPS', 'c', 's', 'rate']

result = list()
for row in node:
    result_row = list()

    for key in headers:
        result_row.append(row[key])

    result.append(result_row)

headers = [headers]
result = headers + result

# write result
write(result, "unemployment.csv")
