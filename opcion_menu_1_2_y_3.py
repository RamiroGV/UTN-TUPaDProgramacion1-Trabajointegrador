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
    
#Abre el CSV lo lee, lo convierte en una lista de diccionarios y esa lista.
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
            print("\n<<<< País encontrado! >>>>\n")
            print(f"País: {pais["nombre"].title()} \nPoblación: {pais["poblacion"]} \nSuperficie: {pais["superficie"]} Km2 \nContinente: {pais["continente"].title()}")
            return

#Para utilizar en otras funciones basta con poner if lista_vacia(): return para que vuelva al menú.
def lista_vacia():
    lista_paises = lista_completa_de_paises()

    if not lista_paises:
        print("\n** Lista vacía, para realizar esta acción primero ingrese paises con opción (1) **\n")
        return True
    return False

        
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
        print("   - Nombre")
        print("   - Población")
        print("   - Superficie (ascendente o descendente)")
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
                print("4. Filtrar Países por:")
            case "5":
                print("5. Ordenar Países por:")
            case "6":
                print("6. Mostrar Estadísticas:")
            case "7":
                print("="*20)
                print("=== Hasta Pronto ===")
                print("="*20)
                break
            case _:
                print("\n** Opción incorrecta, vuelva a intentarlo (1 al 7)**\n")


mostrar_menu()