from time import sleep
import numpy as np
import itertools
from numpy import *
from itertools import combinations
import copy

palabras_vacias = ["a", "acá", "ahí", "ajena", "ajeno", "ajenas", "ajenos", "al", "algo", "algún", "alguna", "alguno", "algunas", "algunos", "allá", "allí", "ambos", "ante", "antes", "aquel", "aquella", "aquello", "aquellas", "aquellos", "aquí", "arriba", "así", "atrás", "aun", "aunque", "bajo", "bastante", "bien", "cabe", "cada", "casi", "cierto", "cierta", "ciertas", "ciertos", "como", "con", "conmigo", "conseguimos", "conseguir", "consigo", "consigue", "consiguen", "consigues", "contigo", "contra", "cual", "cuales", "cualquier", "cualquiera", "cualquieras", "cuan", "cuando", "cuanto", "cuanta", "cuantas", "cuantos", "de", "dejar", "del", "demás", "demasiada", "demasiado", "demasiadas", "demasiados", "dentro", "desde", "donde", "dos", "el", "él", "ella", "ello", "ellas", "ellos", "empleáis", "emplean", "emplear", "empleas", "empleo", "en", "encima", "entonces", "entre", "era", "eras", "eramos", "eran", "eres", "es", "esa", "ese", "eso", "esas", "eses", "esos", "esta", "estas", "estaba", "estado", "estáis", "estamos", "están", "estar", "este", "esto", "estes", "estos", "estoy", "etc", "fin", "fue", "fueron", "fui", "fuimos", "gueno", "ha", "hace", "haces", "hacéis", "hacemos", "hacen", "hacer", "hacia", "hago", "hasta", "incluso", "intenta", "intentas", "intentáis", "intentamos", "intentan", "intentar", "intento", "ir", "jamás", "junto", "juntos", "la", "lo", "las", "los", "largo", "más", "me", "menos", "mi", "mis", "mía", "mías", "mientras", "mío", "míos", "misma", "mismo",
                   "mismas", "mismos", "modo", "mucha", "muchas", "muchísima", "muchísimo", "muchísimas", "muchísimos", "mucho", "muchos", "muy", "nada", "ni", "ningún", "ninguna", "ninguno", "ningunas", "ningunos", "no", "nos", "nosotras" "nosotros", "nuestra", "nuestro", "nuestras", "nuestros", "nunca", "os", "otra", "otro", "otras", "otros", "para", "parecer", "pero", "poca", "poco", "pocas", "pocos", "podéis", "podemos", "poder", "podría", "podrías", "podríais", "podríamos", "podrían", "por", "por qué", "porque", "primero", "puede", "pueden", "puedo", "pues", "que", "qué", "querer", "quién" "quienes", "quienesquiera", "quienquiera", "quizá", "quizas", "sabe", "sabes", "saben", "sabéis", "sabemos", "saber", "se", "según", "ser", "si", "sí", "siempre", "siendo", "sin", "sino", "so", "sobre", "sois", "solamente", "solo", "sólo", "somos", "soy", "sr", "sra", "sres", "sta", "su", "sus", "suya", "suyo", "suyas", "suyos", "tal", "tales", "también", "tampoco", "tan", "tanta" "tanto", "tantas", "tantos", "te", "tenéis", "tenemos", "tener", "tengo", "ti", "tiempo", "tiene", "tienen", "toda", "todo", "todas", "todos", "tomar", "trabaja", "trabajo", "trabajáis", "trabajamos", "trabajan", "trabajar", "trabajas", "tras", "tú", "tu", "tus", "tuya", "tuyo", "tuyas", "tuyos", "último", "ultimo", "un", "una", "uno", "unas", "unos", "usa", "usas", "usáis", "usamos", "usan", "usar", "uso", "usted", "ustedes", "va", "van", "vais", "valor", "vamos", "varias", "varios", "vaya", "verdadera", "voy", "y", "ya", "yo"]


class SistemaRecomendacion():
    
    @staticmethod
    def elimina_signos(opiniones):
        quitar = ",;:.\n!\"'"
        for i in range(len(opiniones)):
            for caracter in quitar:
                opiniones[i] = opiniones[i].replace(caracter, "")
                opiniones[i] = opiniones[i].lower()
        return opiniones

    @staticmethod
    def limpiar(opiniones):
        opiniones_nuevas = []
        for j in opiniones.split():
            if j not in palabras_vacias and j not in opiniones_nuevas:
                opiniones_nuevas.append(j)
        return " ".join(opiniones_nuevas)

    @staticmethod
    def genera_lista(opiniones):
        opiniones_nuevas = []
        for i in range(len(opiniones)):
            opiniones_nuevas += [SistemaRecomendacion.limpiar(opiniones[i])]
        return SistemaRecomendacion.elimina_signos(opiniones_nuevas)

    @staticmethod
    def productos(opiniones_nuevas):
        matriz2 = []
        for z in opiniones_nuevas:
            print(f'z: {z}')
            for z1 in z.split():
                if z1 not in matriz2:
                    matriz2.append(z1)
        return matriz2

    @staticmethod
    def tabla_transacciones(opiniones, opiniones_nuevas, matriz2):
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

        return matriz_grande, contadores


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
    # print(f'nueva_matriz: {nueva_matriz}')
    matriz_ver = np.array(nueva_matriz)
    long = len(matriz_ver)
    w = 0
    matriz_v = []
    for w in range(long):
        if 0 not in nueva_matriz[w]:
            matriz_v.append(nueva_matriz[w])
    for w in range(len(matriz_v)):
        print(matriz_v[w])

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
    print(f'\nSoportes: {contadores}')
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

        for w in range(len(pt)):
            print(pt[w])
        # print(f'\nlen(pt[0]): {pt[0]}')
        fila1 = 1
        (pt, contadores) = filtro_conjuntos(
            min_sup, opiniones_nuevas, pt, combo)

        combo = pt

    return (pt, contadores)
    
        
        
        
    
    
