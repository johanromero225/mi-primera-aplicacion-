from datetime import datetime

class Producto:
    def __init__(self, codigo_barras=None, nombre=None, precio_compra=0, 
                 precio_venta=0, cantidad=0, fecha_vencimiento=None, 
                 laboratorio=None, categoria=None, descripcion=None):
        self.codigo_barras = codigo_barras
        self.nombre = nombre
        self.precio_compra = precio_compra
        self.precio_venta = precio_venta
        self.cantidad = cantidad
        self.fecha_vencimiento = fecha_vencimiento
        self.laboratorio = laboratorio
        self.categoria = categoria
        self.descripcion = descripcion

class Venta:
    def __init__(self, productos=None, metodo_pago="efectivo"):
        self.productos = productos or []
        self.total = sum(p['subtotal'] for p in self.productos)
        self.fecha = datetime.now()
        self.metodo_pago = metodo_pago