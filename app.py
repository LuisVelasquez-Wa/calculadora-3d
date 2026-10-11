import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Calculadora 3D Spark i7", page_icon="🖨️", layout="centered")

st.title("🖨️ Calculadora de Costos 3D")
st.caption("Modo Lote Mejorado — Optimizado para Creality Spark i7")

# 1. Configuración Inicial (Inputs visuales en columnas)
st.header("1. Configuración de Costos")
col1, col2 = st.columns(2)
with col1:
    precio_bobina = st.number_input("Precio del rollo de 1kg (S/)", value=70.0, step=1.0)
    precio_mano_obra = st.number_input("Tu hora de trabajo manual (S/)", value=15.0, step=1.0)
with col2:
    costo_kwh = st.number_input("Costo electricidad por kWh (S/)", value=0.85, step=0.01)
    tiempo_mano_obra = st.number_input("Horas totales de tu tiempo (diseño/post-proceso)", value=1.0, step=0.5)

st.subheader("Margen de Ganancia")
margen_ganancia = st.number_input("¿Qué porcentaje de ganancia neta deseas cobrar? (%)", value=50.0, step=5.0)

# Constantes de la máquina Spark i7
consumo_impresora = 0.18  # kW (Promedio real de 180W)
desgaste_por_hora = 0.60  # S/ 0.60 por hora de impresión (Mantenimiento y amortización)

# 2. Tabla de Piezas Editable
st.header("2. Lista de Piezas")
st.write("Edita la tabla inferior. Agrega filas presionando el botón '+' o haciendo doble clic en la última celda.")

# Inicializar estado de la tabla si no existe
if 'datos' not in st.session_state:
    st.session_state.datos = pd.DataFrame([
        {"Pieza": "Pieza 1", "Gramos (Laminador)": 50.0, "Horas": 2, "Minutos": 30}
    ])

# Mostrar la tabla editable en la web
df_editado = st.data_editor(st.session_state.datos, num_rows="dynamic", use_container_width=True)

# 3. Botón de Cálculo de Producción Real
if st.button("Calcular Lote Completo", type="primary", use_container_width=True):
    # Filtrar filas vacías o con gramos en cero
    df_valido = df_editado[df_editado["Gramos (Laminador)"] > 0]
    num_piezas = len(df_valido)
    
    if num_piezas > 0:
        # Sumas de la tabla editada
        total_gramos_netos = df_valido["Gramos (Laminador)"].sum()
        total_horas_decimales = df_valido["Horas"].sum() + (df_valido["Minutos"].sum() / 60.0)
        
        # --- Lógica de Negocio Mejorada ---
        # Multiplicador del 10% por soportes, purgas del sistema multicolor CFS y fallas
        total_gramos_reales = total_gramos_netos * 1.10 
        
        # Cálculos económicos de fábrica
        costo_material = (precio_bobina / 1000) * total_gramos_reales
        costo_energia = total_horas_decimales * consumo_impresora * costo_kwh
        costo_desgaste_maquina = total_horas_decimales * desgaste_por_hora
        costo_mi_tiempo = tiempo_mano_obra * precio_mano_obra
        
        # Costo real acumulado de producción
        costo_total_produccion = costo_material + costo_energia + costo_desgaste_maquina + costo_mi_tiempo
        
        # Aplicación del margen sobre el costo total
        monto_ganancia = costo_total_produccion * (margen_ganancia / 100)
        precio_venta_final = costo_total_produccion + monto_ganancia
        
        # Reconversión de horas para el resumen visual
        horas_finales = int(total_horas_decimales)
        minutos_finales = int(round((total_horas_decimales - horas_finales) * 60))
        
        # --- Renderizado de Resultados ---
        st.divider()
        st.subheader("📊 Resumen Métrico del Lote")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Piezas a Imprimir", num_piezas)
        m2.metric("Filamento Real (+10% Merma)", f"{total_gramos_reales:.2f} g")
        m3.metric("Tiempo de Máquina", f"{horas_finales}h {minutos_finales}m")
        
        st.subheader("📋 Desglose de Costos de Fábrica")
        st.write(f"🔹 **Costo de Filamento:** S/ {costo_material:.2f}")
        st.write(f"🔹 **Costo de Energía Eléctrica:** S/ {costo_energia:.2f}")
        st.write(f"🔹 **Depreciación de Máquina (por hora):** S/ {costo_desgaste_maquina:.2f}")
        st.write(f"🔹 **Costo de tu Mano de Obra:** S/ {costo_mi_tiempo:.2f}")
        
        st.info(f"🏭 **COSTO TOTAL DE PRODUCCIÓN:** S/ {costo_total_produccion:.2f}")
        st.write(f"💵 **Tu Ganancia Neta ({margen_ganancia}%):** S/ {monto_ganancia:.2f}")
        
        st.success(f"💰 PRECIO SUGERIDO A COBRAR: S/ {precio_venta_final:.2f}")
    else:
        st.error("⚠️ Registra al menos una pieza con peso en gramos superior a 0 para procesar el cálculo.")
