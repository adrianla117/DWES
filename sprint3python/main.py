from .Heroe import Heroe
from .Mazmorra import Mazmorra

def main():
    nombre_heroe = input("Introduce el nombre de tu héroe: ")
    heroe = Heroe(nombre_heroe, ataque=10, defensa=5)
    
    mazmorra = Mazmorra(heroe)
    mazmorra.jugar()

if __name__ == "__main__":
    main()