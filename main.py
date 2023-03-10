import pygame
from sys import exit
from random import randint, choice
from clase_bruja import Bruja
from clase_spell import Spell
from clase_enemy import Enemy


class YSort(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2

    def ysort_draw(self):
        for sprite in sorted(self.sprites(), key=lambda s: s.rect.bottom):
            self.display_surface.blit(sprite.image, sprite.rect)


def ataque_cd(cd_actual):
    if cd_actual > 0:
        cd_actual -= 0.016
    elif cd_actual < 0:
        cd_actual = 0

    return cd_actual


def timer_render(start_time, fuente, color):
    actual_time_s = pygame.time.get_ticks() // 1000 - start_time
    m = (actual_time_s // 60) % 60
    h = (actual_time_s // 60) // 60
    s = actual_time_s % 60
    timer_surf = fuente.render(f'{h:02d}:{m:02d}:{s:02d}', False, color)
    timer_rect = timer_surf.get_rect(center=(400, 40))
    return timer_surf, timer_rect, actual_time_s

class Main:
    def __init__(self):
        # inicializar pygame y screen
        pygame.init()
        self.screen = pygame.display.set_mode((800, 400))
        pygame.display.set_caption('Blue Witch')
        self.fps = pygame.time.Clock()
        icono = pygame.image.load('varios/witch.png').convert()
        pygame.display.set_icon(icono)

        # activo
        self.game_active = True

        # font
        self.fuente = pygame.font.Font('font/Pixeltype.ttf', 40)
        self.fuente_time = pygame.font.Font('font/Pixeltype.ttf', 30)

        # sonidos
        self.spawn = pygame.mixer.Sound('audio/spawn.wav')
        self.muerte = pygame.mixer.Sound('audio/muerte.wav')
        self.restart = pygame.mixer.Sound('audio/restart.wav')
        pygame.mixer.music.load('audio/musica.wav')
        self.fire = pygame.mixer.Sound('audio/fire.wav')
        self.kill = pygame.mixer.Sound('audio/kill.wav')
        self.nextlvl = pygame.mixer.Sound('audio/next.wav')
        self.fire.set_volume(0.12)
        self.restart.set_volume(0.4)
        self.muerte.set_volume(0.8)
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(loops=-1)

        # fondo
        self.fondo_surf = pygame.image.load('varios/fondo2.png').convert()
        self.fondo_rec = self.fondo_surf.get_rect(topleft=(0, 0))
        self.fondo_muerto_surf = pygame.image.load('varios/fondo_muerto.png').convert()
        self.arbusto_fondo = pygame.image.load('varios/arbustos.png')

        # muerte
        self.muerte_surf = pygame.transform.scale2x(pygame.image.load('varios/muerte.png')).convert_alpha()
        self.muerte_rec = self.muerte_surf.get_rect(center=(400, 200))

        # score
        self.score = 0
        self.color = (200, 200, 200)
        self.score_surf = self.fuente.render(f'Score: {self.score}', False, self.color)
        self.score_rec = self.score_surf.get_rect(center=(400, 20))
        self.lvl = 1

        # ysort
        self.ysort_group = YSort()

        # Bruja
        self.bruja = pygame.sprite.GroupSingle()
        self.bruja.add(Bruja([self.bruja, self.ysort_group], self.add_spell))

        # spell
        self.spells = pygame.sprite.Group()
        self.icon_rap_surf = pygame.image.load('iconos/skill.png').convert()
        self.iconcd_rap_surf = pygame.image.load('iconos/skillcd.png').convert()
        self.iconcd_rap_rec = self.icon_rap_surf.get_rect(midbottom=(350, 380))
        self.icon_fuerte_surf = pygame.image.load('iconos/skill_r.png').convert()
        self.iconcd_fuerte_surf = pygame.image.load('iconos/skill_r_cd.png').convert()
        self.iconcd_fuerte_rec = self.icon_rap_surf.get_rect(midbottom=(450, 380))

        # iconos
        self.pickups = {
            'freeze': pygame.image.load('iconos/icono_freeze.png').convert_alpha(),
            'slow': pygame.image.load('iconos/icono_slow.png').convert_alpha(),
            'fast': pygame.image.load('iconos/icono_fast.png').convert_alpha(),
            'ataqueup': pygame.image.load('iconos/icono_ataqueup.png').convert_alpha(),
            'ataquedown': pygame.image.load('iconos/icono_ataquedown.png').convert_alpha(),
            'doble': pygame.image.load('iconos/icono_doble.png').convert_alpha(),
            'inmune': pygame.image.load('iconos/icono_inmune.png').convert_alpha(),
            'confusion': pygame.image.load('iconos/icono_confusion.png').convert_alpha(),
            'block': pygame.image.load('iconos/icono_block.png').convert_alpha(),
            'mov_confusion': pygame.image.load('iconos/icono_mov_confusion.png').convert_alpha(),
            'bothways': pygame.image.load('iconos/icono_bothways.png').convert_alpha(),
        }

        # enemigo
        self.enemigos = pygame.sprite.Group()

        # clock
        self.start_time = 0
        self.tiempo = 0
        self.enemigos_cd = 700
        self.enemigos_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.enemigos_timer, self.enemigos_cd)
        self.pickups_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(self.pickups_timer, 12000)
        self.timer_surf = None
        self.timer_rect = None

        # ataque cd
        self.ataque_rapido_cd = 0
        self.ataque_fuerte_cd = 0

        # pickup
        self.pickup = None
        self.pickup_2 = None

    def add_spell(self, pos, flip, play, type):
        if type == 'cargado':
            self.spells.add(Spell((pos[0] - 30, pos[1] + 5), flip))
        if type == "rapido":
            self.ataque_rapido_cd = 10
            self.spells.add(Spell((pos[0] - 30, pos[1] + 5), flip))
        if type == "ultimate":
            [self.spells.add(Spell((pos[0] - 30, pos[1] + 5), ang)) for ang in
             (0, 45, 135, 180, 225, 315)]
            self.ataque_fuerte_cd = 20
        if play:
            self.fire.play()

    def reiniciar_level(self):
        self.restart.play()
        pygame.mixer.music.set_volume(0.5)
        self.game_active = True
        self.bruja.add(Bruja([self.bruja, self.ysort_group], self.add_spell))
        self.score = 0
        self.score_surf = self.fuente.render(f'Score: {self.score}', False, self.color)
        self.score_rec = self.score_surf.get_rect(center=(400, 20))
        self.ataque_rapido_cd = 0
        self.ataque_fuerte_cd = 0
        self.start_time = pygame.time.get_ticks() // 1000
        pygame.time.set_timer(self.pickups_timer, 12000)
        pygame.time.set_timer(self.enemigos_timer, self.enemigos_cd)

    def check_colision_enemigo_spell(self):
        if pygame.sprite.groupcollide(self.spells, self.enemigos, True, True):  # enemigo alcanzado
            self.kill.play()
            self.score += 1
            self.score_surf = self.fuente.render(f'Score: {self.score}', False, self.color)
            self.score_rec = self.score_surf.get_rect(center=(400, 20))
    def check_colision_enemigo_player(self):
        for sprite in self.enemigos.sprites():
            if sprite.rect.colliderect(self.bruja.sprite.hitbox):
                if not pygame.sprite.collide_mask(self.bruja.sprite, sprite):
                    continue
                self.muerte.play()
                pygame.mixer.music.set_volume(0.2)
                self.enemigos.empty()
                self.bruja.empty()
                self.spells.empty()
                self.ysort_group.empty()
                self.game_active = False
                break
    def check_score_reached(self):
        if self.score == 40 and self.lvl == 1:  # puntuacion alcanzada
            self.lvl = 2
            self.nextlvl.play()
            self.enemigos.empty()
            pygame.time.set_timer(self.enemigos_timer, 0)

    def check_level_status(self):
        self.check_score_reached()
        self.check_colision_enemigo_spell()
        self.check_colision_enemigo_player()

    def mostrar_en_pantalla(self):
        # tiempo actual
        self.timer_surf, self.timer_rect, self.tiempo = timer_render(self.start_time, self.fuente_time, self.color)

        # mostrar en pantalla
        self.screen.blit(self.fondo_surf, self.fondo_rec)
        self.ysort_group.ysort_draw()
        self.screen.blit(self.score_surf, self.score_rec)
        self.screen.blit(self.arbusto_fondo, self.fondo_rec)
        self.screen.blit(self.timer_surf, self.timer_rect)
        self.spells.draw(self.screen)

    def update_clases(self):
        self.spells.update()
        self.enemigos.update()
        self.bruja.update(self.pickup)
        self.pickup = None

    def manage_cooldowns(self):
        self.ataque_rapido_cd = ataque_cd(self.ataque_rapido_cd)
        self.ataque_fuerte_cd = ataque_cd(self.ataque_fuerte_cd)

        if self.ataque_rapido_cd != 0:
            ataque_rap_surf = self.fuente.render(f'{int(self.ataque_rapido_cd + 0.9)}', False, self.color)
            ataque_rap_rec = ataque_rap_surf.get_rect(center=(351, 368))
            self.screen.blit(self.iconcd_rap_surf, self.iconcd_rap_rec)
            self.screen.blit(ataque_rap_surf, ataque_rap_rec)

        else:
            self.screen.blit(self.icon_rap_surf, self.iconcd_rap_rec)

        if self.ataque_fuerte_cd != 0:
            ataque_fuerte_surf = self.fuente.render(f'{int(self.ataque_fuerte_cd + 0.9)}', False, self.color)
            ataque_fuerte_rec = ataque_fuerte_surf.get_rect(center=(451, 368))
            self.screen.blit(self.iconcd_fuerte_surf, self.iconcd_fuerte_rec)
            self.screen.blit(ataque_fuerte_surf, ataque_fuerte_rec)
        else:
            self.screen.blit(self.icon_fuerte_surf, self.iconcd_fuerte_rec)

        if self.tiempo != 0 and (self.tiempo - 9) % 12 < 3:
            spell_time_surf = self.fuente.render(str(3 - ((self.tiempo - 1) % 4)), False, self.color)
            spell_time_rect = spell_time_surf.get_rect(center=self.bruja.sprite.rect.midtop)
            self.screen.blit(spell_time_surf, spell_time_rect)

        if self.bruja.sprite.pickup_timer:
            pickup_rect = self.pickups[self.pickup_2].get_rect(center=self.bruja.sprite.rect.topright)
            self.screen.blit(self.pickups[self.pickup_2], pickup_rect)

    def pantalla_muerte(self):
        if self.tiempo >= 120:
            perdiste_surf = self.fuente.render('Tiempo  fuera', False, self.color)
        else:
            perdiste_surf = self.fuente.render('Has muerto', False, self.color)
        perdiste_rec = perdiste_surf.get_rect(center=(400, 100))
        self.score_surf = self.fuente.render(f'Score: {self.score}', False, self.color)
        self.score_rec = self.score_surf.get_rect(center=(400, 300))
        self.timer_rect = self.timer_surf.get_rect(center=(400, 330))

        # mostrar en pantalla
        self.screen.blit(self.fondo_muerto_surf, self.fondo_rec)
        self.screen.blit(perdiste_surf, perdiste_rec)
        self.screen.blit(self.muerte_surf, self.muerte_rec)
        self.screen.blit(self.score_surf, self.score_rec)
        self.screen.blit(self.timer_surf, self.timer_rect)

    def run(self):
        # loop principal
        while True:
            # event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # cierre de ventana
                    pygame.quit()
                    exit()
                if self.game_active:  # ingame
                    if event.type == pygame.USEREVENT + 1:  # spawnear enemigo
                        self.enemigos.add(Enemy(randint(0, 1), [self.ysort_group]))
                        self.spawn.play()
                        pygame.time.set_timer(self.enemigos_timer, self.enemigos_cd - self.score * 14 - self.tiempo * 2)
                    if event.type == pygame.USEREVENT + 2:
                        self.pickup = choice(list(self.pickups))
                        self.pickup_2 = self.pickup
                else:
                    if event.type == pygame.KEYDOWN:  # reiniciar partida
                        if event.key == pygame.K_SPACE:
                            self.reiniciar_level()

            if self.game_active:
                self.check_level_status()
                if not self.game_active:
                    continue
                self.mostrar_en_pantalla()
                self.update_clases()
                self.manage_cooldowns()
            else:
                self.pantalla_muerte()

            # display y fps
            pygame.display.update()
            self.fps.tick(60)


if __name__ == "__main__":
    Main().run()

