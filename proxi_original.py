import sys
import csv
import random
from time import time
import pandas as pd
import numpy as np
import itertools
import bisect
import operator
import os
import matplotlib.pyplot as plt
import statistics as stats


# Indica si está en el lado de tierra o no
def esLadoTierra(posicion, bloque):
    if salientesTipos[bloque][2] < posicion:
        listaBloques[bloque][1] = listaBloques[bloque][1] - 1
        return True
    else: return False

# Indica si esta en el lado de mar o no
def esLadoMar (posicion, bloque):
    if salientesTipos[bloque][2] >= posicion:
        listaBloques[bloque][0] = listaBloques[bloque][0] - 1
        return True
    else: return False

# Saca un contenedor del bloque en un instante
def salida(tAnt , tAct, listaSalientes1D, listaSalientes2D, nB, lB, sTipos):
    cont = 0
    sacar = []
    # Metemos en array sacar aquellos tiempos que hay que sacar del bloque
    for listaSalientes1DIndex in range(len(listaSalientes1D)):
        if(listaSalientes1D[listaSalientes1DIndex] <= tAct) and (listaSalientes1D[listaSalientes1DIndex] >= tAnt):
            sacar.append(listaSalientes1D[listaSalientes1DIndex])
        #Para cada tiempo de sacar, hay que buscar a que bloque corresponde
        #y si es a lado de mar o a lado de tierra.
        for s in range(len(sacar)):
        #sacar[s] es el valor que queremos sacar
        #hay que buscarlo en tiempos Salientes, para encontrar el bloque .
            indiceSacar = 0
            for nbl in range(numBloques):
                # Si este es el bloque
                if ((sacar[s] in tiemposSalientes[nbl]) and
                esLadoTierra(tiemposSalientes[nbl].index(int(sacar[s])), nbl)):
                    if((sacar[s] not in listaSacados)):
                        for contar in range(contar_veces(sacar[s], tiemposSalientes1)):
                            listaSacados.append(sacar[s])

                elif ((sacar[s] in tiemposSalientes[nbl]) and
                esLadoMar(tiemposSalientes[nbl].index(int(sacar[s])), nbl)):
                    if ((sacar[s] not in listaSacados)):
                        for contar in range(contar_veces(sacar[s], tiemposSalientes1)):
                            listaSacados.append(sacar[s])

# Saca un contenedor de los que ha entrado nuevos en el bloque en un instante
def salidaNuevo(tAntN , tActN, listaSalientes1DN, nBN, lBN, sNuevo, sNTierra, sNMar):
    contN = 0
    sacarN = [ ]
    # Metemos en array sacar aquel los tiempos que hay que sacar del bloque
    for listaSalientes1DIndexN in range(len(listaSalientes1DN)):
        if ((listaSalientes1DN[listaSalientes1DIndexN][0] <= tActN) and
        (listaSalientes1DN[listaSalientes1DIndexN][0] >= tAntN)):
            sacarN.append(listaSalientes1DN[listaSalientes1DIndexN])
    # Para cada tiempo de sacar hay que buscar a que bloque corresponde y
    # si es al lado de mar o de tierra .
    # Para cada elemento de sacarN
    for sN in range(len(sacarN)):
        bloqueN = 0
        tipo = 0
        for lN in sacarN:
            # Sacamos su bloque y el tipo de contenedor que es
            bloqueN = sacarN[sacarN.index(lN)][2]
            tipo = sacarN[sacarN.index(lN)][1]
            if sacarN[sacarN.index(lN)] not in sNuevo:
                if sacarN[sacarN.index(lN)][1] == 1: #Si es 1 hay que sacarlo del lado de mar
                    # El espacio disponible aumenta
                    lBN[2][0] = lBN[2][0] + 1
                    # Quitamos el contenedor de proximas Salidas
                    listaSalientes1DN = listaSalientes1DN[1:]
                    sNuevo.append(sacarN[sacarN.index(lN)])
                    sNMar.append(sacarN[sacarN.index(lN)])
                elif sacarN[sacarN.index(lN)][1] == 2: #Si es 2 hay que sacarlo del lado de tierra
                    # El espacio disponible aumenta
                    lBN[2][1] = lBN[2][1] + 1
                    # Quitamos el contenedor de proximas Salidas
                    listaSalientes1DN = listaSalientes1DN[1:]
                    sNuevo.append(sacarN[sacarN.index(lN)])
                    sNTierra.append(sacarN[sacarN.index(lN)])

