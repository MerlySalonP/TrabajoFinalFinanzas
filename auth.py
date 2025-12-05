import streamlit as st
import hashlib
from database import get_user, create_user

# =============================
# SEGURIDAD (HASHING)
# =============================
def make_hashes(password):
    """Genera un hash SHA256 de la contraseña."""
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    """Compara una contraseña en texto plano con el hash guardado."""
    if make_hashes(password) == hashed_text:
        return True
    return False

# =============================
# LÓGICA DE NEGOCIO
# =============================

def login_user(username, password):
    """Verifica credenciales y devuelve el usuario si son correctas."""
    user = get_user(username)
    
    # Verificamos si existe el usuario y si el hash coincide
    if user and check_hashes(password, user["password"]):
        return user
    return None

def register_user(username, password, nombre, rol):
    """Intenta registrar un usuario. Devuelve True si éxito, False si falla."""
    if username and password and nombre and rol:
        # Encriptamos la contraseña antes de enviarla a la BD
        hashed_password = make_hashes(password)
        
        # create_user devuelve True o False según si pudo crearlo o no
        return create_user(username, hashed_password, nombre, rol)
    
    return False

# =============================
# COMPONENTES DE INTERFAZ
# =============================

def login_form():
    """Muestra el formulario de login."""
    st.title("🔐 Inicio de Sesión")

    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Ingresar"):
            user = login_user(username, password)
            if user:
                # Guardar sesión
                st.session_state["logged_in"] = True
                st.session_state["username"] = user["username"]
                st.session_state["nombre"] = user["nombre"]
                st.session_state["rol"] = user["rol"]
                st.success(f"Bienvenido {user['nombre']}")
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos")
    
    with col2:
        if st.button("Crear Cuenta Nueva"):
            st.session_state["show_register"] = True
            st.rerun()

def register_form():
    """Muestra el formulario de registro."""
    st.title("📝 Crear Cuenta")

    username = st.text_input("Nuevo Usuario")
    password = st.text_input("Contraseña", type="password")
    confirm_password = st.text_input("Confirmar Contraseña", type="password")
    nombre = st.text_input("Nombre Completo")
    rol = st.selectbox("Rol", ["vendedor", "admin"]) # Ajustado a los roles de tu BD

    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Registrarse"):
            if password != confirm_password:
                st.error("Las contraseñas no coinciden.")
            else:
                if register_user(username, password, nombre, rol):
                    st.success("Cuenta creada con éxito. Por favor inicia sesión.")
                    st.session_state["show_register"] = False # Volver al login
                    st.rerun()
                else:
                    st.error("Error: El usuario ya existe o faltan datos.")
    
    with col2:
        if st.button("Volver al Login"):
            st.session_state["show_register"] = False
            st.rerun()

# =============================
# FUNCIÓN PRINCIPAL DE AUTENTICACIÓN
# =============================

def authenticate():
    """
    Función maestra que gestiona el flujo de autenticación.
    Si el usuario NO está logueado, muestra Login/Registro y detiene la app (st.stop).
    Si el usuario ESTÁ logueado, muestra el Sidebar y permite continuar.
    """
    # 1. Si no hay estado de login, inicializarlo
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    # 2. Si NO está logueado, mostrar pantallas de acceso
    if not st.session_state["logged_in"]:
        if st.session_state.get("show_register", False):
            register_form()
        else:
            login_form()
        st.stop() # DETIENE la ejecución de app.py aquí hasta que se loguee

    # 3. Si ESTÁ logueado, mostrar Sidebar con Logout
    if st.session_state["logged_in"]:
        with st.sidebar:
            st.write(f"👤 **{st.session_state['nombre']}**")
            st.write(f"🛠️ Rol: {st.session_state['rol']}")
            if st.button("Cerrar Sesión"):
                st.session_state.clear()
                st.rerun()