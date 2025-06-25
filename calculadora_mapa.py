import random
import time
import os
from collections import deque

#Pregunta cuanto quiero en mi fila y columna, o sea, para elejir el tamaño
filas = int(input('Ingresa el tamaño de la fila: '))
columnas = int(input('Ingresa el tamaño de la columna: '))

# Funcion que crea un mapa aleatorio con los tamaños
def generar_mapa(filas, columnas):
    valores = [0]*60 + [1]*20 + [2]*15 + [3]*5  # 60% camino libre, 20% edificio, 15% agua, 5% bloqueado
    mapa = []
    for _ in range(filas):
        fila = [random.choice(valores) for _ in range(columnas)]
        mapa.append(fila)
    return mapa

mapa_numerico = generar_mapa(filas, columnas) #genera y guarda ese mapa que acabo de crear

#convierte los numeros del mapa en simbolos que pueda ver en pantalla
def convertir_a_tablero(mapa_numerico): 
    tablero = []
    for fila in mapa_numerico:
        nueva_fila = []
        for celda in fila:
            if celda == 0:
                nueva_fila.append(' ')   # libre
            elif celda == 1:
                nueva_fila.append('#')   # edificio
            elif celda == 2:
                nueva_fila.append('~')   # agua
            elif celda == 3:
                nueva_fila.append('X')   # zona bloqueada temporal
        tablero.append(nueva_fila)
    return tablero

#funcion que pregunta si quiero agregar obstaculo a mano, y dónde
def agregar_obstaculo_personalizado():
    while True:
        opcion = input("¿Quieres agregar un obstáculo personalizado? (s/n): ").lower()
        if opcion == 's':
            try: 
                x = int(input("Fila del obstáculo: "))
                y = int(input("Columna del obstáculo: "))
                tipo = int(input("Tipo (1: edificio, 2: agua, 3: zona bloqueada): "))
                if 0 <= x < filas and 0 <= y < columnas and tipo in [1,2,3]:
                    mapa_numerico[x][y] = tipo
                    print("🧱 obstáculo añadido.")
                else:
                    print("❌ Coordenadas o tipo invalido.")
            except:
                print("⚠ Entrada inválida.")
        else:
            break

#Pedir coordenadas de inicio y fin
def pedir_coordenadas(nombre):
    while True:
        try:
            x = int(input(f"Ingrese la fila de {nombre}: "))
            y = int(input(f"Ingrese la columna de {nombre}: "))
            if 0 <= x < filas and 0 <= y < columnas and tablero[x][y] == ' ':
                return x,y
            else:
                print("❌ Coordenadas inválidas o sobre obstáculo.")
        except:
            print("⚠ Entrada no válida.")



# Visualizacion del Mapa, limpia la pantalla y dibuja el mapa con emojis bonitos para que sea mas divertido
def imprimir_tablero(tablero, visitado=None):
    os.system('cls' if os.name == 'nt' else 'clear')
    for i, fila in enumerate(tablero):
        for j, celda in enumerate(fila):
            if visitado and visitado[i][j] and tablero[i][j] not in ('S', 'E'):
                print("⭐", end=' ')
            elif celda == '⭐' or celda == '*':
                print("⭐", end=' ')    # el que visita
            elif celda == ' ':
                print("🟫", end=' ')    #camino libre
            elif celda == '#':
                print("🏢", end=' ')    #edificios
            elif celda == '~':
                print("💧", end=' ')    #agua
            elif celda == 'X':
                print("⛔", end=' ')    #bloqueo
            elif celda == 'S':
                print("🚩", end=' ')    #inicio
            elif celda == 'E':
                print("🎯", end=' ')    #fin
        print()
    time.sleep(0.2)

#busca paso a paso (explorando caminos) el camino desde inicio y fin usando BFS
def bfs(tablero, inicio, fin):
    filas, columnas = len(tablero), len(tablero[0])
    visitado = [[False]*columnas for _ in range(filas)]
    padre = [[None]*columnas for _ in range(filas)]
    cola = deque()

    x0, y0 = inicio
    cola.append((x0, y0))   # Agrega el inicio para eplorar
    visitado[x0][y0] = True #marca que ya esta visitado

    while cola:
        x, y = cola.popleft()
        imprimir_tablero(tablero, visitado)

        if (x, y) == fin:
            print("¡Ruta encontrada! 🎉")
            return reconstruir_rutas(padre, fin), visitado #si llego al destino, devuelve el camino

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < filas and 0 <= ny < columnas:
                if not visitado[nx][ny] and tablero[nx][ny] in (' ', 'E'):
                    visitado[nx][ny] = True
                    padre[nx][ny] = (x, y)
                    cola.append((nx, ny))

    print("No se encontró un camino 😓")
    return None

#recontruir y mostrar ruta 
#sigue las pistas hacia atrás para armar el camino desde inicio hasta fin
def reconstruir_rutas(padre, fin):  
    camino = []
    x, y = fin
    while padre[x][y]:
        camino.append((x, y))
        x, y = padre[x][y]
    camino.reverse()
    return camino

# ---- EJECUCION PRINCIPAL ------

# Primero agregamos los obstáculos personalizados antes de crear el tablero visual
agregar_obstaculo_personalizado()

#Convertimos el mapa numerico actualizado a tablero visual
tablero = convertir_a_tablero(mapa_numerico)

# Marcar inicio y fin
sx, sy = pedir_coordenadas("INICIO")
ex, ey = pedir_coordenadas("FIN")
tablero[sx][sy] = 'S'
tablero[ex][ey] = 'E'

inicio = (sx, sy)
fin = (ex, ey)
ruta = bfs(tablero, inicio, fin)

if ruta:
    for x, y in ruta:
        if tablero[x][y] == ' ':
            tablero[x][y] = '*'
        imprimir_tablero(tablero, ruta)
        print("✨ Ruta final marcada con ⭐")
    else:
        imprimir_tablero(tablero)