import json
import sys
#I use this file to easily reset the json fies
data = {}
#First the drinks
data['Drinks'] = []
data['Drinks'].append({
    'name': 'Pepsi',
    'cost': '.000011',
    'stock': '10',
    'slot': '1'
})
data['Drinks'].append({
    'name': 'Mountain Dew',
    'cost': '.000012',
    'stock': '10',
    'slot': '2'
})
data['Drinks'].append({
    'name': 'Root Beer',
    'cost': '.000013',
    'stock': '10',
    'slot': '3'
})
data['Drinks'].append({
    'name': 'Sprite',
    'cost': '.000014',
    'stock': '10',
    'slot': '4'
})
data['Drinks'].append({
    'name': 'Starbucks Vanilla',
    'cost': '.0000135',
    'stock': '10',
    'slot': '5'
})
data['Drinks'].append({
    'name': 'Starbucks Mocha',
    'cost': '.000016',
    'stock': '10',
    'slot': '6'
})
data['Snacks'] = []
data['Snacks'].append({
    'name': 'Cheetos',
    'cost': '.000017',
    'stock': '10',
    'slot': '7'
})
data['Snacks'].append({
    'name': 'Dorritos',
    'cost': '.000018',
    'stock': '10',
    'slot': '8'
})
data['Snacks'].append({
    'name': 'Poptart',
    'cost': '.000019',
    'stock': '10',
    'slot': '9'
})
data['Snacks'].append({
    'name': 'Big Texas',
    'cost': '.000020',
    'stock': '10',
    'slot': '10'
})
data['Snacks'].append({
    'name': 'Donut',
    'cost': '.000021',
    'stock': '10',
    'slot': '11'
})
data['Snacks'].append({
    'name': 'Lays',
    'cost': '.000022',
    'stock': '10',
    'slot': '12'
})
with open('Stock_%s.txt' % (sys.argv[1]),'w') as outfile:
    json.dump(data, outfile, indent=4,sort_keys=True)
    