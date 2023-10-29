import pygame
from plantilla_sprites import Plantilla_Sprites
from constantes import *
from boton import Boton
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
        #Carga de imagenes de pausa
        self.titulo_img = pygame.image.load('imagenes/adventure_time.png').convert_alpha()
        self.back_img = pygame.image.load('imagenes/back_btn.png').convert_alpha()
        self.option_2_img = pygame.image.load('imagenes/option_2_btn.png').convert_alpha()
        self.sound_on_2_img = pygame.image.load('imagenes/sound_on_2_btn.png').convert_alpha()
        self.sound_off_2_img = pygame.image.load('imagenes/sound_off_2_btn.png').convert_alpha()
        self.quit_2_img = pygame.image.load('imagenes/quit_2_btn.png').convert_alpha()
        self.menu_img = pygame.image.load('imagenes/menu_btn.png').convert_alpha()
        self.boton_menu = Boton(750, 10, self.menu_img, 1)  
        #Carga de imagen de Sprites solo 1 vez
        self.plantilla_jugador = Plantilla_Sprites('imagenes/character.png')
        self.plantilla_corazones = Plantilla_Sprites('imagenes/corazones.png')
        self.plantilla_arboles = Plantilla_Sprites('imagenes/arboles.png')
        self.plantilla_terreno = Plantilla_Sprites('imagenes/terrain.png')
        self.plantilla_enemigo = Plantilla_Sprites('imagenes/enemy.png')
        self.plantilla_ataque = Plantilla_Sprites('imagenes/attack.png')
        #Carga de música
        self.menu_theme = pygame.mixer.Sound('sonidos/menu_theme.ogg')
        self.battle_theme = pygame.mixer.Sound('sonidos/battle_theme.ogg')
        self.tema_batalla = True
        
        self.pausado = False
        
    def get_reloj(self):
        return self.reloj.tick(FPS)
    
    def pausa(self):
        #Instancia de botones
        boton_back = Boton(320, 300, self.back_img, 1.5)
        boton_sound_on_2 = Boton(470, 400, self.sound_on_2_img, 1.5)
        boton_sound_off_2 = Boton(550, 400, self.sound_off_2_img, 1.5)
        boton_quit_2 = Boton(320, 500, self.quit_2_img, 1.5)
        
        #Ciclo de pausa
        while self.pausado:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
            
            self.screen.fill(AZUL)
            self.screen.blit(self.titulo_img, [50,-70])
            self.screen.blit(pygame.transform.scale(self.option_2_img, (135,55)), [320, 400])
            
            if boton_back.dibujar(self.screen):
                self.pausado = False
            
            if boton_sound_on_2.dibujar(self.screen):
                if not self.tema_batalla:
                    self.battle_theme.play(-1)
                    self.tema_batalla = True
            
            if boton_sound_off_2.dibujar(self.screen):
                self.battle_theme.stop()
                self.tema_batalla = False
                
            if boton_quit_2.dibujar(self.screen):
                pygame.quit()
            
            pygame.display.update()
    
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
                    enemigo = Enemigo(j,i,self.plantilla_enemigo, self.plantilla_terreno, columna)
                    self.enemigo.append(enemigo)
    
    def cargar_mapa(self):
        self.cargar_elementos()
        for enemigo in self.enemigo:
            enemigo.carga_datos()
        self.jugador = Jugador(1, 1, self.plantilla_jugador, self.plantilla_corazones, self.plantilla_ataque, self.arboles, self.agua, self.enemigo, VIDA_INICIAL)
        self.battle_theme.play(-1)

    def vaciar(self):
        self.jugador = None
        self.arboles = []
        self.pisos = []
        self.agua = []
        self.enemigo = []
    
    def verificar(self):
        if self.jugador.termina_juego:
            self.battle_theme.stop()
            self.tema_batalla = False
            return True
        
    def update(self):
        
        self.jugador.update()
        for enemigo in self.enemigo:
            enemigo.update()
        self.camera.update(self.jugador)
        
        self.verificar()
        if pygame.key.get_pressed()[pygame.K_ESCAPE] or self.boton_menu.dibujar(self.screen):
            self.pausado = True
            self.pausa()

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
        self.screen.blit(self.jugador.ataque.image, self.camera.apply(self.jugador.ataque))
        self.screen.blit(self.jugador.image_corazones, (0, 0))
        
        if self.boton_menu.dibujar(self.screen):
            pass
        
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
    def __init__(self, x, y, plantilla, plantilla_corazones, plantilla_ataque, arboles, agua, enemigo, vida):
        super().__init__()
        self.vida = vida
        self.plantilla_corazones = plantilla_corazones
        self.image_corazones = self.plantilla_corazones.get_plantilla(15,4,101,31)
        self.plantilla_ataque = plantilla_ataque
        
        self.x = x * TAMANIO_MOSAICO
        self.y = y * TAMANIO_MOSAICO
        self.ancho = TAMANIO_MOSAICO 
        self.alto = TAMANIO_MOSAICO
        
        self.plantilla_jugador = plantilla
        self.image = plantilla.get_plantilla(3, 2, self.ancho, self.alto)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.proyectiles_colisionados = set()
        
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
        self.ataque = Ataque(-1, -1, self.plantilla_ataque)
        self.ataque_original = Ataque(-1, -1, self.plantilla_ataque)
        self.atacando = False
        self.termina_juego = False
    
    def game_over(self):
        if self.vida < 0 or not self.enemigo:
            self.termina_juego = True
            
    def get_vida(self):
        if self.colision_enemigo() or self.colision_proyectil():
            self.vida -= 1
            if self.vida == 2:
                self.image_corazones = self.plantilla_corazones.get_plantilla(15,40,101,30)
            if self.vida == 1:
                self.image_corazones = self.plantilla_corazones.get_plantilla(15,76,101,30)
            if self.vida == 0:
                self.image_corazones = self.plantilla_corazones.get_plantilla(15,112,101,30)
    
    def atacar(self):
        if self.atacando:
            self.ataque.animacion(self.direccion)
            for enemigo in self.enemigo:
                if self.ataque.rect.colliderect(enemigo.rect):
                    self.enemigo.remove(enemigo)
        if self.ataque.bucle_animacion == 0:
            self.atacando = False
            self.ataque = self.ataque_original
    
    def update(self):
        self.get_vida()
        self.acciones()
        self.animacion()
        self.atacar()
        
        self.rect.x += self.x_cambio
        self.colision_arboles('x')
        self.rect.y += self.y_cambio
        self.colision_arboles('y')
        
        self.x_cambio = 0
        self.y_cambio = 0
        
        self.game_over()
    
    def acciones(self):
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
        if teclas[pygame.K_SPACE]:
                self.atacando = True
                if self.direccion == "abajo":
                    self.ataque = Ataque(self.rect.x, self.rect.y + TAMANIO_MOSAICO, self.plantilla_ataque)
                if self.direccion == "arriba":
                    self.ataque = Ataque(self.rect.x, self.rect.y - TAMANIO_MOSAICO, self.plantilla_ataque)
                if self.direccion == "izquierda":
                    self.ataque = Ataque(self.rect.x - TAMANIO_MOSAICO, self.rect.y, self.plantilla_ataque)
                if self.direccion == "derecha":
                    self.ataque = Ataque(self.rect.x + TAMANIO_MOSAICO, self.rect.y, self.plantilla_ataque)
    
    def colision_enemigo(self):
        for enemigo in self.enemigo:
            if self.rect.colliderect(enemigo.rect):
                return True
            
    def colision_proyectil(self):
        for enemigo in self.enemigo:
            if enemigo.proyectil not in self.proyectiles_colisionados:
                if self.rect.colliderect(enemigo.proyectil.rect):
                    self.proyectiles_colisionados.add(enemigo.proyectil)
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

