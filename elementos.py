import pygame
import sys
import os

class Caja(pygame.sprite.Sprite):
	def __init__(self, pos, cont):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join('pics', 'caja.png'))
		self.rect = self.image.get_rect()
		self.rect.x = pos[0]
		self.rect.y = pos[1]
		self.tag = 'Caja_'+str(cont)
		self.id = cont
		self.font = pygame.font.SysFont('Arial', 14)
		self.pos = pos
		self.tasa = str(1)
		self.otro = str(1)
		self.conexiones = pygame.sprite.Group()
		self.id_con = list() # Id de conexiones anexas a la caja
		self.con_limite = list() # Puntos de conexion que tocan la caja
		self.mod = 0
		self.enable = 'H'

	def dibujar(self, superficie):
		"""Dibujar elemento sobre superficie"""
		superficie.blit(self.image, self.rect)
		self.image = pygame.image.load(os.path.join('pics', 'caja.png'))
		#print(self.enable)
		if self.enable == 'H':
			enable = (0, 0, 0)
		elif self.enable == 'I':
			print('hm')
			enable = (255, 255, 255)
		print(enable)
		if self.mod == 0:
			#print(enable)
			surf = pygame.Surface((50, 22))
			surf.fill(enable)
			self.image.blit(surf, (20, 25))
			superficie.blit(self.font.render('a', True, (0, 0, 0)), (self.pos[0]+10, self.pos[1]+27))
			superficie.blit(self.font.render(self.tasa, True, (255, 255, 255)), (self.pos[0]+26, self.pos[1]+27))
		elif self.mod == 1:
			surf = pygame.Surface((50, 22))
			self.image.blit(surf, (20, 25))
			superficie.blit(self.font.render('o', True, (0, 0, 0)), (self.pos[0]+10, self.pos[1]+27))
			superficie.blit(self.font.render(self.otro, True, (255, 255, 255)), (self.pos[0]+26, self.pos[1]+27))
		elif self.mod == 2:
			surf = pygame.Surface((50, 22))
			self.image.blit(surf, (20, 15))
			self.image.blit(surf, (20, 45))
			superficie.blit(self.font.render('a', True, (0, 0, 0)), (self.pos[0]+10, self.pos[1]+17))
			superficie.blit(self.font.render('o', True, (0, 0, 0)), (self.pos[0]+10, self.pos[1]+47))
			superficie.blit(self.font.render(self.tasa, True, (255, 255, 255)), (self.pos[0]+26, self.pos[1]+17))
			superficie.blit(self.font.render(self.otro, True, (255, 255, 255)), (self.pos[0]+26, self.pos[1]+47))

		superficie.blit(self.font.render(self.tag, True, (255, 0, 0)), (self.pos[0]+10, self.pos[1]+82))

class CajaFondo(pygame.sprite.Sprite):
	def __init__(self, pos, cont):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join('pics', 'caja_fondo.png'))
		self.rect = self.image.get_rect()
		self.rect.x = pos[0]-20
		self.rect.y = pos[1]-20
		self.id = cont

	def dibujar(self, superficie):
		"""Dibujar elemento sobre superficie"""
		superficie.blit(self.image, self.rect)

class Bola(pygame.sprite.Sprite):
	def __init__(self, pos, cont):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join('pics', 'stand_by.png'))
		self.rect = self.image.get_rect()
		self.rect.center = [pos[0]+39, pos[1]+39]
		self.tag = 'StandBy_'+str(cont)
		self.id = cont
		self.recta_trabajo = pygame.Rect(80, 170, 760, 480)
		self.font = pygame.font.SysFont('Arial', 14)
		self.pos = pos
		self.conexiones = pygame.sprite.Group()
		#----------------------
		self.cajas = pygame.sprite.Group()
		self.fondos_cajas = pygame.sprite.Group()
		self.caja_1 = Caja((pos[0]+80, pos[1]-40), 1)
		self.fondo_caja_1 = CajaFondo((pos[0]+80, pos[1]-40), 1)
		self.cajas.add(self.caja_1)
		self.fondos_cajas.add(self.fondo_caja_1)
		self.caja_2 = Caja((pos[0]+80, pos[1]+60), 2)
		self.fondo_caja_2 = CajaFondo((pos[0]+80, pos[1]+60), 2)
		self.cajas.add(self.caja_2)
		self.fondos_cajas.add(self.fondo_caja_2)
		self.cajas_fin = 60 # Donde esta la ultima caja
		self.aum = 0 # Aumento de 100 por cada caja
		self.rest_h = pos[1]+160
		self.max_h = 670
		self.conexiones = pygame.sprite.Group()
		self.id_con = list() # Id de conexiones anexas a la caja
		self.con_propia_ini = [(self.pos[0]+160, self.pos[1]), (self.pos[0]+180, self.pos[1]), (self.pos[0]+180, self.pos[1]+100)]
		self.con_propia_fin = [(self.pos[0]+180, self.pos[1]), (self.pos[0]+180, self.pos[1]+100), (self.pos[0]+160, self.pos[1]+100)]
		self.tail_points = [(self.pos[0]+180, self.pos[1]+40), (self.pos[0]+180, self.pos[1]+60),
							(self.pos[0]+180, self.pos[1]+80), (self.pos[0]+180, self.pos[1]+100),
							(self.pos[0]+180, self.pos[1]+120), (self.pos[0]+180, self.pos[1]+140),
							(self.pos[0]+180, self.pos[1]+160)]
		
	def dibujar(self, superficie, show_danger):
		"""Dibujar elemento sobre superficie"""
		superficie.blit(self.image, self.rect)		
		superficie.blit(self.font.render(self.tag, True, (255, 0, 0)), (self.pos[0]-6, self.pos[1]+81))
		for i, linea in enumerate(self.con_propia_ini):
			pygame.draw.aaline(superficie, (0, 0, 0), self.con_propia_ini[i],  self.con_propia_fin[i])
		if show_danger:
			for fondo in self.fondos_cajas:
				fondo.dibujar(superficie)
		for _, caja in enumerate(self.cajas):
			caja.dibujar(superficie)

