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

# Procesar cada URL y guardar en archivo
def procesar_pagina(url, archivo_resultado):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Guardar y mostrar URL y código de respuesta HTTP
        with open(archivo_resultado, 'a') as f:
            f.write(f"\nURL: {url}\n")
            f.write(f"Código de respuesta HTTP: {response.status_code}\n")
            print(f"\nURL: {url}")
            print(f"Código de respuesta HTTP: {response.status_code}")

            # Guardar y mostrar encabezados HTTP
            f.write("\n--- Encabezados ---\n")
            print("\n--- Encabezados ---")
            encabezados = obtener_header(response)
            for clave, valor in encabezados.items():
                f.write(f"{clave}: {valor}\n")
                print(f"{clave}: {valor}")

            # Guardar y mostrar título
            f.write("\n--- Título ---\n")
            titulo = obtener_titulo(soup)
            f.write(f"{titulo}\n")
            print(f"\n--- Título ---")
            print(titulo)

            # Guardar y mostrar resumen
            f.write("\n--- Resumen ---\n")
            resumen = obtener_resumen(soup)
            f.write(f"{resumen}\n")
            print(f"\n--- Resumen ---")
            print(resumen)

    except requests.exceptions.RequestException as e:
        with open(archivo_resultado, 'a') as f:
            f.write(f"No se pudo procesar la URL {url}. Error: {e}\n")
        print(f"No se pudo procesar la URL {url}. Error: {e}")

# Ruta al archivo con las URLs
archivo_txt = "urls.txt"
# Ruta al archivo donde se guardarán los resultados
archivo_resultado = "resultados.txt"

# Limpiar o crear archivo de resultados
with open(archivo_resultado, 'w') as f:
    f.write("Resultados del procesamiento de URLs:\n")

# Leer las URLs y procesarlas
urls = leer_urls(archivo_txt)
if urls:
    for url in urls:
        procesar_pagina(url, archivo_resultado)
else:
    print("No se encontraron URLs para procesar.")
