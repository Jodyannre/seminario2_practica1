import pandas as pd
import warnings
import subprocess
import os


warnings.filterwarnings('ignore')

__queries = {
    1:"SELECT COUNT(*) as contador FROM pais",
    2:"SELECT COUNT(*) as contador FROM fecha",
    3:"SELECT COUNT(*) as contador FROM fenomeno",
    4:"SELECT COUNT(*) as contador FROM temporal",
    5:'''
        SELECT COUNT(fenomeno.fecha) as cantidad, fecha.anio as 'año' 
        FROM fenomeno 
        JOIN fecha ON fecha.id = fenomeno.fecha
        GROUP BY fenomeno.fecha,fecha.anio
        ORDER BY cantidad DESC
    ''',
    6:'''
        SELECT fecha.anio as 'año',pais.nombre, pais.id FROM fenomeno
        JOIN fecha
        ON fecha.id = fenomeno.fecha
        JOIN pais
        ON pais.id = fenomeno.pais
        GROUP BY fenomeno.fecha,fenomeno.pais,fecha.anio,pais.nombre, pais.id
        ORDER BY pais.nombre, anio
    ''',
    7:'''
        SELECT pais.nombre,ROUND(AVG(fenomeno.total_danio),2) as promedio FROM fenomeno
        JOIN pais 
        ON pais.id = fenomeno.pais
        GROUP BY pais.nombre
        ORDER BY promedio DESC
    ''',
    8:'''
        SELECT TOP 5 pais.nombre,SUM(fenomeno.total_muertes) as total FROM fenomeno
        JOIN pais 
        ON pais.id = fenomeno.pais
        WHERE fenomeno.total_muertes > 0
        GROUP BY pais.nombre
        ORDER BY total DESC
    ''',
    9:'''
        SELECT TOP 5 fecha.anio as 'año',SUM(fenomeno.total_muertes) as total FROM fenomeno
        JOIN fecha 
        ON fecha.id = fenomeno.fecha
        WHERE fenomeno.total_muertes > 0
        GROUP BY fecha.anio
        ORDER BY total DESC
    ''',
    10:'''
        SELECT TOP 5 COUNT(fenomeno.fecha) as cantidad, fecha.anio as 'año' FROM fenomeno 
        JOIN fecha ON fecha.id = fenomeno.fecha
        GROUP BY fenomeno.fecha,fecha.anio
        ORDER BY cantidad DESC;    
    ''',
    11:'''
        SELECT TOP 5 pais.nombre,SUM(fenomeno.total_casas_destruidas) as total FROM fenomeno
        JOIN pais 
        ON pais.id = fenomeno.pais
        WHERE fenomeno.total_casas_destruidas > 0
        GROUP BY pais.nombre
        ORDER BY total DESC
    ''',
    12:'''
        SELECT TOP 5 pais.nombre,SUM(fenomeno.total_casas_daniadas) as total FROM fenomeno
        JOIN pais 
        ON pais.id = fenomeno.pais
        WHERE fenomeno.total_casas_daniadas > 0
        GROUP BY pais.nombre
        ORDER BY total DESC
    ''',
    13:'''
        SELECT pais.nombre,ROUND(AVG(fenomeno.altura_maxima),2) as promedio FROM fenomeno
        JOIN pais 
        ON pais.id = fenomeno.pais
        GROUP BY pais.nombre
        ORDER BY promedio DESC
    ''',
    14:'''EXEC borrar_tablas;''',
    15:'''EXEC crear_tablas;''',
    16:'''EXEC cargar_informacion;''',
    17:'''SET NOCOUNT ON; DROP TABLE pais;'''
}

def ejecutarQuery(num,cursor):
    #cursor.execute(__queries.get(num))
    data = pd.read_sql(__queries.get(num), cursor)
    #print(data)
    return data


def ejecutar(num,cursor):
    result = None
    match num:
        case 1:
            modificarModelo(14,cursor)
        case 2:
            modificarModelo(15,cursor)
        case 3:
            extrarInformacion(cursor)
        case 4:
            modificarModelo(16,cursor)
        case 5:
            ejecutarConsultas(cursor)


def ejecutarConsultas(cursor):
    os.system('cls')
    consulta1(cursor)
    consulta2(cursor)
    consulta3(cursor)
    for x in range (4,11):
        consulta4_10(x,cursor)
    print('Archivo con resultados de consultas generado con éxito')
    input()
    os.system('cls')

