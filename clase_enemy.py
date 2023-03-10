import pygame
from random import randint , choice

class Enemy(pygame.sprite.Sprite):
	def __init__(self, flip, groups):
		super().__init__(groups)

		self.import_enemy_graficos()

		#estados
		self.fun_index = 0
		self.flip = flip
		self.velocidad = randint(2,6)

		#direccion y rect
		if self.flip:
			self.image = self.fungant_flip[self.fun_index]
			self.rect = self.image.get_rect(topleft = (800, randint(0,370)))
		else:
			self.image = self.fungant[self.fun_index]
			self.rect = self.image.get_rect(topright = (0, randint(0,370)))

		self.hitbox = self.rect.inflate(0,-10)

		#mask	
		self.mask = pygame.mask.from_surface(self.image)

	def import_enemy_graficos(self):
		#fungant
		fungant_1 = pygame.transform.scale2x(pygame.image.load('fungant/fungant_1.png').convert_alpha())
		fungant_2 = pygame.transform.scale2x(pygame.image.load('fungant/fungant_2.png').convert_alpha())
		fungant_3 = pygame.transform.scale2x(pygame.image.load('fungant/fungant_3.png').convert_alpha())
		fungant_4 = pygame.transform.scale2x(pygame.image.load('fungant/fungant_4.png').convert_alpha())
		fungant_1_flip = pygame.transform.flip(fungant_1,True,False)
		fungant_2_flip = pygame.transform.flip(fungant_2,True,False)
		fungant_3_flip = pygame.transform.flip(fungant_3,True,False)
		fungant_4_flip = pygame.transform.flip(fungant_4,True,False)
		self.fungant = [fungant_1, fungant_2, fungant_3, fungant_4]
		self.fungant_flip = [fungant_1_flip, fungant_2_flip, fungant_3_flip, fungant_4_flip]


	def animacion(self):
		#animacion actual
		self.fun_index += 0.12
		if self.fun_index >= len(self.fungant): self.fun_index = 0

		#direccion
		if self.flip:
			self.image = self.fungant_flip[int(self.fun_index)]
		else:
			self.image = self.fungant[int(self.fun_index)]

	def mover(self):
		#movimiento
		if self.flip:
			self.hitbox.x -= self.velocidad
		else:
			self.hitbox.x += self.velocidad

		self.rect.center = self.hitbox.center

	def destroy(self):
		#limite de pantalla
		if self.flip and self.rect.right < 0:
			self.kill()
		elif not self.flip and self.rect.left > 800:
			self.kill()

	def update(self):
		self.animacion()
		self.mover()
		self.destroy()