import pyodbc


def crearConexion():
    datos = ("Driver={SQL Server};"
                "Server=localhost,1433;"
                "Database=semi2_practica1;"
                "UID=sa;"
                "PWD=siESesta12.;")
    conn = pyodbc.connect(datos)
    #cursor = conn.cursor()
    return conn