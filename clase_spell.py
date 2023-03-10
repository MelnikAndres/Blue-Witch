import pygame

class Spell(pygame.sprite.Sprite):
	def __init__(self, pos, flip):
		super().__init__()

		#graficos
		self.import_spell_graficos(flip)
		
		#estados
		self.flip_state = 1 if 90 < flip < 270 else 0
		self.flip = flip
		self.fireball_index = 0
		self.image = self.fireball[self.fireball_index]

		#direccion
		if self.flip_state:
			self.rect = self.image.get_rect(midright = (pos[0]+120, pos[1]))
		else:
			self.rect = self.image.get_rect(midleft = pos)

	def import_spell_graficos(self, flip):
		#fireball
		fireball_1 = pygame.transform.rotate(pygame.transform.scale2x(pygame.image.load('fireball/fireball2_1.png')), flip).convert_alpha()
		fireball_2 = pygame.transform.rotate(pygame.transform.scale2x(pygame.image.load('fireball/fireball2_2.png')), flip).convert_alpha()
		fireball_3 = pygame.transform.rotate(pygame.transform.scale2x(pygame.image.load('fireball/fireball2_3.png')), flip).convert_alpha()
		fireball_4 = pygame.transform.rotate(pygame.transform.scale2x(pygame.image.load('fireball/fireball2_4.png')), flip).convert_alpha()
		self.fireball = [fireball_1, fireball_2, fireball_3, fireball_4]


	def animacion(self):
		#animacion actual
		self.fireball_index +=0.1
		if self.fireball_index >= len(self.fireball): self.fireball_index = 0
		self.image = self.fireball[int(self.fireball_index)]

	def update(self):
		#movimiento
		if self.flip == 45:
			self.rect.x += 3.5
			self.rect.y -= 3.5
		elif self.flip == 135:
			self.rect.x -= 3.5
			self.rect.y -= 3.5
		elif self.flip == 180:
			self.rect.x -=5
		elif self.flip == 225:
			self.rect.x -= 3.5
			self.rect.y +=3.5
		elif self.flip == 315:
			self.rect.x += 3.5
			self.rect.y += 3.5
		else:
			self.rect.x += 5
			
		self.animacion()
		self.destroy()

	def destroy(self):

		#limite de pantalla
		if self.rect.x >= 800 or self.rect.right <= 0:
			self.kill()