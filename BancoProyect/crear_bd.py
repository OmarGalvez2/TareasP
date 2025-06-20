import sqlite3

def crear_bd():
    conexion = sqlite3.connect('banco.db')
    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        usuario TEXT NOT NULL UNIQUE,
        hash_contrasena TEXT NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cuentas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER NOT NULL,
        numero_cuenta TEXT NOT NULL UNIQUE,
        tipo_cuenta TEXT NOT NULL,
        saldo REAL NOT NULL DEFAULT 0.0,
        FOREIGN KEY (id_cliente) REFERENCES clientes(id)
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transacciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cuenta_origen INTEGER,
        id_cuenta_destino INTEGER,
        monto REAL NOT NULL,
        tipo_transaccion TEXT NOT NULL,
        fecha_hora TEXT NOT NULL,
        FOREIGN KEY (id_cuenta_origen) REFERENCES cuentas(id),
        FOREIGN KEY (id_cuenta_destino) REFERENCES cuentas(id)
    )""")

    conexion.commit()
    conexion.close()
    print("🗃️ Base de datos creada con éxito.")

if __name__ == "__main__":
    crear_bd()
