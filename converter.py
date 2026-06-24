"""
Módulo encargado de la extracción estructurada de texto y tablas desde archivos PDF.
Implementado mediante un algoritmo de segmentación geométrica determinista con pdfplumber.
Garantiza la preservación del orden cronológico visual y del formato de tablas en Markdown,
eliminando por completo dependencias de Inteligencia Artificial, OCR o entornos ONNX.
"""
import os
import re
import pdfplumber

def limpiar_texto_para_filtro(texto: str) -> str:
    """
    Normaliza el texto plano del PDF eliminando múltiples espacios horizontales
    y limpiando saltos de línea huérfanos para entregar tokens continuos al filtro.
    """
    if not texto:
        return ""

    lineas = texto.split('\n')
    lineas_limpias = []

    for linea in lineas:
        l = linea.strip()
        if l:
            # Colapsar múltiples espacios o tabulaciones inter-palabra
            l = re.sub(r'[ \t]+', ' ', l)
            lineas_limpias.append(l)

    if not lineas_limpias:
        return ""

    texto_unido = lineas_limpias[0]
    for i in range(1, len(lineas_limpias)):
        linea_anterior = lineas_limpias[i-1]
        linea_actual = lineas_limpias[i]

        # Heurísticas para mantener el salto de línea:
        # 1. La línea anterior termina en punto, dos puntos, u otra puntuación de cierre
        termina_en_puntuacion = re.search(r'[.:;!?]$', linea_anterior) is not None
        # 2. La línea actual es todo mayúsculas (un título)
        es_mayusculas = linea_actual.isupper()
        # 3. La línea actual empieza con una viñeta o número
        es_vineta = re.match(r'^([-*•]|\d+\.)', linea_actual) is not None
        # 4. La línea actual tiene un ":" (indica un nuevo campo) y la línea anterior era corta
        es_nuevo_campo = (':' in linea_actual) and len(linea_anterior) < 60

        if termina_en_puntuacion:
            # Ya tiene puntuación, solo agregamos un espacio
            texto_unido += " " + linea_actual
        elif es_mayusculas or es_vineta or es_nuevo_campo:
            # Es una idea nueva pero no tenía puntuación previa, insertamos un punto como separador seguro
            texto_unido += ". " + linea_actual
        else:
            # Es la continuación del párrafo (nombres largos o textos envueltos)
            texto_unido += " " + linea_actual

    return texto_unido