class Ataque(pygame.sprite.Sprite):
    def __init__(self, x, y, plantilla):
        super().__init__()
        
        self.x = x# * TAMANIO_MOSAICO
        self.y = y# * TAMANIO_MOSAICO
        self.ancho = TAMANIO_MOSAICO
        self.alto = TAMANIO_MOSAICO
        
        self.plantilla_ataque = plantilla
        self.image = self.plantilla_ataque.get_plantilla(0, 64, self.ancho, self.alto)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
        self.bucle_animacion = 0
        
        self.animaciones_derecha = [self.plantilla_ataque.get_plantilla(0, 64, self.ancho, self.alto),
                        self.plantilla_ataque.get_plantilla(32, 64, self.ancho, self.alto),
                        self.plantilla_ataque.get_plantilla(64, 64, self.ancho, self.alto),
                        self.plantilla_ataque.get_plantilla(96, 64, self.ancho, self.alto),
                        self.plantilla_ataque.get_plantilla(128, 64, self.ancho, self.alto)]

        self.animaciones_abajo = [self.plantilla_ataque.get_plantilla(0, 32, self.ancho, self.alto),
                        self.plantilla_ataque.get_plantilla(32, 32, self.ancho, self.alto),
                        self.plantilla_ataque.get_plantilla(64, 32, self.ancho, self.alto),
                        self.plantilla_ataque.get_plantilla(96, 32, self.ancho, self.alto),
                        self.plantilla_ataque.get_plantilla(128, 32, self.ancho, self.alto)]

        self.animaciones_izquierda = [self.plantilla_ataque.get_plantilla(0, 96, self.ancho, self.alto),
                        self.plantilla_ataque.get_plantilla(32, 96, self.ancho, self.alto),
                        self.plantilla_ataque.get_plantilla(64, 96, self.ancho, self.alto),
                        self.plantilla_ataque.get_plantilla(96, 96, self.ancho, self.alto),
                        self.plantilla_ataque.get_plantilla(128, 96, self.ancho, self.alto)]

        self.animaciones_arriba = [self.plantilla_ataque.get_plantilla(0, 0, self.ancho, self.alto),
                        self.plantilla_ataque.get_plantilla(32, 0, self.ancho, self.alto),
                        self.plantilla_ataque.get_plantilla(64, 0, self.ancho, self.alto),
                        self.plantilla_ataque.get_plantilla(96, 0, self.ancho, self.alto),
                        self.plantilla_ataque.get_plantilla(128, 0, self.ancho, self.alto)]
    
    def animacion(self, direccion):
        if direccion == 'arriba':
            self.image = self.animaciones_arriba[math.floor(self.bucle_animacion)]
            self.bucle_animacion += 0.5
            if self.bucle_animacion >= 5:
                self.image = self.animaciones_arriba[0]
                self.bucle_animacion = 0
        
        if direccion == 'abajo':
            self.image = self.animaciones_abajo[math.floor(self.bucle_animacion)]
            self.bucle_animacion += 0.5
            if self.bucle_animacion >= 5:
                self.image = self.animaciones_abajo[0]
                self.bucle_animacion = 0
        
        if direccion == 'izquierda':
            self.image = self.animaciones_izquierda[math.floor(self.bucle_animacion)]
            self.bucle_animacion += 0.5
            if self.bucle_animacion >= 5:
                self.image = self.animaciones_izquierda[0]
                self.bucle_animacion = 0
        
        if direccion == 'derecha':
            self.image = self.animaciones_derecha[math.floor(self.bucle_animacion)]
            self.bucle_animacion += 0.5
            if self.bucle_animacion >= 5:
                self.image = self.animaciones_derecha[0]
                self.bucle_animacion = 0

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y, plantilla, plantilla_roca, direccion):
        super().__init__()
        self.x = x * TAMANIO_MOSAICO
        self.y = y * TAMANIO_MOSAICO
        self.ancho = TAMANIO_MOSAICO 
        self.alto = TAMANIO_MOSAICO
        
        self.plantilla_enemigo = plantilla
        self.direccion = direccion
        self.image = None
        self.rect = None
        
        self.plantilla_roca = plantilla_roca
        self.proyectil = None
        self.proyectil_x = None
        self.proyectil_y = None
        self.arrojando = False
        self.cont = 0
        
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
            self.proyectil = Proyectil(self.proyectil_x, self.proyectil_y, self.plantilla_roca)
        
        if self.direccion == '4':
            self.image = self.plantilla_enemigo.get_plantilla(3, 99, self.ancho, self.alto)
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
            self.proyectil_x = self.rect.left
            self.proyectil_y = self.rect.centery
            self.proyectil = Proyectil(self.proyectil_x, self.proyectil_y, self.plantilla_roca)
            
        if self.direccion == '6':
            self.image = self.plantilla_enemigo.get_plantilla(3, 67, self.ancho, self.alto)
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
            self.proyectil_x = self.rect.right
            self.proyectil_y = self.rect.centery
            self.proyectil = Proyectil(self.proyectil_x, self.proyectil_y, self.plantilla_roca)
        
        if self.direccion == '8':
            self.image = self.plantilla_enemigo.get_plantilla(3, 35, self.ancho, self.alto)
            self.rect = self.image.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y
            self.proyectil_x = self.rect.centerx
            self.proyectil_y = self.rect.top
            self.proyectil = Proyectil(self.proyectil_x, self.proyectil_y, self.plantilla_roca)
    
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
        if self.direccion == '2':
            if self.bucle_animacion > 1 and not self.arrojando:
                self.arrojando = True
            
            if self.arrojando:
                self.proyectil.rect.y += VELOCIDAD_DISPARO
                self.cont += 1
                if self.cont == 50:
                    self.proyectil = Proyectil(self.proyectil_x, self.proyectil_y, self.plantilla_roca)
                    self.proyectil.rect.y = self.proyectil_y
                    self.cont = 0
                    self.arrojando = False
        
        if self.direccion == '4':
            if self.bucle_animacion > 1 and not self.arrojando:
                self.arrojando = True
            
            if self.arrojando:
                self.proyectil.rect.x -= VELOCIDAD_DISPARO
                self.cont += 1
                if self.cont == 50:
                    self.proyectil = Proyectil(self.proyectil_x, self.proyectil_y, self.plantilla_roca)
                    self.proyectil.rect.x = self.proyectil_x
                    self.cont = 0
                    self.arrojando = False
        
        if self.direccion == '8':
            if self.bucle_animacion > 1 and not self.arrojando:
                self.arrojando = True
            
            if self.arrojando:
                self.proyectil.rect.y -= VELOCIDAD_DISPARO
                self.cont += 1
                if self.cont == 50:
                    self.proyectil = Proyectil(self.proyectil_x, self.proyectil_y, self.plantilla_roca)
                    self.proyectil.rect.y = self.proyectil_y
                    self.cont = 0
                    self.arrojando = False
        
        if self.direccion == '6':
            if self.bucle_animacion > 1 and not self.arrojando:
                self.arrojando = True
            
            if self.arrojando:
                self.proyectil.rect.x += VELOCIDAD_DISPARO
                self.cont += 1
                if self.cont == 50:
                    self.proyectil = Proyectil(self.proyectil_x, self.proyectil_y, self.plantilla_roca)
                    self.proyectil.rect.x = self.proyectil_x
                    self.cont = 0
                    self.arrojando = False
    def update(self):
        self.animacion()
        self.crear_roca()
    
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

class Proyectil (pygame.sprite.Sprite):
    def __init__ (self, x, y, plantilla):
        super().__init__()
        self.ancho = 15
        self.alto = 12
        self.plantilla_roca = plantilla
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