class BolasFondo(pygame.sprite.Sprite):
	def __init__(self, pos, cont):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join('pics', 'bola_fondo.png'))
		self.rect = self.image.get_rect()
		self.rect.x = pos[0]-20
		self.rect.y = pos[1]-20
		self.id = cont

	def dibujar(self, superficie):
		"""Dibujar elemento sobre superficie"""
		superficie.blit(self.image, self.rect)

class CajaKnn(pygame.sprite.Sprite):
	def __init__(self, pos, cont):
		pygame.sprite.Sprite.__init__(self)
		self.font = pygame.font.SysFont('Arial', 14)
		self.image = pygame.image.load(os.path.join('pics', 'knn_back.png'))
		self.rect = self.image.get_rect()
		self.rect.x = pos[0]+24
		self.rect.y = pos[1]-20
		self.cajas = pygame.sprite.Group()
		self.fondos_cajas = pygame.sprite.Group()
		self.caja_1 = Caja((pos[0]+20, pos[1]), 1)
		self.fondo_caja_1 = CajaFondo((pos[0]+20, pos[1]), 1)
		self.cajas.add(self.caja_1)
		self.fondos_cajas.add(self.fondo_caja_1)
		self.caja_2 = Caja((pos[0]+20, pos[1]+100), 2)
		self.fondo_caja_2 = CajaFondo((pos[0]+20, pos[1]+100), 2)
		self.cajas.add(self.caja_2)
		self.fondos_cajas.add(self.fondo_caja_2)
		self.tag = 'KNN_'+str(cont)
		self.pos = pos
		self.aum = 0
		self.rest_h = pos[1]+200 # Donde s
		self.max_h = 670 # Maximo permitido para dibujar
		self.cajas_fin = 100 # Donde esta la ultima caja
		self.enable = 1
		#-----
		self.con_der_ini = [(self.pos[0]+100, self.pos[1]+40), (self.pos[0]+120, self.pos[1]+40), (self.pos[0]+120, self.pos[1]+140)]
		self.con_der_fin = [(self.pos[0]+120, self.pos[1]+40), (self.pos[0]+120, self.pos[1]+140), (self.pos[0]+100, self.pos[1]+140)]
		self.con_izq_ini = [(self.pos[0]+20, self.pos[1]+40), (self.pos[0], self.pos[1]+40), (self.pos[0], self.pos[1]+140)]
		self.con_izq_fin = [(self.pos[0], self.pos[1]+40), (self.pos[0], self.pos[1]+140), (self.pos[0]+20, self.pos[1]+140)]

	def dibujar(self, superficie, show_danger):
		superficie.blit(self.image, self.rect)
		superficie.blit(self.font.render(self.tag, True, (255, 0, 0)), (self.pos[0]+38, self.pos[1]-20))
		if show_danger:
			for fondo in self.fondos_cajas:
				fondo.dibujar(superficie)
		for _, caja in enumerate(self.cajas):
			caja.dibujar(superficie)

		for i, linea in enumerate(self.con_der_ini):
			pygame.draw.aaline(superficie, (0, 0, 0), self.con_der_ini[i],  self.con_der_fin[i])

		for i, linea in enumerate(self.con_izq_fin):
			pygame.draw.aaline(superficie, (0, 0, 0), self.con_izq_ini[i],  self.con_izq_fin[i])

