import pygame
from plantilla_sprites import Plantilla_Sprites
from constantes import *
import math

class Juego:
    def __init__(self):
        pygame.display.set_caption("Adventure Time")
        self.screen = pygame.display.set_mode((PANTALLA_ANCHO, PANTALLA_ALTO))
        self.reloj = pygame.time.Clock()
        self.camera = Camera(self.screen.get_rect())
        self.jugador = None
        self.arboles = []
        self.pisos = []
        self.agua = []
        self.enemigo = []
        #Carga de imagen de Sprites solo 1 vez
        self.plantilla_jugador = Plantilla_Sprites('imagenes/character.png')
        self.plantilla_corazones = Plantilla_Sprites('imagenes/corazones.png')
        self.plantilla_arboles = Plantilla_Sprites('imagenes/arboles.png')
        self.plantilla_terreno = Plantilla_Sprites('imagenes/terrain.png')
        self.plantilla_enemigo = Plantilla_Sprites('imagenes/enemy.png')
        
    def get_reloj(self):
        return self.reloj.tick(FPS)
    
    def cargar_elementos(self):
        for i, fila in enumerate(MAPA):
            for j, columna in enumerate(fila):
                piso = Piso(j,i,self.plantilla_terreno)
                self.pisos.append(piso)
                if columna == 'A':
                    arbol = Arbol(j,i,self.plantilla_arboles)
                    self.arboles.append(arbol)
                if columna == 'W':
                    agua = Agua(j,i,self.plantilla_terreno)
                    self.agua.append(agua)
                if columna == '2' or columna == '4' or columna == '6' or columna == '8':
                    enemigo = Enemigo(j,i,self.plantilla_enemigo, columna)
                    self.enemigo.append(enemigo)
    
    def cargar_mapa(self):
        self.cargar_elementos()
        for enemigo in self.enemigo:
            enemigo.carga_datos()
        self.jugador = Jugador(1, 1, self.plantilla_jugador, self.plantilla_corazones, self.arboles, self.agua, self.enemigo, VIDA_INICIAL)

    def update(self):
        self.jugador.update()
        for enemigo in self.enemigo:
            enemigo.update()
        self.camera.update(self.jugador)

    def dibujar(self):
        self.screen.fill(NEGRO)
        
        for piso in self.pisos:
            self.screen.blit(piso.image, self.camera.apply(piso))
        for arbol in self.arboles:
            self.screen.blit(arbol.image, self.camera.apply(arbol))
        for agua in self.agua:
            self.screen.blit(agua.image, self.camera.apply(agua))
        for enemigo in self.enemigo:
            self.screen.blit(enemigo.image, self.camera.apply(enemigo))
            self.screen.blit(enemigo.proyectil.image, self.camera.apply(enemigo.proyectil))
        self.screen.blit(self.jugador.image, self.camera.apply(self.jugador))
        self.screen.blit(self.jugador.image_corazones, (0, 0))
        
        pygame.display.flip()

class Camera:
    def __init__(self, target_rect):
        self.camera = pygame.Rect(0, 0, target_rect.width, target_rect.height)
        self.target = target_rect

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(self.camera.width / 2)
        y = -target.rect.centery + int(self.camera.height / 2)
        x = min(0, x)
        y = min(0, y)
        self.camera = pygame.Rect(x, y, self.camera.width, self.camera.height)

