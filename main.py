import pygame
from juego import Juego
from intro import Intro
from game_over import Game_Over


pygame.init()

def main():
    intro = Intro()
    intro.menu()
    
    juego = Juego()
    game_over = Game_Over()
    
    perder = False
    while not perder:
        juego.cargar_mapa()
        
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            juego.update()
            juego.dibujar()
            juego.get_reloj()
            
            if juego.verificar():
                game_over.menu()
                if game_over.verificar():
                    juego.vaciar()
                    run = False
                else:
                    run = False
                    perder = True

    pygame.quit()

if __name__ == "__main__":
    main()