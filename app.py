import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf
import io
import os
from auth import login_user, register_user
from database import init_db
from PIL import Image  # Necesitamos PIL para cargar la imagen
import auth
from database import init_db

# Inicializar BD al iniciar la app
init_db()
auth.authenticate()
# Configuración de página
st.set_page_config(page_title="CreditHouse", layout="wide")

# Mostrar logo en la parte superior de la barra lateral
try:
    logo = Image.open("assets/logo.png")  # Asegúrate de que el logo esté en la carpeta assets/
    st.sidebar.image(logo, use_container_width=True)
except Exception:
    # Si la imagen no existe, no rompemos la app
    st.sidebar.write("Logo (assets/logo.png no encontrado)")

# Títulos y botones en la barra lateral con claves únicas
st.sidebar.title("Simulador Hipotecario Mi Vivienda")
st.sidebar.markdown("### Menú Principal")

# Inicializar page en session_state si no existe
if "page" not in st.session_state:
    st.session_state["page"] = "inicio"  # página por defecto

# Crear botones de navegación (cada botón pone la "page")
user_email = st.session_state.get('email', 'default')

if st.sidebar.button("Inicio", key=f"inicio_button_{user_email}"):
    st.session_state["page"] = "inicio"

if st.sidebar.button("Perfil", key=f"perfil_button_{user_email}"):
    st.session_state["page"] = "perfil"

if st.sidebar.button("Clientes", key=f"clientes_button_{user_email}"):
    st.session_state["page"] = "clientes"

if st.sidebar.button("Simulador Hipotecario", key=f"simulador_button_{user_email}"):
    st.session_state["page"] = "simulador"

if st.sidebar.button("Letras", key=f"letras_button_{user_email}"):
    st.session_state["page"] = "letras"

# Botón cerrar sesión en sidebar (global)
if st.sidebar.button("Cerrar sesión", key=f"cerrar_sesion_button_{user_email}"):
    st.session_state.clear()
    st.experimental_rerun()

# Manejo de sesión (login)
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["nombre"] = ""

# === AUTENTICACIÓN ===
def login_screen():
    st.title("Iniciar Sesión")

    email = st.text_input("Correo Electrónico")
    password = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        if login_user(email, password):
            st.session_state["logged_in"] = True
            st.session_state["email"] = email
            st.session_state["nombre"] = email.split('@')[0]  # Suponiendo que el nombre es el correo antes del '@'
            st.success(f"Bienvenido, {email}!")
            st.experimental_rerun()  # Vuelve a cargar la app después del login
        else:
            st.error("Usuario o contraseña incorrectos")

def register_screen():
    st.title("Crear Cuenta")

    email = st.text_input("Correo Electrónico")
    password = st.text_input("Contraseña", type="password")
    confirm_password = st.text_input("Confirmar Contraseña", type="password")

    if st.button("Registrarse"):
        if password == confirm_password:
            if register_user(email, password):
                st.success("Cuenta creada con éxito. Ahora inicia sesión.")
                st.session_state["show_register"] = False
                st.experimental_rerun()
            else:
                st.error("Este correo ya está registrado.")
        else:
            st.error("Las contraseñas no coinciden.")

    if st.button("Volver al login"):
        st.session_state["show_register"] = False
        st.experimental_rerun()

# Si no está logeado → mostrar login/registro y detener ejecución
if st.session_state["logged_in"] is False:
    if st.session_state.get("show_register"):
        register_screen()
    else:
        login_screen()
    st.stop()

# Si está logeado → Zona privada
st.sidebar.title(f"Bienvenido, {st.session_state['nombre']}")

# Contenido de cada página (solo se mostrará lo que corresponda)
page = st.session_state.get("page", "inicio")

# -------------------- Página: INICIO --------------------
if page == "inicio":
    st.title("Bienvenido a CreditHouse")

    st.markdown("""
        ## ¿Qué es CreditHouse?
        CreditHouse es una herramienta tecnológica diseñada para pequeñas y medianas empresas, facilitando la gestión de cobranza mediante el descuento de letras y facturas.
        Nuestro objetivo es ayudar a las empresas a mejorar su flujo de caja y tomar decisiones financieras informadas, con un enfoque en el cálculo de la Tasa de Costo Efectivo Anual (TCEA).
    """)
    
    st.markdown("""
        ## Ofrecemos lo siguiente:
        - **Gestión de letras y facturas**
        - **Cálculo de la Tasa de Costo Efectivo Anual (TCEA)**
        - **Descuento de letras y facturas**
        - **Información sobre seguros de gravamen**
    """)
    
    st.markdown("""
        ### Seguros de Gravamen
        Ofrecemos información sobre los seguros de gravamen que distintas entidades financieras ofrecen:
    """)

    # Crear una fila con las tarjetas de las entidades financieras
    col1, col2, col3 = st.columns(3)
    with col1:
        try:
            st.image("assets/bcp.png", caption="BCP", width=150)
        except:
            st.write("BCP")
        st.markdown("**Tasa de Seguro: 0.16%**")
    with col2:
        try:
            st.image("assets/bbva.png", caption="BBVA", width=150)
        except:
            st.write("BBVA")
        st.markdown("**Tasa de Seguro: 0.25%**")
    with col3:
        try:
            st.image("assets/scotiabank.png", caption="Scotiabank", width=150)
        except:
            st.write("Scotiabank")
        st.markdown("**Tasa de Seguro: 0.25%**")
    
    st.markdown("[Ver más detalles sobre seguros](#)")

