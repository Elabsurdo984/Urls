import os
import requests
from bs4 import BeautifulSoup

# Leer URLs desde el archivo .txt
def leer_urls(archivo):
    if not os.path.exists(archivo):
        print(f"Error: El archivo '{archivo}' no existe.")
        return []
    
    with open(archivo, 'r') as f:
        urls = [line.strip() for line in f.readlines()]
        
    if not urls:
        print(f"El archivo '{archivo}' está vacío.")
        
    return urls

# Obtener el encabezado de la página
def obtener_header(response):
    return response.headers

# Obtener el título de la página
def obtener_titulo(soup):
    titulo = soup.title.string if soup.title else "No se encontró título"
    return titulo

# Obtener la descripción de la página
def obtener_resumen(soup):
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc and meta_desc.get('content'):
        return meta_desc['content']
    else:
        return "No se encontró resumen."

# Procesar cada URL
def procesar_pagina(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Imprimir URL y código de respuesta HTTP
        print(f"\nURL: {url}")
        print(f"Código de respuesta HTTP: {response.status_code}")

        # Imprimir encabezados de forma estructurada
        print("\n--- Encabezados ---")
        encabezados = obtener_header(response)
        for clave, valor in encabezados.items():
            print(f"{clave}: {valor}")

        # Imprimir título y resumen
        print("\n--- Título ---")
        print(obtener_titulo(soup))

        print("\n--- Resumen ---")
        print(obtener_resumen(soup))

    except requests.exceptions.RequestException as e:
        print(f"No se pudo procesar la URL {url}. Error: {e}")

# Ruta al archivo con las URLs
archivo_txt = "urls.txt"

# Leer las URLs y procesarlas
urls = leer_urls(archivo_txt)
if urls:
    for url in urls:
        procesar_pagina(url)
else:
    print("No se encontraron URLs para procesar.")

