import json
import sys
#I use this file to easily reset the json fies
def Reffill(id):
    data = []
    #First the drinks


    data.append({
        'name': 'Pepsi',
        'cost': '1',
        'stock': '10',
        'slot': '1'
    })
    data.append({
        'name': 'Mountain Dew',
        'cost':  '1',
        'stock': '10',
        'slot': '2'
    })
    data.append({
        'name': 'Root Beer',
        'cost':  '1',
        'stock': '10',
        'slot': '3'
    })
    data.append({
        'name': 'Sprite',
        'cost':  '1',
        'stock': '10',
        'slot': '4'
    })
    data.append({
        'name': 'Starbucks Vanilla',
        'cost':  '2',
        'stock': '10',
        'slot': '5'
    })
    data.append({
        'name': 'Starbucks Mocha',
        'cost':  '2',
        'stock': '10',
        'slot': '6'
    })

    data.append({
        'name': 'Cheetos',
        'cost':  '1',
        'stock': '10',
        'slot': '7'
    })
    data.append({
        'name': 'Dorritos',
        'cost':  '1',
        'stock': '10',
        'slot': '8'
    })
    data.append({
        'name': 'Poptart',
        'cost':  '1',
        'stock': '10',
        'slot': '9'
    })
    data.append({
        'name': 'Big Texas',
        'cost':  '1.5',
        'stock': '10',
        'slot': '10'
    })
    data.append({
        'name': 'Donuts',
        'cost':  '1.5',
        'stock': '10',
        'slot': '11'
    })
    data.append({
        'name': 'Lays',
        'cost':  '1',
        'stock': '10',
        'slot': '12'
    })
    with open('Stock_%s.json' % id,'w') as outfile:
        json.dump(data, outfile, indent=4,sort_keys=True)
    