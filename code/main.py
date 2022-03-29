import pygame
import sys
import time
from sprites import BG, Ground, Obstacle, Plane
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, FRAMERATE


class Game:
    def __init__(self):

        # setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.active = True

        # sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # scale factor
        bg_height = pygame.image.load(
            "graphics/environment/background.png"
        ).get_height()
        self.scale_factor = WINDOW_HEIGHT / bg_height

        # sprite setup
        BG(self.all_sprites, self.scale_factor)
        Ground([self.all_sprites, self.collision_sprites], self.scale_factor)
        self.plane = Plane(self.all_sprites, self.scale_factor * 0.6)

        # timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1200)

        # text
        self.font = pygame.font.Font("graphics/font/BD_Cartoon_Shout.ttf", 30)
        self.score = 0

        # menu
        self.menu_surface = pygame.image.load("graphics/ui/menu.png").convert_alpha()
        self.menu_rect = self.menu_surface.get_rect(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        )

    def collisions(self):
        if (
            pygame.sprite.spritecollide(
                self.plane,
                self.collision_sprites,
                dokill=False,
                collided=pygame.sprite.collide_mask,
            )
            or self.plane.rect.top <= 0
        ):
            self.active = False

    def display_score(self):
        if self.active:
            self.score = pygame.time.get_ticks() // 1000
            y = WINDOW_HEIGHT / 10
        else:
            y = WINDOW_HEIGHT / 2 + self.menu_rect.height * 0.6

        score_surf = self.font.render(f"{self.score}", True, "black")
        score_rect = score_surf.get_rect(midtop=(WINDOW_WIDTH / 2, y))
        self.display_surface.blit(score_surf, score_rect)

    def run(self):
        last_time = time.time()
        while True:

            # delta time
            dt = time.time() - last_time
            last_time = time.time()

            # event loop
            for event in pygame.event.get(
                [pygame.QUIT, pygame.MOUSEBUTTONDOWN, self.obstacle_timer]
            ):
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.plane.jump()
                if event.type == self.obstacle_timer:
                    Obstacle(
                        [self.all_sprites, self.collision_sprites], self.scale_factor
                    )

            # game logic
            self.display_surface.fill((0, 0, 0))
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)

            self.display_score()

            if self.active:
                self.collisions()
            else:
                self.display_surface.blit(self.menu_surface, self.menu_rect)

            pygame.display.update()
            self.clock.tick(FRAMERATE)


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
