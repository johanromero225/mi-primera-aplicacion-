from database import FarmaciaDB

class PuntoVenta:
    def __init__(self):
        self.db = FarmaciaDB()
        self.carrito = []
    
    def agregar_al_carrito(self, codigo_barras, cantidad=1):
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nombre, precio_venta, cantidad 
                FROM productos 
                WHERE codigo_barras = ? AND cantidad >= ?
            """, (codigo_barras, cantidad))
            
            producto = cursor.fetchone()
            
            if producto:
                item = {
                    'producto_id': producto[0],
                    'nombre': producto[1],
                    'precio': producto[2],
                    'cantidad': cantidad,
                    'subtotal': producto[2] * cantidad
                }
                self.carrito.append(item)
                return True, f"Agregado: {producto[1]} - ${item['subtotal']:.2f}"
            else:
                return False, "Producto no disponible o sin stock suficiente"
    
    def ver_carrito(self):
        if not self.carrito:
            return "Carrito vacío"
        
        resultado = "\n=== CARRITO DE COMPRAS ===\n"
        for i, item in enumerate(self.carrito, 1):
            resultado += f"{i}. {item['nombre']} - {item['cantidad']} x ${item['precio']:.2f} = ${item['subtotal']:.2f}\n"
        
        total = sum(item['subtotal'] for item in self.carrito)
        resultado += f"\nTOTAL: ${total:.2f}"
        return resultado
    
    def procesar_venta(self, metodo_pago="efectivo"):
        if not self.carrito:
            return False, "Carrito vacío"
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            total = sum(item['subtotal'] for item in self.carrito)
            
            try:
                cursor.execute("""
                    INSERT INTO ventas (total, metodo_pago)
                    VALUES (?, ?)
                """, (total, metodo_pago))
                venta_id = cursor.lastrowid
                
                for item in self.carrito:
                    cursor.execute("""
                        INSERT INTO detalles_venta 
                        (venta_id, producto_id, cantidad, precio_unitario, subtotal)
                        VALUES (?, ?, ?, ?, ?)
                    """, (venta_id, item['producto_id'], item['cantidad'], 
                          item['precio'], item['subtotal']))
                    
                    cursor.execute("""
                        UPDATE productos 
                        SET cantidad = cantidad - ? 
                        WHERE id = ?
                    """, (item['cantidad'], item['producto_id']))
                
                conn.commit()
                self.carrito = []
                return True, f"Venta procesada. Total: ${total:.2f}"
            
            except Exception as e:
                conn.rollback()
                return False, f"Error: {str(e)}"