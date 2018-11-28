import os
import sys
import pygame
import numpy as np
from elementos import Inicio, Fin, LimitesFondo

BLANCO = (255, 255, 255)
VERDE = ( 0, 255, 0)
INICIO_ZONA = (90, 150)
class Propiedades(pygame.sprite.Sprite):
	"""Propiedades de la interfaz"""
	def __init__(self, superficie):
		pygame.sprite.Sprite.__init__(self)
		self.grid = pygame.image.load(os.path.join('pics', 'empty.png'))
		self.area_trabajo = pygame.Surface((900, 520))
		self.area_trabajo.fill(VERDE) # Superficie que contendra el area de trabajo
		self.fondo_dibujo = pygame.Surface((2000, 2000))
		self.fondo_dibujo.fill(BLANCO)
		self.imagen_caja = pygame.image.load(os.path.join('pics', 'caja_mini.png'))
		self.recta_caja = self.imagen_caja.get_rect()
		self.recta_caja.center = (480, 70)
		self.imagen_bola = pygame.image.load(os.path.join('pics', 'stand_by_mini.png'))
		self.recta_bola = self.imagen_bola.get_rect()
		self.recta_bola.center = (535, 70)
		self.imagen_knn = pygame.image.load(os.path.join('pics', 'knn_mini.png'))
		self.recta_knn = self.imagen_knn.get_rect()
		self.recta_knn.center = (580, 70)
		self.imagen_linea = pygame.image.load(os.path.join('pics', 'linea.png'))
		self.recta_conexion = self.imagen_linea.get_rect()
		self.recta_conexion.center = (630, 70)
		#----------------Acciones
		self.imagen_mover = pygame.image.load(os.path.join('pics', 'mover.png'))
		self.recta_mover = self.imagen_mover.get_rect()
		self.recta_mover.center = (50, 200)
		self.imagen_borrar = pygame.image.load(os.path.join('pics', 'borrar.png'))
		self.recta_borrar = self.imagen_borrar.get_rect()
		self.recta_borrar.center = (50, 240)
		self.imagen_export = pygame.image.load(os.path.join('pics', 'export.png'))
		self.recta_export = self.imagen_export.get_rect()
		self.recta_export.center = (50, 280)
		self.imagen_import = pygame.image.load(os.path.join('pics', 'import.png'))
		self.recta_import = self.imagen_import.get_rect()
		self.recta_import.center = (50, 320)
		self.imagen_save = pygame.image.load(os.path.join('pics', 'save.png'))
		self.recta_save = self.imagen_save.get_rect()
		self.recta_save.center = (50, 360)
		self.imagen_load = pygame.image.load(os.path.join('pics', 'open.png'))
		self.recta_load = self.imagen_load.get_rect()
		self.recta_load.center = (50, 400)
		self.imagen_help = pygame.image.load(os.path.join('pics', 'help.png'))
		self.recta_help = self.imagen_help.get_rect()
		self.recta_help.center = (50, 440)
		self.imagen_info = pygame.image.load(os.path.join('pics', 'info.png'))
		self.recta_info = self.imagen_info.get_rect()
		self.recta_info.center = (50, 480)
		#--------------Propiedades
		self.image_grid = pygame.image.load(os.path.join('pics', 'switch_on.png'))
		self.recta_grid = self.image_grid.get_rect()
		self.recta_grid.center = (920, 70)
		self.image_danger = pygame.image.load(os.path.join('pics', 'switch_off.png'))
		self.recta_danger = self.image_danger.get_rect()
		self.recta_danger.center = (920, 100)
		self.image_español = pygame.image.load(os.path.join('pics', 'idioma_es.png'))
		self.recta_español = self.image_español.get_rect()
		self.recta_español.center = (50, 580)
		self.image_ingles = pygame.image.load(os.path.join('pics', 'idioma_en.png'))
		self.recta_ingles = self.image_ingles.get_rect()
		self.recta_ingles.center = (50, 620)
		#--------------opciones
		self.panel_opciones = pygame.image.load(os.path.join('pics', 'opciones.png'))
		self.panel_acciones = pygame.image.load(os.path.join('pics', 'acciones.png'))
		self.panel_elementos = pygame.image.load(os.path.join('pics', 'elementos.png'))
		self.font = pygame.font.SysFont('Arial', 14)
		self.font2 = pygame.font.SysFont('Arial', 29)
		#-------------- Pestaña propiedades
		self.image_draw = pygame.image.load(os.path.join('pics', 'draw.png'))
		self.recta_draw = self.image_draw.get_rect()

	def dibujar_panel(self, superficie):
		superficie.blit(self.panel_acciones, (25, 180))		
		superficie.blit(self.panel_opciones, (800, 10))
		superficie.blit(self.panel_elementos, (450, 10))
		superficie.blit(self.imagen_caja, self.recta_caja)		
		superficie.blit(self.imagen_bola, self.recta_bola)
		superficie.blit(self.imagen_knn, self.recta_knn)
		superficie.blit(self.imagen_linea, self.recta_conexion)
		superficie.blit(self.imagen_mover, self.recta_mover)
		superficie.blit(self.imagen_borrar, self.recta_borrar)
		superficie.blit(self.imagen_export, self.recta_export)
		superficie.blit(self.imagen_import, self.recta_import)
		superficie.blit(self.imagen_save, self.recta_save)
		superficie.blit(self.imagen_load, self.recta_load)
		superficie.blit(self.imagen_help, self.recta_help)
		superficie.blit(self.imagen_info, self.recta_info)
		superficie.blit(self.image_grid, self.recta_grid)
		superficie.blit(self.image_danger, self.recta_danger)
		superficie.blit(self.image_español, self.recta_español)
		superficie.blit(self.image_ingles, self.recta_ingles)

		superficie.blit(self.font.render('Rejilla', True, (0, 0, 0)), (830, 62))
		superficie.blit(self.font.render('Restricciones', True, (0, 0, 0)), (810, 92))
		superficie.blit(self.font2.render('DiCon', True, (0, 0, 0)), (40, 30))

	def activar_grid(self, active):
		if active == True:
			active = False
			self.image_grid = pygame.image.load(os.path.join('pics', 'switch_off.png'))
			self.recta_grid = self.image_grid.get_rect()
			self.recta_grid.center = (920, 70)

		elif active == False:
			active = True
			self.image_grid = pygame.image.load(os.path.join('pics', 'switch_on.png'))
			self.recta_grid = self.image_grid.get_rect()
			self.recta_grid.center = (920, 70)
		return active

	def danger_zone(self, danger):
		if danger == True:
			danger = False
			self.image_danger = pygame.image.load(os.path.join('pics', 'switch_off.png'))
			self.recta_danger = self.image_danger.get_rect()
			self.recta_danger.center = (920, 100)
		elif danger == False:
			danger = True
			self.image_danger = pygame.image.load(os.path.join('pics', 'switch_on.png'))
			self.recta_danger = self.image_danger.get_rect()
			self.recta_danger.center = (920, 100)
		return danger

	def dibujar_area(self, superficie, grid):
		"""Dibujar grid en el espacio de dibujo"""
		imagen = pygame.image.load(os.path.join('pics', 'punto.png'))
		imagen_2 = pygame.image.load(os.path.join('pics', 'punto2.png'))
		iter_fila = 0
		iter_col = 0
		if grid:
			for fila in range(25):
				iter_fila += 20
				iter_col = 0
				for columna in range(50):
					iter_col += 20
					pos_circle = (iter_col, iter_fila)
					self.fondo_dibujo.blit(imagen, pos_circle)
		else:
			for fila in range(25):
				iter_fila += 20
				iter_col = 0
				for columna in range(50):
					iter_col += 20
					pos_circle = (iter_col, iter_fila)
					self.fondo_dibujo.blit(imagen_2, pos_circle)
		self.area_trabajo.blit(self.fondo_dibujo, (0, 0))
		superficie.blit(self.area_trabajo, INICIO_ZONA)


	def dibujar_espacio(self, superficie):
		"""Dibuja area de trabajo (posiciones reticulares)}
			Inutilizado en este momento"""
		MARGEN = 1
		MARGEN_ALTO = 1
		LARGO = 140
		ALTO = 140
		for fila in range(5):
			for columna in range(5):
				color = BLANCO
				cuadro = pygame.draw.rect(superficie, color,
					[(MARGEN + LARGO) * (columna) + MARGEN + 100,
					(MARGEN_ALTO + ALTO) * (fila) + MARGEN + 100, LARGO, ALTO])
				superficie.blit(self.grid, cuadro)

	def pestaña_propiedades(self):
		pass

