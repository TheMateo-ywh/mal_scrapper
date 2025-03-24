from gazpacho import get, Soup
import pandas as pd
import datetime as dt
import pathlib

hoy=dt.date.today()

url1 = "https://myanimelist.net/topanime.php"
url2 = "https://myanimelist.net/topanime.php?limit=50"
html1 = get(url1)
html2 = get(url2)
soup1 = Soup(html1)
soup2 = Soup(html2)
cards1=soup1.find('tr',{'class':'ranking-list'})
cards2=soup2.find('tr',{'class':'ranking-list'})

def scrapping (card):
    rank=card.find('span',{'class':'lightLink top-anime-rank-text'}).text
    name=card.find('a',{'class':'hoverinfo_trigger'},partial=False).text
    score=card.find('span', {'class':'text on score'}).text
    return {'rank':rank,'name':name,'score':score}
text1=[scrapping(i) for i in cards1]
text2= [scrapping(i) for i in cards2]
text=text1+text2

if text:
    encabezados = list(text[0].keys())
    ancho_columnas = {encabezado: len(encabezado) for encabezado in encabezados}

    # Calcular el ancho máximo de cada columna
    for diccionario in text:
        for clave, valor in diccionario.items():
            ancho_columnas[clave] = max(ancho_columnas[clave], len(str(valor)))

    # Formatear los encabezados
    linea_encabezados = " | ".join(encabezado.ljust(ancho_columnas[encabezado]) for encabezado in encabezados)

    # Formatear las filas
    lineas_filas = []
    for diccionario in text:
        linea_fila = " | ".join(str(diccionario[clave]).ljust(ancho_columnas[clave]) for clave in encabezados)
        lineas_filas.append(linea_fila)

    # Combinar encabezados y filas
    tabla_formateada = linea_encabezados + "\n" + "\n".join(lineas_filas)
    
    p = pathlib.Path('List',f'{hoy}.txt')
    if not p.parent.exists():
        p.parent.mkdir()
        p.write_text(tabla_formateada, encoding='utf-8')
else:
    pathlib.Path(f'{hoy}.txt').write_text("Lista de diccionarios vacía.", encoding='utf-8')