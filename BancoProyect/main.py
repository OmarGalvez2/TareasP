from banco import Banco

def menu_principal():
    banco = Banco()
    while True:
        print("\n=== Bienvenido a Banca Digital ===")
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            nombre = input("Nombre completo: ")
            usuario = input("Nombre de usuario: ")
            clave = input("Contraseña: ")
            try:
                banco.registrar_cliente(nombre, usuario, clave)
            except Exception as e:
                print("Error:", e)

        elif opcion == "2":
            usuario = input("Usuario: ")
            clave = input("Contraseña: ")
            try:
                cliente = banco.login(usuario, clave)
                menu_cliente(banco, cliente)
            except Exception as e:
                print("Error:", e)

        elif opcion == "3":
            print("Gracias por usar Banca Digital.")
            break

        else:
            print("Opción no válida.")

def menu_cliente(banco, cliente):
    while True:
        print(f"\n=== Menú de {cliente.nombre} ===")
        print("1. Crear cuenta")
        print("2. Ver cuentas")
        print("3. Realizar depósito")
        print("4. Realizar retiro")
        print("5. Transferir entre cuentas")
        print("6. Generar extracto")
        print("7. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            tipo = input("Tipo de cuenta (ahorro, corriente, inversion): ")
            banco.crear_cuenta_para_cliente(cliente, tipo)

        elif opcion == "2":
            banco.mostrar_cuentas(cliente)

        elif opcion == "3":
            banco.realizar_deposito(cliente)

        elif opcion == "4":
            banco.realizar_retiro(cliente)

        elif opcion == "5":
            banco.realizar_transferencia(cliente)

        elif opcion == "6":
            banco.generar_extracto(cliente)

        elif opcion == "7":
            break

        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu_principal()
