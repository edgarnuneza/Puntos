from json_file import leer_json_file, crear_json_file
import json

x = leer_json_file('juego')
z = json.dumps(x, indent=0)

print(z)