class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y, plantilla, plantilla_corazones, arboles, agua, enemigo, vida):
        super().__init__()
        self.vida = vida
        self.plantilla_corazones = plantilla_corazones
        self.image_corazones = self.plantilla_corazones.get_plantilla(15,4,101,31)
        
        self.x = x * TAMANIO_MOSAICO
        self.y = y * TAMANIO_MOSAICO
        self.ancho = TAMANIO_MOSAICO 
        self.alto = TAMANIO_MOSAICO
        
        self.plantilla_jugador = plantilla
        self.image = plantilla.get_plantilla(3, 2, self.ancho, self.alto)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.x_cambio = 0
        self.y_cambio = 0
        
        self.direccion = "abajo"
        self.bucle_animacion = 1
        
        self.animaciones_bajar = [self.plantilla_jugador.get_plantilla(3, 2, self.ancho, self.alto),
                        self.plantilla_jugador.get_plantilla(35, 2, self.ancho, self.alto),
                        self.plantilla_jugador.get_plantilla(68, 2, self.ancho, self.alto)]

        self.animaciones_subir = [self.plantilla_jugador.get_plantilla(3, 34, self.ancho, self.alto),
                        self.plantilla_jugador.get_plantilla(35, 34, self.ancho, self.alto),
                        self.plantilla_jugador.get_plantilla(68, 34, self.ancho, self.alto)]

        self.animaciones_izquierda = [self.plantilla_jugador.get_plantilla(3, 98, self.ancho, self.alto),
                        self.plantilla_jugador.get_plantilla(35, 98, self.ancho, self.alto),
                        self.plantilla_jugador.get_plantilla(68, 98, self.ancho, self.alto)]

        self.animaciones_derecha = [self.plantilla_jugador.get_plantilla(3, 66, self.ancho, self.alto),
                            self.plantilla_jugador.get_plantilla(35, 66, self.ancho, self.alto),
                            self.plantilla_jugador.get_plantilla(68, 66, self.ancho, self.alto)]
        
        self.enemigo = enemigo
        self.arboles = arboles
        self.agua = agua
    
    def recibir_ataque(self):
        pass
    
    def get_vida(self):
        if self.colision_enemigo() or self.recibir_ataque():
            self.vida -= 1
            if self.vida == 3:
                return self.vida
            if self.vida == 2:
                self.image_corazones = self.plantilla_corazones.get_plantilla(15,40,101,30)
            if self.vida == 1:
                self.image_corazones = self.plantilla_corazones.get_plantilla(15,76,101,30)
            if self.vida == 0:
                self.image_corazones = self.plantilla_corazones.get_plantilla(15,112,101,30)
            if self.vida < 0:
                pygame.quit()
        
    def update(self):
        self.get_vida()
        self.movimiento()
        self.animacion()
        
        self.rect.x += self.x_cambio
        self.colision_arboles('x')
        self.rect.y += self.y_cambio
        self.colision_arboles('y')
        
        self.x_cambio = 0
        self.y_cambio = 0
    
    def movimiento(self):
        teclas = pygame.key.get_pressed()
        
        if teclas[pygame.K_LEFT]:
            self.direccion = "izquierda"
            if self.colision_agua():
                self.x_cambio -= VELOCIDAD_REDUCIDA
            else:
                self.x_cambio -= VELOCIDAD_JUGADOR
        if teclas[pygame.K_RIGHT]:
            self.direccion = "derecha"
            if self.colision_agua():
                self.x_cambio += VELOCIDAD_REDUCIDA
            else:
                self.x_cambio += VELOCIDAD_JUGADOR
        if teclas[pygame.K_UP]:
            self.direccion = "arriba"
            if self.colision_agua():
                self.y_cambio -= VELOCIDAD_REDUCIDA
            else:
                self.y_cambio -= VELOCIDAD_JUGADOR
        if teclas[pygame.K_DOWN]:
            self.direccion = "abajo" 
            if self.colision_agua():
                self.y_cambio += VELOCIDAD_REDUCIDA
            else:
                self.y_cambio += VELOCIDAD_JUGADOR
    
    def colision_enemigo(self):
        for enemigo in self.enemigo:
            if self.rect.colliderect(enemigo.rect):
                return True
    
    def colision_agua(self):
        for agua in self.agua:
            if self.rect.colliderect(agua.rect):
                return True
    
    def colision_arboles(self, direccion):
        for arbol in self.arboles:
            if self.rect.colliderect(arbol.rect):
                if direccion == 'x':
                            if self.x_cambio > 0:
                                self.rect.x = arbol.rect.left - self.rect.width
                            if self.x_cambio < 0:
                                self.rect.x = arbol.rect.right
                if direccion == 'y':
                            if self.y_cambio > 0:
                                self.rect.y = arbol.rect.top - self.rect.height
                            if self.y_cambio < 0:
                                self.rect.y = arbol.rect.bottom
    def animacion(self):
        if self.direccion == "abajo":
            if self.y_cambio == 0: #Si se queda parado
                self.image = self.plantilla_jugador.get_plantilla(3, 2, self.ancho, self.alto)
            else: #Si se mueve hacia abajo
                self.image = self.animaciones_bajar[math.floor(self.bucle_animacion)]
                self.bucle_animacion += 0.1
                if self.bucle_animacion >= 3:
                    self.bucle_animacion = 1
        
        if self.direccion == "arriba":
            if self.y_cambio == 0: #Si se queda parado
                self.image = self.plantilla_jugador.get_plantilla(3, 34, self.ancho, self.alto)
            else: #Si se mueve
                self.image = self.animaciones_subir[math.floor(self.bucle_animacion)]
                self.bucle_animacion += 0.1
                if self.bucle_animacion >= 3:
                    self.bucle_animacion = 1
        
        if self.direccion == "izquierda":
            if self.x_cambio == 0: #Si se queda parado
                self.image = self.plantilla_jugador.get_plantilla(3, 98, self.ancho, self.alto)
            else: #Si se mueve
                self.image = self.animaciones_izquierda[math.floor(self.bucle_animacion)]
                self.bucle_animacion += 0.1
                if self.bucle_animacion >= 3:
                    self.bucle_animacion = 1
        
        if self.direccion == "derecha":
            if self.x_cambio == 0: #Si se queda parado
                self.image = self.plantilla_jugador.get_plantilla(3, 66, self.ancho, self.alto)
            else: #Si se mueve
                self.image = self.animaciones_derecha[math.floor(self.bucle_animacion)]
                self.bucle_animacion += 0.1
                if self.bucle_animacion >= 3:
                    self.bucle_animacion = 1

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y, plantilla, direccion):
        super().__init__()
        self.x = x * TAMANIO_MOSAICO
        self.y = y * TAMANIO_MOSAICO
        self.ancho = TAMANIO_MOSAICO 
        self.alto = TAMANIO_MOSAICO
        
        self.plantilla_enemigo = plantilla
        self.direccion = direccion
        self.image = None
        self.rect = None
        
        self.proyectil = None
        self.proyectil_x = None
        self.proyectil_y = None
        self.proyectil_x_cambio = None
        self.proyectil_y_cambio = None
        
        self.bucle_animacion = 0
        
        self.animaciones_abajo = [self.plantilla_enemigo.get_plantilla(3, 2, self.ancho, self.alto),
                                self.plantilla_enemigo.get_plantilla(68, 2, self.ancho, self.alto)]
        
        self.animaciones_arriba = [self.plantilla_enemigo.get_plantilla(3, 34, self.ancho, self.alto),
                        self.plantilla_enemigo.get_plantilla(68, 34, self.ancho, self.alto)]

        self.animaciones_izquierda = [self.plantilla_enemigo.get_plantilla(3, 98, self.ancho, self.alto),
                        self.plantilla_enemigo.get_plantilla(68, 98, self.ancho, self.alto)]

        self.animaciones_derecha = [self.plantilla_enemigo.get_plantilla(3, 66, self.ancho, self.alto),
                            self.plantilla_enemigo.get_plantilla(68, 66, self.ancho, self.alto)]
    
    def carga_datos(self):
        if self.direccion == '2':
            self.image = self.plantilla_enemigo.get_plantilla(3, 2, self.ancho, self.alto)
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
            self.proyectil_x = self.rect.centerx
            self.proyectil_y = self.rect.bottom
            self.proyectil_y_cambio = self.proyectil_y
            self.proyectil = Proyectil(self.proyectil_x, self.proyectil_y_cambio)
            #for proyectil in self.proyectiles:
            #    proyectil.y += VELOCIDAD_DISPARO
        if self.direccion == '4':
            self.image = self.plantilla_enemigo.get_plantilla(3, 99, self.ancho, self.alto)
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
            self.proyectil_x = self.rect.left
            self.proyectil_y = self.rect.centery
            self.proyectil = Proyectil(self.proyectil_x, self.proyectil_y)
            #for proyectil in self.proyectiles:
            #    proyectil.x -= VELOCIDAD_DISPARO
        if self.direccion == '6':
            self.image = self.plantilla_enemigo.get_plantilla(3, 67, self.ancho, self.alto)
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
            self.proyectil_x = self.rect.right
            self.proyectil_y = self.rect.centery
            self.proyectil = Proyectil(self.proyectil_x, self.proyectil_y)
            #for proyectil in self.proyectiles:
            #    proyectil.x += VELOCIDAD_DISPARO
        if self.direccion == '8':
            self.image = self.plantilla_enemigo.get_plantilla(3, 35, self.ancho, self.alto)
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
            self.proyectil_x = self.rect.centerx
            self.proyectil_y = self.rect.top
            self.proyectil = Proyectil(self.proyectil_x, self.proyectil_y)
            #for proyectil in self.proyectiles:
            #    proyectil.y -= VELOCIDAD_DISPARO
    
    def animacion(self):
        if self.direccion == '2':
            self.image = self.animaciones_abajo[0]
            self.bucle_animacion += 0.01
            if self.bucle_animacion > 1:
                self.image = self.animaciones_abajo[1]
                if self.bucle_animacion > 1.1:
                    self.bucle_animacion = 0
        
        if self.direccion == '4':
            self.image = self.animaciones_izquierda[0]
            self.bucle_animacion += 0.01
            if self.bucle_animacion > 1:
                self.image = self.animaciones_izquierda[1]
                if self.bucle_animacion > 1.1:
                    self.bucle_animacion = 0
        
        if self.direccion == '6':
            self.image = self.animaciones_derecha[0]
            self.bucle_animacion += 0.01
            if self.bucle_animacion > 1:
                self.image = self.animaciones_derecha[1]
                if self.bucle_animacion > 1.1:
                    self.bucle_animacion = 0
        
        if self.direccion == '8':
            self.image = self.animaciones_arriba[0]
            self.bucle_animacion += 0.01
            if self.bucle_animacion > 1:
                self.image = self.animaciones_arriba[1]
                if self.bucle_animacion > 1.1:
                    self.bucle_animacion = 0
                    
    def crear_roca(self):
        if self.bucle_animacion >= 1:
            if self.direccion == '2':
                self.proyectil_y_cambio += VELOCIDAD_DISPARO
                self.proyectil = Proyectil(self.proyectil_x, self.proyectil_y_cambio)
        if self.bucle_animacion == 0:
            self.proyectil = Proyectil(self.proyectil_x, self.proyectil_y)
            self.proyectil_y_cambio = self.proyectil_y
    
    def update(self):
        self.animacion()
        self.crear_roca()
    #    if self.direccion == '2':
    #        self.proyectil_y += VELOCIDAD_DISPARO
    #    if self.direccion == '4':
    #        self.proyectil_x -= VELOCIDAD_DISPARO
    #    if self.direccion == '6':
    #        self.proyectil_x += VELOCIDAD_DISPARO
    #    if self.direccion == '8':
    #        self.proyectil_y -= VELOCIDAD_DISPARO
    #def crear_proyectil(self):
    #    proyectil = Proyectil(self.rect.centerx, self.rect.centery)
    #    self.proyectiles.append(proyectil.dibujar(self.screen))
    
    def disparar(self, screen, tiempo_actual):
        if self.direccion == '2':
            if tiempo_actual - self.ultimo_disparo >= self.intervalo_disparo:
                pygame.draw.circle(screen, ROJO, (self.proyectil_x, self.proyectil_y), 5)
                self.ultimo_disparo = 0
        if self.direccion == '4':
            if tiempo_actual - self.ultimo_disparo >= self.intervalo_disparo:
                pygame.draw.circle(screen, ROJO, (self.proyectil_x, self.proyectil_y), 5)
                self.ultimo_disparo = 0
        if self.direccion == '6':
            if tiempo_actual - self.ultimo_disparo >= self.intervalo_disparo:
                pygame.draw.circle(screen, ROJO, (self.proyectil_x, self.proyectil_y), 5)
                self.ultimo_disparo = 0
        if self.direccion == '8':
            if tiempo_actual - self.ultimo_disparo >= self.intervalo_disparo:
                pygame.draw.circle(screen, ROJO, (self.proyectil_x, self.proyectil_y), 5)
                self.ultimo_disparo = 0
