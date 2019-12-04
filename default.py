import json
import sys
#I use this file to easily reset the json fies
data = {}
#First the drinks

data['Drinks'] = []
data['Drinks'].append({
    'name': 'Pepsi',
    'cost': '1',
    'stock': '10',
    'slot': '1'
})
data['Drinks'].append({
    'name': 'Mountain Dew',
    'cost':  '1',
    'stock': '10',
    'slot': '2'
})
data['Drinks'].append({
    'name': 'Root Beer',
    'cost':  '1',
    'stock': '10',
    'slot': '3'
})
data['Drinks'].append({
    'name': 'Sprite',
    'cost':  '1',
    'stock': '10',
    'slot': '4'
})
data['Drinks'].append({
    'name': 'Starbucks Vanilla',
    'cost':  '2',
    'stock': '10',
    'slot': '5'
})
data['Drinks'].append({
    'name': 'Starbucks Mocha',
    'cost':  '2',
    'stock': '10',
    'slot': '6'
})
data['Snacks'] = []
data['Snacks'].append({
    'name': 'Cheetos',
    'cost':  '1',
    'stock': '10',
    'slot': '7'
})
data['Snacks'].append({
    'name': 'Dorritos',
    'cost':  '1',
    'stock': '10',
    'slot': '8'
})
data['Snacks'].append({
    'name': 'Poptart',
    'cost':  '1',
    'stock': '10',
    'slot': '9'
})
data['Snacks'].append({
    'name': 'Big Texas',
    'cost':  '1.5',
    'stock': '10',
    'slot': '10'
})
data['Snacks'].append({
    'name': 'Donuts',
    'cost':  '1.5',
    'stock': '10',
    'slot': '11'
})
data['Snacks'].append({
    'name': 'Lays',
    'cost':  '1',
    'stock': '10',
    'slot': '12'
})
with open('Stock_%s.json' % (sys.argv[1]),'w') as outfile:
    json.dump(data, outfile, indent=4,sort_keys=True)
    