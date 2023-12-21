from flask import Flask, request, jsonify
from algoritmo import traducir, guardar_en_excel, extraer_palabras
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Conectar a base de datos

# Cambia esto por una clave secreta fuerte
app.config['SECRET_KEY'] = 'clave-secreta'


@app.route('/')
def inicio():
    guardar_en_excel('hola', 'jarat')
    return 'listo'

# @app.route('/translate', methods=['GET', 'POST'])
# def index():
    

#     if request.method == 'POST':
#         package = request.json
#         data = package['paquete']
#         idiom1 = data['idiom1'] 
#         idiom2 = data['idiom2']
#         varidioma = data['texto']
#         print(idiom1, idiom2, varidioma)


#         num_palabras = len(varidioma.split())
#         print(num_palabras)
#         consulta = ""

#         if num_palabras == 1:
#             cursor = cnx.cursor()
#             # Consulta en caso de valores iguales

#             if idiom1 == 'Español' and idiom2 == 'Español':
#                 consulta = ("SELECT español FROM palabras WHERE español = %s", (varidioma,))
#             elif idiom1 == 'Embera' and idiom2 == 'Embera':
#                 consulta = ("SELECT embera FROM palabras WHERE embera = %s", (varidioma,))
#             elif idiom1 == 'Español' and idiom2 == 'Embera':
#                 consulta = ("SELECT embera FROM palabras WHERE español = %s", (varidioma,))
#             elif idiom1 == 'Embera' and idiom2 == 'Español':
#                 consulta = ("SELECT español FROM palabras WHERE embera = %s", (varidioma,))

#             cursor.execute(*consulta)
#             data = cursor.fetchone()
#             print('data', data)
#             cursor.close()
#             cnx.close()

#             output = ''
#             for palabra in data:
#                 output += palabra[0]
#             print(output)

#             if not output:
#                 print('No se encontraron coincidencias.')
#                 return jsonify({'translate': ''})
#             else:
#                 return jsonify({'translate': output})

#         elif num_palabras >= 2:
#             resultado = traducir(varidioma)
#             output = resultado[0] if resultado else ''
#             print(output)

#             if not output:
#                 print('No se encontraron coincidencias.')
#                 return jsonify({'translate': ''})
#             else:
#                 return jsonify({'translate': output})        
#     return jsonify({'translate': ''})


@app.route('/translate', methods=['GET', 'POST'])
def index():
    

    if request.method == 'POST':
        package = request.json
        data = package['paquete']
        idiom1 = data['idiom1'] 
        idiom2 = data['idiom2']
        varidioma = data['texto']
        print(idiom1, idiom2, varidioma)
        num_palabras = len(varidioma.split())
        print(num_palabras)
        if varidioma == "":
            return jsonify({'translate': ''})  
        else:
            resultado = traducir(varidioma, idiom1)
            output = resultado[0]

            if not output:
                print('No se encontraron coincidencias.')
                return jsonify({'translate': ''})
            else:
                return jsonify({'translate': output})
                
    return jsonify({'translate': ''})  

@app.route('/palabras', methods=['GET', 'POST'])
def introducir():

    if request.method == 'POST':

        data = request.json
        print(data)
        palabras = data['paquete']
        español = palabras['espanol']
        embera = palabras['embera']
        print(español, embera)
       # resultado = "Texto traducido" # Aquí debería estar el resultado de la traducción
        
        guardar_en_excel(español, embera)

        msge = f"{español}', '{embera}' guardadas correctamente"

        return jsonify({'msge': msge})



@app.route('/obtener', methods=['GET'])
def obtener_palabras():
    # Llamar a la función que extrae las palabras
    palabras_es, palabras_em = extraer_palabras()

    # Verificar si ambas listas tienen la misma longitud
    if len(palabras_es) != len(palabras_em):
        return jsonify({"error": "Las listas de palabras no tienen la misma longitud"})

    # Crear una lista de objetos con campos "espanol" y "embera"
    palabras_objetos = [{"espanol": palabras_es[i], "embera": palabras_em[i]} for i in range(len(palabras_es))]
    print(palabras_objetos)
    return jsonify(palabras_objetos)


if __name__ == '__main__':
    app.run(debug=True)


