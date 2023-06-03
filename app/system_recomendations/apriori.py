import pandas as pd
from itertools import combinations
import os

class Apriori:
    
    def __init__(self, lista_inicial: list, soporte_minimo: int, confianza: float):
        self.lista_inicial = lista_inicial
        self.soporte_minimo = soporte_minimo
        self.confianza = confianza
        self.tabla_inicial = None # La genera la función representar datos (DataFrame)
        self.nombre_columnas = None # La genera la función representar datos (List)
        self.resultados_iteraciones = None # La genera la función iteraciones (List)
        self.iteraciones_obtenidas = [] # La genera la función iteraciones (Lista de diccionarios)
        
    def iniciar_algoritmo(self):
        self.representar_datos()
        self.iteraciones()
        return self.generar_reglas()
             
    def representar_datos(self):
        
        # Se obtienen los nombres de las columnas #
        nombre_columnas = set()
        for elementos in self.lista_inicial:
            for elemento in elementos:
                nombre_columnas.add(elemento)
        nombre_columnas = sorted(list(nombre_columnas))
        
        # Se genera una matriz que contiene ceros y unos representando si existe o no un elemento en una transacción #
        matriz_elementos = []
        for elementos in self.lista_inicial:
            contabilizacion = []
            for nombre_columna in nombre_columnas:
                if nombre_columna in elementos:
                    contabilizacion.append(1)
                else:
                    contabilizacion.append(0)
            matriz_elementos.append(contabilizacion)
        
        # Se muestra una tabla donde se representa si en una transacción tiene un cierto item #
        print(type(matriz_elementos))
        dataframe_datos = pd.DataFrame(matriz_elementos)
        dataframe_datos.columns = nombre_columnas
        print("#####################################")
        print("##### FORMATO DE DATOS TABULAR #####")
        print("#####################################\n")
        print(dataframe_datos)
        print("\n")
                
        self.tabla_inicial = dataframe_datos
        self.nombre_columnas = nombre_columnas
              
    def iteraciones(self, num_iteracion: int = 1, datos_a_eliminar: list = []):
        
        print("#####################################")
        print(f"#####        ITERACIÓN {num_iteracion}       #####")
        print("#####################################\n")
        
        # Se generan las combinaciones #
        combinaciones = combinations(self.nombre_columnas, num_iteracion)
        combinaciones = list(combinaciones)
        print("## NÚMERO DE COMBINACIONES ##")
        print(len(combinaciones))
        
        # Se realiza la poda #
        combinaciones = self.eliminar_combinaciones(combinaciones, datos_a_eliminar)
        print("## NÚMERO DE COMBINACIONES DESPUÉS DE APLICAR PODA ##")
        print(len(combinaciones))
        
        # Se contabiliza el número de coincidencias que hay de cada combinación #
        resultados = []
        for combinacion in combinaciones:
            
            dataframe_combinacion = self.tabla_inicial[combinacion[0]] # Empieza como Serie
            series_arreglo = []
            for elemento in combinacion[1:]: # Se guardan las columnas del dataframe
                series_arreglo.append(self.tabla_inicial[elemento])
            if series_arreglo: # Si hay datos en el arreglo, se crea un dataframe
                series_arreglo.append(dataframe_combinacion)
                dataframe_combinacion = pd.concat(series_arreglo, axis=1)

            # Se contabiliza el numero de coincidencias #
            coincidencias = 0
            if isinstance(dataframe_combinacion, pd.DataFrame):
                
                for i in range(len(dataframe_combinacion)):
                    valores_fila = dataframe_combinacion.loc[i]
                    if all(valor== 1 for valor in valores_fila):
                        coincidencias += 1

            if isinstance(dataframe_combinacion, pd.Series):
                for elemento in dataframe_combinacion:
                    if elemento == 1:
                        coincidencias += 1
            
            datos_combinacion = (combinacion, coincidencias)
            resultados.append(datos_combinacion)
        
        print("# CONJUNTO DE ELEMENTOS FRECUENTES #\n")
        dict_resultados = {}
        dict_resultados['Items'] = []
        dict_resultados['Cantidad'] = []
        for resultado in resultados:
            combinacion_str = ', '.join(str(elemento) for elemento in resultado[0])
            dict_resultados['Items'].append(combinacion_str)
            dict_resultados['Cantidad'].append(resultado[1])
        
        dataframe_resultados = pd.DataFrame.from_dict(dict_resultados)
        print(dataframe_resultados)
        
        # Se eliminan los elementos que no cumplan con el soporte minimo #
        datos_removidos = []
        datos_resultantes = []
        for resultado in resultados:
            if resultado[-1] < self.soporte_minimo: # Ultima posicion
                datos_removidos.append(resultado)
            else:
                datos_resultantes.append(resultado)
                
        self.iteraciones_obtenidas.append({num_iteracion: datos_resultantes})
        
        print(f"\n# CONJUNTO DE ELEMENTOS ELIMINADOS ITERACIÓN {num_iteracion} #\n")
        dict_eliminados = {}
        dict_eliminados['Items'] = []
        dict_eliminados['Cantidad'] = []
        for resultado in datos_removidos:
            combinacion_str = ', '.join(str(elemento) for elemento in resultado[0])
            dict_eliminados['Items'].append(combinacion_str)
            dict_eliminados['Cantidad'].append(resultado[1])
        
        dataframe_eliminados = pd.DataFrame.from_dict(dict_eliminados)
        print(dataframe_eliminados)
        print("\n")
        
        print(f"\n# CONJUNTO DE ELEMENTOS CORRECTOS ITERACIÓN {num_iteracion} #\n")
        dict_resultantes = {}
        dict_resultantes['Items'] = []
        dict_resultantes['Cantidad'] = []
        for resultado in datos_resultantes:
            combinacion_str = ', '.join(str(elemento) for elemento in resultado[0])
            dict_resultantes['Items'].append(combinacion_str)
            dict_resultantes['Cantidad'].append(resultado[1])
        
        dataframe_resultante = pd.DataFrame.from_dict(dict_resultantes)
        print(dataframe_resultante)
        print("\n")
        
        """
        print(f"DATOS RESULTANTES DE ITERACIÓN {num_iteracion}: ")
        print(datos_resultantes)
        print("")
        """
        # Se verifica que ya no se pueda hacer otra iteración #
        hay_valores_diferentes = False 
        for resultado in datos_resultantes:
            if resultado[1] != self.soporte_minimo:
                hay_valores_diferentes = True
                break
        
        if hay_valores_diferentes:
            num_iteracion += 1
            elementos_eliminados = [combinacion[0] for combinacion in datos_removidos]
            self.iteraciones(num_iteracion, elementos_eliminados)
        else:
            self.resultados_iteraciones = datos_resultantes
    
    def eliminar_combinaciones(self, combinaciones, a_eliminar):
        resultado = []
        for combinacion in combinaciones:
            mantener = True
            for eliminar in a_eliminar:
                # Verificar que todos los elementos a eliminar están en la combinación
                if all(elem in combinacion for elem in eliminar):
                    mantener = False
                    break
            if mantener:
                resultado.append(combinacion)
        return resultado
    
    def generar_reglas(self):
        print("##########################################")
        print(f"### GENERACIÓN DE REGLAS DE ASOCIACIÓN ##")
        print("##########################################\n")
        """
        print("CONJUNTO DE ELEMENTOS FRECUENTES FINALES")
        # print(self.iteraciones_obtenidas)
        """
        reglas = []
        conjunto_elementos_frecuentes = [elementos[0] for elementos in self.resultados_iteraciones]
        numero_transacciones = len(self.lista_inicial)
        
        for conjunto_elementos in conjunto_elementos_frecuentes:
            
            dataframe_conjunto = self.tabla_inicial[list(conjunto_elementos)]
            lista_combinaciones = self.generar_combinaciones(list(conjunto_elementos))
            for iteracion in self.resultados_iteraciones:
                for conjunto in lista_combinaciones:
                    datos_conjunto = {}
                    datos_conjunto["antecedente"] = conjunto[0]
                    datos_conjunto["consecuente"] = conjunto[1]
                    datos_conjunto["soporte"] = round(iteracion[1] / numero_transacciones, 2)
                    
                    support_countA = 0
                    support_count_inter = 0
                    for i in range(len(dataframe_conjunto)):
                        valores_fila = dataframe_conjunto.loc[i]
                        if all(valor== 1 for valor in valores_fila):
                            support_countA += 1
                            
                        if all(dataframe_conjunto[col][i] == 1 for col in conjunto[0]):
                            support_count_inter += 1
                    if round(support_countA / support_count_inter, 2) < self.confianza:
                        continue
                    datos_conjunto["confianza"] = round(support_countA / support_count_inter, 2)
                    reglas.append(datos_conjunto)
        
        reglas_sin_repeticiones = [dict(t) for t in set(tuple(d.items()) for d in reglas)]
        print(reglas_sin_repeticiones)
        return reglas_sin_repeticiones
            
    def generar_combinaciones(self, lista):
        resultados = []
        n = len(lista)

        for i in range(1, n):
            comb = list(combinations(lista, i))
            for c in comb:
                temp = lista.copy()
                for elemento in c:
                    temp.remove(elemento)
                resultados.append([c, tuple(temp)])

        return resultados
