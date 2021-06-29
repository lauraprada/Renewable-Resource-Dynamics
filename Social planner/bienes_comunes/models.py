import random
# import itertools
from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
	)

from django import forms


authors = 'Alfredo Orozco, Darwin Cortés, César Mantilla'

doc = """
Esta es una implementación virtual del experimento clásico de dilema de los comunes.
En particular, esta versión está inspirada en el paper:

Hopfensitz, A., Mantilla, C., & Miquel-Florensa, J. (2018). 
Catch Uncertainty and Reward Schemes in a Commons Dilemma: 
An Experimental Study. Environmental and Resource Economics, (6), 1–33. 
https://doi.org/10.1007/s10640-018-0241-0
"""


class Constants(BaseConstants):
	
	indicadora_planificador_central = True

	# Constantes de configuración básica de la aplicación
	name_in_url = 'bienes_comunes'
	
	if (indicadora_planificador_central):
		players_per_group = None
	else:
		players_per_group = 4
	
	num_rounds = 10

	# Constantes para identificar los 4 tratamientos.
	# Permutaciones de: precios fijos vs condicionales
	# y función de prod. determinística vs estocástica
	tra_fixed_determ = 1
	tra_fixed_stoch = 2
	tra_cond_determ = 3
	tra_cond_stoch = 4

	# Constantes específicas del juego

	if (indicadora_planificador_central):
		barcos_por_jugador = 12
		decision_minima_barcos = 4
		choices_list = [4,5,6,7,8,9,10,11,12]
	else:
		barcos_por_jugador = 3
		decision_minima_barcos = 1
		choices_list = [1,2,3]
	
	tasa_crecimiento_intrinseca_r = 1/3
	capacidad_de_carga_recurso_K = 100
	capturas_dia_bueno_por_barco = 5
	capturas_dia_regular_por_barco = 3
	capturas_dia_malo_por_barco = 1
	probabilidad_dia_bueno = 1/3
	probabilidad_dia_regular = 1/3
	probabilidad_dia_malo = 1 - probabilidad_dia_bueno - probabilidad_dia_regular
	captura_por_barco_determinado = 3
	precio_por_unidad_caso_fijo = c(2)


