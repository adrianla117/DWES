from .Tesoro import Tesoro
from .Monstruo import Monstruo
from .Heroe import Heroe

class Mazmorra:
    def __init__(self, heroe):
        self.heroe = heroe
        self.monstruos = [
            Monstruo("Orco", ataque=15, defensa=8, salud=50),
            Monstruo("Goblin", ataque=10, defensa=5, salud=30),
            Monstruo("Troll", ataque=20, defensa=10, salud=60)
        ]
        self.tesoro = Tesoro()

    def jugar(self):
        print(f"{self.heroe.nombre} entra en la mazmorra.")

        for monstruo in self.monstruos:
            print(f"\nTe has encontrado con un {monstruo.nombre}.")
            self.enfrentar_enemigo(monstruo)

            if not self.heroe.esta_vivo():
                print("Héroe ha sido derrotado.")
                return

            self.buscar_tesoro()

        print(f"{self.heroe.nombre} ha derrotado a todos los monstruos")

    def enfrentar_enemigo(self, enemigo):
        while self.heroe.esta_vivo() and enemigo.esta_vivo():
            print("\n¿Qué deseas hacer?")
            print("1. Atacar")
            print("2. Defender")
            print("3. Curarse")
            opcion = input("Elige una opción: ").strip()

            if opcion == "1":
                self.heroe.atacar(enemigo)
                if enemigo.esta_vivo():
                    enemigo.atacar(self.heroe)

            elif opcion == "2":
                self.heroe.defenderse()
                if enemigo.esta_vivo():
                    enemigo.atacar(self.heroe)
                self.heroe.reset_defensa()

            elif opcion == "3":
                self.heroe.curarse()
                if enemigo.esta_vivo():
                    enemigo.atacar(self.heroe)

            else:
                print("Opción no válida.")

    def buscar_tesoro(self):
        print("\nBuscando tesoro...")
        self.tesoro.encontrar_tesoro(self.heroe)
