
from conexion import obtener_conexion

try:
    conexion = obtener_conexion()
    print("¡Conexión exitosa con Autos Colombia!")

    conexion.close()
    print("Conexión cerrada correctamente.")

except Exception as error:
    print("No se pudo conectar a la base de datos.")
    print("Revisa la configuración y la contraseña.")
    print("Detalle:", error)
