from database import FarmaciaDB
from datetime import datetime

class Reportes:
    def __init__(self):
        self.db = FarmaciaDB()
    
    def ventas_del_dia(self, fecha=None):
        if fecha is None:
            fecha = datetime.now().date()
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    v.id,
                    v.fecha,
                    COUNT(dv.id) as num_productos,
                    v.total,
                    v.metodo_pago
                FROM ventas v
                LEFT JOIN detalles_venta dv ON v.id = dv.venta_id
                WHERE DATE(v.fecha) = ?
                GROUP BY v.id
                ORDER BY v.fecha DESC
            """, (fecha,))
            
            ventas = cursor.fetchall()
            
            cursor.execute("""
                SELECT 
                    COUNT(*) as num_ventas,
                    SUM(total) as total_dia,
                    AVG(total) as ticket_promedio
                FROM ventas
                WHERE DATE(fecha) = ?
            """, (fecha,))
            
            totales = cursor.fetchone()
            
            cursor.execute("""
                SELECT 
                    p.nombre,
                    SUM(dv.cantidad) as cantidad_vendida,
                    SUM(dv.subtotal) as total_producto
                FROM detalles_venta dv
                JOIN productos p ON dv.producto_id = p.id
                JOIN ventas v ON dv.venta_id = v.id
                WHERE DATE(v.fecha) = ?
                GROUP BY p.id, p.nombre
                ORDER BY cantidad_vendida DESC
                LIMIT 5
            """, (fecha,))
            
            top_productos = cursor.fetchall()
            
            return self._formatear_reporte(fecha, ventas, totales, top_productos)
    
    def _formatear_reporte(self, fecha, ventas, totales, top_productos):
        reporte = []
        reporte.append("=" * 50)
        reporte.append(f"REPORTE DE VENTAS - {fecha}")
        reporte.append("=" * 50)
        
        if totales and totales[0] > 0:
            reporte.append(f"\n📊 TOTAL DEL DÍA: ${totales[1]:.2f}")
            reporte.append(f"   Ventas realizadas: {totales[0]}")
            if totales[2]:
                reporte.append(f"   Ticket promedio: ${totales[2]:.2f}")
            
            reporte.append(f"\n🛒 VENTAS:")
            for venta in ventas:
                hora = venta[1].split()[1] if ' ' in str(venta[1]) else venta[1]
                reporte.append(f"   Venta #{venta[0]} - {hora} - ${venta[3]:.2f}")
            
            reporte.append(f"\n🏆 TOP 5 PRODUCTOS:")
            for i, prod in enumerate(top_productos, 1):
                reporte.append(f"   {i}. {prod[0]} - {prod[1]} uds (${prod[2]:.2f})")
        else:
            reporte.append("\nNo hubo ventas en este día.")
        
        return "\n".join(reporte)
    
    def guardar_reporte(self, contenido, nombre_archivo=None):
        if nombre_archivo is None:
            fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"reporte_{fecha}.txt"
        
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write(contenido)
        
        return nombre_archivo