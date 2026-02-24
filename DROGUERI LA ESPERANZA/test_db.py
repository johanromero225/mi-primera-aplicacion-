import sqlite3
import os

print("=" * 50)
print("PRUEBA DE CONEXIÓN A BASE DE DATOS")
print("=" * 50)

# 1. Intentar crear/conectar a la base de datos
try:
    conn = sqlite3.connect("farmacia.db")
    print("✅ Conexión exitosa a farmacia.db")
except Exception as e:
    print(f"❌ Error al conectar: {e}")
    exit()

# 2. Crear un cursor y probar crear una tabla simple
try:
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prueba_conexion (
            id INTEGER PRIMARY KEY,
            mensaje TEXT
        )
    """)
    print("✅ Tabla de prueba creada correctamente")
except Exception as e:
    print(f"❌ Error al crear tabla: {e}")

# 3. Insertar un dato de prueba
try:
    cursor.execute("INSERT INTO prueba_conexion (mensaje) VALUES (?)", 
                   ("Primera prueba exitosa",))
    conn.commit()
    print("✅ Dato insertado correctamente")
except Exception as e:
    print(f"❌ Error al insertar: {e}")

# 4. Leer el dato insertado
try:
    cursor.execute("SELECT * FROM prueba_conexion")
    resultado = cursor.fetchone()
    print(f"✅ Dato recuperado: {resultado[1]}")
except Exception as e:
    print(f"❌ Error al leer: {e}")

# 5. Cerrar conexión
conn.close()
print("✅ Conexión cerrada correctamente")

print("\n" + "=" * 50)
print("🎉 ¡Base de datos funcionando correctamente!")
print("=" * 50)
print("\nArchivo creado: farmacia.db")
print("Ubicación:", os.path.abspath("farmacia.db"))