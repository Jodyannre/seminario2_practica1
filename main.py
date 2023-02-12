import ingreso,operacion,conexion
import os

def main():
    os.system('cls')
    #Crear conexion
    conn = conexion.crearConexion()
    #Validar salida
    salir = False
    #Obtener opción del menú
    while not salir:
        #ingreso.imprimirMenu()
        opcion = ingreso.solicitarNumero()
        #Ejecutar operación
        operacion.ejecutar(opcion,conn)
        #Verificar salir
        salir = opcion == 6
    del conn
    os.system('cls')
if __name__ == "__main__":
    main()
