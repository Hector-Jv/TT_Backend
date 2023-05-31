from time import sleep
import numpy as np
from numpy import *
from itertools import combinations
import copy

palabras_vacias = ["a", "acá", "ahí", "ajena", "ajeno", "ajenas", "ajenos", "al", "algo", "algún", "alguna", "alguno", "algunas", "algunos", "allá", "allí", "ambos", "ante", "antes", "aquel", "aquella", "aquello", "aquellas", "aquellos", "aquí", "arriba", "así", "atrás", "aun", "aunque", "bajo", "bastante", "bien", "cabe", "cada", "casi", "cierto", "cierta", "ciertas", "ciertos", "como", "con", "conmigo", "conseguimos", "conseguir", "consigo", "consigue", "consiguen", "consigues", "contigo", "contra", "cual", "cuales", "cualquier", "cualquiera", "cualquieras", "cuan", "cuando", "cuanto", "cuanta", "cuantas", "cuantos", "de", "dejar", "del", "demás", "demasiada", "demasiado", "demasiadas", "demasiados", "dentro", "desde", "donde", "dos", "el", "él", "ella", "ello", "ellas", "ellos", "empleáis", "emplean", "emplear", "empleas", "empleo", "en", "encima", "entonces", "entre", "era", "eras", "eramos", "eran", "eres", "es", "esa", "ese", "eso", "esas", "eses", "esos", "esta", "estas", "estaba", "estado", "estáis", "estamos", "están", "estar", "este", "esto", "estes", "estos", "estoy", "etc", "fin", "fue", "fueron", "fui", "fuimos", "gueno", "ha", "hace", "haces", "hacéis", "hacemos", "hacen", "hacer", "hacia", "hago", "hasta", "incluso", "intenta", "intentas", "intentáis", "intentamos", "intentan", "intentar", "intento", "ir", "jamás", "junto", "juntos", "la", "lo", "las", "los", "largo", "más", "me", "menos", "mi", "mis", "mía", "mías", "mientras", "mío", "míos", "misma", "mismo",
                   "mismas", "mismos", "modo", "mucha", "muchas", "muchísima", "muchísimo", "muchísimas", "muchísimos", "mucho", "muchos", "muy", "nada", "ni", "ningún", "ninguna", "ninguno", "ningunas", "ningunos", "no", "nos", "nosotras" "nosotros", "nuestra", "nuestro", "nuestras", "nuestros", "nunca", "os", "otra", "otro", "otras", "otros", "para", "parecer", "pero", "poca", "poco", "pocas", "pocos", "podéis", "podemos", "poder", "podría", "podrías", "podríais", "podríamos", "podrían", "por", "por qué", "porque", "primero", "puede", "pueden", "puedo", "pues", "que", "qué", "querer", "quién" "quienes", "quienesquiera", "quienquiera", "quizá", "quizas", "sabe", "sabes", "saben", "sabéis", "sabemos", "saber", "se", "según", "ser", "si", "sí", "siempre", "siendo", "sin", "sino", "so", "sobre", "sois", "solamente", "solo", "sólo", "somos", "soy", "sr", "sra", "sres", "sta", "su", "sus", "suya", "suyo", "suyas", "suyos", "tal", "tales", "también", "tampoco", "tan", "tanta" "tanto", "tantas", "tantos", "te", "tenéis", "tenemos", "tener", "tengo", "ti", "tiempo", "tiene", "tienen", "toda", "todo", "todas", "todos", "tomar", "trabaja", "trabajo", "trabajáis", "trabajamos", "trabajan", "trabajar", "trabajas", "tras", "tú", "tu", "tus", "tuya", "tuyo", "tuyas", "tuyos", "último", "ultimo", "un", "una", "uno", "unas", "unos", "usa", "usas", "usáis", "usamos", "usan", "usar", "uso", "usted", "ustedes", "va", "van", "vais", "valor", "vamos", "varias", "varios", "vaya", "verdadera", "voy", "y", "ya", "yo"]