# Devuelve una lista con los repetidos
def encontrarTiemposRep(lista):
    repetido = []
    unico = []
    for x in lista:
        if x not in unico: unico.append(x)
        else: repetido.append(x)
    return repetido

# Devuelve el numero de veces que se repite un tiempo de salida
def contar_veces(elemento, lista):
    veces = 0
    for i in lista:
        if elemento == i:
            veces += 1
    return veces

def noHaySitiosTierra():
    hay = True
    for bloq in range(numBloques):
        if(listaBloques[bloq][1] > 0): hay = False

def noHaySitiosMar():
    hay = True
    for bloq in range(numBloques):
        if (listaBloques[bloq][0] > 0): hay = False

def buscarAleatorioMar():
    bl = random.randint(0, numBloques - 1)
    while listaBloques[bl][0] == 0: bl = random.randint(0, numBloques - 1)
    listaBloques[bl][0] = listaBloques[bl][0] - 1
    return bl

def buscarAleatorioTierra():
    bl = random.randint(0, numBloques - 1)
    while listaBloques[bl][1] == 0: bl = random.randint(0, numBloques - 1)
    listaBloques[bl][1] = listaBloques[bl][1] - 1
    return bl

def read_text_file(file_path):
    with open(file_path, "r") as f:
        f.read()