def convert_file(file_path: str) -> str:
    """
    Función principal encargada de la conversión de archivos para Streamlit.
    Aplica segmentación vertical por coordenadas para entrelazar texto y tablas en orden exacto.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No se encontró el archivo: {file_path}")

    if not file_path.lower().endswith('.pdf'):
        raise ValueError(f"Solo se admiten archivos PDF: {file_path}")

    contenido_documento = []

    # Abrir el PDF mediante procesamiento geométrico puro (pdfplumber)
    with pdfplumber.open(file_path) as pdf:
        for pagina in pdf.pages:
            ancho_pag = pagina.width
            alto_pag = pagina.height

            # 1. Detectar las tablas presentes en la página utilizando topología de líneas
            tablas_detectadas = pagina.find_tables()

            # 2. Ordenar las tablas de arriba hacia abajo de forma secuencial estricta
            tablas_ordenadas = sorted(tablas_detectadas, key=lambda t: (t.bbox[1], t.bbox[0]))

            y_actual = 0  # Puntero de rastreo vertical en la página

            for tabla in tablas_ordenadas:
                x0_t, top_t, x1_t, bottom_t = tabla.bbox

                # --- PASO A: EXTRAER TEXTO PREVIO A LA TABLA ---
                # Validamos con un pequeño margen de tolerancia para evitar recortes inversos
                if top_t > (y_actual + 0.5):
                    region_texto = pagina.crop((0, y_actual, ancho_pag, top_t))
                    texto_extraido = region_texto.extract_text()
                    if texto_extraido:
                        texto_limpio = limpiar_texto_para_filtro(texto_extraido)
                        if texto_limpio:
                            contenido_documento.append(texto_limpio)

                # --- PASO B: EXTRAER TABLA Y TRANSFORMARLA A MARKDOWN REAL ---
                matriz_tabla = tabla.extract()
                if matriz_tabla and len(matriz_tabla) > 0:
                    # Dividir la matriz principal en sub-tablas lógicas usando el estado temporal
                    sub_tablas = []
                    tabla_actual = []
                    ha_leido_datos = False

                    for fila in matriz_tabla:
                        celdas_limpias = [str(c or "").strip().replace("\n", " ") for c in fila]
                        celdas_con_texto = [c for c in celdas_limpias if c]

                        # Determinar si la fila actúa como Título (la primera celda con texto termina en ":")
                        es_titulo = False
                        if celdas_con_texto:
                            # Encontrar la primera celda que no está vacía
                            for c in celdas_limpias:
                                if c:
                                    if c.endswith(":"):
                                        es_titulo = True
                                    break

                        if es_titulo and ha_leido_datos:
                            # Corte: encontramos un título después de haber leído datos
                            if tabla_actual:
                                sub_tablas.append(tabla_actual)
                            tabla_actual = [fila]
                            ha_leido_datos = False
                        else:
                            # Continuar armando la tabla actual
                            tabla_actual.append(fila)
                            if not es_titulo and celdas_con_texto:
                                # Si no es título y tiene contenido, empezamos a ver datos reales o sub-encabezados
                                ha_leido_datos = True

                    if tabla_actual:
                        sub_tablas.append(tabla_actual)

                    # Procesar cada sub-tabla independientemente
                    for sub_matriz in sub_tablas:
                        if not sub_matriz:
                            continue

                        # Calcular dinámicamente cuántas filas conforman el encabezado para esta sub-tabla
                        header_rows = 0
                        for f in sub_matriz:
                            c_limpias = [str(c or "").strip().replace("\n", " ") for c in f]
                            c_texto = [c for c in c_limpias if c]
                            if c_texto:
                                es_tit = False
                                for c in c_limpias:
                                    if c:
                                        if c.endswith(":"):
                                            es_tit = True
                                        break
                                if es_tit:
                                    header_rows += 1
                                else:
                                    break
                            else:
                                break

                        # Si la última fila de título detectada tenía celdas vacías,
                        # es probable que la siguiente fila contenga los sub-encabezados (ej. signo | unidad)
                        if header_rows > 0 and header_rows < len(sub_matriz):
                            ultima_fila_titulo = sub_matriz[header_rows - 1]
                            if any(not str(c).strip() for c in ultima_fila_titulo):
                                header_rows += 1
                        elif header_rows == 0:
                            header_rows = 1
                            if len(sub_matriz) > 2 and any(not str(c).strip() for c in sub_matriz[0]):
                                header_rows = 2

                        # Construir los encabezados combinando las filas detectadas
                        headers = [""] * len(sub_matriz[0])
                        for i in range(header_rows):
                            for j in range(len(headers)):
                                val = str(sub_matriz[i][j] or "").strip().replace("\n", " ")
                                if val:
                                    if headers[j]:
                                        headers[j] += " " + val
                                    else:
                                        headers[j] = val

                        # Si aún hay encabezados vacíos, asignarles un nombre genérico
                        for j in range(len(headers)):
                            if not headers[j]:
                                headers[j] = f"Columna_{j+1}"

                        # Construir el texto en formato estructurado de pares clave-valor
                        lineas_texto = []
                        for fila in sub_matriz[header_rows:]:
                            celdas_fila = [str(celda or "").strip().replace("\n", " ") for celda in fila]
                            if any(celdas_fila):  # Excluir filas que estén completamente vacías
                                pares_fila = []
                                for i, celda in enumerate(celdas_fila):
                                    if celda: # Solo incluir si hay un valor en la celda
                                        header_name = headers[i] if i < len(headers) else f"Columna_{i+1}"
                                        pares_fila.append(f"{header_name}: {celda}")
                                if pares_fila:
                                    lineas_texto.append("- " + ", ".join(pares_fila) + ".")

                        if lineas_texto:
                            tabla_texto = " " + " ".join(lineas_texto) + " "
                            contenido_documento.append(tabla_texto)

                # Desplazar el puntero vertical al final de la tabla actual, asegurando avance positivo
                y_actual = max(y_actual, bottom_t)

            # --- PASO C: EXTRAER TEXTO REMANENTE AL FINAL DE LA PÁGINA ---
            if y_actual < (alto_pag - 0.5):
                region_final = pagina.crop((0, y_actual, ancho_pag, alto_pag))
                texto_final = region_final.extract_text()
                if texto_final:
                    texto_limpio_final = limpiar_texto_para_filtro(texto_final)
                    if texto_limpio_final:
                        contenido_documento.append(texto_limpio_final)

    # Consolidar todos los bloques manteniendo una separación plana y continua para JSONL
    resultado_final = " ".join(contenido_documento).strip()
    # Limpieza final para colapsar múltiples espacios que pudieron generarse
    resultado_final = re.sub(r'[ \t]+', ' ', resultado_final)
    return resultado_final