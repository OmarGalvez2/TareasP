class Cliente:
    def __init__(self, nombre, usuario, contrasena, id_cliente):
        self.nombre = nombre
        self.usuario = usuario
        self.contrasena = contrasena
        self.id = id_cliente
        self.cuentas = []

    def agregar_cuenta(self, cuenta):
        self.cuentas.append(cuenta)

    def obtener_cuenta(self, numero):
        for cuenta in self.cuentas:
            if cuenta.numero == numero:
                return cuenta
        return None