class CajaKnnFondo(pygame.sprite.Sprite):
	def __init__(self, pos, cont):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join('pics', 'caja_fondo.png'))
		self.rect = self.image.get_rect()
		self.rect.x = pos[0]-20
		self.rect.y = pos[1]-20
		self.id = cont

	def dibujar(self, superficie):
		"""Dibujar elemento sobre superficie"""
		superficie.blit(self.image, self.rect)

class Nodo(pygame.sprite.Sprite):
	def __init__(self, pos, cont):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join('pics', 'nodo.png'))
		self.rect = self.image.get_rect()
		self.rect.center = [pos[0], pos[1]]
		self.tag = 'Nodo_'+str(cont)
		self.recta_trabajo = pygame.Rect(80, 170, 760, 480)
		self.id = cont

	def dibujar(self, superficie):
		"""Dibujar elemento sobre superficie"""
		superficie.blit(self.image, self.rect)

class NodoFondo(pygame.sprite.Sprite):
	def __init__(self, pos, cont):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join('pics', 'nodo_fondo.png'))
		self.rect = self.image.get_rect()
		self.rect.x = pos[0]-15
		self.rect.y = pos[1]-15
		self.id_fondo = cont

	def dibujar(self, superficie):
		"""Dibujar elemento sobre superficie"""
		superficie.blit(self.image, self.rect)

class Conexion(pygame.sprite.Sprite):
	def __init__(self, cont, ini, fin, puntos):
		pygame.sprite.Sprite.__init__(self)
		self.id = cont
		self.ini = ini
		self.fin = fin
		self.puntos = puntos

class Modulo(pygame.sprite.Sprite):
	def __init__(self, pos, tag):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join('pics', 'modulo.png'))
		self.rect = self.image.get_rect()
		self.rect.x = pos[0]
		self.rect.y = pos[1]
		self.tag = tag
		self.font = pygame.font.SysFont('Arial', 14)
		self.pos = pos

	def dibujar(self, superficie):
		"""Dibujar elemento sobre superficie"""
		superficie.blit(self.image, self.rect)
		superficie.blit(self.font.render(self.tag, True, (255, 0, 0)), (self.pos[0]+10, self.pos[1]+82))

class ModuloFondo(pygame.sprite.Sprite):
	def __init__(self, pos, tag):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join('pics', 'modulo_fondo.png'))
		self.rect = self.image.get_rect()
		self.rect.x = pos[0]-20
		self.rect.y = pos[1]-20
		self.id = tag
		self.pos = pos
		self.contenido = None

	def dibujar(self, superficie):
		"""Dibujar elemento sobre superficie"""
		superficie.blit(self.image, self.rect)
		superficie.blit(self.font.render(self.tag, True, (255, 0, 0)), (self.pos[0]+10, self.pos[1]+82))

class Inicio(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)
		self.font = pygame.font.SysFont('Arial', 14)
		self.image = pygame.image.load(os.path.join('pics', 'inicio.png'))
		self.rect = self.image.get_rect()
		self.rect.center = [pos[0]+20, pos[1]+20]
		self.tag = 'Inicio'
		self.pos = pos
		self.recta_trabajo = pygame.Rect(80, 170, 760, 480)
		self.conexiones = pygame.sprite.Group()
		self.id_con = list() # Id de conexiones anexas a la caja

	def dibujar(self, superficie):
		"""Dibujar elemento sobre superficie"""
		superficie.blit(self.image, self.rect)
		superficie.blit(self.font.render(self.tag, True, (255, 0, 0)), (self.pos[0]+6, self.pos[1]+42))

class Fin(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)
		self.font = pygame.font.SysFont('Arial', 14)
		self.image = pygame.image.load(os.path.join('pics', 'fin.png'))
		self.rect = self.image.get_rect()
		self.rect.center = [pos[0]+20, pos[1]+20]
		self.pos = pos
		self.tag = 'Fin'
		self.conexiones = pygame.sprite.Group()
		self.id_con = list() # Id de conexiones anexas a la caja

	def dibujar(self, superficie):
		"""Dibujar elemento sobre superficie"""
		superficie.blit(self.image, self.rect)
		superficie.blit(self.font.render(self.tag, True, (255, 0, 0)), (self.pos[0]+11, self.pos[1]+42))

class LimitesFondo(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join('pics', 'limite_fondo.png'))
		self.rect = self.image.get_rect()
		self.rect.x = pos[0]-20
		self.rect.y = pos[1]-20
		#self.id_fondo = cont

	def dibujar(self, superficie):
		"""Dibujar elemento sobre superficie"""
		superficie.blit(self.image, self.rect)
