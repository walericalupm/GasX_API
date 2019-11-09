import requests
import json
import unicodedata
from flask import Flask, jsonify

# Call above function
app = Flask(__name__)

@app.route('/api/v1/gas/price/<city>', methods=['GET'])
def readeraccession(city):
    obtainCityData(city.upper())
    return jsonify(obtainCityData(city.upper())), {'Content-Type': 'application/json'}

#obtiene la data de la API y la customiza
def obtainCityData(city):
    cityGas = []
    cityGasItem = {}
    url = 'https://www.mapabase.es/arcgis/rest/services/Otros/Gasolineras/FeatureServer/0/query?where=UPPER(localidad)%20like%20\'%25' + city + '%25\'&outFields=objectid,provincia,municipio,localidad,dirección,longitud,latitud,precio_gasolina_95,precio_gasóleo_a,precio_gasóleo_b,precio_bioetanol,precio_nuevo_gasóleo_a,precio_biodiesel,precio_gasolina_98,rótulo,tipo_venta,rem_,horario,horario00,fecha&outSR=4326&f=json'
    response = requests.get(url)
    if response.status_code == 200:
        data = json.loads(response.content.decode('utf8'))
        for gas in data['features']:
            print(gas['attributes'])
            for item in gas['attributes'].items():
                key = changeAccent(item[0])
                if item[1] == None:
                    if "precio"in item[0]:
                        cityGasItem.__setitem__(key, 0.00)
                    else:
                        cityGasItem.__setitem__(key, "")
                else:
                    cityGasItem.__setitem__(key, item[1])
            cityGas.append(cityGasItem)
    return cityGas

def changeAccent(key):
    trans_tab = dict.fromkeys(map(ord, u'\u0301\u0308'), None)
    noAccent = unicodedata.normalize('NFKC', unicodedata.normalize('NFKD', key).translate(trans_tab))
    return noAccent

if __name__=='__main__':
    app.run(host='0.0.0.0',
            debug=True,
            port=9200)

