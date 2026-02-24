import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from inventario import Inventario
from ventas import PuntoVenta
from reportes import Reportes
from models import Producto
import time
import os
import re
import json

# Configuración de la página (DEBE SER LO PRIMERO)
st.set_page_config(
    page_title="Farmacia La Esperanza",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== DISEÑO PROFESIONAL - CSS MEJORADO ==========
st.markdown("""
    <style>
    /* Estilos generales */
    .main {
        padding: 1rem 2rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Tarjetas de métricas */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
    }
    .metric-card h3 {
        color: #2c3e50;
        font-size: 1rem;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .metric-card .metric-value {
        color: #27ae60;
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    /* Botones principales */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        border: 1px solid rgba(255,255,255,0.2);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
    }
    
    /* Botones de acción secundaria */
    .stButton > button.secondary {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    /* Tarjetas de reportes */
    .report-box {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        border-left: 5px solid #27ae60;
        font-family: 'Courier New', monospace;
        white-space: pre-wrap;
        margin: 1rem 0;
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    /* Encabezados */
    h1, h2, h3 {
        color: #2c3e50;
        font-weight: 600;
    }
    
    /* Sidebar mejorado */
    .css-1d391kg {
        background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
    }
    .sidebar-content {
        color: white;
    }
    
    /* Inputs y selectboxes */
    .stTextInput > div > div > input, .stSelectbox > div > div > select {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 0.75rem;
        transition: all 0.3s ease;
    }
    .stTextInput > div > div > input:focus, .stSelectbox > div > div > select:focus {
        border-color: #27ae60;
        box-shadow: 0 0 0 3px rgba(39, 174, 96, 0.1);
    }
    
    /* Dataframes con diseño mejorado */
    .dataframe {
        border: none !important;
        border-radius: 15px !important;
        overflow: hidden !important;
        box-shadow: 0 5px 20px rgba(0,0,0,0.05) !important;
    }
    .dataframe thead th {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 1rem !important;
        border: none !important;
    }
    .dataframe tbody td {
        padding: 0.75rem !important;
        border-bottom: 1px solid #f0f0f0 !important;
    }
    .dataframe tbody tr:hover {
        background-color: #f8f9fa !important;
        transition: all 0.3s ease;
    }
    
    /* Alertas y mensajes */
    .stAlert {
        border-radius: 10px !important;
        border: none !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05) !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: white !important;
        border-radius: 10px !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05) !important;
        border: 1px solid rgba(0,0,0,0.05) !important;
        padding: 1rem !important;
        font-weight: 600 !important;
        color: #2c3e50 !important;
    }
    .streamlit-expanderHeader:hover {
        background: #f8f9fa !important;
    }
    
    /* Pestañas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background: white;
        padding: 0.5rem;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Estilo para items de factura */
    .factura-item {
        background: white;
        padding: 0.5rem;
        border-radius: 5px;
        margin-bottom: 0.5rem;
        border-left: 3px solid #3498db;
        display: flex;
        justify-content: space-between;
    }
    .factura-item .descripcion {
        font-weight: 500;
    }
    .factura-item .precio {
        color: #27ae60;
        font-weight: bold;
    }
    .factura-total {
        background: #27ae60;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 1rem 0;
    }
    
    /* Estilo para modales */
    .modal {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        border-left: 5px solid #27ae60;
        margin: 1rem 0;
        animation: slideIn 0.3s ease;
    }
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar componentes
@st.cache_resource
def init_sistema():
    return {
        'inventario': Inventario(),
        'ventas': PuntoVenta(),
        'reportes': Reportes()
    }

# Inicializar carrito en session state
if 'carrito' not in st.session_state:
    st.session_state.carrito = []
    
# Inicializar pedido en session state
if 'pedido' not in st.session_state:
    st.session_state.pedido = []

# Inicializar modal de factura
if 'modal_factura' not in st.session_state:
    st.session_state.modal_factura = None

sistema = init_sistema()

# ========== FUNCIONES PARA PROVEEDORES ==========
PROVEEDORES_FILE = "proveedores.json"
COMPRAS_FILE = "compras.json"
FACTURA_FILE = "facturas.json"

def cargar_proveedores():
    if os.path.exists(PROVEEDORES_FILE):
        with open(PROVEEDORES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def guardar_proveedores(proveedores):
    with open(PROVEEDORES_FILE, 'w', encoding='utf-8') as f:
        json.dump(proveedores, f, indent=2, ensure_ascii=False)

def cargar_compras():
    if os.path.exists(COMPRAS_FILE):
        with open(COMPRAS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def guardar_compra(compra):
    compras = cargar_compras()
    compras.append(compra)
    with open(COMPRAS_FILE, 'w', encoding='utf-8') as f:
        json.dump(compras, f, indent=2, ensure_ascii=False)

def cargar_facturas():
    if os.path.exists(FACTURA_FILE):
        with open(FACTURA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def guardar_factura(factura):
    facturas = cargar_facturas()
    facturas.append(factura)
    with open(FACTURA_FILE, 'w', encoding='utf-8') as f:
        json.dump(facturas, f, indent=2, ensure_ascii=False)

# ========== TÍTULO PRINCIPAL ==========
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);">
            <h1 style="color: white; font-size: 3rem; margin-bottom: 0;">💊 FARMACIA LA ESPERANZA</h1>
            <p style="color: rgba(255,255,255,0.9); font-size: 1.2rem;">Sistema de Gestión Profesional</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

# ========== MENÚ LATERAL MEJORADO ==========
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <h2 style="color: white;">💊 Menú Principal</h2>
        </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio(
        "Seleccione una opción:",
        ["🏠 Inicio", "📦 Ingreso de Mercancía", "💰 Punto de Venta", 
         "🔍 Buscar Productos", "📊 Reportes", "⚠️ Stock Bajo", 
         "👥 Proveedores", "📝 Editar/Eliminar Productos", "📋 Historial de Compras", "❌ Salir"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: rgba(255,255,255,0.7); padding: 1rem;">
            <p>© 2024 - Sistema de Gestión</p>
            <p style="font-size: 0.8rem;">Versión 2.0 Profesional</p>
        </div>
    """, unsafe_allow_html=True)

# ========== PÁGINAS ==========

# 🏠 INICIO MEJORADO
if menu == "🏠 Inicio":
    st.markdown("<h2 style='color: #2c3e50;'>📊 Panel de Control</h2>", unsafe_allow_html=True)
    
    # Obtener datos para el dashboard
    try:
        productos = sistema['inventario'].buscar_producto()
        total_productos = len(productos) if productos else 0
        stock_bajo = len(sistema['inventario'].verificar_stock_bajo())
        proveedores = cargar_proveedores()
        compras = cargar_compras()
        facturas = cargar_facturas()
        
        # Ventas del día
        hoy = str(date.today())
        facturas_hoy = [f for f in facturas if f['fecha'] == hoy]
        total_ventas_hoy = sum(f['total'] for f in facturas_hoy)
        
        # Métricas en columnas con diseño mejorado
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <h3>📦 Total Productos</h3>
                    <div class="metric-value">{total_productos}</div>
                    <p style="color: #7f8c8d; font-size: 0.9rem;">en inventario</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <h3>⚠️ Stock Bajo</h3>
                    <div class="metric-value" style="color: #e74c3c;">{stock_bajo}</div>
                    <p style="color: #7f8c8d; font-size: 0.9rem;">necesitan reposición</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <h3>👥 Proveedores</h3>
                    <div class="metric-value">{len(proveedores)}</div>
                    <p style="color: #7f8c8d; font-size: 0.9rem;">registrados</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
                <div class="metric-card">
                    <h3>💰 Ventas Hoy</h3>
                    <div class="metric-value" style="color: #27ae60;">${total_ventas_hoy:,.2f}</div>
                    <p style="color: #7f8c8d; font-size: 0.9rem;">{len(facturas_hoy)} facturas</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Últimos productos agregados
        st.markdown("<h3 style='color: #2c3e50;'>📋 Últimos Productos Agregados</h3>", unsafe_allow_html=True)
        if productos:
            df_productos = pd.DataFrame(productos[:10])
            df_productos.columns = ['ID', 'Código', 'Nombre', 'Descripción', 'Categoría',
                                   'P.Compra', 'P.Venta', 'Stock', 'Vencimiento', 'Laboratorio', 'Created_At']
            
            st.dataframe(df_productos[['Nombre', 'P.Venta', 'Stock', 'Laboratorio']], use_container_width=True)
        
    except Exception as e:
        st.info("🌟 Bienvenido al sistema. Comience registrando productos.")

# 📦 INGRESO DE MERCANCÍA MEJORADO CON FECHA DE COMPRA
elif menu == "📦 Ingreso de Mercancía":
    st.markdown("<h2 style='color: #2c3e50;'>📦 Registrar Ingreso de Mercancía</h2>", unsafe_allow_html=True)
    
    # Cargar proveedores
    proveedores = cargar_proveedores()
    opciones_proveedor = ["Seleccione un proveedor"] + [p['nombre'] for p in proveedores]
    
    with st.form("form_ingreso", clear_on_submit=True):
        st.markdown("### 📋 Datos del Producto")
        col1, col2 = st.columns(2)
        
        with col1:
            codigo = st.text_input("🔖 Código de barras *", help="Código único del producto")
            nombre = st.text_input("📝 Nombre del producto *", help="Nombre comercial del producto")
            laboratorio = st.text_input("🏭 Laboratorio", help="Laboratorio fabricante")
            categoria = st.text_input("📋 Categoría", help="Ej: Analgésicos, Antibióticos, etc.")
        
        with col2:
            precio_compra = st.number_input("💰 Precio de compra ($) *", min_value=0.0, step=100.0, help="Precio al que compró el producto")
            precio_venta = st.number_input("💵 Precio de venta ($) *", min_value=0.0, step=100.0, help="Precio al que venderá el producto")
            cantidad = st.number_input("🔢 Cantidad *", min_value=1, value=1, help="Número de unidades que ingresan")
            fecha_venc = st.date_input("📅 Fecha de vencimiento", value=None, min_value=date.today(), help="Fecha de vencimiento del producto")
        
        st.markdown("---")
        st.markdown("### 📦 Datos de la Compra")
        col3, col4 = st.columns(2)
        
        with col3:
            fecha_compra = st.date_input("📅 Fecha de compra", value=date.today(), help="Cuándo realizó la compra")
            proveedor = st.selectbox("🏢 Proveedor", opciones_proveedor, help="Seleccione el proveedor")
        
        with col4:
            numero_factura = st.text_input("🧾 Número de factura", help="Número de factura de la compra")
            notas_compra = st.text_area("📝 Notas", help="Información adicional de la compra", height=68)
        
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            submitted = st.form_submit_button("✅ Registrar Ingreso", use_container_width=True)
        
        if submitted:
            if not codigo or not nombre:
                st.error("❌ Código y nombre son obligatorios")
            elif precio_compra <= 0:
                st.error("❌ El precio de compra debe ser mayor a 0")
            elif precio_venta <= 0:
                st.error("❌ El precio de venta debe ser mayor a 0")
            else:
                try:
                    producto = Producto(
                        codigo_barras=codigo,
                        nombre=nombre,
                        precio_compra=precio_compra,
                        precio_venta=precio_venta,
                        cantidad=cantidad,
                        laboratorio=laboratorio,
                        fecha_vencimiento=str(fecha_venc) if fecha_venc else None,
                        categoria=categoria
                    )
                    
                    # Registrar en inventario
                    sistema['inventario'].registrar_ingreso(producto, cantidad)
                    
                    # Guardar en historial de compras
                    nueva_compra = {
                        'fecha_compra': str(fecha_compra),
                        'fecha_registro': str(datetime.now()),
                        'codigo_producto': codigo,
                        'nombre_producto': nombre,
                        'cantidad': cantidad,
                        'precio_compra': precio_compra,
                        'precio_venta': precio_venta,
                        'proveedor': proveedor if proveedor != "Seleccione un proveedor" else "",
                        'numero_factura': numero_factura,
                        'notas': notas_compra,
                        'laboratorio': laboratorio,
                        'categoria': categoria,
                        'fecha_vencimiento': str(fecha_venc) if fecha_venc else None
                    }
                    guardar_compra(nueva_compra)
                    
                    # Mensaje de éxito con estilo
                    st.markdown(f"""
                        <div style="background: linear-gradient(135deg, #a8e6cf 0%, #d4edda 100%); padding: 1.5rem; border-radius: 15px; border-left: 5px solid #27ae60; margin: 1rem 0;">
                            <h4 style="color: #155724; margin-bottom: 0.5rem;">✅ ¡Producto registrado exitosamente!</h4>
                            <p style="color: #155724;"><strong>{nombre}</strong> - {cantidad} unidades</p>
                            <p style="color: #155724; font-size: 0.9rem;">📅 Fecha compra: {fecha_compra}</p>
                            <p style="color: #155724; font-size: 0.9rem;">🏢 Proveedor: {proveedor if proveedor != 'Seleccione un proveedor' else 'No especificado'}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    time.sleep(2)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# 💰 PUNTO DE VENTA - SISTEMA DE FACTURACIÓN PROFESIONAL
elif menu == "💰 Punto de Venta":
    st.markdown("<h2 style='color: #2c3e50;'>💰 Sistema de Facturación</h2>", unsafe_allow_html=True)
    
    # ===== CONTROL DE CAJA =====
    CAJA_FILE = "estado_caja.json"
    
    def cargar_estado_caja():
        if os.path.exists(CAJA_FILE):
            with open(CAJA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            'abierta': False,
            'fecha_apertura': None,
            'hora_apertura': None,
            'fecha_cierre': None,
            'hora_cierre': None,
            'usuario': None,
            'ventas_del_dia': [],
            'total_ventas': 0,
            'efectivo_inicial': 0,
            'efectivo_final': 0,
            'ultima_factura': 1000
        }
    
    def guardar_estado_caja(estado):
        with open(CAJA_FILE, 'w', encoding='utf-8') as f:
            json.dump(estado, f, indent=2, ensure_ascii=False)
    
    # Inicializar estado de caja
    if 'caja' not in st.session_state:
        st.session_state.caja = cargar_estado_caja()
    
    # Inicializar factura actual
    if 'factura_actual' not in st.session_state:
        st.session_state.factura_actual = []
    
    # Asegurar que ultima_factura existe
    if 'ultima_factura' not in st.session_state.caja:
        st.session_state.caja['ultima_factura'] = 1000
    
    # ===== ESTADO DE CAJA EN SIDEBAR =====
    with st.sidebar:
        if st.session_state.caja['abierta']:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                    <h4 style="color: white; margin: 0;">✅ CAJA ABIERTA</h4>
                    <p style="color: white; margin: 0; font-size: 0.9rem;">{st.session_state.caja['fecha_apertura']}</p>
                    <p style="color: white; margin: 0; font-size: 0.9rem;">{st.session_state.caja['hora_apertura']}</p>
                    <p style="color: white; margin: 0; font-size: 0.9rem;">👤 {st.session_state.caja['usuario']}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Número de factura actual
            numero_factura = st.session_state.caja['ultima_factura'] + 1
                
            st.markdown(f"""
                <div style="background: #3498db; padding: 0.5rem; border-radius: 5px; margin: 0.5rem 0;">
                    <p style="color: white; text-align: center; margin: 0;">🧾 Factura N°: <b>POS-{numero_factura}</b></p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); padding: 1rem; border-radius: 10px; margin: 1rem 0;">
                    <h4 style="color: white; margin: 0;">❌ CAJA CERRADA</h4>
                    <p style="color: white; margin: 0; font-size: 0.9rem;">{st.session_state.caja['fecha_cierre'] or ''}</p>
                    <p style="color: white; margin: 0; font-size: 0.9rem;">{st.session_state.caja['hora_cierre'] or ''}</p>
                </div>
            """, unsafe_allow_html=True)
    
    # ===== PESTAÑAS DE CAJA =====
    if not st.session_state.caja['abierta']:
        # Mostrar formulario de apertura
        st.markdown("### 🔓 Abrir Caja")
        
        with st.form("form_abrir_caja"):
            col1, col2 = st.columns(2)
            with col1:
                usuario = st.text_input("👤 Nombre del cajero", help="Quién abre la caja")
                efectivo_inicial = st.number_input("💰 Efectivo inicial ($)", min_value=0.0, step=1000.0, help="Dinero con el que se abre la caja")
            with col2:
                st.markdown("""
                    <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px;">
                        <h4>📋 Reglas de caja:</h4>
                        <ul style="margin: 0; padding-left: 1.5rem;">
                            <li>Debe ingresar efectivo inicial</li>
                            <li>No se puede vender con caja cerrada</li>
                            <li>Al cerrar se generará reporte</li>
                        </ul>
                    </div>
                """, unsafe_allow_html=True)
            
            if st.form_submit_button("✅ Abrir Caja", use_container_width=True):
                if not usuario:
                    st.error("❌ Debe ingresar el nombre del cajero")
                else:
                    # Abrir caja manteniendo el número de factura
                    st.session_state.caja = {
                        'abierta': True,
                        'fecha_apertura': str(date.today()),
                        'hora_apertura': datetime.now().strftime("%H:%M:%S"),
                        'fecha_cierre': None,
                        'hora_cierre': None,
                        'usuario': usuario,
                        'ventas_del_dia': [],
                        'total_ventas': 0,
                        'efectivo_inicial': efectivo_inicial,
                        'efectivo_final': 0,
                        'ultima_factura': st.session_state.caja.get('ultima_factura', 1000)
                    }
                    guardar_estado_caja(st.session_state.caja)
                    st.success(f"✅ Caja abierta por {usuario} con ${efectivo_inicial:,.2f} inicial")
                    time.sleep(1)
                    st.rerun()
    else:
        # ===== SISTEMA DE FACTURACIÓN =====
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 🔍 Agregar Productos")
            
            # Buscador de productos
            busqueda = st.text_input("Buscar producto por código o nombre", key="buscar_producto_factura", placeholder="Ej: Ibuprofeno o 123456789")
            
            if busqueda:
                with st.spinner("Buscando..."):
                    if busqueda.isdigit():
                        resultados = sistema['inventario'].buscar_producto(codigo_barras=busqueda)
                    else:
                        resultados = sistema['inventario'].buscar_producto(nombre=busqueda)
                
                if resultados:
                    # Mostrar resultados como botones
                    st.markdown("#### Productos encontrados:")
                    for idx, prod in enumerate(resultados[:5]):
                        with st.container():
                            col_info, col_btn = st.columns([4, 1])
                            with col_info:
                                st.markdown(f"**{prod[2]}**")
                                st.caption(f"Código: {prod[1]} | Stock: {prod[7]} | Precio: ${prod[6]:,.2f}")
                            with col_btn:
                                if prod[7] > 0:
                                    if st.button("➕", key=f"agregar_factura_{idx}_{prod[0]}"):
                                        # Agregar a factura actual
                                        item = {
                                            'codigo': prod[1],
                                            'nombre': prod[2],
                                            'cantidad': 1,
                                            'precio': prod[6],
                                            'subtotal': prod[6]
                                        }
                                        st.session_state.factura_actual.append(item)
                                        st.success(f"✅ {prod[2]} agregado")
                                        time.sleep(0.5)
                                        st.rerun()
                                else:
                                    st.error("❌")
                else:
                    st.warning("No se encontraron productos")
            
            # Entrada manual
            with st.expander("📝 Entrada manual por código"):
                with st.form("form_manual"):
                    codigo_manual = st.text_input("Código de barras")
                    cantidad_manual = st.number_input("Cantidad", min_value=1, value=1)
                    
                    if st.form_submit_button("✅ Agregar"):
                        if codigo_manual:
                            resultados = sistema['inventario'].buscar_producto(codigo_barras=codigo_manual)
                            if resultados:
                                prod = resultados[0]
                                if prod[7] >= cantidad_manual:
                                    for _ in range(cantidad_manual):
                                        item = {
                                            'codigo': prod[1],
                                            'nombre': prod[2],
                                            'cantidad': 1,
                                            'precio': prod[6],
                                            'subtotal': prod[6]
                                        }
                                        st.session_state.factura_actual.append(item)
                                    st.success(f"✅ {cantidad_manual} x {prod[2]} agregado")
                                    time.sleep(0.5)
                                    st.rerun()
                                else:
                                    st.error(f"❌ Stock insuficiente. Disponible: {prod[7]}")
                            else:
                                st.error("❌ Producto no encontrado")
        
        with col2:
            st.markdown("### 🧾 Factura Actual")
            
            # Mostrar número de factura actual
            numero_factura = st.session_state.caja['ultima_factura'] + 1
                
            st.markdown(f"""
                <div style="background: #2c3e50; color: white; padding: 0.5rem; border-radius: 5px; margin-bottom: 1rem; text-align: center;">
                    <b>FACTURA N°: POS-{numero_factura}</b>
                </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.factura_actual:
                # Mostrar items de la factura
                for i, item in enumerate(st.session_state.factura_actual):
                    st.markdown(f"""
                        <div class="factura-item">
                            <span class="descripcion">{item['nombre'][:30]}</span>
                            <span class="precio">${item['precio']:,.2f}</span>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Calcular total
                total_factura = sum(item['subtotal'] for item in st.session_state.factura_actual)
                
                # Mostrar total
                st.markdown(f"""
                    <div class="factura-total">
                        TOTAL: ${total_factura:,.2f}
                    </div>
                """, unsafe_allow_html=True)
                
                # Formulario de pago
                with st.form("form_pago"):
                    pago = st.number_input("💰 Monto recibido ($)", min_value=0.0, value=total_factura, step=1000.0)
                    cambio = pago - total_factura
                    
                    if cambio >= 0:
                        st.success(f"✅ Cambio: ${cambio:,.2f}")
                    else:
                        st.error(f"❌ Faltan: ${abs(cambio):,.2f}")
                    
                    col_p1, col_p2 = st.columns(2)
                    with col_p1:
                        if st.form_submit_button("✅ Procesar Venta", use_container_width=True):
                            if pago >= total_factura:
                                # Obtener el número de factura actual
                                numero_actual = st.session_state.caja['ultima_factura'] + 1
                                
                                # Generar factura
                                nueva_factura = {
                                    'numero': numero_actual,
                                    'fecha': str(date.today()),
                                    'hora': datetime.now().strftime("%H:%M:%S"),
                                    'vendedor': st.session_state.caja['usuario'],
                                    'items': st.session_state.factura_actual.copy(),
                                    'total': total_factura,
                                    'pago': pago,
                                    'cambio': cambio
                                }
                                
                                # Guardar factura
                                guardar_factura(nueva_factura)
                                
                                # Agregar a ventas del día
                                for item in st.session_state.factura_actual:
                                    venta = {
                                        'fecha': str(datetime.now()),
                                        'codigo': item['codigo'],
                                        'nombre': item['nombre'],
                                        'precio': item['precio'],
                                        'vendedor': st.session_state.caja['usuario'],
                                        'factura': numero_actual
                                    }
                                    st.session_state.caja['ventas_del_dia'].append(venta)
                                    st.session_state.caja['total_ventas'] += item['precio']
                                
                                # Actualizar número de factura
                                st.session_state.caja['ultima_factura'] = numero_actual
                                guardar_estado_caja(st.session_state.caja)
                                
                                # Actualizar stock
                                from database import FarmaciaDB
                                db = FarmaciaDB()
                                with db.get_connection() as conn:
                                    cursor = conn.cursor()
                                    for item in st.session_state.factura_actual:
                                        cursor.execute("UPDATE productos SET cantidad = cantidad - 1 WHERE codigo_barras = ?", (item['codigo'],))
                                    conn.commit()
                                
                                # Mostrar factura procesada
                                st.success(f"✅ Venta completada - Factura #{numero_actual}")
                                
                                # Limpiar factura actual
                                st.session_state.factura_actual = []
                                time.sleep(2)
                                st.rerun()
                            else:
                                st.error("❌ Pago insuficiente")
                    
                    with col_p2:
                        if st.form_submit_button("🗑️ Cancelar", use_container_width=True):
                            st.session_state.factura_actual = []
                            st.rerun()
            else:
                st.info("No hay productos en la factura")
        
        # Botón para cerrar caja
        if st.button("🔒 Cerrar Caja", use_container_width=True):
            st.session_state.cerrando_caja = True
            st.rerun()
    
    # ===== CIERRE DE CAJA =====
    if 'cerrando_caja' in st.session_state and st.session_state.cerrando_caja:
        st.markdown("---")
        st.markdown("### 🔒 Cierre de Caja")
        
        total_ventas = len(st.session_state.caja['ventas_del_dia'])
        total_dinero = st.session_state.caja['total_ventas']
        efectivo_inicial = st.session_state.caja['efectivo_inicial']
        
        st.markdown(f"""
            <div style="background: white; padding: 2rem; border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);">
                <h4>📊 Resumen del Día</h4>
                <table style="width: 100%;">
                    <tr>
                        <td><b>Cajero:</b></td>
                        <td>{st.session_state.caja['usuario']}</td>
                    </tr>
                    <tr>
                        <td><b>Fecha apertura:</b></td>
                        <td>{st.session_state.caja['fecha_apertura']} {st.session_state.caja['hora_apertura']}</td>
                    </tr>
                    <tr>
                        <td><b>Fecha cierre:</b></td>
                        <td>{date.today()} {datetime.now().strftime('%H:%M:%S')}</td>
                    </tr>
                    <tr>
                        <td><b>Productos vendidos:</b></td>
                        <td>{total_ventas}</td>
                    </tr>
                    <tr>
                        <td><b>Total ventas:</b></td>
                        <td>${total_dinero:,.2f}</td>
                    </tr>
                    <tr>
                        <td><b>Efectivo inicial:</b></td>
                        <td>${efectivo_inicial:,.2f}</td>
                    </tr>
                    <tr>
                        <td><b>Efectivo final esperado:</b></td>
                        <td><b>${efectivo_inicial + total_dinero:,.2f}</b></td>
                    </tr>
                </table>
            </div>
        """, unsafe_allow_html=True)
        
        with st.form("form_cierre_caja"):
            efectivo_real = st.number_input("💰 Efectivo real en caja ($)", min_value=0.0, step=1000.0, help="Cuente el dinero y ingréselo")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("✅ Confirmar Cierre", use_container_width=True):
                    # Calcular diferencia
                    diferencia = efectivo_real - (efectivo_inicial + total_dinero)
                    
                    # Guardar cierre
                    st.session_state.caja['fecha_cierre'] = str(date.today())
                    st.session_state.caja['hora_cierre'] = datetime.now().strftime("%H:%M:%S")
                    st.session_state.caja['efectivo_final'] = efectivo_real
                    
                    # Generar reporte de cierre
                    reporte_cierre = f"""
                    ========================================
                    CIERRE DE CAJA
                    ========================================
                    Fecha: {date.today()}
                    Hora: {datetime.now().strftime('%H:%M:%S')}
                    Cajero: {st.session_state.caja['usuario']}
                    
                    APERTURA:
                    - Fecha: {st.session_state.caja['fecha_apertura']}
                    - Hora: {st.session_state.caja['hora_apertura']}
                    - Efectivo inicial: ${efectivo_inicial:,.2f}
                    
                    VENTAS DEL DÍA:
                    - Total productos: {total_ventas}
                    - Total ventas: ${total_dinero:,.2f}
                    
                    CIERRE:
                    - Efectivo esperado: ${efectivo_inicial + total_dinero:,.2f}
                    - Efectivo real: ${efectivo_real:,.2f}
                    - Diferencia: ${diferencia:,.2f}
                    
                    {'' if diferencia == 0 else '⚠️ HAY DIFERENCIA EN CAJA'}
                    ========================================
                    """
                    
                    # Guardar reporte en informes/cierres_caja
                    carpeta = os.path.join("informes", "cierres_caja")
                    os.makedirs(carpeta, exist_ok=True)
                    archivo = f"cierre_caja_{date.today()}.txt"
                    with open(os.path.join(carpeta, archivo), 'w', encoding='utf-8') as f:
                        f.write(reporte_cierre)
                    
                    # Marcar caja como cerrada
                    st.session_state.caja['abierta'] = False
                    guardar_estado_caja(st.session_state.caja)
                    
                    if diferencia == 0:
                        st.success(f"✅ Caja cerrada correctamente. ¡Cuadre perfecto!")
                    else:
                        st.warning(f"⚠️ Caja cerrada con diferencia de ${diferencia:,.2f}")
                    
                    st.info(f"📄 Reporte guardado: {archivo}")
                    del st.session_state.cerrando_caja
                    time.sleep(3)
                    st.rerun()
            
            with col2:
                if st.form_submit_button("❌ Cancelar", use_container_width=True):
                    del st.session_state.cerrando_caja
                    st.rerun()

# 🔍 BUSCAR PRODUCTOS (mejorado visualmente)
elif menu == "🔍 Buscar Productos":
    st.markdown("<h2 style='color: #2c3e50;'>🔍 Buscar Productos</h2>", unsafe_allow_html=True)
    
    busqueda = st.text_input("Buscar por nombre o código de barras", placeholder="Ej: Ibuprofeno o 123456789", key="input_buscar")
    
    if busqueda:
        with st.spinner("Buscando..."):
            if busqueda.isdigit():
                resultados = sistema['inventario'].buscar_producto(codigo_barras=busqueda)
            else:
                resultados = sistema['inventario'].buscar_producto(nombre=busqueda)
        
        if resultados:
            st.success(f"✅ {len(resultados)} producto(s) encontrado(s)")
            
            df = pd.DataFrame(resultados)
            df.columns = ['ID', 'Código', 'Nombre', 'Descripción', 'Categoría',
                         'P.Compra', 'P.Venta', 'Stock', 'Vencimiento', 'Laboratorio', 'Created_At']
            
            df_display = df[['Nombre', 'Código', 'P.Compra', 'P.Venta', 'Stock', 'Laboratorio', 'Vencimiento']].copy()
            df_display['P.Compra'] = df_display['P.Compra'].apply(lambda x: f"${x:,.2f}")
            df_display['P.Venta'] = df_display['P.Venta'].apply(lambda x: f"${x:,.2f}")
            
            st.dataframe(df_display, use_container_width=True)
            
            if len(resultados) == 1:
                st.markdown("---")
                st.markdown("### 📋 Detalle del Producto")
                col_det1, col_det2, col_det3 = st.columns(3)
                with col_det1:
                    st.markdown(f"**Código:** {resultados[0][1]}")
                    st.markdown(f"**Nombre:** {resultados[0][2]}")
                    st.markdown(f"**Laboratorio:** {resultados[0][9]}")
                with col_det2:
                    st.markdown(f"**Precio Compra:** ${resultados[0][5]:,.2f}")
                    st.markdown(f"**Precio Venta:** ${resultados[0][6]:,.2f}")
                    st.markdown(f"**Stock:** {resultados[0][7]} unidades")
                with col_det3:
                    st.markdown(f"**Vencimiento:** {resultados[0][8] or 'No registrado'}")
                    st.markdown(f"**Categoría:** {resultados[0][4] or 'Sin categoría'}")
        else:
            st.warning("❌ No se encontraron productos")

# 📊 REPORTES (CORREGIDO - CON TODAS LAS FACTURAS)
elif menu == "📊 Reportes":
    st.markdown("<h2 style='color: #2c3e50;'>📊 Reportes de Ventas</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📅 Reporte Diario", "📆 Reporte Mensual", "📂 Ver Informes Guardados"])
    
    # ===== PESTAÑA 1: REPORTE DIARIO =====
    with tab1:
        st.markdown("### 📅 Facturas del Día")
        
        facturas = cargar_facturas()
        hoy = str(date.today())
        
        # Filtrar facturas de hoy
        facturas_hoy = [f for f in facturas if f['fecha'] == hoy]
        
        if facturas_hoy:
            total_dia = sum(f['total'] for f in facturas_hoy)
            st.metric("💰 TOTAL DEL DÍA", f"${total_dia:,.2f}")
            
            st.markdown("---")
            
            # Mostrar cada factura con su botón
            for i, factura in enumerate(facturas_hoy):
                col1, col2, col3 = st.columns([2, 1, 1])
                with col1:
                    st.markdown(f"**Factura #{factura['numero']}** - {factura['hora']}")
                with col2:
                    st.markdown(f"**${factura['total']:,.2f}**")
                with col3:
                    if st.button(f"🔍 Ver", key=f"ver_factura_{i}"):
                        st.session_state.modal_factura = factura
                        st.rerun()
            
            # Modal para ver detalle de factura
            if st.session_state.modal_factura:
                with st.container():
                    st.markdown('<div class="modal">', unsafe_allow_html=True)
                    factura = st.session_state.modal_factura
                    
                    st.markdown(f"### 🧾 Factura #{factura['numero']}")
                    st.markdown(f"**Fecha:** {factura['fecha']} - {factura['hora']}")
                    st.markdown(f"**Vendedor:** {factura['vendedor']}")
                    
                    st.markdown("---")
                    st.markdown("**Productos:**")
                    
                    for item in factura['items']:
                        st.markdown(f"• {item['nombre']}: ${item['precio']:,.2f}")
                    
                    st.markdown("---")
                    st.markdown(f"**TOTAL:** ${factura['total']:,.2f}")
                    st.markdown(f"**Pago:** ${factura['pago']:,.2f}")
                    st.markdown(f"**Cambio:** ${factura['cambio']:,.2f}")
                    
                    if st.button("❌ Cerrar", key="cerrar_modal"):
                        st.session_state.modal_factura = None
                        st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No hay facturas registradas hoy")
    
    # ===== PESTAÑA 2: REPORTE MENSUAL =====
    with tab2:
        col_mes, col_btn2 = st.columns([3, 1])
        with col_mes:
            mes = st.date_input("Seleccionar mes", value=date.today(), key="fecha_mensual_reporte")
        with col_btn2:
            st.write("")
            st.write("")
            generar_mensual = st.button("📊 Generar Reporte Mensual", key="btn_mensual", use_container_width=True)
        
        if generar_mensual:
            with st.spinner("Generando reporte mensual..."):
                primer_dia = date(mes.year, mes.month, 1)
                if mes.month == 12:
                    ultimo_dia = date(mes.year + 1, 1, 1) - timedelta(days=1)
                else:
                    ultimo_dia = date(mes.year, mes.month + 1, 1) - timedelta(days=1)
                
                # Filtrar facturas del mes
                facturas_mes = [f for f in facturas if primer_dia <= datetime.strptime(f['fecha'], '%Y-%m-%d').date() <= ultimo_dia]
                
                reporte_mensual = f"REPORTE MENSUAL - {mes.strftime('%B %Y')}\n"
                reporte_mensual += "=" * 50 + "\n\n"
                
                total_mes = 0
                ventas_mes = 0
                
                for factura in facturas_mes:
                    reporte_mensual += f"Factura #{factura['numero']} - {factura['hora']} - ${factura['total']:,.2f}\n"
                    total_mes += factura['total']
                    ventas_mes += 1
                
                reporte_mensual += "\n" + "=" * 50 + "\n"
                reporte_mensual += f"RESUMEN MENSUAL:\n"
                reporte_mensual += f"Total del mes: ${total_mes:,.2f}\n"
                reporte_mensual += f"Facturas: {ventas_mes}\n"
                
                st.markdown(f'<div class="report-box">{reporte_mensual}</div>', unsafe_allow_html=True)
                
                carpeta_base = "informes"
                carpeta_mensuales = os.path.join(carpeta_base, "mensuales")
                os.makedirs(carpeta_mensuales, exist_ok=True)
                
                nombre_archivo = f"{mes.year}-{mes.month:02d}.txt"
                ruta_completa = os.path.join(carpeta_mensuales, nombre_archivo)
                
                with open(ruta_completa, 'w', encoding='utf-8') as f:
                    f.write(reporte_mensual)
                
                st.success(f"✅ Reporte guardado en: informes/mensuales/")
                
                # Botón de descarga con KEY ÚNICO
                st.download_button(
                    label="📥 Descargar Reporte Mensual",
                    data=reporte_mensual,
                    file_name=nombre_archivo,
                    mime="text/plain",
                    key=f"download_mensual_{mes.year}_{mes.month}"
                )
    
    # ===== PESTAÑA 3: VER INFORMES GUARDADOS =====
    with tab3:
        st.markdown("### 📂 Informes Guardados")
        carpeta_base = "informes"
        
        if os.path.exists(carpeta_base):
            col_diarios, col_mensuales = st.columns(2)
            
            with col_diarios:
                st.markdown("#### 📅 Informes Diarios")
                carpeta_diarios = os.path.join(carpeta_base, "diarios")
                if os.path.exists(carpeta_diarios):
                    archivos = sorted(os.listdir(carpeta_diarios), reverse=True)
                    if archivos:
                        seleccion = st.selectbox("Seleccionar:", archivos, key="sel_diario_informe")
                        if seleccion:
                            with open(os.path.join(carpeta_diarios, seleccion), 'r', encoding='utf-8') as f:
                                contenido = f.read()
                                st.markdown(f'<div class="report-box">{contenido}</div>', unsafe_allow_html=True)
                                
                                # Botón con KEY ÚNICO usando el nombre del archivo
                                st.download_button(
                                    label="📥 Descargar",
                                    data=contenido,
                                    file_name=seleccion,
                                    mime="text/plain",
                                    key=f"download_diario_{seleccion.replace('.', '_')}"
                                )
                    else:
                        st.info("No hay informes diarios")
                else:
                    st.info("No hay informes diarios")
            
            with col_mensuales:
                st.markdown("#### 📆 Informes Mensuales")
                carpeta_mensuales = os.path.join(carpeta_base, "mensuales")
                if os.path.exists(carpeta_mensuales):
                    archivos = sorted(os.listdir(carpeta_mensuales), reverse=True)
                    if archivos:
                        seleccion = st.selectbox("Seleccionar:", archivos, key="sel_mensual_informe")
                        if seleccion:
                            with open(os.path.join(carpeta_mensuales, seleccion), 'r', encoding='utf-8') as f:
                                contenido = f.read()
                                st.markdown(f'<div class="report-box">{contenido}</div>', unsafe_allow_html=True)
                                
                                # Botón con KEY ÚNICO usando el nombre del archivo
                                st.download_button(
                                    label="📥 Descargar",
                                    data=contenido,
                                    file_name=seleccion,
                                    mime="text/plain",
                                    key=f"download_mensual_{seleccion.replace('.', '_')}"
                                )
                    else:
                        st.info("No hay informes mensuales")
                else:
                    st.info("No hay informes mensuales")
        else:
            st.info("No hay informes guardados aún")

# ⚠️ STOCK BAJO - CORREGIDO CON VISUALIZACIÓN DE PEDIDOS
elif menu == "⚠️ Stock Bajo":
    st.markdown("<h2 style='color: #2c3e50;'>⚠️ Productos con Stock Bajo</h2>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📝 Generar Pedido", "📂 Ver Pedidos Guardados"])
    
    # ===== PESTAÑA 1: GENERAR PEDIDO =====
    with tab1:
        limite = st.slider("Límite de stock mínimo", 1, 50, 10, key="limite_stock")
        incluir_cero = st.checkbox("Incluir productos con stock 0", value=True, key="incluir_cero")
        
        with st.spinner("Verificando inventario..."):
            # Obtener productos con stock bajo
            bajos = sistema['inventario'].verificar_stock_bajo(limite)
            productos_con_codigo = []
            
            for producto in bajos:
                resultados = sistema['inventario'].buscar_producto(nombre=producto[0])
                if resultados:
                    codigo = resultados[0][1]
                    precio_compra = resultados[0][5]
                    productos_con_codigo.append((producto[0], producto[1], producto[2], codigo, precio_compra))
                else:
                    productos_con_codigo.append((producto[0], producto[1], producto[2], "S/C", 0))
            
            if incluir_cero:
                todos = sistema['inventario'].buscar_producto()
                for prod in todos:
                    if prod[7] == 0:
                        existe = any(p[0] == prod[2] for p in productos_con_codigo)
                        if not existe:
                            productos_con_codigo.append((prod[2], 0, prod[6], prod[1], prod[5]))
        
        if productos_con_codigo:
            df = pd.DataFrame(productos_con_codigo, columns=['Producto', 'Stock', 'P.Venta', 'Código', 'P.Compra'])
            df['P.Venta'] = df['P.Venta'].apply(lambda x: f"${x:,.2f}")
            df['P.Compra'] = df['P.Compra'].apply(lambda x: f"${x:,.2f}")
            
            st.dataframe(df[['Código', 'Producto', 'Stock', 'P.Compra', 'P.Venta']], use_container_width=True)
            
            st.markdown("---")
            st.markdown("### 📋 Resumen")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total productos", len(productos_con_codigo))
            with col2:
                critico = sum(1 for p in productos_con_codigo if p[1] < 5)
                st.metric("Stock crítico (<5)", critico)
            with col3:
                cero = sum(1 for p in productos_con_codigo if p[1] == 0)
                st.metric("Stock CERO", cero, delta_color="inverse")
            
            st.markdown("---")
            st.markdown("### 📝 Generar Pedido")
            
            if 'pedido' not in st.session_state:
                st.session_state.pedido = []
            
            for idx, p in enumerate(productos_con_codigo):
                nombre, stock, pv, codigo, pc = p
                with st.container():
                    cols = st.columns([3, 1, 1, 1])
                    with cols[0]:
                        st.write(f"**{nombre}**")
                        st.caption(f"Código: {codigo} | Compra: ${pc:,.2f}")
                    with cols[1]:
                        if stock == 0:
                            st.write("🔴 **AGOTADO**")
                        else:
                            st.write(f"Stock: {stock}")
                    with cols[2]:
                        sugerencia = 10 if stock == 0 else max(limite - stock + 5, 5)
                        cant = st.number_input("Cantidad", min_value=1, value=sugerencia, key=f"cant_{idx}", label_visibility="collapsed")
                    with cols[3]:
                        if st.button("➕ Agregar", key=f"btn_{idx}"):
                            st.session_state.pedido.append({
                                'codigo': codigo, 'nombre': nombre, 'stock_actual': stock,
                                'cantidad_pedido': cant, 'precio_compra': pc
                            })
                            st.success(f"✅ {nombre} agregado")
                            time.sleep(0.5)
                            st.rerun()
            
            if st.session_state.pedido:
                st.markdown("---")
                st.markdown("### 📋 Resumen del Pedido")
                
                df_pedido = pd.DataFrame(st.session_state.pedido)
                st.dataframe(df_pedido[['codigo', 'nombre', 'stock_actual', 'cantidad_pedido', 'precio_compra']])
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🗑️ Vaciar Pedido", key="btn_vaciar_pedido", use_container_width=True):
                        st.session_state.pedido = []
                        st.rerun()
                with col2:
                    if st.button("📥 Generar Pedido", key="btn_generar_pedido", use_container_width=True):
                        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        mes = datetime.now().strftime("%Y-%m")
                        
                        contenido = f"PEDIDO GENERADO - {fecha}\n"
                        contenido += "="*60 + "\n\n"
                        total_u = total_c = 0
                        
                        for item in st.session_state.pedido:
                            contenido += f"Código: {item['codigo']}\n"
                            contenido += f"Producto: {item['nombre']}\n"
                            contenido += f"Stock actual: {item['stock_actual']}\n"
                            contenido += f"Cantidad a pedir: {item['cantidad_pedido']}\n"
                            contenido += f"Precio compra: ${item['precio_compra']:,.2f}\n"
                            contenido += f"Subtotal: ${item['precio_compra'] * item['cantidad_pedido']:,.2f}\n"
                            contenido += "-"*40 + "\n"
                            total_u += item['cantidad_pedido']
                            total_c += item['precio_compra'] * item['cantidad_pedido']
                        
                        contenido += f"\nTOTAL: {len(st.session_state.pedido)} productos, {total_u} unidades\n"
                        contenido += f"COSTO TOTAL: ${total_c:,.2f}"
                        
                        # Guardar en carpeta por mes
                        carpeta_base = "pedidos"
                        carpeta_mes = os.path.join(carpeta_base, mes)
                        os.makedirs(carpeta_mes, exist_ok=True)
                        
                        nombre_archivo = f"pedido_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                        ruta_completa = os.path.join(carpeta_mes, nombre_archivo)
                        
                        with open(ruta_completa, 'w', encoding='utf-8') as f:
                            f.write(contenido)
                        
                        st.success(f"✅ Pedido guardado en carpeta: {carpeta_mes}/")
                        
                        # Botón para descargar
                        st.download_button(
                            label="📥 Descargar Pedido",
                            data=contenido,
                            file_name=nombre_archivo,
                            mime="text/plain",
                            key=f"download_pedido_{datetime.now().timestamp()}"
                        )
        else:
            st.success("✅ No hay productos con stock bajo")
    
    # ===== PESTAÑA 2: VER PEDIDOS GUARDADOS =====
    with tab2:
        st.markdown("### 📂 Pedidos Guardados")
        
        carpeta_base = "pedidos"
        
        if os.path.exists(carpeta_base):
            # Listar meses disponibles
            meses = sorted([d for d in os.listdir(carpeta_base) if os.path.isdir(os.path.join(carpeta_base, d))], reverse=True)
            
            if meses:
                mes_seleccionado = st.selectbox("Seleccionar mes:", meses, key="select_mes_pedido")
                
                if mes_seleccionado:
                    carpeta_mes = os.path.join(carpeta_base, mes_seleccionado)
                    archivos = sorted([f for f in os.listdir(carpeta_mes) if f.endswith('.txt')], reverse=True)
                    
                    if archivos:
                        archivo_seleccionado = st.selectbox("Seleccionar pedido:", archivos, key="select_pedido")
                        
                        if archivo_seleccionado:
                            ruta = os.path.join(carpeta_mes, archivo_seleccionado)
                            with open(ruta, 'r', encoding='utf-8') as f:
                                contenido = f.read()
                                
                                st.markdown(f'<div class="report-box">{contenido}</div>', unsafe_allow_html=True)
                                
                                st.download_button(
                                    label="📥 Descargar Pedido",
                                    data=contenido,
                                    file_name=archivo_seleccionado,
                                    mime="text/plain",
                                    key=f"download_ver_pedido_{archivo_seleccionado.replace('.', '_')}"
                                )
                    else:
                        st.info(f"No hay pedidos en {mes_seleccionado}")
            else:
                st.info("No hay carpetas de pedidos")
        else:
            st.info("No hay pedidos guardados aún")

# 👥 PROVEEDORES (se mantiene igual pero con mejor estilo visual)
elif menu == "👥 Proveedores":
    st.markdown("<h2 style='color: #2c3e50;'>👥 Gestión de Proveedores</h2>", unsafe_allow_html=True)
    
    proveedores = cargar_proveedores()
    tab1, tab2 = st.tabs(["📋 Ver Proveedores", "➕ Registrar Nuevo"])
    
    with tab1:
        if proveedores:
            st.markdown(f"### Total: {len(proveedores)} proveedores")
            for idx, p in enumerate(proveedores):
                with st.expander(f"🏢 {p['nombre']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**NIT:** {p.get('nit', 'N/A')}")
                        st.markdown(f"**Contacto:** {p.get('contacto', 'N/A')}")
                        st.markdown(f"**Teléfono:** {p.get('telefono', 'N/A')}")
                    with col2:
                        st.markdown(f"**Email:** {p.get('email', 'N/A')}")
                        st.markdown(f"**Dirección:** {p.get('direccion', 'N/A')}")
                        st.markdown(f"**Días pedido:** {p.get('dias_pedido', 'N/A')}")
                    st.markdown(f"**Notas:** {p.get('notas', 'Sin notas')}")
                    
                    col_e, col_d = st.columns(2)
                    with col_e:
                        if st.button("✏️ Editar", key=f"edit_{idx}"):
                            st.session_state.editando_proveedor = idx
                            st.rerun()
                    with col_d:
                        if st.button("🗑️ Eliminar", key=f"del_{idx}"):
                            if st.checkbox(f"Confirmar", key=f"conf_{idx}"):
                                proveedores.pop(idx)
                                guardar_proveedores(proveedores)
                                st.success("✅ Eliminado")
                                time.sleep(1)
                                st.rerun()
            
            if 'editando_proveedor' in st.session_state:
                i = st.session_state.editando_proveedor
                prov = proveedores[i]
                with st.form("edit_prov"):
                    st.text_input("Nombre", value=prov['nombre'], key="edit_nombre")
                    st.text_input("NIT", value=prov.get('nit',''), key="edit_nit")
                    st.text_input("Contacto", value=prov.get('contacto',''), key="edit_contacto")
                    st.text_input("Teléfono", value=prov.get('telefono',''), key="edit_tel")
                    st.text_input("Email", value=prov.get('email',''), key="edit_email")
                    st.text_input("Dirección", value=prov.get('direccion',''), key="edit_dir")
                    st.text_input("Días pedido", value=prov.get('dias_pedido',''), key="edit_dias")
                    st.text_area("Notas", value=prov.get('notas',''), key="edit_notas")
                    
                    col_s, col_c = st.columns(2)
                    with col_s:
                        if st.form_submit_button("💾 Guardar"):
                            proveedores[i] = {
                                'nombre': st.session_state.edit_nombre,
                                'nit': st.session_state.edit_nit,
                                'contacto': st.session_state.edit_contacto,
                                'telefono': st.session_state.edit_tel,
                                'email': st.session_state.edit_email,
                                'direccion': st.session_state.edit_dir,
                                'dias_pedido': st.session_state.edit_dias,
                                'notas': st.session_state.edit_notas
                            }
                            guardar_proveedores(proveedores)
                            del st.session_state.editando_proveedor
                            st.success("✅ Actualizado")
                            time.sleep(1)
                            st.rerun()
                    with col_c:
                        if st.form_submit_button("❌ Cancelar"):
                            del st.session_state.editando_proveedor
                            st.rerun()
        else:
            st.info("No hay proveedores registrados")
    
    with tab2:
        with st.form("nuevo_prov"):
            col1, col2 = st.columns(2)
            with col1:
                nombre = st.text_input("Nombre *")
                nit = st.text_input("NIT")
                contacto = st.text_input("Contacto")
                telefono = st.text_input("Teléfono")
            with col2:
                email = st.text_input("Email")
                direccion = st.text_input("Dirección")
                dias = st.text_input("Días de pedido")
                notas = st.text_area("Notas")
            
            if st.form_submit_button("✅ Registrar"):
                if nombre:
                    proveedores.append({
                        'nombre': nombre, 'nit': nit, 'contacto': contacto,
                        'telefono': telefono, 'email': email, 'direccion': direccion,
                        'dias_pedido': dias, 'notas': notas
                    })
                    guardar_proveedores(proveedores)
                    st.success(f"✅ {nombre} registrado")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Nombre obligatorio")

# 📝 EDITAR/ELIMINAR PRODUCTOS (con eliminación real de BD)
elif menu == "📝 Editar/Eliminar Productos":
    st.markdown("<h2 style='color: #2c3e50;'>📝 Editar o Eliminar Productos</h2>", unsafe_allow_html=True)
    
    busqueda = st.text_input("Buscar producto por nombre o código", key="buscar_eliminar")
    
    if busqueda:
        with st.spinner("Buscando..."):
            if busqueda.isdigit():
                resultados = sistema['inventario'].buscar_producto(codigo_barras=busqueda)
            else:
                resultados = sistema['inventario'].buscar_producto(nombre=busqueda)
        
        if resultados:
            st.success(f"✅ {len(resultados)} encontrado(s)")
            for idx, prod in enumerate(resultados):
                with st.expander(f"📦 {prod[2]} (Stock: {prod[7]})"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**ID:** {prod[0]}")
                        st.markdown(f"**Código:** {prod[1]}")
                        st.markdown(f"**Nombre:** {prod[2]}")
                        st.markdown(f"**Laboratorio:** {prod[9]}")
                    with col2:
                        st.markdown(f"**Compra:** ${prod[5]:,.2f}")
                        st.markdown(f"**Venta:** ${prod[6]:,.2f}")
                        st.markdown(f"**Stock:** {prod[7]}")
                        st.markdown(f"**Vence:** {prod[8] or 'N/A'}")
                    
                    col_e, col_d = st.columns(2)
                    with col_e:
                        if st.button("✏️ Editar", key=f"edit_{idx}_{prod[0]}"):
                            st.session_state.editando = prod
                            st.rerun()
                    with col_d:
                        if st.button("🗑️ Eliminar", key=f"del_{idx}_{prod[0]}"):
                            st.session_state.eliminar = prod
                            st.rerun()
            
            # Eliminación real
            if 'eliminar' in st.session_state:
                prod = st.session_state.eliminar
                st.markdown("---")
                st.warning(f"¿Eliminar '{prod[2]}' permanentemente?")
                col_s, col_n = st.columns(2)
                with col_s:
                    if st.button("✅ Sí, Eliminar", key="btn_confirmar_eliminar"):
                        try:
                            from database import FarmaciaDB
                            db = FarmaciaDB()
                            with db.get_connection() as conn:
                                cursor = conn.cursor()
                                cursor.execute("DELETE FROM productos WHERE id = ?", (prod[0],))
                                conn.commit()
                                if cursor.rowcount > 0:
                                    st.success(f"✅ Producto eliminado")
                                    time.sleep(2)
                                    del st.session_state.eliminar
                                    st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error: {e}")
                with col_n:
                    if st.button("❌ No", key="btn_cancelar_eliminar"):
                        del st.session_state.eliminar
                        st.rerun()
        else:
            st.warning("No se encontraron productos")

# 📋 HISTORIAL DE COMPRAS (NUEVO)
elif menu == "📋 Historial de Compras":
    st.markdown("<h2 style='color: #2c3e50;'>📋 Historial de Compras</h2>", unsafe_allow_html=True)
    
    compras = cargar_compras()
    
    if compras:
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            proveedores = list(set(c.get('proveedor', '') for c in compras if c.get('proveedor')))
            proveedor_filtro = st.selectbox("Filtrar por proveedor", ["Todos"] + proveedores, key="filtro_proveedor")
        with col2:
            meses = list(set(c['fecha_compra'][:7] for c in compras))
            mes_filtro = st.selectbox("Filtrar por mes", ["Todos"] + sorted(meses, reverse=True), key="filtro_mes")
        
        # Aplicar filtros
        compras_filtradas = compras
        if proveedor_filtro != "Todos":
            compras_filtradas = [c for c in compras_filtradas if c.get('proveedor') == proveedor_filtro]
        if mes_filtro != "Todos":
            compras_filtradas = [c for c in compras_filtradas if c['fecha_compra'][:7] == mes_filtro]
        
        # Mostrar tabla
        df = pd.DataFrame(compras_filtradas)
        if not df.empty:
            df = df[['fecha_compra', 'nombre_producto', 'cantidad', 'precio_compra', 'proveedor', 'numero_factura']]
            df['precio_compra'] = df['precio_compra'].apply(lambda x: f"${x:,.2f}")
            df.columns = ['Fecha', 'Producto', 'Cantidad', 'P.Compra', 'Proveedor', 'Factura']
            st.dataframe(df, use_container_width=True)
            
            # Totales
            total_compras = len(compras_filtradas)
            total_unidades = sum(c['cantidad'] for c in compras_filtradas)
            total_invertido = sum(c['precio_compra'] * c['cantidad'] for c in compras_filtradas)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total compras", total_compras)
            with col2:
                st.metric("Unidades compradas", total_unidades)
            with col3:
                st.metric("Total invertido", f"${total_invertido:,.2f}")
        else:
            st.info("No hay compras con esos filtros")
    else:
        st.info("No hay compras registradas")

# ❌ SALIR
elif menu == "❌ Salir":
    st.markdown("""
        <div style="text-align: center; padding: 4rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px;">
            <h1 style="color: white;">👋 ¡Hasta luego!</h1>
            <p style="color: rgba(255,255,255,0.9); font-size: 1.2rem;">Gracias por usar el sistema</p>
            <p style="color: rgba(255,255,255,0.7);">💊 Farmacia La Esperanza</p>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🔒 Cerrar sesión", key="btn_salir"):
        st.stop()