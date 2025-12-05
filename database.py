import sqlite3
import os

# Ruta de la base de datos
DB_FOLDER = "data"
DB_PATH = os.path.join(DB_FOLDER, "mivivienda.db")

# Crear carpeta /data si no existe
if not os.path.exists(DB_FOLDER):
    os.makedirs(DB_FOLDER)

def get_connection():
    """Conecta a la base de datos y devuelve la conexión."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False) # check_same_thread=False ayuda en entornos web simples
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Crea todas las tablas si no existen."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            
            # Tabla usuarios
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    nombre TEXT NOT NULL,
                    rol TEXT NOT NULL DEFAULT 'vendedor'
                );
            """)

            # Tabla clientes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombres TEXT NOT NULL,
                    apellidos TEXT NOT NULL,
                    dni TEXT UNIQUE NOT NULL,
                    telefono TEXT,
                    email TEXT,
                    ingresos_mensuales REAL,
                    direccion TEXT
                );
            """)
            conn.commit()
    except Exception as e:
        print(f"Error inicializando la BD: {e}")

# =============================
# FUNCIONES USUARIOS
# =============================

def create_user(username, password, nombre, rol="vendedor"):
    """Crea un usuario. Devuelve True si éxito, False si ya existe."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            # NOTA: Aquí deberías hashear la contraseña antes de guardar
            cursor.execute("""
                INSERT INTO usuarios (username, password, nombre, rol)
                VALUES (?, ?, ?, ?);
            """, (username, password, nombre, rol))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        print(f"Error: El usuario '{username}' ya existe.")
        return False
    except Exception as e:
        print(f"Error desconocido creando usuario: {e}")
        return False

def get_user(username):
    """Función para obtener los detalles de un usuario por su username."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
        user = cursor.fetchone()
        return user
    finally:
        conn.close()

# =============================
# FUNCIONES CLIENTES
# =============================

def save_client(cliente_data):
    """Guarda cliente. Devuelve True si éxito, False si DNI duplicado."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO clientes (nombres, apellidos, dni, telefono, email, ingresos_mensuales, direccion)
                VALUES (?, ?, ?, ?, ?, ?, ?);
            """, (
                cliente_data["nombres"], 
                cliente_data["apellidos"], 
                cliente_data["dni"], 
                cliente_data["telefono"], 
                cliente_data["email"], 
                cliente_data["ingresos_mensuales"], 
                cliente_data["direccion"]
            ))
            conn.commit()
            return True
    except sqlite3.IntegrityError:
        print(f"Error: El cliente con DNI '{cliente_data['dni']}' ya existe.")
        return False
    except Exception as e:
        print(f"Error guardando cliente: {e}")
        return False

def get_client(dni):
    """Función para obtener los detalles de un cliente por su DNI."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM clientes WHERE dni = ?", (dni,))
        client = cursor.fetchone()
        return client
    finally:
        conn.close()

# =============================
# INICIALIZACIÓN
# =============================

# Esta lógica se ejecutará solo si llamas a init_db explícitamente o al importar
# He añadido una comprobación extra para no intentar crear al admin si ya existe y fallar.

if not os.path.exists(DB_PATH):
    print("--- Base de datos no encontrada. Inicializando... ---")
    init_db()
    # Intentamos crear el admin
    if create_user("admin", "123456", "Administrador", "admin"):
        print("Usuario admin creado: admin / 123456")
    else:
        print("La base de datos se creó, pero el usuario admin no pudo crearse (quizás ya existía).")
else:
    # Aseguramos que las tablas existan aunque el archivo esté ahí
    init_db()