for i in range(1):
    tInicialProceso = time()
    path = r"C:\Users\Hoyos O\Desktop\Universidad\Tesis\instancias_prueba"
    os.chdir(path)
    tiemposInstancias  = []
    t_graf = []
    t_grafms = []
    for file in os.listdir():
        if file.endswith(".txt"):
            file_path = f"{path}\{file}"
            read_text_file(file_path)
    #read text files
    # abro archivo con nombre de listas
        tiempoInicialInstancia = time()
        #abro archivo
        with open(file) as tabla:
            #inicializacion de variables necesarias:
            numBloques = 0
            numCont = 0
            numRows = 0
            numCol = 0
            bloquesMar = []
            bloquesTierra = []
            saleSea = 0
            saleLand = 0
            saleMarPrimeros = 0
            salientesTipos = []
            tiemposSalientes = []
            tSalientesRes = []
            TsalenSea = []
            TsalenLand = []
            listaContenedores = []
            listaBloques = []
            listaSacados = []
            listaSacadosLand = []
            listaSacadosSea = []
            contenedoresAsignados = []
            solucion = []
            tiemposRepetidos = []
            proximasSalidas = []
            proximasSalidasDatos = [[]]
            listaSacadosNuevos = []
            listaSacadosNMar = []
            listaSacadosNTierra = []
            tiemposAsignados = []
            bloquesAsignados = []
            res = []
            #print(datos.readlines())

            datos = tabla.readlines()
            datos = [x.strip() for x in datos]
            datos = iter(datos)

            # para cada linea del archivo
            for linea in datos:

                # Numero de bloques
                if linea.startswith("number of blocks"):
                    instanciaNumBloques = next(datos).strip()
                    instanciaNumBloques = instanciaNumBloques.replace("\t", ",")
                    numBloques = int(instanciaNumBloques)


                #Numero de contenedores
                if linea.startswith("number of containers"):
                    instanciaNumCont = next(datos).strip()
                    instanciaNumCont = instanciaNumCont.replace("\t", ",")
                    numCont = instanciaNumCont


                #Numero de  filas
                if linea.startswith("number of rows"):
                    instanciaNumRows = next(datos).strip()
                    instanciaNumRows = instanciaNumRows.replace("\t", ",")
                    numRows = instanciaNumRows


                #Numero de columnas
                if linea.startswith("number of columns"):
                    instanciaNumCol = next(datos).strip()
                    instanciaNumCol = instanciaNumCol.replace("\t", ",")
                    numCol = instanciaNumCol


                #TODO EL PROBLEMA ESTÁ AQUÍ

                #Datos sobre los bloques
                for b in range (int(numBloques + 1)):
                    if linea.startswith("#Block\t" + str(b)):
                        instanciaFreeSea = next(datos).strip()
                        instanciaFreeSea = instanciaFreeSea.replace("\t", ",")


                        instanciaFreeLand = next(datos).strip()
                        instanciaFreeLand = instanciaFreeLand.replace("\t", ",")


                        instanciasSaleMar = next(datos).strip()
                        instanciasSaleMar = instanciasSaleMar.replace("\t", ",")


                        instanciasSaleLand = next(datos).strip()
                        instanciasSaleLand = instanciasSaleLand.replace("\t", ",")


                        instanciasSaleMarPrimeros = next(datos).strip()
                        instanciasSaleMarPrimeros = instanciasSaleMarPrimeros.replace("\t", ",")


                        instanciaFreeSea = list(map(str, instanciaFreeSea.split(",")))
                        instanciaFreeLand = list(map(str, instanciaFreeLand.split(",")))
                        instanciasSaleMar = list(map(str, instanciasSaleMar.split(",")))
                        instanciasSaleLand = list(map(str, instanciasSaleLand.split(",")))
                        instanciasSaleMarPrimeros = list(map(str, instanciasSaleMarPrimeros.split(",")))

                        instanciaBloque = [instanciaFreeSea[1], instanciaFreeLand[1]]

                        instanciaBloquesMar = instanciaFreeSea
                        instanciaBloquesTierra = instanciaFreeLand
                        instanciaBloque = [int(x) for x in instanciaBloque]
                        bloquesMar.append(instanciaBloquesMar[1])
                        bloquesTierra.append(instanciaBloquesTierra[1])
                        listaBloques.append(instanciaBloque)
                        bloquesMar = [int(x) for x in bloquesMar]
                        bloquesTierra = [int(x) for x in bloquesTierra]
                        saleSea = int(instanciasSaleMar[1])
                        saleLand = int(instanciasSaleLand[1])
                        saleMarPrimeros = int(instanciasSaleMarPrimeros[2])
                        salientesTipos.append([int(saleSea), int(saleLand), int(saleMarPrimeros)])
                        instanciatiempos = []
                        instanciaTSaliente = next(datos).strip()

                        for j in range((int(saleSea) + int(saleLand))):
                            instanciaTSaliente = next(datos).strip()
                            instanciaTSaliente = instanciaTSaliente.replace("\t", ",")
                            instanciatiempos.append(instanciaTSaliente)
                            tSalientesRes.append(instanciaTSaliente)
                        instanciatiempos = [int(x) for x in instanciatiempos]
                        TsalenSea.append(instanciatiempos[:int(saleMarPrimeros)])
                        TsalenLand.append(instanciatiempos[int(saleMarPrimeros):])
                        tiemposSalientes.append(instanciatiempos)


                #Datos sobre los contenedores
                if linea.startswith("#Type"):
                    for n in range(int(numCont)):
                        instanciaCont = next(datos).strip()
                        instanciaCont = instanciaCont.replace("\t", ",")
                        instanciaCont = list(map(int, instanciaCont.split(",")))
                        listaContenedores.append(instanciaCont)
                    pass
                pass

            listaCDesordenada = listaContenedores
            listaContenedores.sort(key = operator.itemgetter(1, 2))
            tiemposSalientes1 = sorted(list(itertools.chain.from_iterable(tiemposSalientes)))
            tiemposRepetidos = encontrarTiemposRep(tiemposSalientes1)
            tActual = 0
            tAnterior = 0
            tProximo = 0
            contenedoresAs = 0
            noAs = 0


            for c in listaContenedores:
                #Definimos bloque Asignado para indicar si el bloque ya ha sido asignado.
                #Estara a 0 cuando aun no haya sido asignado.
                bloqueAsignado = 0
                bloque = 0

                #Esperamos hasta que haya contenedor disponible
                while (tActual < c[1]):
                    salida(tAnterior, tActual, tiemposSalientes1, tiemposSalientes, numBloques,
                        listaBloques,salientesTipos)
                    tAnterior = tActual
                    tActual = tActual + 1

                #A partir de la 4 posicion tenemos las  distancias
                time1 = time()
                dist = c[4:]
                dist = [int(x) for x in dist]
                #Las ordenamos de menor a mayor instantedetiempo
                dist.sort()
                #dist_menores = dist[:3]
                #bloque = random.choice(dist_menores)
                #lista_menores = dist[:3]
                #print(lista_menores)


                #Mientras que no este asignado seguiremos iterando
                while (bloqueAsignado == 0) and (bloque < numBloques):

                    #Sacamos el bloque que mas cerca esta
                    bloqueMasCerca = c[4:].index(dist[bloque])

                    if c[0] == 1: #Si viene por mar va a lado de mar
                        if listaBloques[bloqueMasCerca][0] > 0:
                            # Asignamos
                            listaBloques[bloqueMasCerca][0] = listaBloques[bloqueMasCerca][0] - 1
                            bloqueAsignado = 1
                            contenedoresAs = contenedoresAs + 1
                            # Tiempos que han sido asignados
                            tiemposAsignados.append(c[1])
                            #Meto el contenedor en la lista de proximas salidas(Lo ultimo dice que bloque es)
                            bisect.insort(proximasSalidas, ([c[2], c[0], str(c[4:].index(int(dist[bloque])) + 1)]))
                            #Sabre por donde llega, tiempo de salida y bloque en el que esta asigando x
                            tProximo = tActual + c[4+ int(bloqueMasCerca)]

                        else:
                            # Busco un bloque aleatorio en el lado de mar
                            blq = buscarAleatorioMar()
                            bloqueAsignado = 1
                            bloqueMasCerca = blq
                            contenedoresAs = contenedoresAs + 1
                            tiemposAsignados.append(c[1])
                            bisect.insort(proximasSalidas, ([tActual + c[2], c[0], str(c[4:].index(int(dist[blq])) + 1)]))
                            tProximo = tActual + c[4+ int(blq)]


                    elif c[0] == 2: #Si viene por tierra va a lado de tierra
                        if listaBloques[bloqueMasCerca][1] > 0:
                            # Asignamos
                            listaBloques[bloqueMasCerca][1] = listaBloques[bloqueMasCerca][1]-1
                            bloqueAsignado = 1
                            contenedoresAs = contenedoresAs + 1
                            #Tiempos que han sido asignados
                            tiemposAsignados.append(c[1])
                            #Meto el contenedor en la lista de proximas salidas (Lo ultimo dice que bloque es)
                            ######################################################
                            bisect.insort(proximasSalidas, ([tActual + c[2], c[0], str(c[4:].index(int(dist[bloque])) + 1)]))
                            ######################################################
                            #Sabre por donde llega, tiempo de salida y bloque en el que esta asigando x
                            tProximo = tActual + c[4+ int(bloqueMasCerca)]

                        else:
                            #Busco un bloque aleatorio en el lado de tierra
                            blq = buscarAleatorioTierra()
                            bloqueAsignado = 1
                            bloqueMasCerca = blq
                            contenedoresAs = contenedoresAs + 1
                            tiemposAsignados.append(c[1])
                            bisect.insort(proximasSalidas, ([c[2], c[0], str(c[4:].index(int(dist[blq])) + 1 )]))
                            tProximo = tActual + c[4+ int(blq)]

                salida(tActual, tProximo, tiemposSalientes1, tiemposSalientes, numBloques, listaBloques, salientesTipos)
                salidaNuevo(tActual, tProximo, proximasSalidas, numBloques, listaBloques, listaSacadosNuevos, listaSacadosNTierra, listaSacadosNMar)

                #Añadimos el componente a la solucion
                solucion.append([c, c[0], c[4:], bloqueMasCerca+1, c[4], c[5], c[6], c[7], c[8], tActual, tProximo])
                res.append([c, bloqueMasCerca, tActual])
                #Actualizamos los tiempos
                tAnterior = tActual
                tActual = tProximo

                if(bloque < numBloques):
                    bloquesAsignados.append(c[4:].index(int(dist[bloque])) + 1)
                else:
                    noAs = contenedoresAs

            tiempoFinalInstancia = time()
            tiempoTotalInstancia = tiempoFinalInstancia - tiempoInicialInstancia
            tiemposInstancias.append([str(file), solucion[-1][-1], tiempoTotalInstancia])

            print("\nTiempo solucion para la instancia " + str(file) + ": " + str(solucion[-1][-1]))
            print("El tiempo total del proceso de asignacion: " + str(tiempoTotalInstancia) + "ms.")
            #print(solucion)
            #print(listaContenedores)
            #print(res)


            t_graf.append(int(str(solucion[-1][-1])))
            t_grafms.append(float(str(tiempoTotalInstancia)))
