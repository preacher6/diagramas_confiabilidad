 #!/usr/bin/python env

import pygame 
import sys
import os
import math
import sqlite3
import pickle
import easygui as eg 
from pygame.locals import *
from propiedades import *
from elementos import Nodo, Caja, CajaFondo
from items import Items
from acciones import Mover

COLOR_FONDO = (232, 195, 158)

def main():
	pygame.init() # Inicializa modulo pygame
	os.environ['SDL_VIDEO_CENTERED'] = '1' # Centra la interfaz
	DIMENSION_VENTANA = [1000, 700] # Dimensiones de la interfaz
	pantalla = pygame.display.set_mode(DIMENSION_VENTANA) # Define la pantalla
	pygame.display.set_caption("Diagramas confiabilidad")
	reloj = pygame.time.Clock()
	font = pygame.font.SysFont('Arial', 15)	
	#------------------------------------------
	prop = Propiedades(pantalla)
	item = Items()
	#--------------------------------------
	pos_pres = (0, 0) # Inicializar posicion presionad
	desp = [0, 0] 
	hold_consultar = False # Sostener consultas
	hold_acciones = False # Sostener acciones
	show_danger = False # Enseñar zonas prohibidas
	close = False # Cerrar intefaz
	erase = pygame.Surface((1000, 1000))
	erase.fill((255, 255, 255))
	stop = False # Auxiliar para continuar dibujando
	hold_move = False
	active = True
	pestañas = pygame.sprite.Group()
	stand_by = pygame.sprite.Group()
	kdn = pygame.sprite.Group()
	cont_pestana = 1
	tag_pestaña = 1
	conte_1 = Contenedor((90, 120), cont_pestana, tag_pestaña)
	contenido = conte_1 # Aca se enseña la pestaña q esta activa
	pestañas.add(conte_1)
	pressed = True
	archivo_modulos = 'data_mod.txt'
	archivo_all = 'data_all.txt'
	try: # Cargar modulos
		with open(archivo_modulos, 'rb') as fp:
			data_mod = pickle.load(fp)
			lista_modulos = data_mod['lista_modulos']
			lista_nombres = data_mod['lista_nombres']
	except:
		print('No hay modulos que cargar')
		lista_modulos = list()
		lista_nombres = list()
	try: # Cargar archivos almacenados
		with open(archivo_modulos, 'rb') as fp:
			data_mod = pickle.load(fp)
			lista_modulos = data_mod['lista_modulos']
			lista_nombres = data_mod['lista_nombres']
	except:
		print('No hay archivos que cargar')
		all_data = {}
	lista_total = list()
	lista_opciones = list()
	lista_opciones.append('1. Stand By')
	lista_opciones.append('2. Inicial')
	lista_opciones.append('3. Final')
	default_name = None
	timer = 0
	dt = 0
	cont_conec = 1 # Conexion actual
	while not close: # Loop
		keys = pygame.key.get_pressed() # Obtencion de tecla presionada
		for evento in pygame.event.get():
			if evento.type == pygame.QUIT:
				close = eg.ynbox(msg='¿Desea salir?',
					title='Salir',
					choices=('Si', 'No'),
					image=None)
			elif evento.type == pygame.MOUSEBUTTONDOWN or keys[K_ESCAPE] or keys[K_n]:
				pos_pres = pygame.mouse.get_pos()
				if timer == 0:
					timer = 0.001
				elif timer < 0.5: # Doble click apertura modulo
					if len(contenido.modulos)>0: # Apertura modulo
						for mod in contenido.modulos:
							if mod.rect.collidepoint(pos_pres):
								inside = False
								for pes in pestañas:
									if pes.name == mod.tag:
										pes.selected = True
										inside = True
									else:
										pes.selected = False

								if inside == False: # Pestaña cerrada, se abre en nueva pestaña
									print(cont_pestana)
									cont_pestana += 1
									for l_m in lista_modulos:
										if l_m.name == mod.tag:
											contenido = l_m
											print(contenido)
											contenido.cont = cont_pestana
											contenido.selected = True
											pestañas.add(contenido)

					if len(contenido.cajas)>0: # Apertura caja
						punto = Nodo(pos_pres, 1)
						hit_caja = pygame.sprite.spritecollide(punto, contenido.cajas, False)
						if hit_caja:
							campos = ['Tasa de fallo:', 'Nombre elemento:']
							valores = list()
							for caja in contenido.cajas:
								if caja.rect.collidepoint(pos_pres):
									valores.append(caja.tasa)
									valores.append(caja.tag)
									datos = eg.multenterbox(msg='Entrada múltiple',
															title='Control: multenterbox',
															fields=campos, values=(valores))
									if not datos:
										pass
									else:
										caja.tasa = datos[0]
										caja.tag = datos[1]

					if len(contenido.cajas_bola)>0:
						punto = Nodo(pos_pres, 1)
						hit_cajas_bola = pygame.sprite.spritecollide(punto, contenido.cajas_bola, False)
						if hit_cajas_bola:
							campos = ['Tasa de fallo:', 'Nombre elemento:']
							valores = list()
							for caja in contenido.cajas_bola:
								if caja.rect.collidepoint(pos_pres):
									print(caja.tag)
									valores.append(caja.tasa)
									valores.append(caja.tag)
									datos = eg.multenterbox(msg='Entrada múltiple',
															title='Control: multenterbox',
															fields=campos, values=(valores))
									if not datos:
										pass
									else:
										caja.tasa = datos[0]
										caja.tag = datos[1]

					if len(contenido.cajas_bola)>0:
						punto = Nodo(pos_pres, 1)
						hit_cajas_bola = pygame.sprite.spritecollide(punto, contenido.cajas_bola, False)
						if hit_cajas_bola:
							campos = ['Tasa de fallo:', 'Nombre elemento:']
							valores = list()
							for caja in contenido.cajas_bola:
								if caja.rect.collidepoint(pos_pres):
									print(caja.tag)
									valores.append(caja.tasa)
									valores.append(caja.tag)
									
									datos = eg.multenterbox(msg='Entrada múltiple',
															title='Control: multenterbox',
															fields=campos, values=(valores))
									if not datos:
										pass
									else:
										caja.tasa = datos[0]
										caja.tag = datos[1]										

					if len(contenido.cajas_knn)>0:
						punto = Nodo(pos_pres, 1)
						hit_cajas_knn = pygame.sprite.spritecollide(punto, contenido.cajas_knn, False)
						if hit_cajas_knn:
							campos = ['Tasa de fallo:', 'Nombre elemento:', 'Habilitado:']
							valores = list()
							for caja in contenido.cajas_knn:
								if caja.rect.collidepoint(pos_pres):
									if caja.enable == 'H':
										print(caja.tag)
										valores.append(caja.tasa)
										valores.append(caja.tag)
										valores.append(caja.enable)
										datos = eg.multenterbox(msg='Entrada múltiple',
																title='Control: multenterbox',
																fields=campos, values=(valores))
										if not datos:
											pass
										else:
											caja.tasa = datos[0]
											caja.tag = datos[1]
											caja.enable = datos[2]

					timer = 0
				#---------------- FIN DOBLE CLICK -----------------------
				if pygame.mouse.get_pressed()[2]: #-------- Derecho ----------------------#
					punto = Nodo(pos_pres, 1)
					hit_caja = pygame.sprite.spritecollide(punto, contenido.cajas, False)
					if hit_caja:
						for caja in contenido.cajas:
							if caja.rect.collidepoint(pos_pres):
								opcion = eg.indexbox(msg='Tipo de confiabilidad:',
														title='Control: indexbox',
														choices=('Exponencial', 'Rayleigh', 'Weibull'),
														image=None)
								caja.mod = opcion

					hit_bola = pygame.sprite.spritecollide(punto, contenido.bolas, False)
					if hit_bola:
						for bola in contenido.bolas:
							if bola.rect.collidepoint(pos_pres):
								num = eg.integerbox(msg='Número de cajas (2-5):',
													title='Ingreso datos',
													default=len(bola.cajas),
													lowerbound=2,
													upperbound=5,
													image=None)
								if len(bola.cajas) ==  num:
									pass
								elif num > len(bola.cajas): # Agregar cajas
									dif = num-len(bola.cajas)									
									for i in range(dif):
										if (bola.max_h-bola.rest_h < 100):
											eg.msgbox(msg='Un máximo de '+str(len(bola.cajas))+' cajas permitidas en el espacio solicitado',
													title='Advertencia', 
													ok_button='Continuar',
													image=None)
											break
										bola.aum += 100
										bola.rest_h += 100
										bola.cajas_fin = bola.cajas_fin+100
										caja = Caja((bola.pos[0]+80, bola.pos[1]+bola.cajas_fin), len(bola.cajas)+1)
										fondo_caja = CajaFondo((bola.pos[0]+80, bola.pos[1]+bola.cajas_fin), len(bola.cajas)+1)								
										bola.cajas.add(caja)
										bola.fondos_cajas.add(fondo_caja)
										bola.con_propia_ini.append((bola.pos[0]+180, bola.pos[1]+bola.aum))
										bola.con_propia_fin.append((bola.pos[0]+180, bola.pos[1]+100+bola.aum))
										bola.con_propia_ini.append((bola.pos[0]+180, bola.pos[1]+100+bola.aum))
										bola.con_propia_fin.append((bola.pos[0]+160, bola.pos[1]+100+bola.aum))
								elif num < len(bola.cajas): # Eliminar cajas
									dif = len(bola.cajas)-num
									for i in range(dif):
										for caja in bola.cajas:
											if caja.id == len(bola.cajas):
												bola.cajas.remove(caja)
												bola.cajas_fin = bola.cajas_fin-100
												bola.aum -= 100
												bola.rest_h -= 100
												del bola.con_propia_ini[-1]
												del bola.con_propia_ini[-1]
												del bola.con_propia_fin[-1]
												del bola.con_propia_fin[-1]
												break

					hit_knn = pygame.sprite.spritecollide(punto, contenido.knn, False)
					if hit_knn: # Agregar/Quitar cajas KNN
						for knn in contenido.knn:
							if knn.rect.collidepoint(pos_pres):
								num = eg.integerbox(msg='Número de cajas (2-5):',
													title='Ingreso datos',
													default=len(knn.cajas),
													lowerbound=2,
													upperbound=5,
													image=None)
								if len(knn.cajas) ==  num:
									pass
								elif num > len(knn.cajas): # Agregar cajas
									dif = num-len(knn.cajas)									
									for i in range(dif):
										if (knn.max_h-knn.rest_h < 100):
											eg.msgbox(msg='Un máximo de '+str(len(knn.cajas))+' cajas permitidas en el espacio solicitado',
													title='Advertencia', 
													ok_button='Continuar',
													image=None)
											break
										knn.aum += 100
										knn.rest_h += 100
										knn.cajas_fin = knn.cajas_fin+100
										caja = Caja((knn.pos[0]+20, knn.pos[1]+knn.cajas_fin), len(knn.cajas)+1)
										fondo_caja = CajaFondo((knn.pos[0]+20, knn.pos[1]+knn.cajas_fin), len(knn.cajas)+1)								
										knn.cajas.add(caja)
										knn.fondos_cajas.add(fondo_caja)
										knn.con_izq_ini.append((knn.pos[0], knn.pos[1]+knn.aum))
										knn.con_izq_fin.append((knn.pos[0], knn.pos[1]+140+knn.aum))
										knn.con_izq_ini.append((knn.pos[0], knn.pos[1]+140+knn.aum))
										knn.con_izq_fin.append((knn.pos[0]+20, knn.pos[1]+140+knn.aum))
										knn.con_der_ini.append((knn.pos[0]+120, knn.pos[1]+knn.aum))
										knn.con_der_fin.append((knn.pos[0]+120, knn.pos[1]+140+knn.aum))
										knn.con_der_ini.append((knn.pos[0]+120, knn.pos[1]+140+knn.aum))
										knn.con_der_fin.append((knn.pos[0]+100, knn.pos[1]+140+knn.aum))
								elif num < len(knn.cajas): # Eliminar cajas
									dif = len(knn.cajas)-num
									for i in range(dif):
										for caja in knn.cajas:
											if caja.id == len(knn.cajas):
												knn.cajas.remove(caja)
												knn.cajas_fin = knn.cajas_fin-100
												knn.aum -= 100
												knn.rest_h -= 100
												del knn.con_der_ini[-1]
												del knn.con_der_fin[-1]
												del knn.con_der_ini[-1]
												del knn.con_der_fin[-1]
												del knn.con_izq_ini[-1]
												del knn.con_izq_fin[-1]
												del knn.con_izq_ini[-1]
												del knn.con_izq_fin[-1]
												break

				if item.draw_line == True and pygame.mouse.get_pressed()[0]: # Dibujar punto final de conexion
					nodo = []
					for con in contenido.conexiones: # Agregar nodo en conexion
						if item.pos_out_fict in con.puntos: # Si el limite de la conexion actual existe dentro de otra conexion
								nodo = Nodo(item.pos_out_fict, con.id)
								contenido.nodos.add(nodo)
								stop = True	
								item.always_draw = False
								item.agregar_conexion(contenido, con.id)
								for conec in contenido.conexiones:
									if conec.id == cont_conec:
										conec.id = con.id

					if not nodo: # Agregar punto final de conexion
						item.agregar_conexion(contenido, cont_conec)
						punto = Nodo(item.pos, 1)
						hit_caja = pygame.sprite.spritecollide(punto, contenido.cajas, False)
						hit_nodo = pygame.sprite.spritecollide(punto, contenido.nodos, False)
						hit_bola = pygame.sprite.spritecollide(punto, contenido.bolas, False)
						if hit_nodo or hit_caja or hit_bola:
							if hit_caja: # Elemento final caja
								for caja in contenido.cajas:
									if caja.rect.collidepoint(pos_pres):
										item.element_con_fin = caja
								for con in contenido.conexiones:
									if con.id == cont_conec:
										item.element_con_fin.conexiones.add(con)
										item.element_con_ini.conexiones.add(con)
										item.element_con_fin.id_con.append(con.id)
										item.element_con_ini.id_con.append(con.id)

							if hit_nodo: # Elemento final nodo
								for nodo in contenido.nodos:
									if nodo.rect.collidepoint(pos_pres):
										item.element_con_fin = nodo
								for con in contenido.conexiones:
									if con.id == cont_conec:
										item.element_con_fin.conexiones.add(con)
										item.element_con_ini.conexiones.add(con)
										item.element_con_fin.id_con.append(con.id)
										item.element_con_ini.id_con.append(con.id)

								if hit_bola: # Elemento final bola
									for bola in contenido.nodos:
										if bola.rect.collidepoint(pos_pres):
											item.element_con_fin = bola
									for con in contenido.conexiones:
										if con.id == cont_conec:
											item.element_con_fin.conexiones.add(con)
											item.element_con_ini.conexiones.add(con)
											item.element_con_fin.id_con.append(con.id)
											item.element_con_ini.id_con.append(con.id)

							cont_conec+=1 # Contador de conexiones
							stop = True	
							item.always_draw = False

				if pygame.mouse.get_pressed()[0]:
					if item.move_element == True: # Posicionar elemento
						hit_caja = pygame.sprite.spritecollide(item.element_selected, contenido.cajas_fondo, False)
						if len(hit_caja)<=1: # Verificar si colisiona con otra caja
							item.move_element = False
							item.element_selected = None
							hold_move = True
							hold_acciones = False

					if hold_consultar == True and item.draw_line==False and stop == False: # Agregar elemento
						item.agregar_elemento(item.pos, tag, recta_trabajo, pos_act, contenido, default_name)

					if hold_acciones == True: # Ejecutar accion
						item.ejecutar_acciones(item.pos, recta_trabajo, pos_pres, contenido, tag)

					if prop.recta_caja.collidepoint(pos_pres): # Elegir elemento caja
						hold_consultar = True
						recta_trabajo = pygame.Rect(80, 170, 800, 420)
						tag = 'caja'
					if prop.recta_bola.collidepoint(pos_pres): # Elegir elemento nodo
						hold_consultar = True
						recta_trabajo = pygame.Rect(100, 190, 720, 320)
						tag = 'bola'
					if prop.recta_knn.collidepoint(pos_pres):
						hold_consultar = True
						recta_trabajo = pygame.Rect(100, 170, 720, 300)
						tag = 'knn'
					if prop.recta_conexion.collidepoint(pos_pres): # Elegir elemento conexion
						hold_consultar = True
						recta_trabajo = pygame.Rect(80, 170, 860, 480)
						tag = 'conexion'
					if prop.recta_mover.collidepoint(pos_pres):
						hold_consultar = True
						hold_acciones = True
						recta_trabajo = pygame.Rect(80, 170, 860, 480)
						tag = 'mover'
					if prop.recta_borrar.collidepoint(pos_pres):
						hold_consultar = True
						hold_acciones = True
						recta_trabajo = pygame.Rect(80, 170, 860, 480)
						tag = 'borrar'
					if prop.recta_export.collidepoint(pos_pres): # Almacenar modulo
						if contenido.inicial_full and contenido.final_full:
							nombre_contenedor = eg.enterbox(msg='Nombre de módulo:',
									title='Almacenar módulo',
									default=contenido.name, strip=True,
									image=None)
							for p in pestañas:
								if p.selected == True:
									p.name = nombre_contenedor
									lista_modulos.append(p)
									lista_nombres.append(p.name)

							data_mod = {'lista_modulos': lista_modulos, 'lista_nombres': lista_nombres, 'item': item,
									}

							with open(archivo_modulos, 'wb') as fp:
								pickle.dump(data_mod, fp)
						else:
							eg.msgbox(msg='El módulo debe poseer un nodo inicial y uno final',
											title='Advertencia', 
											ok_button='Continuar',
											image=None)

					if prop.recta_import.collidepoint(pos_pres):
						nombre_contenedor = eg.choicebox(msg='Seleccionar un módulo:',
								title='Archivo',
								choices=(lista_nombres))
						for p in lista_modulos:
							if p.name == nombre_contenedor:
								hold_consultar = True
								recta_trabajo = pygame.Rect(80, 170, 800, 420)
								tag = 'modulo'
								default_name = p.name
								break
						print(nombre_contenedor)
					if conte_1.recta_new.collidepoint(pos_pres) and cont_pestana<7:
						cont_pestana += 1
						tag_pestaña += 1
						conte = Contenedor((90, 120), cont_pestana, tag_pestaña)
						pestañas.add(conte)
						for pestaña in pestañas:
							if cont_pestana != pestaña.cont:
								pestaña.selected = False

					if hold_move == True:
						hold_move = False
						hold_acciones = True

					if prop.recta_grid.collidepoint(pos_pres):
						active = prop.activar_grid(active)
					if prop.recta_danger.collidepoint(pos_pres):
						show_danger = prop.danger_zone(show_danger)
					pressed = True
					stop = False
				
				if keys[K_ESCAPE]: # Presionar tecla escape
					if item.always_draw == True:
						for c in contenido.conexiones:
							if c.id == cont_conec:
								contenido.conexiones.remove(c)
					hold_consultar = False
					pygame.mouse.set_visible(True)
					item.draw_line = False
					item.waiting_end = False
					hold_acciones = False
					hold_move = False # Auxiliar para continuar moviendo mas de un objeto
					item.always_draw = False

		if timer != 0:
			timer+=dt
			if timer >=0.5:
				timer = 0
		pos_act = pygame.mouse.get_pos() # Posicion en que se encuentra el cursor
		
		pantalla.fill(COLOR_FONDO) # Rellenar pantall de color predeterminado
		#------------ Dibujar sobre pantalla-----------------
		# Borrar todo
		if keys[K_r] and tag == 'borrar':
			contenido.cajas.empty()
			contenido.cajas_fondo.empty()
			contenido.bolas.empty()
			contenido.bolas_fondo.empty()
			contenido.conexiones.empty()
		prop.dibujar_area(pantalla, active) # Dibujar area de trabajo sobre superficie
		prop.dibujar_panel(pantalla) # Dibujar panel de elementos
		if item.out == True:
			hold_consultar = False
			item.out = False
			pygame.mouse.set_visible(True)

		for i, pesta in enumerate(pestañas): # Dibujar pestañas
			pesta.dibujar(pantalla)
			if pesta.selected == True:
				contenido = pesta
			if len(pestañas)>1:
				if pesta.recta_close.collidepoint(pos_pres) and pressed == True:
					pestañas.remove(pesta)
					cont_pestana-=1
					pressed = False					

					for p in pestañas: # Renombrar pestañas en caso de borrar una
						if p.cont > pesta.cont:
							p.cont -= 1
							if pesta.selected == True:
								p.selected = True
								pesta.selected = False

					if pesta.selected == True:
						for p in pestañas:
							if p.cont == cont_pestana:
								p.selected = True
								break
				if pesta.rect.collidepoint(pos_pres) and pressed == True:
					pesta.selected = True
					for p in pestañas:
						if p.name != pesta.name:
							p.selected = False

		if len(pestañas)==0:
			conte_1 = Contenedor((90, 120), cont_pestana)
			pestañas.add(conte_1)
		
		conte_1.dibujar_new(pantalla, cont_pestana)
		if item.draw_line == True: # Dibujar conexion
			item.dibujar_conexion(pantalla)
		if item.move_element == True: # desplazar elemento seleccionadob
			item.element_selected.rect.center = (item.pos[0]+15, item.pos[1]+15)
			item.fondo_selected.rect.center = (item.pos[0]+15, item.pos[1]+15)
			item.element_selected.pos = (item.element_selected.rect.x, item.element_selected.rect.y)
			#for con in item.element_selected:
				#print(con.id)
		
		item.dibujar_elementos(pantalla, contenido, show_danger)

		if hold_consultar == True: # Consultar item elegido
			item.consultar(pos_act, desp, pantalla, tag, recta_trabajo)

		# Acciones pygame
		reloj.tick(60)
		dt = reloj.tick(30) / 1000
		pygame.display.flip()

if __name__.endswith('__main__'):
	main()
