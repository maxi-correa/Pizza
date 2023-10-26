import pygame
from juego import Juego

pygame.init()

def main():
    juego = Juego()

    juego.cargar_mapa()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        #juego.crear_mapa()
        juego.update()
        juego.dibujar()
        juego.get_reloj()
        #pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()