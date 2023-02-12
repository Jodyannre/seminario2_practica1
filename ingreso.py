def solicitarNumero():
    correcto = False
    num = 0
    while (not correcto):
        try:
            num = int(input(imprimirMenu()))
            if num > 6 :
                raise ValueError("")
            correcto = True
        except ValueError:
            print('Error, el elemento ingresado debe ser un número entero en el rango de 1-6.')

    return num

def imprimirMenu():
    return '''
        **************MENU***************
        /////////////////////////////////
        1) Borrar modelo
        2) Crear modelo
        3) Extraer información
        4) Cargar información
        5) Realizar consultas
        6) Salir
        /////////////////////////////////
        *********************************

        Ingrese una opción para continuar: 
    '''