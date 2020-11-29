import json

def crear_json_file(nombre_archivo):
    data = {}
    data= []
    """data.append({
    'x': 50,
        'y': 60,
        'color': '#FFA500'
    })
    data.append({
        'x': 80,
        'y': 60,
        'color': '#F0A325'
    })
    data.append({
        'x': 70,
        'y': 50,
        'color': '#AC3548'
    })
        """
    with open('coordenadas/'+ nombre_archivo +'.txt', 'w') as outfile:
        json.dump(data, outfile)

def leer_json_file(nombre_archivo):
    with open('coordenadas/' + nombre_archivo + '.txt') as json_file:
        data = json.load(json_file)
        
    return data


    """def __init__(self, nombre_archivo):
        data = {}
        data= []
        '''data.append({
            'x': 50,
            'y': 60,
            'color': '#FFA500'
        })
        data.append({
            'x': 80,
            'y': 60,
            'color': '#F0A325'
        })
        data.append({
            'x': 70,
            'y': 50,
            'color': '#AC3548'
            
        })
        '''
        with open('coordenadas/'+ str(nombre_archivo) +'.txt', 'w') as outfile:
            json.dump(data, outfile)
                """
