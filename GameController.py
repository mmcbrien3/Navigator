import pygame, time, math
import PathGenerator, Ship, Obstruction, NEATHandler

width = 480
height = 640

class GameController(object):

    def __init__(self, ai_player=None):
        self.ai_player = ai_player
        self.setup()
        self.play_game()

    def setup(self):
        pygame.init()

        pygame.font.init()
        self.screen_font = pygame.font.SysFont('Comic Sans MS', 12)

        self.screen = pygame.display.set_mode([width, height])
        pygame.display.set_caption("My Computer Learns Pacman")
        self.playing_game = True
        self.score = 0
        self.clock = pygame.time.Clock()

        self.ship = Ship.Ship(width / 2, height - 42, 4)

        self.path_generator = PathGenerator.PathGenerator(480, 640)

    def play_game(self):
        while self.playing_game:

            if self.ai_player is None:
                self.read_keyboard_input()
            else:
                self.get_ai_stimuli()
                self.get_ai_input()

            self.draw_everything()
            self.path_generator.get_next_water_position()

            self.check_for_collision()
            self.path_generator.update_obstructions(self.score)
            self.score += 1

            pygame.display.update()
            pygame.event.pump()

            self.clock.tick(60)


    def check_for_collision(self):
        for b in self.path_generator.right_banks[:50]:
            dx = b.rect.left - self.ship.rect.left
            dy = b.rect.top - self.ship.rect.top
            if self.ship.mask.overlap(b.mask, (dx, dy)):
                self.playing_game = False
        for b in self.path_generator.left_banks[:50]:
            dx = b.rect.left - self.ship.rect.left
            dy = b.rect.top - self.ship.rect.top
            if self.ship.mask.overlap(b.mask, (dx, dy)):
                self.playing_game = False
        if len(self.path_generator.obstructions) > 0:
            ob = self.path_generator.obstructions[0]
            dx = ob.rect.left - self.ship.rect.left
            dy = ob.rect.top - self.ship.rect.top
            if self.ship.mask.overlap(ob.mask, (dx, dy)):
                self.playing_game = False

    def read_keyboard_input(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT]:
            self.ship.move_left()
        if pressed_keys[pygame.K_RIGHT]:
            self.ship.move_right()

    def get_ai_input(self):
        key = self.ai_player.select_key_from_net()
        if key == "left":
            self.ship.move_left()
        if key == "right":
            self.ship.move_right()

    def get_ai_stimuli(self):
        dist_to_bank_x = self.ship.rect.x - self.path_generator.left_banks[0].rect.x
        if len(self.path_generator.obstructions) > 0:
            dist_to_obstruction_x = self.ship.rect.x - self.path_generator.obstructions[0].rect.x
            dist_to_obstruction_y = self.ship.rect.y - self.path_generator.obstructions[0].rect.y
        else:
            dist_to_obstruction_x = 0
            dist_to_obstruction_y = 640
        self.ai_player.set_stimuli((dist_to_bank_x, dist_to_obstruction_x, dist_to_obstruction_y))

    def draw_everything(self):
        self.draw_background()
        self.draw_path()
        self.draw_banks()
        self.draw_obstructions()
        self.draw_ship()
        self.draw_text()

    def draw_ship(self):
        self.screen.blit(self.ship.image, (self.ship.x, height - 42))

    def draw_background(self):
        self.screen.fill((0, 0, 0))

    def draw_path(self):
        water_pos = self.path_generator.water_positions
        for i, w in enumerate(water_pos):
            self.screen.blit(PathGenerator.water_line, (w, height - i - 1))

    def draw_obstructions(self):
        for o in self.path_generator.obstructions:
            self.screen.blit(o.image, (o.rect.x, o.rect.y))


    def draw_banks(self):
        left_banks = self.path_generator.left_banks
        for i, b in enumerate(left_banks):
            self.screen.blit(PathGenerator.bank, (b.x, height - i - 1))
        right_banks = self.path_generator.right_banks
        for i, b in enumerate(right_banks):
            self.screen.blit(PathGenerator.bank, (b.x, height - i - 1))

    def draw_text(self):
        score_surface = self.screen_font.render('Score: %s' % self.score, False, (255, 255, 255))
        self.screen.blit(score_surface, (5, 5))

        if not self.ai_player is None:
            gen_surface = self.screen_font.render('Gen: %s' % self.ai_player.gen, False, (255,255,255))
            num_surface = self.screen_font.render('Num: %s' % self.ai_player.num, False, (255,255,255))

            self.screen.blit(gen_surface, (5, 37))
            self.screen.blit(num_surface, (5, 69))


if __name__ == '__main__':
    GameController()
