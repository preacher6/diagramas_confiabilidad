import pygame
import sys
import os
import math
import easygui as eg
from elementos import *
from acciones import Mover

NEGRO = (0, 0, 0)

class Items(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.cont_cajas = 0
		self.cont_nodos = 0
		self.cajas = pygame.sprite.Group()
		self.cajas_fondo = pygame.sprite.Group()
		self.nodos = pygame.sprite.Group()
		self.nodos_fondo = pygame.sprite.Group()
		self.conexiones = pygame.sprite.Group()
		self.limites = pygame.sprite.Group()
		self.limites_fondo = pygame.sprite.Group()
		self.imagen_caja = pygame.image.load(os.path.join('pics', 'caja.png'))
		self.imagen_modulo = pygame.image.load(os.path.join('pics', 'modulo.png'))
		self.imagen_bola = pygame.image.load(os.path.join('pics', 'stand_by.png'))
		self.imagen_knn = pygame.image.load(os.path.join('pics', 'knn.png'))
		self.imagen_nodo = pygame.image.load(os.path.join('pics', 'nodo.png'))
		self.imagen_linea = pygame.image.load(os.path.join('pics', 'linea.png'))
		self.imagen_linea_on = pygame.image.load(os.path.join('pics', 'linea_on.png'))
		self.imagen_inicial = pygame.image.load(os.path.join('pics', 'inicio.png'))
		self.imagen_final = pygame.image.load(os.path.join('pics', 'fin.png'))
		self.imagen_move = pygame.image.load(os.path.join('pics', 'mover.png'))
		self.imagen_borrar = pygame.image.load(os.path.join('pics', 'borrar.png'))
		self.pos = None
		self.draw_line = False
		self.lista_conexion_ini = list()
		self.lista_conexion_fin = list()
		self.waiting_end = False
		self.final_full = False
		self.inicial_full = False
		self.out = False
		self.acciones_on = False # Ejecutando acción
		self.move_element = False # Permite desplazamiento de elementos
		self.element_selected = None # elementos a ejecutar accion
		self.fondo_selected = None # fondo elemento seleccionado
		self.always_draw = False
		self.element_con_ini = None
		self.element_con_fin = None
		self.con = None

	def consultar(self, pos_act, desp, superficie, tag, recta_trabajo):
		if recta_trabajo.collidepoint(pos_act): # Evaluar si el cursos se encuentra dentro del area de dibujo
			pygame.mouse.set_visible(False)
			posx = pos_act[0]-90
			posy = pos_act[1]-150
			pos = self.round_base(posx, posy)
			if tag == 'nodo':
				imagen = self.imagen_nodo
				self.pos = (pos[0]+86, pos[1]+146)
			elif tag == 'caja':
				imagen = self.imagen_caja
				self.pos = (pos[0]+90, pos[1]+150)
			elif tag == 'conexion':
				imagen = self.imagen_linea_on
				self.pos = (pos[0]+79, pos[1]+139)
			elif tag == 'bola':
				imagen = self.imagen_bola
				self.pos = (pos[0]+71, pos[1]+150)
			elif tag == 'knn':
				imagen = self.imagen_knn
				self.pos = (pos[0]+90, pos[1]+150)
			elif tag == 'mover':
				imagen = self.imagen_move
				self.pos = (pos[0]+75, pos[1]+135)
			elif tag == 'borrar':
				imagen = self.imagen_borrar
				self.pos = (pos[0]+75, pos[1]+135)
			elif tag == 'modulo':
				imagen = self.imagen_modulo
				self.pos = (pos[0]+90, pos[1]+150)
			self.pos_out_fict = (pos[0]+90, pos[1]+150) # linea en caliente
			self.pos_out = (pos[0], pos[1]) # Linea fija
			superficie.blit(imagen, self.pos)
		else:
			pygame.mouse.set_visible(True)
			if tag == 'nodo':
				imagen = self.imagen_nodo
			elif tag == 'caja':
				imagen = self.imagen_caja
			elif tag == 'bola':
				imagen = self.imagen_bola
			elif tag == 'knn':
				imagen = self.imagen_knn
			elif tag == 'conexion':
				imagen = self.imagen_linea_on
			elif tag == 'mover':
				imagen = self.imagen_move
			elif tag == 'borrar':
				imagen = self.imagen_borrar
			elif tag == 'modulo':
				imagen = self.imagen_modulo

			superficie.blit(imagen, pos_act)

	def ejecutar_acciones(self, pos, area_trabajo, pos_act, contenedor, tag):
		if pygame.MOUSEBUTTONDOWN and area_trabajo.collidepoint(pos_act): # Evaluar si el cursor se encuentra dentro del area de dibujo
			if tag == 'mover':
				mover = Mover(pos)
				hit_caja = pygame.sprite.spritecollide(mover, contenedor.cajas, False)
				if hit_caja:
					for caja in contenedor.cajas:
						if caja.rect.collidepoint(pos):
							self.move_element = True
							self.element_selected = caja
							for fondo in contenedor.cajas_fondo:
								if fondo.id == caja.id:
									self.fondo_selected = fondo

				hit_nodo = pygame.sprite.spritecollide(mover, self.cajas, False)

			if tag == 'borrar':
				mover = Mover(pos)
				hit_caja = pygame.sprite.spritecollide(mover, contenedor.cajas, False)
				if hit_caja:
					for caja in contenedor.cajas:
						if caja.rect.collidepoint(pos):
							for con in contenedor.conexiones:
								if con.id in caja.id_con:
									contenedor.conexiones.remove(con)

							for nod in contenedor.nodos:
								if nod.id in caja.id_con:
									contenedor.nodos.remove(nod)

							contenedor.cajas.remove(caja)
							for fondo in contenedor.cajas_fondo:
								if fondo.id == caja.id:
									contenedor.cajas_fondo.remove(fondo)

				hit_bola = pygame.sprite.spritecollide(mover, contenedor.bolas, False)
				if hit_bola:
					for bola in contenedor.bolas:
						if bola.rect.collidepoint(pos):
							for con in contenedor.conexiones:
								if con.id in bola.id_con:
									contenedor.conexiones.remove(con)

							for nod in contenedor.nodos:
								if nod.id in bola.id_con:
									contenedor.nodos.remove(nod)

							contenedor.bolas.remove(bola)
							for fondo in contenedor.bolas_fondo:
								if fondo.id == bola.id:
									contenedor.bolas_fondo.remove(fondo)

				x = pos_act[0]-10
				y = pos_act[1]-10
				all_pos = list()
				for i in range(20):
					for j in range(20):
						all_pos.append((x+i, y+j))

				#print(all_pos)
				s1 = set(all_pos)
				for con in contenedor.conexiones:
					#print(con)
					s2 = set(con.puntos)
					s3 = s1.intersection(s2)
					if s3:
						print('colision en', s3)
						for c in contenedor.conexiones:
							if c.id == con.id:
								contenedor.conexiones.remove(c)

						for n in contenedor.nodos:
							if n.id == con.id:
								contenedor.nodos.remove(n)
			
	def dibujar_conexion(self, superficie): # Dibujar conexion en caliente
		pygame.draw.aaline(superficie, NEGRO, self.pos_ini_fict, self.pos_out_fict)

	def agregar_conexion(self, contenedor, cont): # Adicionar conexion a lista de conexiones		
		ini = self.pos_ini_fict
		fin = self.pos_out_fict
		angle = math.atan2(-(fin[1]-ini[1]), fin[0]-ini[0])
		angle = math.degrees(angle)
		if angle <0:
			angle+=360
		self.draw_line = False
		x = abs(fin[0]-ini[0])
		y = abs(fin[1]-ini[1])
		z = math.sqrt(x**2+y**2)
		delta = 1
		z_n = z
		incremento = 0
		total_points = list()
		total_points.append((ini[0], ini[1]))
		for i in range(round(z)):
			incremento += delta
			x_n = round(incremento*math.cos((angle*math.pi)/180))+ini[0]
			y_n = ini[1]-round(incremento*math.sin((angle*math.pi)/180))
			total_points.append((x_n, y_n))

		con = Conexion(cont, self.pos_ini_fict, self.pos_out_fict, total_points) # Crear elemento conexion
		contenedor.conexiones.add(con)

	def agregar_elemento(self, pos, tag, area_trabajo, pos_act, contenedor, name='default'): # Agregar elementos dentro del area de dibujo
		if pygame.MOUSEBUTTONDOWN and area_trabajo.collidepoint(pos_act):
			if tag == 'caja':
				contenedor.cont_cajas+=1
				caja = Caja(pos, contenedor.cont_cajas)				
				hit_caja = pygame.sprite.spritecollide(caja, contenedor.cajas_fondo, False)
				hit_nodo = pygame.sprite.spritecollide(caja, contenedor.nodos_fondo, False)
				hit_limite = pygame.sprite.spritecollide(caja, contenedor.limites_fondo, False)
				hit_modulo = pygame.sprite.spritecollide(caja, contenedor.modulos_fondo, False)
				hit_bola = pygame.sprite.spritecollide(caja, contenedor.bolas_fondo, False)
				hit_cajas_bola = pygame.sprite.spritecollide(caja, contenedor.cajas_bola_fondo, False)
				hit_cajas_knn = pygame.sprite.spritecollide(caja, contenedor.cajas_knn_fondo, False)
				if not hit_caja and not hit_nodo and not hit_limite and not hit_modulo and not hit_bola and not hit_cajas_bola and not hit_cajas_knn:
					contenedor.cajas.add(caja)
					caja_fondo = CajaFondo(pos, contenedor.cont_cajas)
					contenedor.cajas_fondo.add(caja_fondo)
				else:
					contenedor.cont_cajas-=1
			if tag == 'nodo':
				contenedor.cont_nodos+=1
				nodo = Nodo(pos, contenedor.cont_nodos)			
				hit_caja = pygame.sprite.spritecollide(nodo, contenedor.cajas_fondo, False)
				hit_nodo = pygame.sprite.spritecollide(nodo, contenedor.nodos_fondo, False)
				hit_bola = pygame.sprite.spritecollide(nodo, contenedor.bolas_fondo, False)
				if not hit_caja and not hit_nodo and not hit_bola:
					contenedor.nodos.add(nodo)
					nodo_fondo = NodoFondo(pos, contenedor.cont_nodos)
					contenedor.nodos_fondo.add(nodo_fondo)
			if tag == 'conexion':
				linea = Mover(pos)
				hit_caja = pygame.sprite.spritecollide(linea, contenedor.cajas, False)
				if hit_caja:
					for caja in contenedor.cajas:
						if caja.rect.collidepoint(pos):
							self.element_con_ini = caja
				hit_limite = pygame.sprite.spritecollide(linea, contenedor.limites, False)
				if hit_limite:
					for limite in contenedor.limites:
						if limite.rect.collidepoint(pos):
							self.element_con_ini = limite
				hit_nodo = pygame.sprite.spritecollide(linea, contenedor.nodos, False)
				if hit_nodo:
					for nodo in contenedor.nodos:
						if nodo.rect.collidepoint(pos):
							self.element_con_ini = nodo
				hit_bola = pygame.sprite.spritecollide(linea, contenedor.bolas, False)
				if hit_bola:
					for bola in contenedor.bolas:
						if bola.rect.collidepoint(pos):
							self.element_con_ini = bola
				hit_modulo = pygame.sprite.spritecollide(linea, contenedor.modulos, False)
				if hit_modulo:
					for modulo in contenedor.modulos:
						if modulo.rect.collidepoint(pos):
							self.element_con_ini = modulo			
				if self.always_draw or hit_caja or hit_nodo or hit_bola or hit_modulo or hit_limite:
					self.pos_ini_fict = self.pos_out_fict # Linea en caliente
					self.draw_line = True
					self.always_draw = True

			if tag == 'bola':
				contenedor.cont_bolas+=1
				bola = Bola(pos, contenedor.cont_bolas)
				hit_caja = pygame.sprite.spritecollide(bola, contenedor.cajas_fondo, False)
				hit_nodo = pygame.sprite.spritecollide(bola, contenedor.nodos_fondo, False)
				hit_limite = pygame.sprite.spritecollide(bola, contenedor.limites_fondo, False)
				hit_modulo = pygame.sprite.spritecollide(bola, contenedor.modulos_fondo, False)
				hit_bola = pygame.sprite.spritecollide(bola, contenedor.bolas_fondo, False)
				hit_cajas_bola = pygame.sprite.spritecollide(bola, contenedor.cajas_bola_fondo, False)
				hit_cajas_knn = pygame.sprite.spritecollide(bola, contenedor.cajas_knn_fondo, False)
				if not hit_caja and not hit_nodo and not hit_limite and not hit_modulo and not hit_bola and not hit_cajas_bola and not hit_cajas_knn:					
					contenedor.bolas.add(bola)
					contenedor.cajas_bola.add(bola.caja_1)
					contenedor.cajas_bola.add(bola.caja_2)
					bola_fondo = BolasFondo(pos, contenedor.cont_bolas)
					contenedor.bolas_fondo.add(bola_fondo)
					contenedor.cajas_bola_fondo.add(bola.fondo_caja_1)
					contenedor.cajas_bola_fondo.add(bola.fondo_caja_2)
				else:
					contenedor.cont_bolas-=1

			if tag == 'knn':
				contenedor.cont_knn+=1
				knn = CajaKnn(pos, contenedor.cont_knn)
				hit_caja = pygame.sprite.spritecollide(knn, contenedor.cajas_fondo, False)
				hit_nodo = pygame.sprite.spritecollide(knn, contenedor.nodos_fondo, False)
				hit_limite = pygame.sprite.spritecollide(knn, contenedor.limites_fondo, False)
				hit_modulo = pygame.sprite.spritecollide(knn, contenedor.modulos_fondo, False)
				hit_bola = pygame.sprite.spritecollide(knn, contenedor.bolas_fondo, False)
				hit_knn = pygame.sprite.spritecollide(knn, contenedor.knn_fondo, False)
				hit_cajas_bola = pygame.sprite.spritecollide(knn, contenedor.cajas_bola_fondo, False)
				hit_cajas_knn = pygame.sprite.spritecollide(knn, contenedor.cajas_knn_fondo, False)
				if not hit_caja and not hit_nodo and not hit_limite and not hit_modulo and not hit_bola and not hit_cajas_bola and not hit_cajas_knn and not hit_knn:
					contenedor.knn.add(knn)
					contenedor.cajas_knn.add(knn.caja_1)
					contenedor.cajas_knn.add(knn.caja_2)
					contenedor.cajas_knn_fondo.add(knn.fondo_caja_1)
					contenedor.cajas_knn_fondo.add(knn.fondo_caja_2)
				else:
					contenedor.cont_knn-=1

			if tag == 'modulo':
				modulo = Modulo(pos, name)
				hit_caja = pygame.sprite.spritecollide(modulo, contenedor.cajas_fondo, False)
				hit_nodo = pygame.sprite.spritecollide(modulo, contenedor.nodos_fondo, False)
				hit_limite = pygame.sprite.spritecollide(modulo, contenedor.limites_fondo, False)
				hit_modulo = pygame.sprite.spritecollide(modulo, contenedor.modulos_fondo, False)
				if not hit_caja and not hit_nodo and not hit_limite and not hit_modulo:
					contenedor.modulos.add(modulo)
					modulo_fondo = ModuloFondo(pos, name)
					contenedor.modulos_fondo.add(modulo_fondo)

	def dibujar_elementos(self, pantalla, contenido, show_danger):
		if len(contenido.conexiones)>0:
			for _, linea in enumerate(contenido.conexiones):				
				pygame.draw.aaline(pantalla, (0, 0, 0), linea.ini, linea.fin)

		if len(contenido.cajas)>0: # Dibujar cajas
			if show_danger: # Enseñar zonas prohibidas
				for fondo_caja in contenido.cajas_fondo:
					fondo_caja.dibujar(pantalla)
			for caja in contenido.cajas:
				caja.dibujar(pantalla)

		if len(contenido.bolas)>0: # Dibujar bolas
			if show_danger:
				for fondo_bola in contenido.bolas_fondo:
					fondo_bola.dibujar(pantalla)
			for bola in contenido.bolas:
				bola.dibujar(pantalla, show_danger)

		if len(contenido.knn)>0:
			for knn in contenido.knn:
				knn.dibujar(pantalla, show_danger)

		if len(contenido.nodos)>0: # Dibujar nodos
			if show_danger: # Enseñar zonas prohibidas
				for fondo_nodo in contenido.nodos_fondo:
					fondo_nodo.dibujar(pantalla)
			for nodo in contenido.nodos:
				nodo.dibujar(pantalla)
		if len(contenido.limites)>0:
			if show_danger:
				for fondo_limite in contenido.limites_fondo:
					fondo_limite.dibujar(pantalla)
			for limite in contenido.limites:
				limite.dibujar(pantalla)

		if len(contenido.modulos)>0:
			if show_danger:
				for fondo_modulo in contenido.modulos_fondo:
					fondo_modulo.dibujar(pantalla)
			for modulo in contenido.modulos:
				modulo.dibujar(pantalla)

		"""if len(contenido.conexiones)>0:
			for circ in contenido.conexiones:
				for con in circ.puntos:
					pygame.draw.circle(pantalla, (255, 0, 0), con, 3, 0)"""

	@staticmethod
	def round_base(posx, posy, base=20):
		outx = (base*round(posx/base))
		outy = (base*round(posy/base))		
		out = (outx, outy)
		return out