def modificarModelo(num,conn):
    os.system('cls')
    cursor = conn.cursor()
    cursor.execute(__queries.get(num))
    conn.commit()
    cursor.close()
    match num:
        case 14:
            print("Modelo borrado con éxito.")
        case 15:
            print("Modelo creado con éxito.")
        case 16:
            print("Información cargada con éxito.")
    input()
    os.system('cls')

def borrarModelo(conn):
    os.system('cls')
    cursor = conn.cursor()
    cursor.execute(__queries.get(14))
    conn.commit()
    cursor.close()
    print("Modelo borrado con éxito.")
    input()
    os.system('cls')

def crearModelo(conn):
    os.system('cls')
    cursor = conn.cursor()
    cursor.execute(__queries.get(15))
    conn.commit()
    cursor.close()
    print("Modelo creado con éxito.")
    input()
    os.system('cls')

def cargarInformacion(conn):
    os.system('cls')
    cursor = conn.cursor()
    cursor.execute(__queries.get(16))
    conn.commit()
    cursor.close()
    print("Información cargada con éxito.")
    input()
    os.system('cls')


def consulta1(cursor):
    escribirArchivo("-------------------------------------------------------------------\n")
    escribirArchivo("Consulta 1:\n")
    for x in range(1,5):
        result = ejecutarQuery(x,cursor)
        escribirArchivo(formatearTexto(x,str(result['contador'][0])))
        escribirArchivo("\n")


def consulta2(cursor):
    result = ejecutarQuery(5,cursor)
    escribirArchivo("-------------------------------------------------------------------\n")
    escribirArchivo("Consulta 2:\n")
    escribirArchivo(result.to_string(index=False))
    escribirArchivo("\n")


def consulta3(cursor):
    pre = None
    result = ejecutarQuery(6,cursor)

    pre = result.loc[(result['id'] == 1)]
    anios = list(pre['año'])
    pais = pre['nombre'][0]
    
    escribirArchivo("-------------------------------------------------------------------\n")
    escribirArchivo("Consulta 3:\n")

    #Construir las listas
    for x in range (1,105):
        pre = result.loc[(result['id'] == x)]
        pais = pre['nombre'].values[:1][0]
        anios = list(pre['año'])
        escribirArchivo(pais+": ")
        escribirArchivo(listToString(anios))
        escribirArchivo("\n")  


def consulta4_10(num,cursor):
    result = ejecutarQuery(num+3,cursor)
    escribirArchivo("-------------------------------------------------------------------\n")
    escribirArchivo(f"Consulta {num}:\n")
    escribirArchivo(result.to_string(index=False))
    escribirArchivo("\n")


def escribirArchivo(datos):
    try:
        with open('C:\\Users\\Joddie\\Desktop\\resultados.txt', 'a') as f:
            f.write(datos)
    except FileNotFoundError:
        print("El directorio no exite.")


def formatearTexto(num,datos):
    match num:
        case 1:
            return "Contador de paises: "+datos+"\n"
        case 2:
            return "Contador de fechas: "+datos+"\n"
        case 3:
            return "Contador de fenomenos: "+datos+"\n"
        case 4:
            return "Contador de tabla temporal: "+datos+"\n"


def listToString(lista):
    l = "[ "
    for e in lista:
        l = l+str(e)+" ,"
    l = l[0:len(l)-1] + "]"
    return l


def extrarInformacion(cursor):
    #Obtener ruta del archivo
    ruta = input("Ingrese la ruta del archivo: ")
    try:
        with open('C:\\Users\\Joddie\\Desktop\\output.log', "a") as output:
            subprocess.run(rf"docker cp {ruta} sql1:/tmp/" , shell=True, stdout=output, stderr=output)
        #Obtener el nombre del archivo
        array = ruta.split("\\")
        name = array[len(array)-1]
        cargarTablaTemp(name,cursor)
    except FileNotFoundError:
        print("La ruta del archivo no existe o no es correcta.")
        input("...")


def cargarTablaTemp(name,conn):
    os.system('cls')
    query = f'''
        BULK INSERT
            temporal
        FROM
            '/tmp/{name}'
        WITH(
            FIELDTERMINATOR = ',',
            ROWTERMINATOR = '\n',
            FIRSTROW = 3
        );
    '''
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        conn.commit()
        print("Extracción de información exitosa.")
    except:
        print("Error, el archivo no contiene información o no es de tipo CSV.")
    cursor.close()
    input()
    os.system('cls')


