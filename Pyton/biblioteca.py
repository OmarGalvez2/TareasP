# biblioteca.py
from gestor_bd import GestorBD
from datetime import date

class Biblioteca:
    """
    Clase principal que gestiona las operaciones de la biblioteca.
    Utiliza GestorBD para la persistencia de datos.
    """

    def __init__(self):
        """Inicializa la biblioteca, creando una instancia del gestor de BD."""
        self.db = GestorBD()

    def agregar_libro(self, titulo, autor, isbn):
        """Agrega un nuevo libro a la base de datos."""
        query = "INSERT INTO libros (titulo, autor, isbn) VALUES (?, ?, ?)"
        try:
            self.db.ejecutar_query(query, (titulo, autor, isbn))
            print(f"✅ Libro '{titulo}' agregado correctamente.")
        except Exception as e:
            print(f"❌ Error al agregar el libro: {e}")

    def registrar_socio(self, nombre, id_socio):
        """Registra un nuevo socio en la base de datos."""
        query = "INSERT INTO socios (nombre, id_socio) VALUES (?, ?)"
        try:
            self.db.ejecutar_query(query, (nombre, id_socio))
            print(f"✅ Socio '{nombre}' registrado correctamente.")
        except Exception as e:
            print(f"❌ Error al registrar el socio: {e}")

    def prestar_libro(self, isbn_libro, id_socio):
        """Presta un libro a un socio."""

        # 1. Verificar si el libro existe y está disponible
        libro_query = "SELECT id, disponible FROM libros WHERE isbn = ?"
        libro_res = self.db.seleccionar(libro_query, (isbn_libro,))
        if not libro_res:
            print(f"❌ Error: No se encontró el libro con ISBN {isbn_libro}.")
            return
        id_libro, disponible = libro_res[0]
        if not disponible:
            print(f"❌ Error: El libro '{isbn_libro}' ya está prestado.")
            return

        # 2. Verificar si el socio existe
        socio_query = "SELECT id FROM socios WHERE id_socio = ?"
        socio_res = self.db.seleccionar(socio_query, (id_socio,))
        if not socio_res:
            print(f"❌ Error: No se encontró el socio con ID {id_socio}.")
            return
        id_socio_db = socio_res[0][0]

        # 3. Realizar el préstamo
        try:
            fecha_hoy = date.today().isoformat()
            prestamo_query = "INSERT INTO prestamos (id_libro, id_socio, fecha_prestamo) VALUES (?, ?, ?)"
            self.db.ejecutar_query(prestamo_query, (id_libro, id_socio_db, fecha_hoy))

            update_libro_query = "UPDATE libros SET disponible = 0 WHERE id = ?"
            self.db.ejecutar_query(update_libro_query, (id_libro,))
            print(f"✅ Préstamo realizado: Libro ISBN {isbn_libro} a socio ID {id_socio}.")
        except Exception as e:
            print(f"❌ Error al procesar el préstamo: {e}")

    def devolver_libro(self, isbn_libro):
        """Devuelve un libro, actualizando su estado y el registro del préstamo."""
        libro_query = "SELECT id, disponible FROM libros WHERE isbn = ?"
        libro_res = self.db.seleccionar(libro_query, (isbn_libro,))
        if not libro_res:
            print(f"❌ Error: No se encontró el libro con ISBN {isbn_libro}.")
            return
        id_libro, disponible = libro_res[0]
        if disponible:
            print(f"❌ Error: Este libro no estaba registrado como prestado.")
            return

        update_libro_query = "UPDATE libros SET disponible = 1 WHERE id = ?"
        self.db.ejecutar_query(update_libro_query, (id_libro,))

        fecha_hoy = date.today().isoformat()
        update_prestamo_query = """
        UPDATE prestamos SET fecha_devolucion = ?
        WHERE id_libro = ? AND fecha_devolucion IS NULL
        """
        self.db.ejecutar_query(update_prestamo_query, (fecha_hoy, id_libro))
        print(f"✅ Libro ISBN {isbn_libro} devuelto correctamente.")

    def consultar_libros(self):
        """Muestra todos los libros y su estado."""
        query = "SELECT titulo, autor, isbn, disponible FROM libros"
        libros = self.db.seleccionar(query)
        if not libros:
            print("No hay libros registrados.")
            return

        print("\n--- Catálogo de Libros ---")
        for titulo, autor, isbn, disponible in libros:
            estado = "Disponible" if disponible else "Prestado"
            print(f"'{titulo}' por {autor} (ISBN: {isbn}) - Estado: {estado}")
        print("-------------------------\n")

    def cerrar_conexion(self):
        """Cierra la conexión con la base de datos."""
        self.db.cerrar()
