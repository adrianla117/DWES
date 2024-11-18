from .Heroe import Heroe

class Monstruo:
    def __init__(self, nombre, ataque, defensa, salud):
        self.nombre = nombre
        self.ataque = ataque
        self.defensa = defensa
        self.salud = salud

    def atacar(self, heroe):
        daño = max(0, self.ataque - (heroe.defensa + heroe.defensa_temporal))
        if daño > 0:
            heroe.salud -= daño
            print(f"El monstruo {self.nombre} ataca a {heroe.nombre}")
            print(f"{heroe.nombre} ha recibido {daño} puntos de daño.")
        else:
            print(f"El monstruo {self.nombre} ataca a {heroe.nombre}.")
            print(f"{heroe.nombre} ha bloqueado el ataque.")

    def esta_vivo(self):
        return self.salud > 0
    