class Subsession(BaseSubsession):
	# Métodos y funciones

	def inicializar_atributos_grupo(self, p_grupos):
		for grupo in p_grupos:
			grupo.inicializar_atributos_grupo(0, 0, 0)


	def inicializar_barcos(self, p_grupos):
		for g in p_grupos:
			g.inicializar_barcos(Constants.barcos_por_jugador)

	def asignar_tratamientos(self, p_grupos, p_tratamiento):
		if p_tratamiento != 'RANDOM':
			# Se asignó deterministico
			for g in p_grupos:
				if (p_tratamiento == 'fixed_determ'):
					g.fijar_tratamiento(Constants.tra_fixed_determ)
				elif (p_tratamiento == 'fixed_stock'):
					g.fijar_tratamiento(Constants.tra_fixed_stoch)
				elif (p_tratamiento == 'cond_determ'):
					g.fijar_tratamiento(Constants.tra_cond_determ)
				elif (p_tratamiento == 'cond_stock'):
					g.fijar_tratamiento(Constants.tra_cond_stoch)
				else:
					print('ERROR, EL TRATAMIENTO SE ASIGNÓ MALLLL!!!')
		else:
			# Se asigna aleatorio
			print('Tratamiento se asigna aleatoriamente')
			for g in p_grupos:
				trata = random.choice([Constants.tra_fixed_determ, Constants.tra_fixed_stoch, Constants.tra_cond_determ, Constants.tra_cond_stoch])
				g.fijar_tratamiento(trata)

	def recordar_tratamientos(self, p_grupos):
		for g in p_grupos:
			g.recordar_tratamientos()

	def imprimir_espacio_abrir(self):
		print('*********************************************')
		print('*********************************************')
		print('* * * * * * * * * * * * * * * * * * * * * * *')
		print(' * * * * * * * * * * * * * * * * * * * * * * ')
		print('* * * * * * * * * * * * * * * * * * * * * * *')
		print(' * * * * * * * * * * * * * * * * * * * * * * ')

	def imprimir_espacio_cerrar(self):
		print('* * * * * * * * * * * * * * * * * * * * * * *')
		print(' * * * * * * * * * * * * * * * * * * * * * * ')
		print('* * * * * * * * * * * * * * * * * * * * * * *')
		print(' * * * * * * * * * * * * * * * * * * * * * * ')
		print('*********************************************')
		print('*********************************************')


	def creating_session(self):
		
		# Inicializando constantes desde archivo de configuraciones
		# Constantes específicas del juego
		'''
		Constants.num_rounds = self.session.config['repeticiones_maximas_del_juego']
		Constants.barcos_por_jugador = 12/(self.session.config['num_demo_participants'])
		Constants.tasa_crecimiento_intrinseca_r = self.session.config['tasa_crecimiento_intrinseca_r']
		Constants.capacidad_de_carga_recurso_K = self.session.config['capacidad_de_carga_recurso_K']
		Constants.capturas_dia_bueno_por_barco = self.session.config['capturas_dia_bueno_por_barco']
		Constants.capturas_dia_regular_por_barco = self.session.config['capturas_dia_regular_por_barco']
		Constants.capturas_dia_malo_por_barco = self.session.config['capturas_dia_malo_por_barco']
		Constants.probabilidad_dia_bueno = self.session.config['probabilidad_dia_bueno']
		Constants.probabilidad_dia_regular = self.session.config['probabilidad_dia_regular']
		Constants.probabilidad_dia_malo = 1 - Constants.probabilidad_dia_bueno - Constant.probabilidad_dia_regular
		Constants.captura_por_barco_determinado = self.session.config['captura_por_barco_determinado']
		Constants.precio_por_unidad_caso_fijo = c(self.session.config['precio_por_unidad_caso_fijo'])
		'''

		# Experimento personal, no cambia nada en el juego la siguiente línea:
		# self.probarAleatorizaciones(80000)

		grupos = self.get_players()
		self.inicializar_atributos_grupo(grupos)
		self.inicializar_barcos(grupos)

		if self.round_number == 1:
			if (self.session.config['indicadora_tratamiento_precio_fijo'] == -99 or self.session.config['indicadora_tratamiento_captura_deterministica'] == -99):
				self.imprimir_espacio_abrir()
				print('	ALGUNO DE LOS TRATAMIENTOS SE ASIGNÓ EN MISSING (-99), TRATAMIENTOS ALEATORIZADOS.')
				self.imprimir_espacio_cerrar()

				if 'treatment' in self.session.config:
					# Aquí se asigna tratamiento
					self.asignar_tratamientos(grupos, self.session.config['treatment'])
				else:
					# Random assignment
					self.asignar_tratamientos(grupos, 'RANDOM')
				

				print('[Experimentador]: Se asignaron los tratamientos a los grupos')
			elif (self.session.config['indicadora_tratamiento_precio_fijo'] == 1 and self.session.config['indicadora_tratamiento_captura_deterministica'] == 1):
				for gr in grupos:
					gr.fijar_tratamiento(Constants.tra_fixed_determ)
				self.imprimir_espacio_abrir()
				print('	Se asignó tratamiento precio fijo, captura determinística.')
				self.imprimir_espacio_cerrar()
			elif (self.session.config['indicadora_tratamiento_precio_fijo'] == 1 and self.session.config['indicadora_tratamiento_captura_deterministica'] == 0):
				for gr in grupos:
					gr.fijar_tratamiento(Constants.tra_fixed_stoch)
				self.imprimir_espacio_abrir()
				print(' Se asignó tratamiento precio fijo, captura estocástica.')
				self.imprimir_espacio_cerrar()
			elif (self.session.config['indicadora_tratamiento_precio_fijo'] == 0 and self.session.config['indicadora_tratamiento_captura_deterministica'] == 1):
				for gr in grupos:
					gr.fijar_tratamiento(Constants.tra_cond_determ)
				self.imprimir_espacio_abrir()
				print(' Se asignó tratamiento precio condicional, captura determinística.')
				self.imprimir_espacio_cerrar()
			elif (self.session.config['indicadora_tratamiento_precio_fijo'] == 0 and self.session.config['indicadora_tratamiento_captura_deterministica'] == 0):
				for gr in grupos:
					gr.fijar_tratamiento(Constants.tra_cond_stoch)
				self.imprimir_espacio_abrir()
				print(' Se asignó tratamiento precio condicional, captura estocástica.')
				self.imprimir_espacio_cerrar()

			for g in grupos:
				g.stock = Constants.capacidad_de_carga_recurso_K
				print('[Experimentador]: Se inició con la capacidad de carga del recurso')

		# Cada ronda hay que recordarle al grupo cuál es su tratamiento
		self.recordar_tratamientos(grupos)
	'''
	def probarAleatorizaciones(self, p_repeticiones):
		# Como está
		listaRandom = []
		listaIterator = []
		contador_uno = 0
		contador_dos = 0
		contador_tres = 0
		contador_cuatro = 0

		contador_uno_i = 0
		contador_dos_i = 0
		contador_tres_i = 0
		contador_cuatro_i = 0

		# Generación de tratamientos
		for n in range(p_repeticiones):
			trata = random.choice([Constants.tra_fixed_determ, Constants.tra_fixed_stoch, Constants.tra_cond_determ, Constants.tra_cond_stoch])
			listaRandom.append(trata)

		for n in range(p_repeticiones):
			tratamientos = itertools.cycle([Constants.tra_fixed_determ, Constants.tra_fixed_stoch, Constants.tra_cond_determ, Constants.tra_cond_stoch])
			trata = next(tratamientos)
			listaIterator.append(trata)

		# Contando:

		for a in range(len(listaRandom)):
			if listaRandom[a] == Constants.tra_fixed_determ:
				contador_uno = contador_uno + 1
			elif listaRandom[a] == Constants.tra_fixed_stoch:
				contador_dos = contador_dos + 1
			elif listaRandom[a] == Constants.tra_cond_determ:
				contador_tres = contador_tres + 1
			elif listaRandom[a] == Constants.tra_cond_stoch:
				contador_cuatro = contador_cuatro + 1

		for a in range(len(listaRandom)):
			if listaIterator[a] == Constants.tra_fixed_determ:
				contador_uno_i = contador_uno_i + 1
			elif listaIterator[a] == Constants.tra_fixed_stoch:
				contador_dos_i = contador_dos_i + 1
			elif listaIterator[a] == Constants.tra_cond_determ:
				contador_tres_i = contador_tres_i + 1
			elif listaIterator[a] == Constants.tra_cond_stoch:
				contador_cuatro_i = contador_cuatro_i + 1
		
		# Resultados
		for a in range(6):
			print(' ')
		print('******** PROBANDO TIPOS DE ALEATORIEDAD ********')
		print(' ')
		print('		Tenemos que random.choice(["blue", "red"]) resulta en:')
		print('		'+str(Constants.tra_fixed_determ)+': '+str(contador_uno)+' repeticiones')
		print('		'+str(Constants.tra_fixed_stoch)+': '+str(contador_dos)+' repeticiones')
		print('		'+str(Constants.tra_cond_determ)+': '+str(contador_tres)+' repeticiones')
		print('		'+str(Constants.tra_cond_stoch)+': '+str(contador_cuatro)+' repeticiones')
		print(' ')
		print('		Tenemos que itertools.cycle(["blue", "red"]) resulta en:')
		print('		'+str(Constants.tra_fixed_determ)+': '+str(contador_uno_i)+' repeticiones')
		print('		'+str(Constants.tra_fixed_stoch)+': '+str(contador_dos_i)+' repeticiones')
		print('		'+str(Constants.tra_cond_determ)+': '+str(contador_tres_i)+' repeticiones')
		print('		'+str(Constants.tra_cond_stoch)+': '+str(contador_cuatro_i)+' repeticiones')
		print(' ')
		print('******** FIN DE PRUEBA DE TIPOS DE ALEATORIEDAD ********')
		for a in range(6):
			print(' ')
	'''

