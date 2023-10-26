import pygame
from constantes import *

class Plantilla_Sprites:
    def __init__(self, archivo):
        self.plantilla = pygame.image.load(archivo).convert_alpha()
    
    def get_plantilla(self, x, y, ancho, alto):
        plantilla = pygame.Surface([ancho, alto])
        plantilla.blit(self.plantilla, (0,0), (x, y, ancho, alto))
        plantilla.set_colorkey(NEGRO)
        return plantilla