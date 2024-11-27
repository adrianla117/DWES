from .Monstruo import Monstruo

class Heroe:
    def __init__(self, nombre, ataque, defensa):
        self.nombre = nombre
        self.ataque = ataque
        self.defensa = defensa
        self.salud = 100
        self.salud_maxima = 100
        self.defensa_temporal = 0

    def atacar(self, enemigo):
        daño = max(0, self.ataque - enemigo.defensa)
        if daño > 0:
            enemigo.salud -= daño
            print(f"{self.nombre} ataca a {enemigo.nombre}")
            print(f"El enemigo {enemigo.nombre} ha recibido {daño} puntos de daño")
        else:
            print(f"{self.nombre} ataca a {enemigo.nombre}")
            print(f"El enemigo ha bloqueado el ataque")
    
    def curarse(self):
        cantidad_curacion = 20
        self.salud = min(self.salud + cantidad_curacion, self.salud_maxima)
        print(f"{self.nombre} se ha curado. Salud actual: {self.salud}")

    def defenderse(self):
        self.defensa_temporal = 5
        self.defensa += 5
        print(f"{self.nombre} se defiende. Defensa aumentada temporalmente a {self.defensa + self.defensa_temporal}.")

    def reset_defensa(self):
        if self.defensa_temporal > 0:
            print(f"La defensa de {self.nombre} vuelve a la normalidad.")
        self.defensa = self.defensa - self.defensa_temporal

    def esta_vivo(self):
        return self.salud > 0
    