class Group(BaseGroup):
	pass
		

class Player(BasePlayer):

	#####################################################################################################
	######################################## lo que iba en grupo ########################################
	#####################################################################################################

	# Atributos
	total_esfuerzos = models.IntegerField()
	extraccion_agregada = models.IntegerField()
	tratamiento = models.IntegerField()
	total_producido = models.CurrencyField()
	stock = models.IntegerField()
	otra_ronda = models.BooleanField(initial=False)
	razon_fin_ronda = models.StringField(choices=['se repite','alerta_ambiental','ex_mayor_stock', 'fin_tiempo'])

	stock_post_extraccion_pre_crecimiento = models.IntegerField()
	crecimiento = models.IntegerField()

	extraccion_pre_ajuste = models.IntegerField()


	# Métodos y funciones
	# Inicializa el grupo para un nuevo día de extracción
	
	def inicializar_atributos_grupo(self, p_total_esfuerzos, p_extraccion_agregada, p_total_producido):
		self.total_esfuerzos = p_total_esfuerzos
		self.extraccion_agregada = p_extraccion_agregada
		self.total_producido = p_total_producido
		if self.subsession.round_number == 1:
			self.stock = Constants.capacidad_de_carga_recurso_K

	# A todos los jugadores del grupo ordena que inicialice todos sus barcos
	'''
	def inicializar_barcos(self, p_numero_barcos):
		jugadores = self.get_players()
		self.inicializar_barcos(p_numero_barcos)
	'''

	def fijar_tratamiento(self, p_tratamiento):
		# A cada jugador, se le asignará una variable de tratamiento
		self.participant.vars.update({'tratamiento':str(p_tratamiento)})
		self.tratamiento = p_tratamiento
		print('[Grupo]: Se asignó al grupo, el tratamiento '+str(p_tratamiento)+'.')

	# consulta con algún participante qué tratamiento tenía asignado en el periodo pasado
	def recordar_tratamientos(self):
		# Y también al grupo for the record
		self.tratamiento = int(self.participant.vars['tratamiento'])
		print('[Grupo]: Se recordó al grupo que el tratamiento asignado es '+str(self.tratamiento)+'. (Una vez por cada participante del grupo)')

	# Suma los esfuerzos de todos sus jugadores y lo asigna a total_esfuezos
	def calcular_total_esfuerzos(self):
		self.total_esfuerzos = self.esfuerzo

	# Ordena a todos los jugadores del grupo calcular sus extracciones
	def calcular_extracciones_individuales(self):
		self.calcular_extracciones_individuales_p(self.tratamiento)


	# Suma las extracciones de todos sus jugadores
	def calcular_extraccion_agregada(self):
		self.extraccion_agregada = 0
		self.extraccion_agregada =  self.extracciones

	# Secundario, le asigna el precio ya calculado a todos sus jugadores
	def fijar_precio_a_todos(self, p_precio):
		self.fijar_precio_unitario(p_precio)

	# Dado el tratamiento, si es precio fijo, lo retorna, si es cournot, lo retorna
	# Y se lo asigna a sus jugadores
	def calcular_precio_unitario(self):
		precio_unitario = c(-99) # valor por defecto negativo para debug
		if self.tratamiento == Constants.tra_fixed_determ or self.tratamiento == Constants.tra_fixed_stoch:
			# Tratamiento es precio fijo
			precio_unitario = Constants.precio_por_unidad_caso_fijo
			self.fijar_precio_a_todos(precio_unitario)
			return precio_unitario
		elif self.tratamiento == Constants.tra_cond_determ or self.tratamiento == Constants.tra_cond_stoch:
			# Tratamiento es precio cournot
			if self.extraccion_agregada < 4:
				precio_unitario = c(5)
				self.fijar_precio_a_todos(precio_unitario)
				return precio_unitario
			elif self.extraccion_agregada > 3 and self.extraccion_agregada < 13:
				precio_unitario = c(5)
				self.fijar_precio_a_todos(precio_unitario)
				return precio_unitario
			elif self.extraccion_agregada > 12 and self.extraccion_agregada < 21:
				precio_unitario = c(4)
				self.fijar_precio_a_todos(precio_unitario)
				return precio_unitario
			elif self.extraccion_agregada > 20 and self.extraccion_agregada < 29:
				precio_unitario = c(3)
				self.fijar_precio_a_todos(precio_unitario)
				return precio_unitario
			elif self.extraccion_agregada > 28 and self.extraccion_agregada < 41:
				precio_unitario = c(2)
				self.fijar_precio_a_todos(precio_unitario)
				return precio_unitario
			elif self.extraccion_agregada > 40 and self.extraccion_agregada < 61:
				precio_unitario = c(1)
				self.fijar_precio_a_todos(precio_unitario)
				return precio_unitario

	# Ordena a sus jugadores calcular pagos
	def calcular_pagos_individuales(self):
		self.calcular_pagos_individuales_p()

	# Suma los pagos de todos sus jugadores
	def calcular_total_producido(self):
		self.total_producido = c(0)
		self.total_producido = c(self.total_producido + self.payoff)
		return self.total_producido

	# dado el numero de ronda, verfico 3 condiciones
	def se_repite_ronda(self, stock_anterior):
		print('[Dato Dato Dato]: El stock del grupo ahora es: '+str(self.stock))
		if self.subsession.round_number >= Constants.num_rounds:
			print('[Experimentador]: FIN DEL JUEGO. Número máximo de rondas.')
			print('Número de ronda actual: '+str(self.subsession.round_number)+', y máximo: '+str(Constants.num_rounds))
			# Se completó el número máximo de rondas
			self.otra_ronda = False
			self.razon_fin_ronda = 'fin_tiempo'
			self.extraccion_pre_ajuste = self.extraccion_agregada
			return self.otra_ronda
		elif self.extraccion_agregada >= stock_anterior:
			print('[Experimentador]: FIN DEL JUEGO. Explotación mayor a Stock.')
			print('Extración: '+str(self.extraccion_agregada)+', y stock anterior: '+str(stock_anterior))
			# La extracción agregada superó el stock
			print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
			print('          Ajustando extracciones porque no alcanzó')
			print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

			temp_extraido = self.extraccion_agregada
			self.extraccion_pre_ajuste = self.extraccion_agregada
			self.ajustar_extracciones_individuales(temp_extraido, stock_anterior)

			self.calcular_total_producido()

			self.otra_ronda = False
			self.razon_fin_ronda = 'ex_mayor_stock'
			return self.otra_ronda
		elif (self.stock) <= 12:
			print('[Experimentador]: FIN DEL JUEGO. Niveles de alerta ambiental de recurso.')
			print('Del recurso quedaría: '+str(self.stock)+', que es menor que 13.')
			# Stock alcanzó niveles de alerta ambiental. Gobierno interviene.
			self.otra_ronda = False
			self.razon_fin_ronda ='alerta_ambiental'
			self.extraccion_pre_ajuste = self.extraccion_agregada
			return self.otra_ronda
		else:
			print('[Experimentador]: EL JUEGO CONTINÚA.')
			# No hay razón para no jugar otra ronda
			self.otra_ronda = True
			print('[Experimentador]: Por lo tanto otra_ronda toma valor: '+str(self.otra_ronda))
			self.razon_fin_ronda = 'se repite'
			self.extraccion_pre_ajuste = self.extraccion_agregada
			return self.otra_ronda

	def calcular_crecimiento(self, p_stock):
		if (p_stock > 0 and p_stock <= 3):
			return 0
		elif (p_stock > 3 and p_stock <= 6):
			return 1
		elif (p_stock > 6 and p_stock <= 10):
			return 2
		elif (p_stock > 10 and p_stock <= 14):
			return 3
		elif (p_stock > 14 and p_stock <= 19):
			return 4
		elif (p_stock > 19 and p_stock <= 25):
			return 5
		elif (p_stock > 25 and p_stock <= 32):
			return 6
		elif (p_stock > 32 and p_stock <= 43):
			return 7
		elif (p_stock > 43 and p_stock <= 57):
			return 8
		elif (p_stock > 57 and p_stock <= 68):
			return 7
		elif (p_stock > 68 and p_stock <= 75):
			return 6
		elif (p_stock > 75 and p_stock <= 81):
			return 5
		elif (p_stock > 81 and p_stock <= 86):
			return 4
		elif (p_stock > 86 and p_stock <= 90):
			return 3
		elif (p_stock > 90 and p_stock <= 94):
			return 2
		elif (p_stock > 94 and p_stock <= 97):
			return 1
		elif (p_stock > 97 and p_stock <= 100):
			return 0

	def calcular_nuevo_stock(self):
		inicial = self.stock
		if self.extraccion_agregada > int(self.stock):
			self.stock = 0
			self.stock_post_extraccion_pre_crecimiento = 0
			self.crecimiento = 0


			print('[Grupo]: El stock fue insuficiente para las extracciones agregadas.')
			
			# Y actualizamos el registro en los jugadores
			self.stock_registro_del_jugador = self.stock

			return {'stock_inicial': inicial, 'stock_final':self.stock}
		else:
			print('[Grupo]: El stock es de '+str(self.stock)+'.')
			self.stock = self.stock - self.extraccion_agregada
			self.stock_post_extraccion_pre_crecimiento = self.stock
			print('[Grupo]: La extracción agregada fue de '+str(self.extraccion_agregada)+'.')
			crecimiento = int(self.calcular_crecimiento(self.stock))
			self.crecimiento = crecimiento
			self.stock = self.stock + crecimiento
			print('[Grupo]: El stock quedó en '+str(self.stock)+', después de crecer '+str(crecimiento)+' unidades.')
			

			# Y actualizamos el registro en los jugadores
			self.stock_registro_del_jugador = self.stock

			return {'stock_inicial': inicial, 'stock_final':self.stock}
	#####################################################################################################
	######################################## lo que iba en player #######################################
	#####################################################################################################

	class RadioSelectShips(forms.widgets.ChoiceWidget):
		input_type = 'radio'
		template_name = 'django/forms/widgets/radio.html'
		option_template_name = 'django/forms/widgets/radio_option.html'
		class Media:
			css = {
				'all': ('https://raw.githubusercontent.com/alorozco22/HojasEstilo/master/form.css',)
			}

	# Atributos
	#esfuerzo = models.IntegerField(min=1, max=Constants.barcos_por_jugador) # Número de barcos enviados
	esfuerzo = models.IntegerField(widget=widgets.RadioSelectHorizontal, choices=Constants.choices_list)

	extracciones = models.IntegerField() # Número de peces capturados
	precio_unitario = models.CurrencyField() # Precio al que le pagaron los peces
	stock_registro_del_jugador = models.IntegerField(initial=0)

	# Métodos y funciones

	# Reporta extraccion y envio de todos los barcos de este jugador:
	def reporten_barcos(self):
		print('	[JUGADOR]: RESUMEN DE ESTADO DE BARCOS: ¡REPORTEN!')
		for n1 in range(len(self.participant.vars['barcos_disponibles'])):
			barco_tem = self.participant.vars['barcos_disponibles'][n1]
			print('	[barco '+str(n1)+']: Inicializado con extracción '+str(barco_tem.extraccion)+', y envio: '+str(barco_tem.fue_enviado))


	# Vuelve a traer todos los barcos a la costa (barcos_disponibles.clear() y crea los p_numero_barcos barcos)
	def inicializar_barcos(self, p_numero_barcos):
		self.participant.vars.update({'barcos_disponibles': []})
		print('[Participante '+str(self.participant.id_in_session)+']: Se ha creado una lista de barcos')
		self.participant.vars['barcos_disponibles'].clear()
		for n in range(p_numero_barcos):
			barco_temporal = Ship()
			barco_temporal.fijar_envio(False)
			self.participant.vars['barcos_disponibles'].append(barco_temporal)
		self.reporten_barcos()

	# Manda a cada barco a pescar y suma las extracciones de cada barco y lo asigna a extracciones
	def calcular_extracciones_individuales_p(self, p_tratamiento):
		self.extracciones = 0
		lista_barcos = self.participant.vars['barcos_disponibles']
		print(' ')
		print(' ')
		print('[Participante '+str(self.participant.id_in_session)+']: '+'RONDA: '+str(self.subsession.round_number)+' Daré la orden a '+str(self.esfuerzo)+' barcos. Ajoy!')
		for b in range(0, self.esfuerzo):		
			# Se asignan los barcos que van a pescar primero
			barco_temp = lista_barcos[b]
			barco_temp.fue_enviado = True
			print('	[barco]: ¡Preparándose para zarpar!')

		for barco in self.participant.vars['barcos_disponibles']:
			# Se los manda a pescar
			ex = barco.pescar(p_tratamiento)
			print('	[barco]: Pescamos '+str(ex)+'. Volviendo a la costa.')
			print('	[barco]: ¿Este barco fue a pescar?: '+str(barco.fue_enviado))
			if barco.fue_enviado:
				self.extracciones = self.extracciones + ex
			else:
				pass


		self.reporten_barcos()

	# Una vez el grupo calcula extracciones individuales y grupales, si stock es insuficiente,
	# se invoca este método para recalcular de manera proporcional a las extracciones de cada uno
	def ajustar_extracciones_individuales(self, total_extraido, stock):
		proporcion = self.extracciones/total_extraido
		print('El total extraido fue '+str(total_extraido)+', y el stock era de '+str(stock))
		print(' El jugador '+str(self.participant.id_in_session)+' extrajo '+str(self.extracciones)+', que representa '+str(proporcion)+' del total de peces del grupo. ')
		self.extracciones = round(stock * proporcion)
		print(' Se asignó extracciones de '+str(self.extracciones))
		self.calcular_extraccion_agregada()
		self.calcular_pagos_individuales_p()

	# Calcula pagos multiplicando precio unitario por extracciones
	def calcular_pagos_individuales_p(self):
		self.payoff = c(self.extracciones * self.precio_unitario)
		return self.payoff

	def fijar_precio_unitario(self, p_precio_unitario):
		self.precio_unitario = p_precio_unitario

	def calcular_stock_actual(self):
		if self.subsession.round_number != 1:
			# Lista de jugadores desde la primera ronda hasta la anterior a esta.
			jugadores_anteriores = self.in_previous_rounds()
			tamanio = len(jugadores_anteriores)
			tamanio = tamanio - 1
			jugador_anterior = jugadores_anteriores[tamanio]
			stock_anterior = int(jugador_anterior.stock)
			# Y lo asigno
			self.stock = stock_anterior
		else:
			pass


