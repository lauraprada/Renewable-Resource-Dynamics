from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class ExtractionPage(Page):
	form_model = 'player'
	form_fields = ['esfuerzo']

	def vars_for_template(self):
		
		if self.player.group.tratamiento == Constants.tra_fixed_determ or self.player.group.tratamiento == Constants.tra_cond_determ:
			det = True
		else:
			det = False

		if self.player.group.tratamiento == Constants.tra_fixed_determ or self.player.group.tratamiento == Constants.tra_fixed_stoch:
			fix = True
		else:
			fix = False

		lista_crecimientos = {'0':0}
		for x in range(1,101):
			# lista_crecimientos.append(str(round((Constants.tasa_crecimiento_intrinseca_r*int(self.player.group.stock))-(Constants.tasa_crecimiento_intrinseca_r/Constants.capacidad_de_carga_recurso_K)*(int(self.player.group.stock))**2)))
			nombre = str(x)
			lista_crecimientos.update({nombre: x})
		
		self.player.calcular_stock_actual()

		return {
			'stock_inicial': Constants.capacidad_de_carga_recurso_K,
			'unidades_deterministicas':Constants.captura_por_barco_determinado,
			'unidades_dia_bueno':Constants.capturas_dia_bueno_por_barco,
			'unidades_dia_regular':Constants.capturas_dia_regular_por_barco,
			'unidades_dia_malo':Constants.capturas_dia_malo_por_barco,
			'precio_fijo_valor':Constants.precio_por_unidad_caso_fijo,
			'ultima_ronda':Constants.num_rounds,
			'deterministico': det,
			'precio_fijo': fix,
			'nums': range(1,101),
			'planificador': Constants.indicadora_planificador_central,
			'stock': self.player.group.stock,
		}

class ResultsWaitPage(WaitPage):

	def after_all_players_arrive(self):
		#############################################
		# Espacios
		for x in range(1,10):
			print('+++++++++++++ BIENES COMUNES LLEGARON TODOS +++++++++++++')
		#############################################

		print('[Experimentador]: Pronto iniciarán las extracciones.')

		print('[Experimentador]: Comencemos por inicializar otra vez todos los barcos.')
		lista_con_grupo_actual = [self.group]
		self.group.subsession.inicializar_barcos(lista_con_grupo_actual)

		print(' ')
		print(' ')
		for p in self.group.get_players():
			p.reporten_barcos()
		print(' ')
		print(' ')


		print('[Experimentador]: Calculando el total de esfuerzos de cada grupo.')
		self.group.calcular_total_esfuerzos()
		
		print(' ')
		print(' ')
		for p in self.group.get_players():
			p.reporten_barcos()
		print(' ')
		print(' ')

		print('[Experimentador]: Calculando extracciones individuales.')
		self.group.calcular_extracciones_individuales()

		print(' ')
		print(' ')
		for p in self.group.get_players():
			p.reporten_barcos()
		print(' ')
		print(' ')


		print('[Experimentador]: Calculando extracción agregada de cada grupo.')
		self.group.calcular_extraccion_agregada()
		stock_temp = self.group.stock
		print('[BORAR BORAR BORRAR]: Stock: '+str(stock_temp))
		print('[Experimentador]: Calculando precio unitario del grupo.')
		self.group.calcular_precio_unitario()
		print('[Experimentador]: Checkeando y quedamos en que se repite ronda: '+str(self.group.otra_ronda))
		print('[Experimentador]: Calculando pagos individuales.')
		self.group.calcular_pagos_individuales()
		print('[Experimentador]: Casi terminamos y quedamos en que se repite ronda: '+str(self.group.otra_ronda))
		print('[Experimentador]: Calculando el total producido en cada grupo.')
		self.group.calcular_total_producido()
		print('[Experimentador]: Calculando nuevo stock.')
		print('[Experimentador]: Casi terminamos y quedamos en que se repite ronda: '+str(self.group.otra_ronda))
		self.group.calcular_nuevo_stock()
		print('[Experimentador]: Terminamos y quedamos en que se repite ronda: '+str(self.group.otra_ronda))
		print('[Experimentador]: ¿Se repite ronda?: '+ str(self.group.se_repite_ronda(stock_temp)))
		print('[Experimentador]: RECIÉN y quedamos en que se repite ronda: '+str(self.group.otra_ronda))
		print('++++++++++++++++++++++++++++++++++++++++++++++++++')
		print('INICIALIZANDO BARCOS RONDA: '+str(self.group.subsession.round_number))
		print('++++++++++++++++++++++++++++++++++++++++++++++++++')
		lista_con_grupo_actual = [self.group]
		self.group.subsession.inicializar_barcos(lista_con_grupo_actual)
		


