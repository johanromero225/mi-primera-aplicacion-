import sqlite3

def verificar_tablas():
    conn = sqlite3.connect("farmacia.db")
    cursor = conn.cursor()
    
    # Obtener lista de tablas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tablas = cursor.fetchall()
    
    print("📊 TABLAS EN LA BASE DE DATOS:")
    print("-" * 30)
    for tabla in tablas:
        print(f"📋 Tabla: {tabla[0]}")
        
        # Ver columnas de cada tabla
        cursor.execute(f"PRAGMA table_info({tabla[0]})")
        columnas = cursor.fetchall()
        for col in columnas:
            print(f"   ├─ {col[1]} ({col[2]})")
        print()
    
    conn.close()

if __name__ == "__main__":
    verificar_tablas()