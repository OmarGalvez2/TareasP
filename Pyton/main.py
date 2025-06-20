# main.py
from biblioteca import Biblioteca

def mostrar_menu():
    print("\n--- Sistema de Gestión de Biblioteca ---")
    print("1. Agregar un nuevo libro")
    print("2. Registrar un nuevo socio")
    print("3. Prestar un libro")
    print("4. Devolver un libro")
    print("5. Consultar catálogo de libros")
    print("6. Salir")
    print("--------------------------------------")

def main():
    mi_biblioteca = Biblioteca()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            titulo = input("Ingrese el título del libro: ")
            autor = input("Ingrese el autor del libro: ")
            isbn = input("Ingrese el ISBN del libro: ")
            mi_biblioteca.agregar_libro(titulo, autor, isbn)

        elif opcion == '2':
            nombre = input("Ingrese el nombre del socio: ")
            id_socio = input("Ingrese el ID del socio (ej. S001): ")
            mi_biblioteca.registrar_socio(nombre, id_socio)

        elif opcion == '3':
            isbn = input("Ingrese el ISBN del libro a prestar: ")
            id_socio = input("Ingrese el ID del socio: ")
            mi_biblioteca.prestar_libro(isbn, id_socio)

        elif opcion == '4':
            isbn = input("Ingrese el ISBN del libro a devolver: ")
            mi_biblioteca.devolver_libro(isbn)

        elif opcion == '5':
            mi_biblioteca.consultar_libros()

        elif opcion == '6':
            print("Saliendo del sistema... ¡Hasta pronto!")
            mi_biblioteca.cerrar_conexion()
            break

        else:
            print("❌ Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()