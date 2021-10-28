from collections import namedtuple
import csv
import time
separador = "*" * 80
Detalle_venta = namedtuple("Detalle_venta", "descripcion cantidad precio") 
Clave_venta = namedtuple("Clave_venta", "folio fecha")
ventas = {} #Creando el diccionario donde se guardarán todas las ventas
art = [] #Definiendo una lista temporal que contendrá los articulos del respaldo
print("Buscando Respaldo...")
time.sleep(1)
try: #Proceso de importar los registros de un respaldo de ventas CSV en caso de existir
    with open("ventas.csv", "r", newline="") as archivo: 
        lector = csv.reader(archivo)
        next(lector)
        for folio, fecha, descripcion, cantidad, precio in lector: #Extraccion de datos e introducirlos en las variables
            lista_claves = list(ventas.keys()) 
            for clave in lista_claves: #Proceso para evitar la duplicidad de claves y juntar los articulos con su repectivo folio
                if int(folio) == clave.folio:
                    if fecha == clave.fecha:
                        detalle = Detalle_venta(descripcion, int(cantidad), float(precio))
                        art.append(detalle)
                        ventas[Clave_venta(int(folio), fecha)] = art
                        break
            else:
                art = [] #En caso de no haber duplicidad de clave, se agrega
                detalle = Detalle_venta(descripcion, int(cantidad), float(precio))
                art.append(detalle)
                ventas[Clave_venta(int(folio), fecha)] = art        
except Exception:
    print("No se encontro ningun respaldo\n") # Se omite la carga en caso de no existir el archivo
else: 
    print("Respaldo cargado con exito!\n")
time.sleep(1)
while True:
    print(f"{separador}")
    print("Menú principal")
    print("1. Registrar una venta.\n")
    print("2. Consultar una venta.\n")
    print("3. Obtener un reporte de todas las ventas para una fecha específica.\n")
    print("4. Salir\n")
    print(separador)
    respuesta = int(input("Escribe el número con la opción que deseas realizar: \n"))
    print(separador)
    if respuesta == 1:
        while True:
            folio = int(input("Ingrese el folio: "))
            for clave in ventas.keys(): #Validar que la el folio ingresado no exista en el respaldo
                if folio == clave.folio:
                    print("Este folio ya esta registrado, porfavor intenta uno nuevo\n")
                    break
            else:
                break
        fecha = input("Ingresa la fecha de la venta (DD/MM/YYYY): ")
        clave_venta = Clave_venta(folio, fecha) #Crear tupla nominada con folio y fecha
        articulos = []
        while True:
            print(f'{separador}')
            descripcion = input("Descipcion del articulo: ")
            cantidad = int(input("Cantidad de piezas vendidas: "))
            precio = float(input("Precio del articulo: "))
            venta_en_turno = Detalle_venta(descripcion, cantidad, precio) #Reunir los detalles del articulo en una tupla nominada
            articulos.append(venta_en_turno) #Agregar los articulos de la venta a una lista
            print(f'{separador}')
            seguir_registrando = int(input("¿Seguir registrando ventas? Si=1, No=0: "))
            if seguir_registrando == 0:
                gran_total = 0
                ventas[clave_venta] = articulos #Añadir los articulos con su respectiva clave
                for articulo in ventas[clave_venta]:
                    total_articulo = articulo.cantidad * articulo.precio
                    gran_total = gran_total + total_articulo
                iva = round((gran_total * .16),2)
                total_mas_iva = round((gran_total + iva),2)
                print(f'{separador}')
                print(f"El IVA (16%) de esta compra es de: ${iva}")
                print(f"El total a pagar es de: ${total_mas_iva}\n")
                input("\nPresione cualquier tecla para continuar...")
                break
    elif respuesta == 2:
        folio_a_cosultar = int(input("Ingresa el folio de la venta que deseas consultar: "))
        lista_claves = list(ventas.keys())
        for clave in lista_claves: 
            if folio_a_cosultar == clave.folio: #Validar que el folio exista en el respaldo
                total = 0
                print(f"El Folio de la venta es: {clave.folio}") #Imprimir la venta con ese folio
                print(f"La Fecha de la venta es: {clave.fecha}")
                print(f'{"Cantidad":<5} | {"Descripcion":<10} | {"Precio venta":<15} | {"Total":<20} \n')
                for articulo in ventas[clave]:
                    print(f"{articulo.cantidad:<8} | {articulo.descripcion:<11} | ${articulo.precio:<14} | ${(articulo.cantidad) * (articulo.precio):<20}")
                    total_por_articulo = articulo.cantidad * articulo.precio
                    total = total + total_por_articulo
                iva = round((total * .16),2)
                total_mas_iva = round((total + iva),2)
                print(f"IVA (16%): ${iva}")
                print(f'Total de la venta: ${total_mas_iva}')
                input("\nPresione cualquier tecla para continuar...")
                break
        else:
            print("El folio ingresado no existe, favor de verficarlo\n") #En caso de que no exista
    elif respuesta == 3:
        fecha_especifica = input("Ingresa la fecha de las ventas que deseas buscar(DD/MM/YYYY): ")
        lista_claves = list(ventas.keys())
        for clave in lista_claves:
            if fecha_especifica == clave.fecha: #Validar que la fecha ingresada esté en el respaldo
                total = 0
                print(f'{separador}\n') #Imprimir todas las ventas con esa fecha
                print(f"El Folio de la venta es: {clave.folio}")
                print(f"La Fecha de la venta es: {clave.fecha}")
                print(f'{"Cantidad":<5} | {"Descripcion":<10} | {"Precio venta":<15} | {"Total":<20} \n')
                for articulo in ventas[clave]:
                    print(f"{articulo.cantidad:<8} | {articulo.descripcion:<11} | ${articulo.precio:<14} | ${(articulo.cantidad) * (articulo.precio):<20}")
                    total_por_articulo = articulo.cantidad * articulo.precio
                    total = total + total_por_articulo
                iva = round((total * .16),2)
                total_mas_iva = round((total + iva),2)
                print(f"\nIVA (16%): ${iva}")
                print(f'Total de la venta: ${total_mas_iva}\n')
        input("\nPresione cualquier tecla para continuar...")
    elif respuesta == 4:
        confirmar = int(input("¿Estas seguro que deseas salir? (1:Si | 0:No): "))
        if confirmar == 1: #Confirmar la salida del programa
            print("Guardando Respaldo...")
            time.sleep(1)
            with open("ventas.csv", "w", newline="") as archivo: #Proceso para abrir el archivo y escribir las ventas en respaldo CSV
                        grabador = csv.writer(archivo)
                        grabador.writerow(("Folio", "Fecha", "Descripcion", "Cantidad", "Precio")) #Encabezado
                        for clave, detalle in ventas.items():
                            for articulo in detalle:
                                grabador.writerow((clave.folio, clave.fecha, articulo.descripcion, articulo.cantidad, articulo.precio))
            break