def sistema_recomendacion(opiniones: list):

    def elimina_signos(opiniones):
        quitar = ",;:.\n!\"'"
        for i in range(len(opiniones)):
            for caracter in quitar:
                opiniones[i] = opiniones[i].replace(caracter, "")
                opiniones[i] = opiniones[i].lower()
        return opiniones

    def limpiar(opiniones):
        opiniones_nuevas = []
        for j in opiniones.split():
            if j not in palabras_vacias and j not in opiniones_nuevas:
                opiniones_nuevas.append(j)
        return " ".join(opiniones_nuevas)

    def genera_lista(opiniones):
        opiniones_nuevas = []
        for i in range(len(opiniones)):
            opiniones_nuevas = opiniones_nuevas + \
                [limpiar(opiniones[i])]
        return elimina_signos(opiniones_nuevas)

    def productos(opiniones_nuevas, matriz2):
        for z in opiniones_nuevas:
            # print(f'z: {z}')
            for z1 in z.split():
                if z1 not in matriz2:
                    matriz2.append(z1)
        return matriz2

    def tabla_transacciones(opiniones_nuevas, matriz2):
        matriz = []
        x1, y1 = len(opiniones), len(matriz2)
        matriz_grande = [[0 for x in range(x1)] for y in range(y1)]
        matriz2.sort()
        for i in range(len(opiniones_nuevas)):
            for j in opiniones_nuevas[i].split():
                if j in matriz:
                    index = matriz2.index(j)
                    contadores[j] += 1
                    matriz_grande[index][i] += 1
                else:
                    matriz.append(j)
                    index = matriz2.index(j)
                    contadores[j] = 1
                    matriz_grande[index][i] = 1

        return (matriz_grande, contadores)

    def matriz(matriz):
        dimension = len(matriz)*len(matriz)
        nueva_matriz = [[0 for x in range(n)] for y in range(dimension)]
        return nueva_matriz

    def ordenados(contadores):
        ordenados = dict(sorted(contadores.items()))
        return ordenados

    def filtro(min_sup, matriz_grande, ordenados):
        matriz_2 = []
        matriz_chica = []
        contador_chico = {}
        s = 0
        for mat in ordenados:
            if ordenados[mat] >= min_sup:
                matriz_2.append(matriz2[s])
                contador_chico[mat] = ordenados[mat]
                matriz_chica.append(matriz_grande[s])
            s += 1
        return matriz_2

    def conjuntos_elementos_dos(nueva_matriz, matriz_2):
        nuevo = 0
        contador = 0
        for k in range(len(matriz_2)):
            for j in range(len(matriz_2)):
                if nueva_matriz[nuevo] and matriz_2[k] != matriz_2[j]:
                    for p in range(nuevo):
                        if matriz_2[k] in nueva_matriz[p] and matriz_2[j] in nueva_matriz[p]:
                            contador += 1
                    if contador == 0:
                        nueva_matriz[nuevo] = [matriz_2[k], matriz_2[j]]
                    nuevo += 1
                contador = 0
        matriz_ver = np.array(nueva_matriz)
        long = len(matriz_ver)
        w = 0
        matriz_v = []
        for w in range(long):
            if 0 not in nueva_matriz[w]:
                matriz_v.append(nueva_matriz[w])
        #for w in range(len(matriz_v)):
        #    print(matriz_v[w])

        return matriz_v

    def filtro_soporte(matriz_v, contadores, opiniones_nuevas):
        pt = []
        contador = 0
        conteo = 0
        for c in range(0, len(matriz_v)):
            for i in range(len(opiniones_nuevas)):
                for s in range(0, len(matriz_v[c])):
                    if matriz_v[c][s] in opiniones_nuevas[i]:
                        contador += 1
                    if contador == len(matriz_v[c]):
                        conteo += 1
                    if conteo >= 2 and matriz_v[c] not in pt:
                        pt.append(matriz_v[c])
                contador = 0
            contadores.append(conteo)
            conteo = 0
        # print(f'\nSoportes: {contadores}')
        return (contadores, pt)

    def genera_conjuntos(min_sup, pt, conjuntos):
        combinaciones_c = []
        combo = []
        fila1 = len(pt[0])-1
        aux = []
        fin = 0
        prueba_logica = 0
        contador_nuevo = 0
        esta = 0
        # Primero, se deben eliminar los conjuntos que tengan menos elementos
        for j in range(conjuntos):
            for i in range(len(pt)):
                for j in range(len(pt)):
                    for prueba in range(fila1):
                        if pt[i][prueba] in pt[j]:
                            fin += 1
                            if fin == fila1:
                                prueba_logica = 1
                    # print(f'(i: {i}, fila1: {fila1} in j: {j})')
                    if (((prueba_logica == 0) or (pt[i][fila1] in pt[j]))) and (pt[j][fila1] not in pt[i]):
                        combinaciones_c.append(i)
                        aux = copy.copy(pt[i])
                        aux.append(pt[j][fila1])
                        if aux not in combo:
                            for i in range(len(combo)):
                                aver = np.in1d(aux, combo[i])
                                for i in range(len(aver)):
                                    if aver[i] == True:
                                        contador_nuevo += 1
                                if contador_nuevo == len(aver):
                                    esta = 1
                                contador_nuevo = 0
                            if esta == 0:
                                combo.append(aux)
                                esta = 0
                            esta = 0
                        aux = []
                    prueba_logica = 0
            pt = []
            pt = combo

            # for w in range(len(pt)):
                # print(pt[w])
            fila1 = 1
            (pt, contadores) = filtro_conjuntos(
                min_sup, opiniones_nuevas, pt, combo)

            combo = pt

        return (pt, contadores)

    def filtro_conjuntos(min_sup, opiniones_nuevas, pt, combo):
        contador = 0
        conteo = 0
        contadores = []

        for c in range(0, len(combo)):  # matriz_v - ahora combo
            for i in range(len(opiniones_nuevas)):
                for s in range(0, len(combo[c])):
                    if combo[c][s] in opiniones_nuevas[i]:
                        contador += 1
                    if contador == len(combo[c]):
                        conteo += 1
                    if conteo >= min_sup and combo[c] not in pt:
                        pt.append(combo[c])
                contador = 0
            contadores.append(conteo)
            conteo = 0
        # print(f'\nSoportes: {contadores}')
        return (pt, contadores)

    def filtro_final(min_sup, combo, contadores):
        contadores_fuertes = []
        regla_fuertes = []
        for c in range(len(combo)):  # matriz_v - ahora combo
            if contadores[c] >= min_sup:
                regla_fuertes.append(combo[c])
                contadores_fuertes.append(contadores[c])

        # print(f'\nSoportes: {contadores}')
        return (regla_fuertes, contadores_fuertes)

    def elemento_mayor(pt, contadores):
        elementos = 0
        minimo = 0
        longest = pt[0] if pt else None
        for x in pt:
            if len(x) > len(longest):
                longest = x
                elementos = pt.index(longest)
                minimo = len(x)

        reglas_bien = []
        contadores_bien = []
        for fin in range(elementos, len(pt)):
            if len(pt[fin]) == minimo:
                reglas_bien.append(pt[fin])
                contadores_bien.append(contadores[fin])
        return (reglas_bien, contadores_bien)

    def reglas_asociacion(min_sup, reglas_bien, contadores_bien, matriz_grande, ordenados, conjuntos):

        # Se calculan los soportes
        elemento = []
        reglas = []
        tem = []
        cuenta = 0
        reglas_evaluar = []
        confianzas = []
        confianza = 0.5
        soporte = 0
        for fin in range(len(reglas_bien)):
            elemento = reglas_bien[fin]
            tem = np.array(list(combinations(elemento, conjuntos+1)))
            reglas = [[0 for x in range(len(elemento))]
                    for y in range(int((len(tem) * 2)))]
            p = len(elemento)
            for i in range(len(tem)):
                for j in range(len(tem[0])):
                    reglas[i][j] = tem[i][j]
                    reglas[p][j+1] = tem[i][j]
                p += 1

            faltantes = []
            for contador in range(len(elemento)):
                for j in range(len(elemento)):
                    if elemento[j] not in reglas[contador]:
                        faltantes.append(elemento[j])
                        reglas[contador][len(elemento)-1] = elemento[j]
                        reglas[contador+len(elemento)][0] = elemento[j]
            longitud = len(reglas)
            longitud_m = longitud/2
            registro = []

            # Aqui se calculan las confianzas
            for i in range(len(reglas)):
                p = reglas[i]
                if i < longitud_m:
                    for j in range(len(p)):
                        if p[j] in matriz2:
                            index = matriz2.index(p[j])
                            registro.append(matriz_grande[index])
                    for c in range(len(registro[0])):
                        registro = np.array(registro)
                        if np.all(registro[:len(registro)-1, c] != 0):
                            cuenta += 1
                    if cuenta == 0:
                        cuenta = 10
                    soporte = contadores_bien[fin]/cuenta
                    if soporte >= confianza:
                        reglas_evaluar.append(['0'] + p)
                        confianzas.append(soporte)
                    cuenta = 0
                else:
                    for mat in ordenados:
                        if mat == p[0]:
                            contador = ordenados[mat]
                    soporte = min_sup/contador
                    if soporte >= confianza:
                        reglas_evaluar.append(['1'] + p)
                        confianzas.append(soporte)
                cuenta = 0
                registro = []
        
        
        
        resultados = []
        indice = 0
        for regla in reglas_evaluar:
            regla = [int(elemento) for elemento in regla]
            
            dict = {}
            if regla[0] == 0:
                regla.pop(0)
                dict["recomendacion"] = regla.pop(-1) 
                dict["regla"] = regla
                dict["tipo"] = "Antecedente"
                dict["confianza"] = confianzas[indice]
            if regla[0] == 1:
                regla.pop(0)
                dict["recomendacion"] = regla.pop(0) 
                dict["regla"] = regla
                dict["tipo"] = "Consecuente"
                dict["confianza"] = confianzas[indice]
            resultados.append(dict)
            indice += 1
        
        return resultados
        
            
        """
        for i in range(len(reglas_evaluar)):
            print(reglas_evaluar[i])
        """

    matriz2 = []
    contadores = {}
    soporte_minimo = 4  # Este es el soporte minimo
    contador = 0
    n = 2
    pt = []
    total_conjuntos = 4

    opiniones_nuevas = genera_lista(opiniones)

    matriz2 = productos(opiniones_nuevas, matriz2)

    (matriz_grande, contadores) = tabla_transacciones(opiniones_nuevas, matriz2)

    nueva_matriz = matriz(matriz2)
    ordenados = ordenados(contadores)

    matriz_2 = filtro(soporte_minimo, matriz_grande, ordenados)

    matriz_v = conjuntos_elementos_dos(nueva_matriz, matriz_2)
    contadores = []
    (contadores, pt) = filtro_soporte(matriz_v, contadores, opiniones_nuevas)

    contadores = []
    (pt, contadores) = genera_conjuntos(soporte_minimo, pt, total_conjuntos)

    (reglas_bien, contadores_bien) = elemento_mayor(pt, contadores)

    pt = []
    (regla_fuertes, contadores_fuertes) = filtro_final(soporte_minimo, reglas_bien, contadores_bien)

    return reglas_asociacion(soporte_minimo, regla_fuertes, contadores_fuertes, matriz_grande, ordenados, total_conjuntos)