class Contenedor(pygame.sprite.Sprite):
	def __init__(self, pos, cont, tag):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join('pics', 'pesta_s.png'))
		self.rect = self.image.get_rect()
		self.pos = pos
		self.cont = cont
		self.rect.x = pos[0]+(120*(cont-1))
		self.rect.y = pos[1]
		self.close = pygame.image.load(os.path.join('pics', 'close.png'))
		self.recta_close = self.close.get_rect()
		self.recta_close.x = pos[0]+89+(120*(cont-1))
		self.recta_close.y = pos[1]+5
		self.image_off = pygame.image.load(os.path.join('pics', 'pesta_n.png'))
		self.name = 'Untitled_'+str(tag)
		self.font = pygame.font.SysFont('Arial', 13)
		self.new = pygame.image.load(os.path.join('pics', 'pesta_new.png'))
		self.recta_new = self.new.get_rect()
		self.recta_new.x = pos[0]+120*cont
		self.recta_new.y = pos[1]
		self.add = pygame.image.load(os.path.join('pics', 'add.png'))
		self.recta_add = self.add.get_rect()
		self.recta_add.x = pos[0]+120*cont+8
		self.recta_add.y = pos[1]+6
		self.selected = True
		#-----------------
		self.cajas = pygame.sprite.Group()
		self.cajas_fondo = pygame.sprite.Group()
		self.bolas = pygame.sprite.Group()
		self.bolas_fondo = pygame.sprite.Group()
		self.nodos = pygame.sprite.Group()
		self.nodos_fondo = pygame.sprite.Group()
		self.conexiones = pygame.sprite.Group()
		self.limites = pygame.sprite.Group()
		self.limites_fondo = pygame.sprite.Group()
		self.modulos = pygame.sprite.Group()
		self.modulos_fondo = pygame.sprite.Group()
		self.cajas_bola = pygame.sprite.Group()
		self.cajas_bola_fondo = pygame.sprite.Group()
		self.knn = pygame.sprite.Group()
		self.knn_fondo = pygame.sprite.Group()
		self.cajas_knn = pygame.sprite.Group()
		self.cajas_knn_fondo = pygame.sprite.Group()
		self.lista_conexion_ini = list()
		self.lista_conexion_fin = list()
		#-----------------
		self.cont_cajas = 0
		self.cont_bolas = 0
		self.cont_nodos = 0
		self.cont_knn = 0
		self.final_full = False
		self.inicial_full = False
		self.out = False
		self.contenido = None
		self.puntos_con = list()
		#----
		ini = Inicio((110, 350))
		fondo_ini = LimitesFondo((110, 350))
		self.limites.add(ini)
		self.limites_fondo.add(fondo_ini)
		fin = Fin((930, 350))
		fondo_fin = LimitesFondo((930, 350))
		self.limites.add(fin)
		self.limites_fondo.add(fondo_fin)

	def dibujar(self, superficie):
		self.rect.x = self.pos[0]+(120*(self.cont-1))
		self.rect.y = self.pos[1]
		self.recta_close.x = self.pos[0]+89+(120*(self.cont-1))
		self.recta_close.y = self.pos[1]+5
		if self.selected:
			superficie.blit(self.image, self.rect)
		else:
			superficie.blit(self.image_off, self.rect)
		superficie.blit(self.close, self.recta_close)		
		superficie.blit(self.font.render(self.name, True, (255, 0, 0)), (self.pos[0]+14+(120*(self.cont-1)), self.pos[1]+7))

	def dibujar_new(self, superficie, cont):
		self.recta_new.x = self.pos[0]+120*cont
		self.recta_add.x = self.pos[0]+120*cont+8
		superficie.blit(self.new, self.recta_new)
		superficie.blit(self.add, self.recta_add)

	def elementos_pestaña(self, grupos):
		pass