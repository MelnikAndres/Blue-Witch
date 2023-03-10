import pygame

class Bruja(pygame.sprite.Sprite):
	def __init__(self, groups, add_spell):
		super().__init__(groups)

		#funcion spell
		self.add_spell = add_spell

		#graficos
		self.import_bruja_graficos()

		#indices
		self.stand_index = 0
		self.run_index = 0
		self.atq_index = 0
		

		#ataque
		self.ataque = 0
		self.ataque_e = 0
		self.ataque_r = 0

		#estados
		self.flip_state = 0
		self.velocidad = [0, 0]
		self.atq_realizado = 0
		self.ajustar_rec = 0
		self.inmune = 0
		self.doble = 0
		self.confusion = 0
		self.mov_confusion = 0
		self.block = 0
		self.bothways = 0

		#estadisticas
		self.stat_velocidad = 5
		self.stat_atq_vel = 0.15

		#autotimer
		self.pickup_timer = 0

		#imagen
		self.image = self.stand[self.stand_index]
		self.rect = self.image.get_rect(midbottom = (382,200))
		self.mask = pygame.mask.from_surface(self.image)
		self.hitbox = self.rect.inflate(0, -40)
		
	def import_bruja_graficos(self):
		#stand
		bruja_stand_1 = pygame.transform.scale2x(pygame.image.load('bruja/bruja_stand1.png')).convert_alpha()
		bruja_stand_2 = pygame.transform.scale2x(pygame.image.load('bruja/bruja_stand2.png')).convert_alpha()
		bruja_stand_3 = pygame.transform.scale2x(pygame.image.load('bruja/bruja_stand3.png')).convert_alpha()
		bruja_stand_4 = pygame.transform.scale2x(pygame.image.load('bruja/bruja_stand4.png')).convert_alpha()
		bruja_stand_5 = pygame.transform.scale2x(pygame.image.load('bruja/bruja_stand5.png')).convert_alpha()
		bruja_stand_1_flip = pygame.transform.flip(bruja_stand_1,True,False).convert_alpha()
		bruja_stand_2_flip = pygame.transform.flip(bruja_stand_2,True,False).convert_alpha()
		bruja_stand_3_flip = pygame.transform.flip(bruja_stand_3,True,False).convert_alpha()
		bruja_stand_4_flip = pygame.transform.flip(bruja_stand_4,True,False).convert_alpha()
		bruja_stand_5_flip = pygame.transform.flip(bruja_stand_5,True,False).convert_alpha()
		self.stand = [bruja_stand_1, bruja_stand_2, bruja_stand_3, bruja_stand_4, bruja_stand_5]
		self.stand_flip = [bruja_stand_1_flip, bruja_stand_2_flip, bruja_stand_3_flip, bruja_stand_4_flip, bruja_stand_5_flip]

		#run
		bruja_run_1 = pygame.transform.scale2x(pygame.image.load('bruja_run/bruja_run_1.png')).convert_alpha()
		bruja_run_2 = pygame.transform.scale2x(pygame.image.load('bruja_run/bruja_run_2.png')).convert_alpha()
		bruja_run_3 = pygame.transform.scale2x(pygame.image.load('bruja_run/bruja_run_3.png')).convert_alpha()
		bruja_run_4 = pygame.transform.scale2x(pygame.image.load('bruja_run/bruja_run_4.png')).convert_alpha()
		bruja_run_5 = pygame.transform.scale2x(pygame.image.load('bruja_run/bruja_run_5.png')).convert_alpha()
		bruja_run_6 = pygame.transform.scale2x(pygame.image.load('bruja_run/bruja_run_6.png')).convert_alpha()
		bruja_run_7 = pygame.transform.scale2x(pygame.image.load('bruja_run/bruja_run_7.png')).convert_alpha()
		bruja_run_8 = pygame.transform.scale2x(pygame.image.load('bruja_run/bruja_run_8.png')).convert_alpha()
		bruja_run_1_flip = pygame.transform.flip(bruja_run_1,True,False).convert_alpha()
		bruja_run_2_flip = pygame.transform.flip(bruja_run_2,True,False).convert_alpha()
		bruja_run_3_flip = pygame.transform.flip(bruja_run_3,True,False).convert_alpha()
		bruja_run_4_flip = pygame.transform.flip(bruja_run_4,True,False).convert_alpha()
		bruja_run_5_flip = pygame.transform.flip(bruja_run_5,True,False).convert_alpha()
		bruja_run_6_flip = pygame.transform.flip(bruja_run_6,True,False).convert_alpha()
		bruja_run_7_flip = pygame.transform.flip(bruja_run_7,True,False).convert_alpha()
		bruja_run_8_flip = pygame.transform.flip(bruja_run_8,True,False).convert_alpha()
		self.run = [bruja_run_1, bruja_run_2, bruja_run_3, bruja_run_4, bruja_run_5, bruja_run_6, bruja_run_7, bruja_run_8]
		self.run_flip = [bruja_run_1_flip, bruja_run_2_flip, bruja_run_3_flip, bruja_run_4_flip, bruja_run_5_flip, bruja_run_6_flip, bruja_run_7_flip, bruja_run_8_flip]

		#ataque
		bruja_atq_1 = pygame.transform.scale2x(pygame.image.load('bruja_atq/bruja_atq_1.png')).convert_alpha()
		bruja_atq_2 = pygame.transform.scale2x(pygame.image.load('bruja_atq/bruja_atq_2.png')).convert_alpha()
		bruja_atq_3 = pygame.transform.scale2x(pygame.image.load('bruja_atq/bruja_atq_3.png')).convert_alpha()
		bruja_atq_4 = pygame.transform.scale2x(pygame.image.load('bruja_atq/bruja_atq_4.png')).convert_alpha()
		bruja_atq_5 = pygame.transform.scale2x(pygame.image.load('bruja_atq/bruja_atq_5.png')).convert_alpha()
		bruja_atq_1_flip = pygame.transform.flip(bruja_atq_1,True,False).convert_alpha()
		bruja_atq_2_flip = pygame.transform.flip(bruja_atq_2,True,False).convert_alpha()
		bruja_atq_3_flip = pygame.transform.flip(bruja_atq_3,True,False).convert_alpha()
		bruja_atq_4_flip = pygame.transform.flip(bruja_atq_4,True,False).convert_alpha()
		bruja_atq_5_flip = pygame.transform.flip(bruja_atq_5,True,False).convert_alpha()
		self.atq = [bruja_atq_1, bruja_atq_2, bruja_atq_3, bruja_atq_4, bruja_atq_5]
		self.atq_flip = [bruja_atq_1_flip, bruja_atq_2_flip, bruja_atq_3_flip, bruja_atq_4_flip, bruja_atq_5_flip]

	def animacion(self):
		#ataque
		if self.ataque:
			#reiniciar animaciones 
			self.stand_index, self.run_index = 0, 0

			#animacion actual
			self.atq_index += self.stat_atq_vel
			if self.atq_index >= len(self.atq):
				self.atq_index = 0
				self.atq_realizado = 0

			#direccion	
			if self.flip_state:
				self.image = self.atq_flip[int(self.atq_index)]
				self.mask = pygame.mask.from_surface(self.image)
			else:
				self.image = self.atq[int(self.atq_index)]
				self.mask = pygame.mask.from_surface(self.image)

			#ajustar rec	
			if self.ajustar_rec:
				self.rect = self.image.get_rect(topleft = (self.rect.x-18,self.rect.y-12))
				self.ajustar_rec = 0

		#correr	
		elif self.velocidad != [0, 0]:
			#ajustar rec

			#animacion actual	
			self.run_index +=0.12
			if self.run_index >= len(self.run): self.run_index = 0

			#direccion
			if self.flip_state:
				self.image = self.run_flip[int(self.run_index)]
				self.mask = pygame.mask.from_surface(self.image)
			else:
				self.image = self.run[int(self.run_index)]
				self.mask = pygame.mask.from_surface(self.image)

			if not self.ajustar_rec:
				self.rect = self.image.get_rect(topleft = (self.rect.x+18, self.rect.y+12))


		#parado
		else:

			#ajustar rec
			
			#animacion actual
			self.stand_index +=0.12
			if self.stand_index >= len(self.stand):	self.stand_index = 0

			#direccion
			if self.flip_state:
				self.image = self.stand_flip[int(self.stand_index)]
				self.mask = pygame.mask.from_surface(self.image)
			else:
				self.image = self.stand[int(self.stand_index)]
				self.mask = pygame.mask.from_surface(self.image)
			if not self.ajustar_rec:
				self.rect = self.image.get_rect(topleft = (self.rect.x+18, self.rect.y+12))

	def input_usuario(self):
		teclas = pygame.key.get_pressed()

		#ataque rapido
		if teclas[pygame.K_e] and self.ataque_e == 0:
				self.ataque_e = 10
		if teclas[pygame.K_r] and self.ataque_r == 0:
			self.ataque_r = 20
		#ataque cargado
		if teclas[pygame.K_q] and not self.block:
			self.ataque = 1
			self.velocidad = [0, 0]


		else:
			#reiniciar estados de ataque
			self.ataque = 0
			self.atq_index = 0
			self.atq_realizado = 0

			#movimiento
			if teclas[pygame.K_UP] or teclas[pygame.K_w]:
				self.velocidad[1] = -self.stat_velocidad
			elif teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
				self.velocidad[1] = self.stat_velocidad
			else:
				self.velocidad[1] = 0
			if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
				self.flip_state = 1
				self.velocidad[0] = -self.stat_velocidad
			elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
				self.flip_state = 0
				self.velocidad[0] = self.stat_velocidad
			else:
				self.velocidad[0] = 0
		
	def ejecutar_acciones(self):
		#lanzar ataque cargado
		if int(self.atq_index) == len(self.atq)-1 and not self.atq_realizado:
			self.add_spell(self.rect.midleft, (self.flip_state + self.confusion) * 180, True, 'cargado')
			self.atq_realizado = 1
			if self.doble:
				self.add_spell((self.rect.left, self.rect.centery + 20), self.flip_state*180, False, 'cargado')
			elif self.bothways:
				self.add_spell((self.rect.left, self.rect.centery + 20), self.flip_state*180 + 180, False, 'cargado')
		
		#lanzar ataque rapido
		if self.ataque_e == 10:
			self.add_spell(self.rect.midleft, 0, True, 'rapido')
			self.add_spell(self.rect.midleft, 180, False, 'rapido')
		if self.ataque_r == 20:
			self.add_spell(self.rect.midleft, 0, True, 'ultimate')
			pygame.event.post(pygame.event.Event(pygame.USEREVENT+1, pos = self.rect.midleft, flip = 'all', play = True))

		#cooldown ataque rapido	
		if self.ataque_e > 0:
			self.ataque_e -= 0.016
		elif self.ataque_e < 0:
			self.ataque_e = 0

		if self.ataque_r > 0:
			self.ataque_r -= 0.016
		elif self.ataque_r < 0:
			self.ataque_r = 0

		#ajuste de rec
		if not self.ajustar_rec and (self.run_index or self.stand_index):
			self.ajustar_rec = 1

		#movimiento
		self.hitbox.x += self.velocidad[0]
		self.hitbox.y += self.velocidad[1]
		if self.hitbox.bottom < 10:
			self.hitbox.midtop = (self.hitbox.x+20, 390)
		if self.hitbox.top > 390:
			self.hitbox.midbottom = (self.hitbox.x+20,10)
		if self.hitbox.right < 0:
			self.rect.midleft = (800, self.hitbox.y+42)
		if self.hitbox.left > 800:
			self.hitbox.midright = (0,self.hitbox.y+42)

		#timer
		if self.pickup_timer:
			self.pickup_timer -= 0.0166
			if self.pickup_timer < 0:
				self.pickup_timer = 0
		else:
			self.reset_stats()

		#inmunidad
		if self.inmune:
			self.mask.clear()

		self.rect.center = self.hitbox.center


	def pickup_stats(self, pickup):
		if not pickup:
			return 

		#pickups de velocidad
		elif pickup == 'slow':
			self.stat_velocidad = 2
			self.pickup_timer = 10
		elif pickup == 'fast':
			self.stat_velocidad = 7
			self.pickup_timer = 10
		elif pickup == 'freeze':
			self.stat_velocidad = 0
			self.pickup_timer = 2.8
			self.stat_atq_vel = 0.18

		#pickups de ataque
		elif pickup == 'ataquedown':
			self.stat_atq_vel = 0.08
			self.pickup_timer = 8

		elif pickup == 'ataqueup':
			self.stat_atq_vel = 0.22
			self.pickup_timer = 10

		#pickups locos
		elif pickup == 'inmune':
			self.inmune = 1
			self.pickup_timer = 7
			return self.inmune
		
		elif pickup == 'doble':
			self.doble = 1
			self.pickup_timer = 10
		
		elif pickup == 'confusion':
			self.confusion = 1
			self.stat_atq_vel = 0.17
			self.pickup_timer = 8

		elif pickup == 'mov_confusion':
			self.mov_confusion = -1
			self.stat_velocidad = 4.5
			self.pickup_timer = 8
			self.stat_velocidad *= self.mov_confusion

		elif pickup == 'block':
			self.block = 1
			self.stat_velocidad = 5.5
			self.pickup_timer = 4.2

		elif pickup == 'bothways':
			self.bothways = 1
			self.pickup_timer = 10

	def reset_stats(self):
		self.stat_velocidad = 5
		self.stat_atq_vel = 0.15
		self.inmune = 0
		self.doble = 0
		self.confusion = 0
		self.block = 0
		self.mov_confusion = 0
		self.bothways = 0




	def update(self, pickup = None):
		self.pickup_stats(pickup)
		self.input_usuario()
		self.animacion()
		self.ejecutar_acciones()