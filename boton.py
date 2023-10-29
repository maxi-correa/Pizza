import pygame

#Clase Botón
class Boton():
    def __init__(self, x, y, imagen, escala):
        ancho = imagen.get_width()
        alto = imagen.get_height()
        self.imagen = pygame.transform.scale(imagen,(int(ancho*escala),(int(alto*escala))))
        self.rect = self.imagen.get_rect()
        self.rect.topleft = (x,y)
        self.clickeado = False
    
    def dibujar(self, superficie):
        accion = False
        #Obtener la posición del mouse
        pos = pygame.mouse.get_pos()
        
        #Condiciones de mouse y clickeado
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clickeado == False:
                self.clickeado = True
                accion = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clickeado = False
        
        #Dibujar el botón en la pantalla
        superficie.blit(self.imagen,(self.rect.x, self.rect.y))
        return accion