import csv
import os

NOMBRE_ARCHIVO_CSV = "datos_de_paises.csv"

#Si el archivo no existe lo crea y si existe no hace nada.
if not os.path.exists(NOMBRE_ARCHIVO_CSV):
        with open (NOMBRE_ARCHIVO_CSV, "w", newline="", encoding="utf-8") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=["nombre","poblacion","superficie","continente"])
            escritor.writeheader()

print("\n" + "="*50)
print("========= GESTIONADOR DE DATOS DE PAÍSES =========")


def validacion_solo_letras_input(mensaje_input, mensaje_error):
    while True:
        texto = input(mensaje_input).strip().lower()

        #Elimina espacios duplicados entre palabras.
        texto = " ".join(texto.split())

        if not texto:
            print("\n** No ingresaste nada, volvé a intentarlo **")
            continue

        if not texto.replace(" ", "").isalpha():
            print(mensaje_error)
            continue

        return texto
    
def validacion_solo_numeros_enteros_positivos(mensaje_input, mensaje_error):
    while True:
        numeros = input(mensaje_input).strip()

        if not numeros:
            print("\n** No ingresaste nada, volve a intentarlo **")
            continue

        if not numeros.isdigit():
            print(mensaje_error)
            continue

        return numeros
    
#Abre el CSV lo lee, lo convierte en una lista de diccionarios y devuelve esa lista.
def lista_completa_de_paises():
    lista_datos_paises = []

    with open(NOMBRE_ARCHIVO_CSV, newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            lista_datos_paises.append({"nombre": fila["nombre"], "poblacion": int(fila["poblacion"]),
                                    "superficie": int(fila["superficie"]), "continente": fila["continente"]})
            
    return lista_datos_paises
    
#Sirve para comprobar si existe un país.
def existe_pais(nombre):
    lista_datos_paises = lista_completa_de_paises()

    for pais in lista_datos_paises:
        if pais["nombre"] == nombre:
            return True  #Ya existe ese país.
    return False  #Aún no existe.


def agregar_pais():
    
    nombre_pais = validacion_solo_letras_input("\nIngrese el nombre del país: ",
                "\n** Error: solo letras y espacios permitidos, vuelva a intentarlo **\n")
    if existe_pais(nombre_pais):
        print("\n** El país ya existe, utiliza opción (2) para actualizar sus datos **\n")
        return  #Vuelve al menú.
    
    poblacion = validacion_solo_numeros_enteros_positivos("\nIngrese su población: ",
                "\n** Error: solo números enteros positivos, vuelva a intentarlo **\n")
    superficie = validacion_solo_numeros_enteros_positivos("\nAhora la superficie: ",
                "\n** Error: solo números enteros positivos, vuelva a intentarlo **\n")
    continente = validacion_solo_letras_input("\nPor último su continente: ",
                "\n** Error: solo letras y espacios permitidos, vuelva a intentarlo **\n")
    
    #Si el pais no existe lo agregamos debajo sin reescribir lo anterior.
    with open (NOMBRE_ARCHIVO_CSV, "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=["nombre", "poblacion", "superficie", "continente"])
        escritor.writerow({"nombre": nombre_pais, "poblacion": poblacion, "superficie": superficie, "continente": continente})
    
    print("\n<<<< Agregado con éxito! >>>>\n")
    print(f"País: {nombre_pais.title()} \nPoblación: {poblacion} \nSuperficie: {superficie} Km2 \nContinente: {continente.title()}")
    
#Actualiza población y superficie y luego sobreescribe todo con los datos actualizados.
def actualizar_datos():

    if lista_vacia():
        return  #Si la lista está vacía vuelve al menú.

    nombre = validacion_solo_letras_input("\nIngrese el nombre del país (exacto) a actualizar: ",
                "\n** Error: solo letras y espacios permitidos, vuelva a intentarlo **\n")
    
    paises = lista_completa_de_paises()
    
    for pais in paises:
        if pais["nombre"] == nombre:

            poblacion = validacion_solo_numeros_enteros_positivos("\nIngrese población actualizada: ",
                        "\n** Error: solo números enteros positivos, vuelva a intentarlo **\n")
            superficie = validacion_solo_numeros_enteros_positivos("\nAhora superficie actualizada: ",
                        "\n** Error: solo números enteros positivos, vuelva a intentarlo **\n")
            
            #Actualizamos población y superficie del país indicado.
            pais["poblacion"] = int(poblacion)
            pais["superficie"] = int(superficie)
            break

    else:
        print("\n** El país no se encuentra en la lista, utilice opción (1) para agregarlo **\n")
        return

    #Sobreescribe todo con la población y superficie actualizada.
    with open(NOMBRE_ARCHIVO_CSV, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=["nombre", "poblacion", "superficie", "continente"])
        escritor.writeheader()
        escritor.writerows(paises)

        print("\n<<<< Actualizado con éxito! >>>>\n")
        print(f"País: {nombre.title()} \nPoblación: {poblacion} \nSuperficie: {superficie} Km2")
        return

#Busca el país indicado.
def buscar_pais():

    if lista_vacia():
        return
    
    nombre_pais = validacion_solo_letras_input("\nIngrese el nombre del país (exacto): ",
                    "\n** Error: solo letras y espacios permitidos, vuelva a intentarlo **\n")
    
    if not existe_pais(nombre_pais):
        print(f"\n** El país {nombre_pais.title()} no existe en la lista, utiliza opción (1) para ingresarlo **\n")
        return
    
    lista_paises = lista_completa_de_paises()
    
    for pais in lista_paises:
        if pais["nombre"] == nombre_pais:
            print("\n<<<< País encontrado >>>>\n")
            print(f"País: {pais["nombre"].title()} \nPoblación: {pais["poblacion"]} \nSuperficie: {pais["superficie"]} Km2 \nContinente: {pais["continente"].title()}")
            return

#Para utilizar en otras funciones basta con poner if lista_vacia(): return para que vuelva al menú.
def lista_vacia():
    lista_paises = lista_completa_de_paises()

    if not lista_paises:
        print("\n** Lista vacía, para realizar esta acción primero ingrese países con opción (1) **\n")
        return True
    return False

##Submenu de la opcion 4
def menu_filtrar():
    if lista_vacia():
        return

    print("\n--- FILTRAR POR ---")
    print("a)Continente")
    print("b)Rango de población")
    print("c)Rango de superficie\n")

    while True:
        opcion_filtro = input("Elija una opción: ").strip().lower()
        match opcion_filtro:
            case "a":
                lista = lista_completa_de_paises()
                filtro_por_continente(lista)
                break
            case "b":
                lista = lista_completa_de_paises()
                filtro_por_poblacion(lista)
                break
            case "c":
                lista = lista_completa_de_paises()
                filtro_por_superficie(lista)
                break
            case _:
                print("\n** Opción incorrecta, vuelva a intentarlo (a, b, c) **\n")

#Filtro por continenetes
def filtro_por_continente(paises):
    cont = validacion_solo_letras_input("\nIngrese el continente (exacto) a filtrar: ",
            "\n** Error: solo letras y espacios permitidos, vuelva a intentarlo **\n")
    
    resultado = [pais for pais in paises if pais["continente"].strip().lower() == cont]

    if len(resultado) == 0:
        print("\n** Error: No se encontraron países en ese continente **\n")
        return

    print("\n<<<< Países encontrados >>>>\n")
    for pais in resultado:
        print(f"{pais['nombre'].title()} ({pais['continente'].title()})\n")

#Filtro por poblacion
def filtro_por_poblacion(paises):
    minimo = validacion_solo_numeros_enteros_positivos("\nColoque un mínimo de poblacion: ",
                "\n** Error: solo números enteros positivos, vuelva a intentarlo **\n")
    maximo = validacion_solo_numeros_enteros_positivos("Coloque un máximo de poblacion: ",
            "\n** Error: solo números enteros positivos, vuelva a intentarlo **\n")
    
    minimo = int(minimo)
    maximo = int(maximo)

    if maximo < minimo:
        print("\n** El máximo no puede ser menor que el mínimo **\n")
        return

    resultado = []

    for pais in paises:
        if minimo <= pais["poblacion"] <= maximo:
            resultado.append(pais)
    
    if len(resultado) == 0:
        print("\n** No se encontraron países dentro de ese rango de población **\n")
        return

    print("\n<<<< Países encontrados >>>>\n")
    for pais in resultado:
        print(f"{pais['nombre'].title()} (Población: {pais['poblacion']})")

#Filtro por superficie
def filtro_por_superficie(paises):
    minimo = validacion_solo_numeros_enteros_positivos("\nColoque un mínimo de superficie: ",
            "\n** Error: solo números enteros positivos, vuelva a intentarlo **\n")
    maximo = validacion_solo_numeros_enteros_positivos("Coloque un máximo de superficie: ",
            "\n** Error: solo números enteros positivos, vuelva a intentarlo **\n")
    
    minimo = int(minimo)
    maximo = int(maximo)

    if maximo < minimo:
        print("\n** El máximo no puede ser menor que el mínimo **\n")
        return

    resultado = []

    for pais in paises:
        if minimo <= pais["superficie"] <= maximo:
            resultado.append(pais)

    if len(resultado) == 0:
        print("\n** Error: No se encuentran países con ese rango de superficie **\n")

    else:
        print("\n<<< Países encontrados >>>\n")
        for pais in resultado:
            print(f"{pais['nombre'].title()} (Superficie: {pais['superficie']})")

#Submenu de la opcion 5
def menu_ordenar():
    if lista_vacia():
        return
    print("\n--- ORDENAR POR ---")
    print("a)Nombre")
    print("b)Población")
    print("c)Superficie\n")

    while True:
        opcion_ordenar = input("Elija una opción: ").strip().lower()
        match opcion_ordenar:
            case "a":
                lista = lista_completa_de_paises()
                ordenar_por_nombre(lista)
                break
            case "b":
                lista = lista_completa_de_paises()
                ordenar_por_poblacion(lista, mostrar=True)
                break
            case "c":
                lista = lista_completa_de_paises()
                ordenar_por_superficie(lista, mostrar=True)
                break
            case _:
                print("\n** Opción incorrecta, vuelva a intentarlo (a, b, c) **\n")

#Ordenamos por nombre, comparando cada elemento
def ordenar_por_nombre(paises):
    lista = paises.copy()

    for i in range(len(lista)-1):
        for j in range(len(lista)-1-i):
            if lista[j]["nombre"].lower() > lista[j+1]["nombre"].lower():
                temp = lista[j]
                lista[j] = lista[j+1]
                lista[j+1] = temp

    print("\n<<<< Países ordenados por nombre(A-Z) >>>>\n")
    for pais in lista:
        print(f"{pais['nombre'].title()}")

#Ordenamos por poblacion, comparando cada elemento
def ordenar_por_poblacion(paises, mostrar=False):
    lista = paises.copy()

    for i in range(len(lista)-1):
        for j in range(len(lista)-1-i):
            if lista[j]["poblacion"] > lista[j+1]["poblacion"]:
                temp = lista[j]
                lista[j] = lista[j+1]
                lista[j+1] = temp
    if mostrar:
        print("\n<<<< Países ordenados por Población >>>>\n")
        for pais in lista:
            print(f"{pais['nombre'].title():<15} | Poblacion: {pais['poblacion']}")

    return lista

#Ordenamos por superficie, comparando cada elemento
def ordenar_por_superficie(paises, mostrar=False):
    lista = paises.copy()

    for i in range(len(lista)-1):
        for j in range(len(lista)-1-i):
            if lista[j]["superficie"] > lista[j+1]["superficie"]:
                temp = lista[j]
                lista[j] = lista[j+1]
                lista[j+1] = temp
    if mostrar:
        print("\n<<<< Países ordenados por Superficie >>>>\n")
        for pais in lista:
            print(f"{pais['nombre'].title():<15} | Superficie: {pais['superficie']}")
    return lista

#Llamado de opcion 6
def estadisticas_paises():
    lista = lista_completa_de_paises()
    if lista_vacia():
        return
    print("\n--- ESTADÍSTICAS ---")
    mayor_menor(lista)
    promedio_poblacion(lista)
    promedio_superficie(lista)
    cantidad_paises_por_continente()

#Mostramos el pais que tiene mayor y menor poblacion, llamando a la funcion que los ordena
def mayor_menor(paises):
    lista_ordenada = ordenar_por_poblacion(paises)
    
    menor = lista_ordenada[0]
    mayor = lista_ordenada[-1]

    print("\nPaís con MENOR población:")
    print(f"{menor['nombre'].title()} ({menor['poblacion']})")
    
    print("\nPaís con MAYOR población:")
    print(f"{mayor['nombre'].title()} ({mayor['poblacion']})")

#Sacamos el promedio de poblacion de todos los paises
def promedio_poblacion(paises):
    if len(paises) == 0:
        print("\n** No hay países para calcular promedio, ingreselos con opción (1) **\n")
        return

    suma = 0
    for pais in paises:
        suma += pais["poblacion"]
    
    promedio = suma / len(paises)

    print("\nEl promedio de población total es de:")
    print(f"{promedio:.2f}")

#Sumamos todas las superficies de cada pais y las dividimos por la cantidad de paises
def promedio_superficie(paises):
    if len(paises) == 0:
        print("\n** No hay países para calcular promedio, ingreselos con opción (1) **\n")
        return

    suma = 0
    for pais in paises:
        suma += pais["superficie"]
    
    promedio = suma / len(paises)

    print("\nEl promedio de superficie total es de:")
    print(f"{promedio:.2f}")


def cantidad_paises_por_continente():
    if lista_vacia():
        return

    paises = lista_completa_de_paises()

    conteo = {}

    #Cuenta países por continente.
    for pais in paises:
        continente = pais["continente"]
        if continente not in conteo:
            conteo[continente] = 0
        conteo[continente] += 1

    print("\nCantidad de países por continente:\n")
    for continente, cantidad in conteo.items():
        print(f"{continente.title():<15} | {cantidad} país/es")


def mostrar_menu():
    while True:
        print("="*50)
        print("1. Agregar País (con todos sus datos)")
        print("2. Actualizar Datos (población y superficie km2)")
        print("3. Buscar País por Nombre")
        print("4. Filtrar Países por:")
        print("   - Continente")
        print("   - Rango de población")
        print("   - Rango de superficie")
        print("5. Ordenar Países por:")
        print("   - Nombre (A-Z)")
        print("   - Población (ascendente)")
        print("   - Superficie (ascendente)")
        print("6. Mostrar Estadísticas:")
        print("   - País con mayor y menor población")
        print("   - Promedio de población")
        print("   - Promedio de superficie")
        print("   - Cantidad de países por continente")
        print("7. Salir")
        print("="*50)
        
        opcion_menu = input("Ingrese una opción del menú: ").strip()

        match opcion_menu:
            case "1":
                agregar_pais()
            case "2":
                actualizar_datos()
            case "3":
                buscar_pais()
            case "4":
                menu_filtrar()
            case "5":
                menu_ordenar()
            case "6":
                estadisticas_paises()
            case "7":
                print("="*20)
                print("=== Hasta Pronto ===")
                print("="*20)
                break
            case _:
                print("\n** Opción incorrecta, vuelva a intentarlo (1 al 7)**\n")


mostrar_menu()