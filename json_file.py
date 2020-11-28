import json

import json

data = {}
data['coordenadas'] = []
data['coordenadas'].append({
    'x': 50,
    'y': 60,
    'color': '#FFA500'
})
data['coordenadas'].append({
    'x': 80,
    'y': 60,
    'color': '#F0A325'
})
data['coordenadas'].append({
    'x': 70,
    'y': 50,
    'color': '#AC3548'
    
})

with open('data.txt', 'w') as outfile:
    json.dump(data, outfile)