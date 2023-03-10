import os
import sys
import pygame
import random


def load_image(name):
    fullname = os.path.join('data/image', name)
    if not os.path.isfile(fullname):
        print(f'Файл с изображением {fullname} не найден')
        sys.exit()
    image = pygame.image.load(fullname)
    return image


pygame.mixer.init()
pygame.font.init()
lvl = 0
fon_flag = 0
enemy = pygame.sprite.Group()
player_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
an_sprites = pygame.sprite.Group()
help_grop = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
horizontal_border = pygame.sprite.Group()
vertical_border = pygame.sprite.Group()
ship_image = load_image("Ship (1).png")
fon_dif = load_image("fon.png")
metior_image = load_image("metior.png")
metior_23_image = load_image("mid_met-tran.png")
shooting_sound = pygame.mixer.Sound("data/sound/shoot.wav")
explo_sound = pygame.mixer.Sound("data/sound/invaderkilled.wav")
shooting_sound.set_volume(0.01)
explo_sound.set_volume(0.01)
game_over_sound = pygame.mixer.Sound("data/sound/1.mp3")
bul_im = load_image("bul.png")
help_im = load_image("help.png")
cristal_im = load_image("Big_cristal.png")
GRAVITY = 0.1
scor = 0
met_images = list()
met_images.append(metior_23_image)
met_images.append(metior_image)
with open("schor", "r") as f:
    best_scor = int(f.read())


def terminate():
    pygame.quit()
    sys.exit()


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(an_sprites)
        self.frames = list()
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