class Results(Page):
	def vars_for_template(self):
		print('[Experimentador]: En este momento se están enviando variables a página de resultados.')
		st = self.player.group.otra_ronda
		razon = self.player.group.razon_fin_ronda

		if self.player.group.tratamiento == Constants.tra_fixed_determ or self.player.group.tratamiento == Constants.tra_cond_determ:
			det = True
		else:
			det = False

		if self.player.group.tratamiento == Constants.tra_fixed_determ or self.player.group.tratamiento == Constants.tra_fixed_stoch:
			fix = True
		else:
			fix = False

		return {
			'ronda': self.group.subsession.round_number,
			'siguiente': st,
			'total_esfuerzos': self.player.group.total_esfuerzos,
			'total_extracciones': self.player.group.extraccion_agregada,
			'mi_esfuerzo': self.player.esfuerzo,
			'mi_extraccion': self.player.extracciones,
			'precio_unitario': self.player.precio_unitario,
			'ganancias': self.player.payoff,
			'stock': self.player.group.stock,
			'stock_post_extraccion': self.player.group.stock_post_extraccion_pre_crecimiento,
			'extracciones_pre_ajuste': self.player.group.extraccion_pre_ajuste,
			'crecimiento': self.player.group.crecimiento,
			'deterministico': det,
			'precio_fijo': fix,
			'razon': razon,
		}


class InstructionPage(Page):
	def is_displayed(self):
		return self.subsession.round_number == 1

	def vars_for_template(self):
		
		if self.player.group.tratamiento == Constants.tra_fixed_determ or self.player.group.tratamiento == Constants.tra_cond_determ:
			det = True
		else:
			det = False

		if self.player.group.tratamiento == Constants.tra_fixed_determ or self.player.group.tratamiento == Constants.tra_fixed_stoch:
			fix = True
		else:
			fix = False

		lista_crecimientos = {'0':0}
		for x in range(1,101):
			# lista_crecimientos.append(str(round((Constants.tasa_crecimiento_intrinseca_r*int(self.player.group.stock))-(Constants.tasa_crecimiento_intrinseca_r/Constants.capacidad_de_carga_recurso_K)*(int(self.player.group.stock))**2)))
			nombre = str(x)
			lista_crecimientos.update({nombre: x})

		return {
			'deterministico': det,
			'precio_fijo': fix,
			'precio_fijo_valor':Constants.precio_por_unidad_caso_fijo,
			'stock': self.player.group.stock,
			'planificador': Constants.indicadora_planificador_central,
		}

class ResultsSummary(Page):
	def is_displayed(self):
		return self.player.group.otra_ronda == False

	def vars_for_template(self):

		jugador_en_todas_las_rondas = self.player.in_all_rounds()

		contador_capturas = 0
		contador_ganancias = 0
		for p in jugador_en_todas_las_rondas:
			contador_capturas = contador_capturas + p.extracciones
			contador_ganancias = contador_ganancias + p.payoff
		
		contador_capturas_grupal = 0
		contador_ganancias_grupal = 0
		
		for group_player in self.group.get_players():
			for player in group_player.in_all_rounds():
				contador_capturas_grupal = contador_capturas_grupal + player.extracciones
				contador_ganancias_grupal = contador_ganancias_grupal + player.payoff

		eficiencia = round(100.0*(float(contador_capturas_grupal) / 162.0))
		eficiencia_gananciass = round(100.0*(float(contador_ganancias_grupal) / 666.0))


		if self.player.group.tratamiento == Constants.tra_fixed_determ or self.player.group.tratamiento == Constants.tra_cond_determ:
			det = True
		else:
			det = False

		if self.player.group.tratamiento == Constants.tra_fixed_determ or self.player.group.tratamiento == Constants.tra_fixed_stoch:
			fix = True
		else:
			fix = False
		return {
			'capturas': contador_capturas,
			'ganancias': contador_ganancias,
			'fin': self.group.subsession.round_number,
			'total_capturas_grupo':contador_capturas_grupal,
			'total_ganancias_grupo':contador_ganancias_grupal,
			'eficiencia':eficiencia,
			'eficiencia_ganancias':eficiencia_gananciass,
			'precio_fijo': fix,
			'deterministico': det,
		}



page_sequence = [
	InstructionPage,
	ExtractionPage,
	ResultsWaitPage,
	Results,
	ResultsSummary
]