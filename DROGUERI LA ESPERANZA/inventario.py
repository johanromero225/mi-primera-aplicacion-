from database import FarmaciaDB
from models import Producto

class Inventario:
    def __init__(self):
        self.db = FarmaciaDB()
    
    def registrar_ingreso(self, producto, cantidad, proveedor=""):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT id, cantidad FROM productos WHERE codigo_barras = ?", 
                         (producto.codigo_barras,))
            existente = cursor.fetchone()
            
            if existente:
                nueva_cantidad = existente[1] + cantidad
                cursor.execute("""
                    UPDATE productos 
                    SET cantidad = ?, precio_compra = ?, precio_venta = ?
                    WHERE id = ?
                """, (nueva_cantidad, producto.precio_compra, 
                      producto.precio_venta, existente[0]))
                producto_id = existente[0]
            else:
                cursor.execute("""
                    INSERT INTO productos 
                    (codigo_barras, nombre, descripcion, categoria, 
                     precio_compra, precio_venta, cantidad, fecha_vencimiento, laboratorio)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (producto.codigo_barras, producto.nombre, producto.descripcion,
                      producto.categoria, producto.precio_compra, producto.precio_venta,
                      cantidad, producto.fecha_vencimiento, producto.laboratorio))
                producto_id = cursor.lastrowid
            
            cursor.execute("""
                INSERT INTO ingresos (producto_id, cantidad, precio_compra, proveedor)
                VALUES (?, ?, ?, ?)
            """, (producto_id, cantidad, producto.precio_compra, proveedor))
            
            conn.commit()
            return producto_id
    
    def buscar_producto(self, codigo_barras=None, nombre=None):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            if codigo_barras:
                cursor.execute("SELECT * FROM productos WHERE codigo_barras = ?", 
                             (codigo_barras,))
            elif nombre:
                cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", 
                             (f"%{nombre}%",))
            else:
                cursor.execute("SELECT * FROM productos ORDER BY nombre")
            
            return cursor.fetchall()
    
    def verificar_stock_bajo(self, limite=10):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT nombre, cantidad, precio_venta 
                FROM productos 
                WHERE cantidad <= ?
                ORDER BY cantidad
            """, (limite,))
            return cursor.fetchall()