"""
    def update(self):
        if self.direccion == '2':
            for proyectil in self.proyectiles:
                proyectil.move_ip(0, VELOCIDAD_DISPARO)
        if self.direccion == '4':
            for proyectil in self.proyectiles:
                proyectil.move_ip(-VELOCIDAD_DISPARO, 0)
        if self.direccion == '6':
            for proyectil in self.proyectiles:
                proyectil.move_ip(VELOCIDAD_DISPARO, 0)
        if self.direccion == '8':
            for proyectil in self.proyectiles:
                proyectil.move_ip(0, -VELOCIDAD_DISPARO)
"""
class Proyectil (pygame.sprite.Sprite):
    def __init__ (self, x, y):
        super().__init__()
        self.ancho = 15
        self.alto = 12
        self.plantilla_roca = Plantilla_Sprites('imagenes/terrain.png')
        self.image = self.plantilla_roca.get_plantilla(932, 623, self.ancho, self.alto)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Arbol(pygame.sprite.Sprite):
    def __init__(self, x, y, plantilla):
        super().__init__()
        
        self.x = x * TAMANIO_MOSAICO
        self.y = y * TAMANIO_MOSAICO
        self.ancho = TAMANIO_MOSAICO 
        self.alto = TAMANIO_MOSAICO
        
        self.plantilla_arboles = plantilla
        self.image = self.plantilla_arboles.get_plantilla(102, 49, self.ancho, self.alto)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        #self.rect.topleft = (x, y)

class Piso(pygame.sprite.Sprite):
    def __init__(self, x, y, plantilla):
        super().__init__()
        
        self.x = x * TAMANIO_MOSAICO
        self.y = y * TAMANIO_MOSAICO
        self.ancho = TAMANIO_MOSAICO 
        self.alto = TAMANIO_MOSAICO        
        
        self.plantilla_terreno = plantilla
        self.image = self.plantilla_terreno.get_plantilla(65, 352, self.ancho, self.alto)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

class Agua(pygame.sprite.Sprite):
    def __init__(self, x, y,plantilla):
        super().__init__()
        
        self.x = x * TAMANIO_MOSAICO
        self.y = y * TAMANIO_MOSAICO
        self.ancho = TAMANIO_MOSAICO 
        self.alto = TAMANIO_MOSAICO        
        
        self.plantilla_terreno = plantilla
        self.image = self.plantilla_terreno.get_plantilla(900, 160, self.ancho, self.alto)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y