# gestor_bd.py
import sqlite3

class GestorBD:
    def __init__(self, db_path='biblioteca.db'):
        """Inicializa la conexión a la base de datos y crea las tablas si no existen."""
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self._crear_tablas()

    def _crear_tablas(self):
        """Crea las tablas necesarias si no existen."""
        schema_sql = """
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            isbn TEXT UNIQUE NOT NULL,
            disponible INTEGER NOT NULL DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS socios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            id_socio TEXT UNIQUE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS prestamos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_libro INTEGER NOT NULL,
            id_socio INTEGER NOT NULL,
            fecha_prestamo TEXT NOT NULL,
            fecha_devolucion TEXT,
            FOREIGN KEY (id_libro) REFERENCES libros(id),
            FOREIGN KEY (id_socio) REFERENCES socios(id)
        );
        """
        self.cursor.executescript(schema_sql)
        self.conn.commit()

    def ejecutar_query(self, query, params=()):
        """
        Ejecuta una consulta (INSERT, UPDATE, DELETE) y guarda los cambios.
        """
        self.cursor.execute(query, params)
        self.conn.commit()
        return self.cursor

    def seleccionar(self, query, params=()):
        """
        Ejecuta una consulta SELECT y devuelve todos los resultados.
        """
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def cerrar(self):
        """Cierra la conexión a la base de datos."""
        self.conn.close()