import pandas as pd
import spacy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import os

# Creamos una instancia del modelo de procesamiento del lenguaje natural de Spacy para el idioma español.

  # Cargamos el dataframe que contiene las frases en español y en lengua indígena.
    #df = pd.read_csv('DiccionarioEm.csv')
# nlp = spacy.load("es_core_news_sm")

df = pd.read_excel('DiccionarioEm.xlsx')

def traducir(frase, idiom):
  print(idiom)
  if idiom == 'Embera':
        columna_origen = 'em'
        columna_destino = 'es'
  else: 
        columna_origen = 'es'
        columna_destino = 'em'

  num_palabras = len(frase.split())

  if num_palabras == 1:
        
      traduccion_directa = df.loc[df[columna_origen] == frase, columna_destino].values
      if len(traduccion_directa) > 0:
            return traduccion_directa

    # Creamos una instancia del vectorizador CountVectorizer para convertir las frases en español a vectores.
  vectorizer = CountVectorizer()

    # Convertimos las frases en español a vectores.
  X_vect = vectorizer.fit_transform(df[columna_origen])

    # Creamos una instancia del modelo de regresión logística y lo entrenamos con los datos.
  lr_model = LogisticRegression()
  lr_model.fit(X_vect, df[columna_destino])
   # Utilizamos Spacy para lematizar y procesar la frase en español.
  # doc = nlp(frase)

    # Extraemos los lemas de las palabras en la frase.
  # lemas = [token.lemma_ for token in doc]

    # Convertimos los lemas a una frase procesada.
  # frase_procesada = ' '.join(lemas)

    # Convertimos la frase en español a un vector utilizando el vectorizador CountVectorizer.
  frase_vect = vectorizer.transform([frase])

        # Utilizamos el modelo de regresión logística para predecir la traducción en lengua indígena.
  frase_traducida = lr_model.predict(frase_vect)

  return frase_traducida

def guardar_en_excel(español, embera):

    df = pd.read_excel('DiccionarioEm.xlsx')
    # Agregar las nuevas palabras al DataFrame
    nueva_fila = pd.DataFrame({'es': [español], 'em': [embera]})
    df = pd.concat([df, nueva_fila], ignore_index=True)

    # Guardar el DataFrame actualizado en el archivo Excel
    df.to_excel('DiccionarioEm.xlsx', index=False)

def extraer_palabras():
    # Leer el DataFrame desde el archivo Excel
    df = pd.read_excel('DiccionarioEm.xlsx')

    # Extraer las palabras de las columnas 'es' y 'em'
    palabras_es = df['es'].tolist()
    palabras_em = df['em'].tolist()

    # Retornar las listas de palabras
    return palabras_es, palabras_em