class Ship():

	# Atributos
	fue_enviado = False # Indica si la persona decidió mandar el barco a pescar
	extraccion = 99 # Número de peces que capturó el barco
	
	def __init__(self):
		self.fue_enviado = False # Indica si la persona decidió mandar el barco a pescar
		self.extraccion = 99 # Número de peces que capturó el barco
		print('	[barco]: Se ha inicializado un barco')
		print('	[barco]: extraccion inicial fijada en: '+str(self.extraccion)+', enviado inicialmente fijado en: '+str(self.fue_enviado))

	def fijar_envio(self, p_envio):
		self.extraccion = 0
		self.fue_enviado = p_envio

	# Calcula los peces capturados, almacena el dato y lo retorna
	def pescar(self, p_tratamiento):
		print('	[barco]: (Me asignaron tratamiento: '+str(p_tratamiento)+').')
		if self.fue_enviado == False:
			self.extraccion = 0
			print('	[barco]: Este barco no fue asignado.')
			return self.extraccion
		elif p_tratamiento == Constants.tra_fixed_determ or p_tratamiento == Constants.tra_cond_determ:
			self.extraccion = Constants.captura_por_barco_determinado
			print('	[barco]: Este barco extrajo '+str(self.extraccion))
			return self.extraccion
		elif p_tratamiento == Constants.tra_fixed_stoch or p_tratamiento == Constants.tra_cond_stoch:
			posibles_extracciones = [Constants.capturas_dia_bueno_por_barco, Constants.capturas_dia_regular_por_barco, Constants.capturas_dia_malo_por_barco]
			probabilidades = [Constants.probabilidad_dia_bueno, Constants.probabilidad_dia_regular, Constants.probabilidad_dia_malo]
			self.extraccion = random.choices(posibles_extracciones, probabilidades)
			self.extraccion = sum(self.extraccion)
			print('	[barco]: Este barco capturó '+str(self.extraccion))
			return self.extraccion


