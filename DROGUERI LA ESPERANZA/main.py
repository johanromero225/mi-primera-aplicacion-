import os
from inventario import Inventario
from ventas import PuntoVenta
from reportes import Reportes
from models import Producto
from datetime import datetime

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    print("\n" + "=" * 50)
    print("      SISTEMA DE GESTIÓN DE FARMACIA")
    print("=" * 50)
    print("1. 📦 Registrar ingreso de mercancía")
    print("2. 💰 Realizar venta")
    print("3. 🔍 Buscar productos")
    print("4. 📊 Ver reporte de ventas del día")
    print("5. ⚠️  Ver productos con stock bajo")
    print("6. 💾 Guardar reporte del día")
    print("7. ❌ Salir")
    print("=" * 50)

def registrar_ingreso():
    inventario = Inventario()
    limpiar_pantalla()
    print("\n=== REGISTRO DE INGRESO ===\n")
    
    try:
        codigo = input("Código de barras: ")
        nombre = input("Nombre del producto: ")
        precio_compra = float(input("Precio de compra: $"))
        precio_venta = float(input("Precio de venta: $"))
        cantidad = int(input("Cantidad: "))
        laboratorio = input("Laboratorio (opcional): ")
        
        producto = Producto(
            codigo_barras=codigo,
            nombre=nombre,
            precio_compra=precio_compra,
            precio_venta=precio_venta,
            cantidad=cantidad,
            laboratorio=laboratorio
        )
        
        inventario.registrar_ingreso(producto, cantidad)
        print(f"\n✅ Producto registrado exitosamente!")
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    input("\nPresione Enter para continuar...")

def realizar_venta():
    pv = PuntoVenta()
    limpiar_pantalla()
    print("\n=== PUNTO DE VENTA ===\n")
    
    while True:
        print(pv.ver_carrito())
        print("\n1. Agregar producto")
        print("2. Procesar venta")
        print("3. Cancelar")
        
        opcion = input("\nOpción: ")
        
        if opcion == "1":
            codigo = input("Código de barras: ")
            try:
                cantidad = int(input("Cantidad: "))
                success, msg = pv.agregar_al_carrito(codigo, cantidad)
                print(f"\n{msg}")
            except:
                print("\n❌ Error")
        
        elif opcion == "2":
            if pv.carrito:
                metodo = input("Método de pago (efectivo/tarjeta): ") or "efectivo"
                success, msg = pv.procesar_venta(metodo)
                print(f"\n{msg}")
                if success:
                    break
            else:
                print("\n❌ Carrito vacío")
        
        elif opcion == "3":
            break
        
        input("\nPresione Enter...")
        limpiar_pantalla()

def main():
    inventario = Inventario()
    reportes = Reportes()
    
    while True:
        limpiar_pantalla()
        mostrar_menu()
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            registrar_ingreso()
        
        elif opcion == "2":
            realizar_venta()
        
        elif opcion == "3":
            limpiar_pantalla()
            print("\n=== BUSCAR PRODUCTOS ===\n")
            termino = input("Código o nombre: ")
            
            if termino.isdigit():
                resultados = inventario.buscar_producto(codigo_barras=termino)
            else:
                resultados = inventario.buscar_producto(nombre=termino)
            
            if resultados:
                for r in resultados:
                    print(f"📦 {r[2]} - Stock: {r[7]} - ${r[6]:.2f}")
            else:
                print("No se encontraron productos")
            
            input("\nPresione Enter...")
        
        elif opcion == "4":
            limpiar_pantalla()
            print(reportes.ventas_del_dia())
            input("\nPresione Enter...")
        
        elif opcion == "5":
            limpiar_pantalla()
            print("\n=== STOCK BAJO ===\n")
            bajos = inventario.verificar_stock_bajo()
            if bajos:
                for p in bajos:
                    print(f"⚠️  {p[0]}: {p[1]} unidades")
            else:
                print("Todo bien con el stock")
            input("\nPresione Enter...")
        
        elif opcion == "6":
            limpiar_pantalla()
            reporte = reportes.ventas_del_dia()
            archivo = reportes.guardar_reporte(reporte)
            print(f"Reporte guardado: {archivo}")
            input("\nPresione Enter...")
        
        elif opcion == "7":
            print("\n¡Hasta luego!")
            break

if __name__ == "__main__":
    main()