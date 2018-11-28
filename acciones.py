import os
import sys
import pygame
import numpy as np

class Mover(pygame.sprite.Sprite):
	def __init__(self, pos):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join('pics', 'mover.png'))
		self.rect = self.image.get_rect()
		self.rect.center = pos

	def dibujar_acciones(self, superficie):
		superficie.blit(self.image, self.rect)

	def ejecutar_accion(self):
		pass