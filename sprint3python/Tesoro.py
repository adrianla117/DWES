import random
from .Heroe import Heroe

class Tesoro:
    def __init__(self):

        self.beneficios = ["aumento_ataque", "aumento_defensa", "restauracion_salud"]

    def encontrar_tesoro(self, heroe):

        beneficio = random.choice(self.beneficios)
        
        if beneficio == "aumento_ataque":
            aumento = 5 
            heroe.ataque += aumento
            print(f"{heroe.nombre} ha encontrado un tesoro: aumento de ataque.")
            print(f"El ataque de {heroe.nombre} aumenta a {heroe.ataque}.")
        
        elif beneficio == "aumento_defensa":
            aumento = 5 
            heroe.defensa += aumento
            print(f"{heroe.nombre} ha encontrado un tesoro: aumento de defensa.")
            print(f"La defensa de {heroe.nombre} aumenta a {heroe.defensa}.")
        
        elif beneficio == "restauracion_salud":
            heroe.salud = heroe.salud_maxima
            print(f"{heroe.nombre} ha encontrado un tesoro: restauración de salud.")
            print(f"La salud de {heroe.nombre} ha sido restaurada a {heroe.salud}.")
            