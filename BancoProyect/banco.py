import sqlite3
import hashlib
from cliente import Cliente
from datetime import datetime

class BaseDeDatos:
    _instancia = None

    def __init__(self):
        self.conexion = sqlite3.connect('banco.db', check_same_thread=False)
        self.cursor = self.conexion.cursor()

    @classmethod
    def obtener_instancia(cls):
        if not cls._instancia:
            cls._instancia = BaseDeDatos()
        return cls._instancia

    def ejecutar(self, query, params=()):
        self.cursor.execute(query, params)
        self.conexion.commit()

    def consultar(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

class Banco:
    def __init__(self):
        self.bd = BaseDeDatos.obtener_instancia()

    def registrar_cliente(self, nombre, usuario, contraseña):
        if self.buscar_cliente(usuario):
            raise ValueError("Usuario ya existe.")
        hash_pass = hashlib.sha256(contraseña.encode()).hexdigest()
        self.bd.ejecutar(
            "INSERT INTO clientes (nombre, usuario, hash_contrasena) VALUES (?, ?, ?)",
            (nombre, usuario, hash_pass)
        )
        print("✅ Registro exitoso.")

    def login(self, usuario, contraseña):
        resultado = self.bd.consultar(
            "SELECT id, nombre, hash_contrasena FROM clientes WHERE usuario = ?",
            (usuario,)
        )
        if resultado:
            id_cliente, nombre, hash_almacenado = resultado[0]
            hash_ingresado = hashlib.sha256(contraseña.encode()).hexdigest()
            if hash_almacenado == hash_ingresado:
                return Cliente(nombre, usuario, contraseña, id_cliente)
        raise ValueError("Credenciales incorrectas.")

    def buscar_cliente(self, usuario):
        resultado = self.bd.consultar(
            "SELECT * FROM clientes WHERE usuario = ?", (usuario,)
        )
        return resultado[0] if resultado else None

    # Nuevo método para crear cuentas para un cliente
    def crear_cuenta_para_cliente(self, cliente, tipo):
        # Generar número de cuenta simple
        numero = f"{cliente.id}{len(cliente.cuentas) + 1:04d}"
        # Insertar en la BD
        self.bd.ejecutar(
            "INSERT INTO cuentas (id_cliente, numero_cuenta, tipo_cuenta, saldo) VALUES (?, ?, ?, ?)",
            (cliente.id, numero, tipo, 0.0)
        )
        cliente.agregar_cuenta(numero)
        print(f"Cuenta {tipo} creada con número {numero}.")

    def mostrar_cuentas(self, cliente):
        cuentas = self.bd.consultar(
            "SELECT numero_cuenta, tipo_cuenta, saldo FROM cuentas WHERE id_cliente = ?",
            (cliente.id,)
        )
        if not cuentas:
            print("No tienes cuentas.")
            return
        print("Tus cuentas:")
        for c in cuentas:
            print(f"Número: {c[0]}, Tipo: {c[1]}, Saldo: {c[2]}")

    def realizar_deposito(self, cliente):
        numero = input("Número de cuenta para depósito: ")
        monto = float(input("Monto a depositar: "))
        cuenta = self.bd.consultar(
            "SELECT id, saldo FROM cuentas WHERE numero_cuenta = ? AND id_cliente = ?",
            (numero, cliente.id)
        )
        if not cuenta:
            print("Cuenta no encontrada.")
            return
        id_cuenta, saldo_actual = cuenta[0]
        nuevo_saldo = saldo_actual + monto
        self.bd.ejecutar(
            "UPDATE cuentas SET saldo = ? WHERE id = ?",
            (nuevo_saldo, id_cuenta)
        )
        self.bd.ejecutar(
            "INSERT INTO transacciones (id_cuenta_origen, id_cuenta_destino, monto, tipo_transaccion, fecha_hora) VALUES (?, ?, ?, ?, ?)",
            (None, id_cuenta, monto, 'deposito', datetime.now().isoformat())
        )
        print("Depósito realizado.")

    def realizar_retiro(self, cliente):
        numero = input("Número de cuenta para retiro: ")
        monto = float(input("Monto a retirar: "))
        cuenta = self.bd.consultar(
            "SELECT id, saldo FROM cuentas WHERE numero_cuenta = ? AND id_cliente = ?",
            (numero, cliente.id)
        )
        if not cuenta:
            print("Cuenta no encontrada.")
            return
        id_cuenta, saldo_actual = cuenta[0]
        if saldo_actual < monto:
            print("Saldo insuficiente.")
            return
        nuevo_saldo = saldo_actual - monto
        self.bd.ejecutar(º
            "UPDATE cuentas SET saldo = ? WHERE id = ?",
            (nuevo_saldo, id_cuenta)
        )
        self.bd.ejecutar(
            "INSERT INTO transacciones (id_cuenta_origen, id_cuenta_destino, monto, tipo_transaccion, fecha_hora) VALUES (?, ?, ?, ?, ?)",
            (id_cuenta, None, -monto, 'retiro', datetime.now().isoformat())
        )
        print("Retiro realizado.")

    def realizar_transferencia(self, cliente):
        origen_num = input("Número de cuenta origen: ")
        destino_num = input("Número de cuenta destino: ")
        monto = float(input("Monto a transferir: "))

        cuenta_origen = self.bd.consultar(
            "SELECT id, saldo FROM cuentas WHERE numero_cuenta = ? AND id_cliente = ?",
            (origen_num, cliente.id)
        )
        if not cuenta_origen:
            print("Cuenta origen no encontrada o no te pertenece.")
            return

        cuenta_destino = self.bd.consultar(
            "SELECT id, saldo FROM cuentas WHERE numero_cuenta = ?",
            (destino_num,)
        )
        if not cuenta_destino:
            print("Cuenta destino no encontrada.")
            return

        id_origen, saldo_origen = cuenta_origen[0]
        id_destino, saldo_destino = cuenta_destino[0]

        if saldo_origen < monto:
            print("Saldo insuficiente en cuenta origen.")
            return

        # Simular transacción atómica
        try:
            nuevo_saldo_origen = saldo_origen - monto
            nuevo_saldo_destino = saldo_destino + monto

            self.bd.ejecutar("UPDATE cuentas SET saldo = ? WHERE id = ?", (nuevo_saldo_origen, id_origen))
            self.bd.ejecutar("UPDATE cuentas SET saldo = ? WHERE id = ?", (nuevo_saldo_destino, id_destino))

            self.bd.ejecutar(
                "INSERT INTO transacciones (id_cuenta_origen, id_cuenta_destino, monto, tipo_transaccion, fecha_hora) VALUES (?, ?, ?, ?, ?)",
                (id_origen, id_destino, monto, 'transferencia', datetime.now().isoformat())
            )
            print("Transferencia exitosa.")
        except Exception as e:
            print("Error en transferencia:", e)

    def generar_extracto(self, cliente):
        numero = input("Número de cuenta para extracto: ")
        desde = input("Fecha desde (YYYY-MM-DD): ")
        hasta = input("Fecha hasta (YYYY-MM-DD): ")

        cuenta = self.bd.consultar(
            "SELECT id FROM cuentas WHERE numero_cuenta = ? AND id_cliente = ?",
            (numero, cliente.id)
        )
        if not cuenta:
            print("Cuenta no encontrada.")
            return

        id_cuenta = cuenta[0][0]
        desde_dt = datetime.fromisoformat(desde)
        hasta_dt = datetime.fromisoformat(hasta)

        transacciones = self.bd.consultar(
            "SELECT tipo_transaccion, monto, fecha_hora FROM transacciones WHERE (id_cuenta_origen = ? OR id_cuenta_destino = ?) AND fecha_hora BETWEEN ? AND ? ORDER BY fecha_hora",
            (id_cuenta, id_cuenta, desde, hasta)
        )

        print(f"Extracto de cuenta {numero} desde {desde} hasta {hasta}:")
        if not transacciones:
            print("No hay transacciones en ese rango.")
        else:
            for t in transacciones:
                print(f"{t[2]} - {t[0]}: {t[1]}") 