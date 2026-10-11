import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Calculadora 3D", page_icon="🖨️", layout="centered")

st.title("🖨️ Calculadora de Costos 3D")
st.caption("Modo Lote Indestructible")

# 1. Configuración Inicial
st.header("1. Configuración")
col1, col2, col3 = st.columns(3)
with col1:
    precio_bobina = st.number_input("Bobina 1kg (S/)", value=65.0, step=1.0)
with col2:
    costo_kwh = st.number_input("Costo kWh (S/)", value=0.85, step=0.01)
with col3:
    margen_ganancia = st.number_input("Ganancia (%)", value=30.0, step=1.0)

consumo_impresora = 0.15 # kW

# 2. Tabla de Piezas
st.header("2. Lista de Piezas")
st.write("Edita la tabla. Para agregar otra pieza, haz clic en el botón '+' o en la última fila.")

# Creamos una tabla inicial vacía si no existe
if 'datos' not in st.session_state:
    st.session_state.datos = pd.DataFrame([
        {"Pieza": "Pieza 1", "Gramos": 0.0, "Horas": 0, "Minutos": 0}
    ])

# Mostramos la tabla editable
df_editado = st.data_editor(st.session_state.datos, num_rows="dynamic", use_container_width=True)

# 3. Botón de Cálculo
if st.button("Calcular Costos", type="primary", use_container_width=True):
    # Filtrar solo las filas donde se hayan ingresado gramos
    df_valido = df_editado[df_editado["Gramos"] > 0]
    num_piezas = len(df_valido)
    
    if num_piezas > 0:
        total_gramos = df_valido["Gramos"].sum()
        total_horas_decimales = df_valido["Horas"].sum() + (df_valido["Minutos"].sum() / 60.0)
        
        # Cálculos matemáticos
        desgaste_total = 1.50 * num_piezas
        costo_material = (precio_bobina / 1000) * total_gramos
        costo_energia = total_horas_decimales * consumo_impresora * costo_kwh
        costo_total_produccion = costo_material + costo_energia + desgaste_total
        
        monto_ganancia = costo_total_produccion * (margen_ganancia / 100)
        precio_venta_final = costo_total_produccion + monto_ganancia
        
        horas_finales = int(total_horas_decimales)
        minutos_finales = int(round((total_horas_decimales - horas_finales) * 60))
        
        # Mostrar los resultados
        st.divider()
        st.subheader("📊 Resumen del Lote")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Piezas", num_piezas)
        c2.metric("Filamento", f"{total_gramos:.2f} g")
        c3.metric("Tiempo", f"{horas_finales}h {minutos_finales}m")
        
        st.write(f"**Costo de Material:** S/ {costo_material:.2f}")
        st.write(f"**Costo de Energía:** S/ {costo_energia:.2f}")
        st.write(f"**Desgaste (x{num_piezas}):** S/ {desgaste_total:.2f}")
        st.write(f"**COSTO DE FÁBRICA:** S/ {costo_total_produccion:.2f}")
        st.write(f"**Ganancia ({margen_ganancia}%):** S/ {monto_ganancia:.2f}")
        
        st.success(f"PRECIO TOTAL A COBRAR: S/ {precio_venta_final:.2f}")
    else:
        st.error("⚠️ Agrega al menos una pieza con peso (gramos) para calcular.")