def start_screen():
    game_over_sound.play(-1)
    game_over_sound.set_volume(0.1)
    global best_scor, help_grop, player_group, bullet_group, horizontal_border, all_sprites, vertical_border, enemy
    with open("schor", "r") as f:
        best_scor = int(f.read())
    intro_text = ["Space defender", "", "", "",
                  f" Лучший результат: {best_scor}", "", "",
                  "Назмите конпку 'spase' чтобы начать игры",
                  "Назмите конпку на английскую кнопку 'H' чтобы",
                  "узнать правила игры"]
    global width, height
    fon = pygame.transform.scale(load_image('start.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 100
    pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    horizontal_border = pygame.sprite.Group()
    vertical_border = pygame.sprite.Group()
    enemy = pygame.sprite.Group()
    for line in intro_text:
        string_rendered = font.render(line, True, (255, 239, 213))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_h:
                help_screen()
        pygame.display.flip()
        clock.tick(fps)


def help_screen():
    global best_scor, help_grop, player_group, bullet_group, horizontal_border, \
        all_sprites, vertical_border, enemy, width, height
    intro_text = ["Правила игры:", "Нажимате кнопки wasd или стрелочки,",
                  "чтобы управлять судном.",
                  "Чтобы стрелять зажимате клавишу 'space.'", "", "Старайтесь уклонатся от метеоритов",
                  "и собирать кристалики", "нажмите space чтобы продолжить"]
    fon = pygame.transform.scale(fon_dif, (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 100
    pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    horizontal_border = pygame.sprite.Group()
    vertical_border = pygame.sprite.Group()
    enemy = pygame.sprite.Group()
    for line in intro_text:
        string_rendered = font.render(line, True, (255, 239, 213))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return
        pygame.display.flip()
        clock.tick(fps)


def dificult_screen():
    intro_text = ["Выберете сложность", "Нажмите на клавиатуре цифру обозночающую сложность",
                  "1.Легко Мало метеоритов", "2. Средняя сложность Метеоритов больше",
                  "3.Сложно  Метеоритов еще больше колличестов",
                  "4.impossible Метеоритов огромной колличесто,"]
    global width, height, lvl, fon_flag
    fon = pygame.transform.scale(fon_dif, (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, True, (255, 239, 213))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                lvl = 10
                fon_flag = 1
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                lvl = 15
                fon_flag = 2
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                lvl = 25
                fon_flag = 3
                return
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                lvl = 35
                fon_flag = 4
                return
        pygame.display.flip()
        clock.tick(fps)


def final_screen():
    game_over_sound.stop()
    global width, height, running, scor, an_sprites
    an_sprites = pygame.sprite.Group()
    intro_text = ["Defead", "", "", "",
                  f"Результат: {scor}", "", "",
                  "Нажмите нaа кнопу SPASE чтобы вернуктся ", "",
                                                              "на стартовый экран"]
    fon = pygame.transform.scale(load_image('final_fon.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 100
    animacion = AnimatedSprite(load_image("131-trans.png"), 8, 1, 400, 400)
    for line in intro_text:
        string_rendered = font.render(line, True, (255, 239, 213))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if best_scor < scor:
                    with open("schor", "w") as f:
                        f.write(str(scor))
                Control_screen()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                Control_screen()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                running = False
                if best_scor < scor:
                    with open("schor", "w") as f:
                        f.write(str(scor))
                scor = 0
                return
        fon = pygame.transform.scale(load_image('final_fon.png'), (width, height))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font(None, 30)
        text_coord = 100
        for line in intro_text:
            string_rendered = font.render(line, True, (255, 239, 213))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        an_sprites.draw(screen)
        an_sprites.update()
        pygame.display.flip()
        clock.tick(fps)


def Control_screen():
    global running
    intro_text = ["Вы точно хотите выйти?", "Нажмите escape, чтобы выйти",
                  'Или нажмите spase чтобы продолжить']
    fon = pygame.transform.scale(load_image('final_fon.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 100
    for line in intro_text:
        string_rendered = font.render(line, True, (255, 239, 213))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                terminate()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return
        pygame.display.flip()
        clock.tick(fps)


class Particle(pygame.sprite.Sprite):
    fire = [load_image('metior.png')]
    for scale in (5, 10, 15, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super(Particle, self).__init__(all_sprites)
        self.image = random.choice(self.fire[1:])
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position):
    particle_count = 5
    numbers = range(-5, 5)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


class Metior(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super(Metior, self).__init__(all_sprites)
        self.add(enemy)
        self.radius = radius
        self.image = pygame.transform.scale(metior_image, (50, 50))
        self.rect = pygame.Rect(x, y, radius, radius)
        self.vx = random.randint(-1, 1)
        self.vy = 1 + scor / 500
        self.metior_image_1 = random.choice(met_images)
        self.image = pygame.transform.scale(self.metior_image_1, (radius, radius))
        self.rect = pygame.Rect(x, y, radius, radius)
        self.vx = random.randint(-2, 2)
        self.vy = random.randint(1, 5)

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_border):
            self.kill()
        if pygame.sprite.spritecollideany(self, vertical_border):
            self.kill()


class Buff(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Buff, self).__init__(all_sprites)
        self.add(help_grop)
        self.image = pygame.transform.scale(help_im, (25, 25))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        global scor, buff_flag
        self.rect.y += 3
        if self.rect.top < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, player_group, False):
            self.kill()
            buff_flag = True
            if fon_flag == 1:
                scor += 1
            if fon_flag == 2:
                scor += 2
            if fon_flag == 3:
                scor += 4
            if fon_flag == 4:
                scor += 8


class Buff_2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Buff_2, self).__init__(all_sprites)
        self.add(help_grop)
        self.image = pygame.transform.scale(cristal_im, (25, 25))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        global scor, buff_flag
        self.rect.y += 3
        if self.rect.top < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, player_group, False):
            self.kill()
            buff_flag = True
            if fon_flag == 1:
                scor += 5
            if fon_flag == 2:
                scor += 10
            if fon_flag == 3:
                scor += 20
            if fon_flag == 4:
                scor += 40


class Bulet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Bulet, self).__init__(all_sprites)
        self.add(bullet_group)
        self.image = pygame.transform.scale(bul_im, (20, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        shooting_sound.play()

    def update(self):
        global scor
        self.rect.y -= 7
        if self.rect.top > 600:
            self.kill()
        if pygame.sprite.spritecollide(self, enemy, True):
            self.kill()
            explo_sound.play()
            create_particles((self.rect.x, self.rect.y))
            if random.randrange(1, 10) == 1:
                Buff(self.rect.x, self.rect.y)
            if random.randrange(1, 50) == 1:
                Buff_2(self.rect.x, self.rect.y)
            if fon_flag == 1:
                scor += 2
            if fon_flag == 2:
                scor += 4
            if fon_flag == 3:
                scor += 8
            if fon_flag == 4:
                scor += 16


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_border)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_border)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Player, self).__init__(all_sprites)
        self.add(player_group)
        self.image = pygame.transform.scale(ship_image, (40, 40))
        self.rect = pygame.Rect(20, 20, 40, 40)
        self.rect.center = (x, y)
        self.last_shot = pygame.time.get_ticks()

    def draw(self):
        screen.blit(self.image, self.rect.topleft)

    def move(self):
        global player_group, all_sprites, bullet_group, horizontal_border, vertical_border, enemy
        keys = pygame.key.get_pressed()
        time_now = pygame.time.get_ticks()
        cooldown = 200
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= VEL
            if self.rect.x < 0:
                self.rect.x = 600
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += VEL
            if self.rect.x > 600:
                self.rect.x = 0
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= VEL
            if self.rect.y < 0:
                self.rect.y = 600
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += VEL
            if self.rect.y > 600:
                self.rect.y = 0
        if keys[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            Bulet(self.rect.left + 20, self.rect.top)
            self.last_shot = time_now
        if pygame.sprite.spritecollide(self, enemy, False):
            final_screen()
            self.kill()
            player_group = pygame.sprite.Group()
            all_sprites = pygame.sprite.Group()
            bullet_group = pygame.sprite.Group()
            horizontal_border = pygame.sprite.Group()
            vertical_border = pygame.sprite.Group()
            enemy = pygame.sprite.Group()


if __name__ == '__main__':
    pygame.init()
    main_run = True
    while main_run:
        pygame.display.set_caption('Space defender')
        size = width, height = 600, 600
        screen = pygame.display.set_mode(size)
        fps = 50
        clock = pygame.time.Clock()
        screen_rect = (0, 0, width, height)
        start_screen()
        dificult_screen()
        running = True
        Border(5, 5, width - 5, 5)
        Border(5, height - 5, width - 5, height - 5)
        Border(5, 5, 5, height - 5)
        Border(width - 5, 5, width - 5, height - 5)
        player = Player(300, 550)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Control_screen()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    Control_screen()
            if len(enemy) < lvl:
                Metior(random.randrange(50, 80), random.randrange(0, 550), 20)
            if fon_flag == 1:
                fon = pygame.transform.scale(load_image('Batl_fon.png'), (width, height))
                VEL = 10
            if fon_flag == 2:
                fon = pygame.transform.scale(load_image('batl_fon2.png'), (width, height))
                VEL = 10
            if fon_flag == 3:
                fon = pygame.transform.scale(load_image('batl_fon3.png'), (width, height))
                VEL = 5
            if fon_flag == 4:
                fon = pygame.transform.scale(load_image('batl_fon4.png'), (width, height))
                VEL = 5
            screen.blit(fon, (0, 0))
            font = pygame.font.Font(None, 30)
            text_coord = 10
            string_rendered = font.render(f"Очки: {scor}", True, (255, 239, 213))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
            player.move()
            player.draw()
            all_sprites.draw(screen)
            all_sprites.update()
            pygame.display.flip()
            clock.tick(fps)
    pygame.quit()