# -------------------- Página: PERFIL --------------------
elif page == "perfil":
    st.title("Mi Perfil")
    st.write(f"Nombre: {st.session_state.get('nombre', '')}")
    st.write(f"Usuario: {st.session_state.get('email', '')}")
    if 'rol' in st.session_state:
        st.write(f"Rol: {st.session_state['rol']}")

# -------------------- Página: CLIENTES --------------------
elif page == "clientes":
    st.title("Clientes Registrados")
    st.write("Aquí se mostrará la tabla de clientes registrados (funcionalidad pendiente).")

# -------------------- Página: LETRAS --------------------
elif page == "letras":
    st.title("Letras")
    st.write("Aquí se mostrarán las letras y opciones de descuento (funcionalidad pendiente).")

# -------------------- Página: SIMULADOR HIPOTECARIO --------------------
elif page == "simulador":
    # ===========================
    # TODO: TODO: TODO
    # Todo lo referente al simulador va solamente dentro de este bloque.
    # ===========================
    st.title("Simulador Hipotecario - Nuevo Crédito Mi Vivienda")

    # --- Configuración por entidad financiera ---
    BANCOS_CONFIG = {
        "BCP": {
            "valor_vivienda_min": 68800,
            "valor_vivienda_max": 488800,
            "cuota_inicial_min_rango1": 7.5,
            "cuota_inicial_min_rango2": 10.0,
            "plazo_min": 60,
            "plazo_max": 300,
            "tasa_min": 7.49,
            "tasa_max": 9.99,
            "seguro_desgravamen": 0.055,
            "seguro_riesgo": 0.028,
            "costos_iniciales": 1500,
            "portes": 25,
            "descripcion": "Tasas desde 7.49% - 9.99% TEA"
        },
        "BBVA": {
            "valor_vivienda_min": 68800,
            "valor_vivienda_max": 450000,
            "cuota_inicial_min_rango1": 10.0,
            "cuota_inicial_min_rango2": 10.0,
            "plazo_min": 84,
            "plazo_max": 300,
            "tasa_min": 7.90,
            "tasa_max": 10.50,
            "seguro_desgravamen": 0.060,
            "seguro_riesgo": 0.030,
            "costos_iniciales": 1800,
            "portes": 30,
            "descripcion": "Tasas desde 7.90% - 10.50% TEA"
        },
        "Interbank": {
            "valor_vivienda_min": 68800,
            "valor_vivienda_max": 488800,
            "cuota_inicial_min_rango1": 7.5,
            "cuota_inicial_min_rango2": 10.0,
            "plazo_min": 60,
            "plazo_max": 300,
            "tasa_min": 7.99,
            "tasa_max": 10.99,
            "seguro_desgravamen": 0.058,
            "seguro_riesgo": 0.029,
            "costos_iniciales": 1600,
            "portes": 28,
            "descripcion": "Tasas desde 7.99% - 10.99% TEA"
        },
        "Scotiabank": {
            "valor_vivienda_min": 68800,
            "valor_vivienda_max": 488800,
            "cuota_inicial_min_rango1": 7.5,
            "cuota_inicial_min_rango2": 10.0,
            "plazo_min": 60,
            "plazo_max": 300,
            "tasa_min": 7.75,
            "tasa_max": 10.25,
            "seguro_desgravamen": 0.056,
            "seguro_riesgo": 0.027,
            "costos_iniciales": 1700,
            "portes": 26,
            "descripcion": "Tasas desde 7.75% - 10.25% TEA"
        },
        "Banco de la Nación": {
            "valor_vivienda_min": 68800,
            "valor_vivienda_max": 362100,
            "cuota_inicial_min_rango1": 10.0,
            "cuota_inicial_min_rango2": 10.0,
            "plazo_min": 60,
            "plazo_max": 240,
            "tasa_min": 6.99,
            "tasa_max": 8.99,
            "seguro_desgravamen": 0.050,
            "seguro_riesgo": 0.025,
            "costos_iniciales": 1200,
            "portes": 20,
            "descripcion": "Tasas desde 6.99% - 8.99% TEA"
        },
        "Mibanco": {
            "valor_vivienda_min": 68800,
            "valor_vivienda_max": 362100,
            "cuota_inicial_min_rango1": 10.0,
            "cuota_inicial_min_rango2": 10.0,
            "plazo_min": 60,
            "plazo_max": 240,
            "tasa_min": 8.50,
            "tasa_max": 11.50,
            "seguro_desgravamen": 0.062,
            "seguro_riesgo": 0.032,
            "costos_iniciales": 1400,
            "portes": 22,
            "descripcion": "Tasas desde 8.50% - 11.50% TEA"
        },
        "Otro banco": {
            "valor_vivienda_min": 68800,
            "valor_vivienda_max": 488800,
            "cuota_inicial_min_rango1": 7.5,
            "cuota_inicial_min_rango2": 10.0,
            "plazo_min": 60,
            "plazo_max": 300,
            "tasa_min": 7.50,
            "tasa_max": 11.50,
            "seguro_desgravamen": 0.055,
            "seguro_riesgo": 0.028,
            "costos_iniciales": 1500,
            "portes": 25,
            "descripcion": "Condiciones referenciales MiVivienda: S/ 68,800 - S/ 488,800 (BBP hasta S/ 362,100)"
        }
    }

    # --- funciones auxiliares ---
    def df_to_excel_bytes(df):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Cronograma')
        output.seek(0)
        return output.getvalue()

    def calcular_bbp(valor_vivienda_soles):
        if 68800 <= valor_vivienda_soles < 98100:
            return 27400.0
        elif 98100 <= valor_vivienda_soles < 146900:
            return 22800.0
        elif 146900 <= valor_vivienda_soles < 244600:
            return 20900.0
        elif 244600 <= valor_vivienda_soles <= 362100:
            return 7800.0
        return 0.0

    def calcular_bono_verde_monto(valor_vivienda, porcentaje):
        return (porcentaje / 100.0) * valor_vivienda

    dias = {"Mensual": 30, "Trimestral": 90, "Semestral": 180, "Anual": 360}

    # --- estado de sesión del simulador (solo si estamos en esta página) ---
    if 'banco_selected' not in st.session_state:
        st.session_state.banco_selected = "Seleccionar..."
    if 'moneda' not in st.session_state:
        st.session_state.moneda = "Seleccionar..."
    if 'incluye_bono' not in st.session_state:
        st.session_state.incluye_bono = "Seleccionar..."
    if 'bono_tipo' not in st.session_state:
        st.session_state.bono_tipo = "Seleccionar..."
    if 'tipo_tasa' not in st.session_state:
        st.session_state.tipo_tasa = "Seleccionar..."
    if 'tipo_pg' not in st.session_state:
        st.session_state.tipo_pg = "Seleccionar..."

    st.markdown(""" 
        <style>
        .main-header {
            font-size: 2.2rem;
            font-weight: bold;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 1.5rem;
        }
        .metric-card {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #1f77b4;
        }
        .warning-box {
            background-color: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 0.3rem;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="main-header">Simulador Hipotecario - Nuevo Crédito MiVivienda</p>', unsafe_allow_html=True)

    st.subheader(" Selección de Entidad Financiera")
    col_banco1, col_banco2 = st.columns([2, 1])
    with col_banco1:
        banco_options = ["Seleccionar..."] + list(BANCOS_CONFIG.keys())
        banco = st.selectbox("Seleccione el banco", banco_options, index=banco_options.index(st.session_state.banco_selected))
        st.session_state.banco_selected = banco

    with col_banco2:
        if st.session_state.banco_selected and st.session_state.banco_selected != "Seleccionar...":
            config = BANCOS_CONFIG[st.session_state.banco_selected]
            st.info(f" {config['descripcion']}")

    # Si no se seleccionó banco, mostramos nota y no continuamos
    if st.session_state.banco_selected and st.session_state.banco_selected != "Seleccionar...":
        config_banco = BANCOS_CONFIG[st.session_state.banco_selected]
        
        st.divider()
        st.subheader(" Datos del Préstamo")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            moneda_options = ["Seleccionar...", "PEN", "USD"]
            moneda = st.selectbox("Moneda", moneda_options, index=moneda_options.index(st.session_state.moneda))
            st.session_state.moneda = moneda

        tipo_cambio = 1.0
        V = None
        V_soles = 0

        if st.session_state.moneda == "USD":
            with col2:
                tipo_cambio = st.number_input(
                    "Tipo de cambio (S/ por USD)",
                    min_value=1.00, max_value=10.00,
                    value=3.75,
                    step=0.01,
                    format="%.4f",
                    help="Ej: 3.75"
                )

        with col3:
            if st.session_state.moneda == "USD":
                if tipo_cambio and tipo_cambio > 0:
                    min_usd = config_banco["valor_vivienda_min"] / tipo_cambio
                    max_usd = config_banco["valor_vivienda_max"] / tipo_cambio
                    
                    V = st.number_input(
                        "Valor de la vivienda (USD)", 
                        min_value=float(min_usd), 
                        max_value=float(max_usd), 
                        value=None if 'V_usd' not in st.session_state else st.session_state.get('V_usd'),
                        step=100.0,
                        placeholder=f"Rango: {min_usd:,.2f} - {max_usd:,.2f}",
                        help=f"Rango del {st.session_state.banco_selected}"
                    )
                    if V:
                        st.session_state['V_usd'] = V
                        V_soles = V * tipo_cambio
                else:
                    st.warning(" Ingrese un tipo de cambio válido primero")
                    V = None
                    V_soles = 0
                    
            elif st.session_state.moneda == "PEN":
                V = st.number_input(
                    "Valor de la vivienda (S/)", 
                    min_value=float(config_banco["valor_vivienda_min"]), 
                    max_value=float(config_banco["valor_vivienda_max"]), 
                    value=None if 'V_pen' not in st.session_state else st.session_state.get('V_pen'),
                    step=1000.0,
                    placeholder="Ingrese valor",
                    help=f"Rango {st.session_state.banco_selected}: S/ {config_banco['valor_vivienda_min']:,.0f} - S/ {config_banco['valor_vivienda_max']:,.0f}"
                )
                if V:
                    st.session_state['V_pen'] = V
                    V_soles = V
                else:
                    V_soles = 0
            else:
                st.info(" Seleccione una moneda para continuar")
                V = None
                V_soles = 0

        with col4:
            if st.session_state.moneda == "USD" and V and V_soles > 0:
                if V_soles > 362100:
                    st.metric("Valor en Soles", f"S/ {V_soles:,.2f}")
                    st.warning(" Sin Bono BBP (>S/ 362,100)")
                else:
                    st.metric("Valor en Soles", f"S/ {V_soles:,.2f}")
                    st.success(" Aplica para Bono BBP")

        col5, col6 = st.columns(2)
        with col5:
            if V_soles > 0:
                # Aplicar la lógica MiVivienda para cuota inicial mínima según rango de valor de la vivienda
                if V_soles <= 244600:
                    min_ci = config_banco["cuota_inicial_min_rango1"]
                    max_financiamiento = 100 - min_ci
                    ci_help = f"Cuota inicial mínima {st.session_state.banco_selected}: {min_ci}% (vivienda hasta S/ 244,600)"
                elif 244600 < V_soles <= 362100:
                    min_ci = config_banco["cuota_inicial_min_rango2"]
                    max_financiamiento = 100 - min_ci
                    ci_help = f"Cuota inicial mínima {st.session_state.banco_selected}: {min_ci}% (vivienda desde S/ 244,601 hasta S/ 362,100)"
                else:
                    min_ci = config_banco.get("cuota_inicial_min_rango2", 10.0)
                    max_financiamiento = 100 - min_ci
                    ci_help = f"Vivienda > S/ 362,100: no aplica Bono BBP. Cuota inicial mínima referencial: {min_ci}%"
            else:
                min_ci = config_banco["cuota_inicial_min_rango1"]
                max_financiamiento = 100 - min_ci
                ci_help = "Ingrese valor de vivienda para calcular cuota inicial mínima"
            
            CI = st.number_input(
                "Cuota inicial (%)", 
                min_value=float(min_ci), 
                max_value=90.0, 
                value=None if 'CI' not in st.session_state else st.session_state.get('CI'),
                step=0.5,
                placeholder=f"Mínimo {min_ci}%",
                help=ci_help
            )
            if CI is not None:
                st.session_state['CI'] = CI
            
            if CI is not None and V_soles > 0:
                financiamiento_solicitado_pct = 100 - CI
                if financiamiento_solicitado_pct > max_financiamiento:
                    st.error(f" Con {CI}% de cuota inicial, financiaría el {financiamiento_solicitado_pct}% (máximo: {max_financiamiento}%)")
                    st.info(f" Aumente a mínimo **{100-max_financiamiento}%**")
                else:
                    st.success(f" Financiamiento: {financiamiento_solicitado_pct}%")
        with col6:
            n_meses = st.number_input(
                "Plazo (meses)", 
                min_value=int(config_banco["plazo_min"]), 
                max_value=int(config_banco["plazo_max"]), 
                value=None if 'n_meses' not in st.session_state else st.session_state.get('n_meses'),
                step=12,
                placeholder=f"{config_banco['plazo_min']}-{config_banco['plazo_max']} meses",
                help=f"Plazo permitido por {st.session_state.banco_selected}"
            )
            if n_meses is not None:
                st.session_state['n_meses'] = n_meses

        st.divider()
        st.subheader(" Configuración de Tasa de Interés")

        col8, col9, col10, col11 = st.columns(4)
        with col8:
            tipo_options = ["Seleccionar...", "TN", "TE"]
            tipo = st.selectbox("Tipo de tasa", tipo_options, index=tipo_options.index(st.session_state.tipo_tasa))
            st.session_state.tipo_tasa = tipo

        with col9:
            tasa = st.number_input(
                "Valor de tasa (%)", 
                min_value=0.0, 
                max_value=50.0, 
                value=None if 'tasa' not in st.session_state else st.session_state.get('tasa'),
                step=0.1,
                placeholder=f"{config_banco['tasa_min']}-{config_banco['tasa_max']}% TEA",
                help=f"Rango referencial {st.session_state.banco_selected}: {config_banco['tasa_min']}-{config_banco['tasa_max']}% TEA"
            )
            if tasa is not None:
                st.session_state['tasa'] = tasa

        with col10:
            if st.session_state.tipo_tasa == "TN":
                freq_options = ["Seleccionar...", "Mensual", "Trimestral", "Semestral", "Anual"]
                freq = st.selectbox("Frecuencia de capitalización (TN)", freq_options, index=0)
                plazo_tasa = "Anual"
            elif st.session_state.tipo_tasa == "TE":
                plazo_options = ["Seleccionar...", "Mensual", "Trimestral", "Semestral", "Anual"]
                plazo_tasa = st.selectbox("Plazo de tasa efectiva (TE)", plazo_options, index=0)
                freq = None
            else:
                freq = None
                plazo_tasa = None

        st.divider()
        st.subheader(" Bonos y Subsidios del Nuevo Crédito MiVivienda")

        col12, col13 = st.columns(2)
        with col12:
            incluye_bono_options = ["Seleccionar...", "No", "Sí"]
            incluye_bono = st.selectbox("¿Incluye bono del FMV?", incluye_bono_options, index=incluye_bono_options.index(st.session_state.incluye_bono))
            st.session_state.incluye_bono = incluye_bono

        bono_tipo = None
        bono_bbp = 0.0
        bono_verde_pct = 0.0
        bono_verde_monto = 0.0

        if st.session_state.incluye_bono == "Sí":
            with col13:
                bono_tipo_options = ["Seleccionar...", "Bono Buen Pagador (BBP)", "Bono Mi Vivienda Verde", "Ambos"]
                bono_tipo = st.radio("Seleccione tipo de bono", bono_tipo_options, index=0)
                if bono_tipo != "Seleccionar...":
                    st.session_state.bono_tipo = bono_tipo
            
            if bono_tipo in ("Bono Buen Pagador (BBP)", "Ambos") and V_soles > 0:
                if V_soles > 362100:
                    st.warning(" El valor de la vivienda (S/ {:,.2f}) excede S/ 362,100. No aplica Bono BBP.".format(V_soles))
                    bono_bbp = 0.0
                else:
                    bono_bbp = calcular_bbp(V_soles)
                    st.success(f" **Bono Buen Pagador calculado:** S/ {bono_bbp:,.2f}")
            
            if bono_tipo in ("Bono Mi Vivienda Verde", "Ambos") and V_soles > 0:
                st.info("🌱 El Bono Mi Vivienda Verde es del 3% o 4% del valor de la vivienda para viviendas sostenibles certificadas.")
                bono_verde_pct = st.number_input(
                    "Porcentaje Bono Mi Vivienda Verde (%)", 
                    min_value=3.0, 
                    max_value=4.0, 
                    value=None,
                    step=0.01, 
                    format="%.2f",
                    placeholder="3.0 - 4.0"
                )
                if bono_verde_pct:
                    bono_verde_monto = calcular_bono_verde_monto(V_soles, bono_verde_pct)
                    st.success(f"🌱 **Bono Verde calculado:** S/ {bono_verde_monto:,.2f}")

        total_bonos = bono_bbp + bono_verde_monto

        if total_bonos > 0:
            st.metric(" Total de Bonos y Subsidios", f"S/ {total_bonos:,.2f}")

        st.divider()
        st.subheader(" Seguros y Costos Adicionales")

        col14, col15, col16, col17 = st.columns(4)
        with col14:
            SD = st.number_input(
                "Seguro Desgravamen (% mensual)", 
                min_value=0.0, 
                max_value=1.0, 
                value=float(config_banco["seguro_desgravamen"]), 
                step=0.001, 
                format="%.3f",
                help=f"Valor típico {st.session_state.banco_selected}"
            )
        with col15:
            SR = st.number_input(
                "Seguro de Riesgo (% mensual)", 
                min_value=0.0, 
                max_value=1.0, 
                value=float(config_banco["seguro_riesgo"]), 
                step=0.001, 
                format="%.3f",
                help=f"Valor típico {st.session_state.banco_selected}"
            )
        with col16:
            CI_ini = st.number_input(
                "Costos iniciales (S/)", 
                min_value=0.0, 
                value=float(config_banco["costos_iniciales"]), 
                step=100.0,
                help=f"Valor típico {st.session_state.banco_selected}: Tasación, registros, etc."
            )
        with col17:
            CM = st.number_input(
                "Portes mensuales (S/)", 
                min_value=0.0, 
                value=float(config_banco["portes"]), 
                step=5.0,
                help=f"Valor típico {st.session_state.banco_selected}"
            )

        st.divider()
        st.subheader("⏸ Periodo de Gracia")
        colg1, colg2 = st.columns(2)
        with colg1:
            tipo_pg_options = ["Seleccionar...", "Sin gracia", "Gracia total", "Gracia parcial"]
            tipo_pg = st.selectbox("Tipo de gracia", tipo_pg_options, index=tipo_pg_options.index(st.session_state.tipo_pg))
            st.session_state.tipo_pg = tipo_pg

        with colg2:
            PG = 0
            if st.session_state.tipo_pg in ("Gracia total", "Gracia parcial"):
                PG = st.number_input(
                    "Meses de gracia", 
                    min_value=0, 
                    max_value=6, 
                    value=0,
                    step=1,
                    help="Máximo 6 meses de gracia"
                )

        # Botón de cálculo
        if st.button(" Calcular Simulación", type="primary", use_container_width=True):
            try:
                errores = []
                
                # Validaciones
                if st.session_state.moneda is None or st.session_state.moneda == "Seleccionar...":
                    errores.append("Seleccione una moneda")
                if V is None or V == 0:
                    errores.append("Ingrese el valor de la vivienda")
                if CI is None:
                    errores.append("Ingrese la cuota inicial")
                else:
                    if V_soles > 0:
                        financiamiento_pct = 100 - CI
                        max_permitido = 92.5 if V_soles <= 244600 else 90.0
                        if financiamiento_pct > max_permitido:
                            errores.append(f"La cuota inicial es insuficiente (mínimo {100-max_permitido}% )")
                if n_meses is None:
                    errores.append("Ingrese el plazo en meses")
                if st.session_state.tipo_tasa is None or st.session_state.tipo_tasa == "Seleccionar...":
                    errores.append("Seleccione el tipo de tasa")
                if 'tasa' not in st.session_state or st.session_state.get('tasa') is None:
                    errores.append("Ingrese el valor de la tasa")
                if st.session_state.tipo_tasa == "TN" and (freq is None or freq == "Seleccionar..."):
                    errores.append("Seleccione la frecuencia de capitalización")
                if st.session_state.tipo_tasa == "TE" and (plazo_tasa is None or plazo_tasa == "Seleccionar..."):
                    errores.append("Seleccione el plazo de tasa efectiva")
                if SD is None:
                    errores.append("Ingrese el seguro desgravamen")
                if SR is None:
                    errores.append("Ingrese el seguro de riesgo")
                if CI_ini is None:
                    errores.append("Ingrese los costos iniciales")
                if CM is None:
                    errores.append("Ingrese los portes mensuales")
                if st.session_state.tipo_pg is None or st.session_state.tipo_pg == "Seleccionar...":
                    errores.append("Seleccione el tipo de gracia")
                
                if errores:
                    st.error("⚠️ Complete los siguientes campos:")
                    for error in errores:
                        st.write(f"• {error}")
                    st.stop()
                
                if V_soles < config_banco["valor_vivienda_min"] or V_soles > config_banco["valor_vivienda_max"]:
                    st.error(f" El valor de la vivienda debe estar entre S/ {config_banco['valor_vivienda_min']:,.0f} y S/ {config_banco['valor_vivienda_max']:,.0f} para {st.session_state.banco_selected}")
                    st.stop()
                
                V_calc = V_soles
                CI_monto = V_calc * (CI / 100.0)
                P = V_calc - CI_monto - total_bonos

                if P <= 0:
                    st.warning(" Los bonos y cuota inicial cubren o superan el valor de la vivienda. No se requiere financiamiento.")
                    st.stop()

                # Cálculo TEM
                if st.session_state.tipo_tasa == "TN":
                    TNA = st.session_state['tasa'] / 100
                    m = {"Mensual": 12, "Trimestral": 4, "Semestral": 2, "Anual": 1}[freq]
                    n = dias["Mensual"] / dias[freq]
                    TEM = (1 + (TNA / m)) ** n - 1
                else:
                    TE = st.session_state['tasa'] / 100
                    if plazo_tasa == "Mensual":
                        TEM = TE
                    else:
                        TEM = (1 + TE) ** (dias["Mensual"] / dias[plazo_tasa]) - 1

                # Periodo de gracia
                if tipo_pg == "Gracia total" and PG > 0:
                    P_used = P * (1 + TEM) ** PG
                    n_used = n_meses
                    inicio_pago_cuota = PG + 1
                elif tipo_pg == "Gracia parcial" and PG > 0:
                    P_used = P
                    n_used = n_meses
                    inicio_pago_cuota = PG + 1
                else:
                    P_used = P
                    n_used = n_meses
                    inicio_pago_cuota = 1

                n_amortizacion = n_meses - PG if PG > 0 else n_meses
                
                if n_amortizacion > 0:
                    if TEM == 0:
                        C = P_used / n_amortizacion
                    else:
                        C = P_used * ((TEM * (1 + TEM) ** n_amortizacion) / (((1 + TEM) ** n_amortizacion) - 1))
                else:
                    C = 0

                meses = list(range(0, n_meses + 1))
                saldo_ini = [0] * (n_meses + 1)
                interes = [0] * (n_meses + 1)
                amort = [0] * (n_meses + 1)
                sdg = [0] * (n_meses + 1)
                sris = [0] * (n_meses + 1)
                cuota = [0] * (n_meses + 1)
                cuota_total = [0] * (n_meses + 1)
                saldo_fin = [0] * (n_meses + 1)

                current_principal = P
                saldo_ini[0] = saldo_fin[0] = current_principal

                for i in range(1, n_meses + 1):
                    saldo_ini[i] = current_principal
                    interes[i] = current_principal * TEM

                    if i <= PG:
                        if tipo_pg == "Gracia total":
                            amort[i] = 0
                            cuota[i] = 0
                            current_principal += interes[i]
                        elif tipo_pg == "Gracia parcial":
                            amort[i] = 0
                            cuota[i] = interes[i]
                    else:
                        cuota[i] = C
                        amort[i] = cuota[i] - interes[i]
                        if amort[i] < 0:
                            amort[i] = 0
                        current_principal -= amort[i]
                        if current_principal < 0.01:
                            current_principal = 0

                    saldo_fin[i] = current_principal
                    sdg[i] = saldo_ini[i] * (SD / 100)
                    sris[i] = saldo_ini[i] * (SR / 100)
                    cuota_total[i] = cuota[i] + sdg[i] + sris[i] + CM

                df = pd.DataFrame({
                    "Mes": meses,
                    "Saldo Inicial": saldo_ini,
                    "Interés": interes,
                    "Amortización": amort,
                    "Cuota": cuota,
                    "Seguro Desgravamen": sdg,
                    "Seguro Riesgo": sris,
                    "Portes": [0] + [CM] * n_meses,
                    "Cuota Total": cuota_total,
                    "Saldo Final": saldo_fin
                })

                flujos = [-CI_ini - CI_monto] + cuota_total[1:]
                
                try:
                    TIR = npf.irr(flujos)
                    TCEA = (1 + TIR) ** 12 - 1 if TIR is not None and TIR > -1 else None
                except:
                    TIR = None
                    TCEA = None
                
                try:
                    VAN = npf.npv(TEM, flujos) if TEM > 0 else sum(flujos)
                except:
                    VAN = None

                st.success(" Simulación calculada exitosamente")
                st.markdown("""
                <style>
                /* Reduce tamaño de los st.metric */
                [data-testid="stMetricValue"] {
              font-size: 18px;   /* valor numérico (antes ~28px) */
                }

                /* Reduce el título del indicador (TCEA, TIR, VAN, etc.) */
                [data-testid="stMetricLabel"] {
               font-size: 14px;
                }

                /* Reduce el delta (si existiera) */
                [data-testid="stMetricDelta"] {
              font-size: 12px;
                }
                </style>
                """, unsafe_allow_html=True)


                st.subheader(" Indicadores Financieros Principales")

                col1, col2, col3, col4, col5, col6 = st.columns(6)

                simbolo = "USD" if st.session_state.moneda == "USD" else "S/"
                monto_display = P / tipo_cambio if st.session_state.moneda == "USD" else P

                col1.metric("Monto Financiado", f"{simbolo} {monto_display:,.2f}")
                col2.metric("Cuota Mensual", f"S/ {C:,.2f}")
                col3.metric("TEM", f"{TEM*100:.4f}%")


                col4.metric("TIR", f"{TIR*100:.4f}%" if TIR is not None else "N/A")


                col5.metric("TCEA", f"{TCEA*100:.2f}%" if TCEA is not None else "N/A")


                col6.metric("VAN", f"S/ {VAN:,.2f}" if VAN is not None else "N/A")

                col5, col6, col7, col8 = st.columns(4)
                total_intereses = sum(interes[1:])
                total_seguros = sum(sdg[1:]) + sum(sris[1:])
                total_pagado = sum(cuota_total[1:]) + CI_ini + CI_monto
                
                col5.metric("Total Intereses", f"S/ {total_intereses:,.2f}")
                col6.metric("Total Seguros", f"S/ {total_seguros:,.2f}")
                col7.metric("Costo Total del Crédito", f"S/ {total_pagado:,.2f}")
                col8.metric("Inversión Inicial", f"S/ {CI_ini + CI_monto:,.2f}")

                st.divider()
                st.subheader(" Resumen de Bonos Aplicados")
                
                if total_bonos > 0:
                    resumen_bonos = {}
                    if bono_bbp > 0:
                        resumen_bonos["Bono Buen Pagador (BBP)"] = f"S/ {bono_bbp:,.2f}"
                    if bono_verde_monto > 0:
                        resumen_bonos["Bono Mi Vivienda Verde"] = f"S/ {bono_verde_monto:,.2f} ({bono_verde_pct}%)"
                    resumen_bonos["**Total Bonos**"] = f"**S/ {total_bonos:,.2f}**"
                    
                    for concepto, valor in resumen_bonos.items():
                        st.write(f"• {concepto}: {valor}")
                else:
                    st.info("No se aplicaron bonos en esta simulación")

                st.divider()
                st.subheader(" Cronograma de Pagos Detallado")
                
                df_display = df.copy()
                for col_name in df_display.columns:
                    if col_name != "Mes":
                        df_display[col_name] = df_display[col_name].apply(lambda x: f"S/ {x:,.2f}")
                
                st.dataframe(df_display, use_container_width=True, height=400)

                excel = df_to_excel_bytes(df)
                st.download_button(
                    label=" Descargar cronograma en Excel",
                    data=excel,
                    file_name=f"cronograma_{st.session_state.banco_selected}_{int(V if V else 0)}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )

                st.divider()
                valor_vivienda_display = f"{simbolo} {V:,.2f}" if V else f"{simbolo} 0.00"
                if st.session_state.moneda == "USD" and V:
                    valor_vivienda_display += f" (S/ {V_soles:,.2f})"
                
                st.info(f"""
                ** Información del Crédito:**
                - Banco: {st.session_state.banco_selected}
                - Moneda: {st.session_state.moneda}
                - Valor vivienda: {valor_vivienda_display}
                - Plazo: {n_meses} meses ({n_meses//12} años)
                - Periodo de gracia: {PG} meses ({tipo_pg})
                """)

            except Exception as e:
                st.error(f" Error en el cálculo: {str(e)}")
                st.exception(e)

    else:
        st.info("Seleccione un banco para comenzar la simulación")

    st.divider()
    st.markdown("""
        <div style='text-align: center; color: #666; padding: 1rem;'>
            <p><strong>Simulador Hipotecario v3.2 - Nuevo Crédito MiVivienda</strong></p>
            <p style='font-size: 0.9rem;'>Sistema con configuración por entidad financiera | 
            Basado en normativa del Fondo MiVivienda 2025</p>
            <p style='font-size: 0.8rem; margin-top: 0.5rem;'>
             Bancos incluidos: BCP, BBVA, Interbank, Scotiabank, Banco de la Nación, Mibanco, Otro banco
            </p>
            <p style='font-size: 0.8rem;'>
             Los valores son referenciales. Consulte con su entidad financiera para condiciones exactas.
            </p>
        </div>
    """, unsafe_allow_html=True)

# -------------------- Página por defecto (fallback) --------------------
else:
    st.write("Página no encontrada. Use el menú lateral para navegar.")
