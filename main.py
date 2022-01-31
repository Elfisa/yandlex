import os
import pygame
import random
import sys

pygame.init()
SIDE = 710
SIZE = WIDTH, HEIGHT = SIDE, SIDE


def game_font(font_size, font_name):
    # из шрифтов ещё Mistral стильненько выглядит (единственный для кириллицы подходит)), Chiller как будто хоррор-игра,
    # Harrington как что-то про средневековых королей, а Jokerman что-то просто очень весёленькое, вайбы Куми-Куми хыхы
    # в принципе можно поискать и скачать какой-нибудь симатичный шрифт, который подойдёт для кириллицы
    return pygame.font.SysFont(font_name, font_size)


def decimal_conversion(n, res_system):  # десятичное число(int) и сс, в которую надо перевести(int)
    result = []
    alphabet = '0123456789ABCDEF'
    while n >= res_system:
        new_n = n // res_system
        result.append(alphabet[n - (new_n * res_system)])
        n = new_n
    if n > 0:
        result.append(alphabet[n])
    return ''.join(result)[::-1]


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if color_key:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_group, sheet, columns, rows, x, y):
        super().__init__(sprite_group)
        self.frames = []
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


class Buttons:
    def __init__(self, to_sys, font_name):
        self.to_sys = to_sys
        self.font = font_name
        btns_dict = {16: 2, 8: 3, 4: 4, 2: 8}
        self.is_pause = False
        self.btns_n = btns_dict[to_sys]
        self.btn_font = game_font(WIDTH // 12, font_name)
        self.btn_size, self.extrabtn_size = WIDTH // 10, WIDTH // (10 + to_sys // 2)
        self.btns_x = []
        self.btn_y = HEIGHT - self.btn_size - 10  # для всех кнопок одинаковое значение
        self.solution = ['0'] * self.btns_n
        self.extra_btns = [False, None]  # если True, второй элемент - номер кнопки
        self.alphabet = '0123456789ABCDEF'

    def render(self, surface):
        pygame.draw.rect(surface, (186, 172, 199), (WIDTH - 52, 8, 44, 44))  # кнопка паузы
        if not self.is_pause:
            pygame.draw.line(surface, (106, 92, 119), (WIDTH - 36, 16), (WIDTH - 36, 42), 4)
            pygame.draw.line(surface, (106, 92, 119), (WIDTH - 26, 16), (WIDTH - 26, 42), 4)
        else:
            pygame.draw.polygon(surface, (106, 92, 119),
                                ((WIDTH - 39, 16), (WIDTH - 20, 29), (WIDTH - 39, 42)))
        if self.btns_x:
            for i in range(len(self.btns_x)):
                pygame.draw.rect(surface, (186, 172, 199), (self.btns_x[i], self.btn_y, self.btn_size, self.btn_size))
                numb = self.btn_font.render(self.solution[i], True, (61, 40, 89))
                x = self.btns_x[i] + self.btn_size // 2 - numb.get_width() // 2
                y = self.btn_y + self.btn_size // 2 - numb.get_height() // 2
                surface.blit(numb, (x, y))
                if self.extra_btns[0] and self.extra_btns[1] == i and not self.is_pause:
                    self.add_btns(surface, i)
        else:
            for i in range(self.btns_n):
                btn_x = ((WIDTH - self.btn_size * self.btns_n) / (self.btns_n + 1)) * (i + 1) + self.btn_size * i
                self.btns_x.append(btn_x)

    def add_btns(self, surface, i):
        pygame.draw.rect(surface, (186, 172, 199), (self.btns_x[i], self.btn_y - self.extrabtn_size * self.to_sys,
                                                    self.extrabtn_size, self.extrabtn_size * self.to_sys))
        for j in range(self.to_sys):
            x1, y1 = self.btns_x[i], self.btn_y - self.extrabtn_size * (self.to_sys - j - 1)
            x2, y2 = self.btns_x[i] + self.extrabtn_size, self.btn_y - self.extrabtn_size * (self.to_sys - j - 1)
            pygame.draw.line(surface, (106, 92, 119), (x1, y1), (x2, y2), 3)
            new_numb = game_font(WIDTH // (12 + self.to_sys // 2), self.font).render(self.alphabet[j], True,
                                                                                     (61, 40, 89))
            new_x = self.btns_x[i] + self.extrabtn_size // 2 - new_numb.get_width() // 2
            new_y = (self.btn_y + self.extrabtn_size // 2 - new_numb.get_height() // 2) - self.extrabtn_size * (j + 1)
            surface.blit(new_numb, (new_x, new_y))

    def get_btn(self, mouse_pos):  # если кликнули на кнопку, возвращает её номер, иначе None
        if WIDTH - 52 <= mouse_pos[0] <= WIDTH - 8 and 8 <= mouse_pos[1] <= 52:
            return 'pause'
        for i in range(len(self.btns_x)):
            if self.btns_x[i] <= mouse_pos[0] <= self.btns_x[i] + self.btn_size:
                if self.btn_y <= mouse_pos[1] <= self.btn_y + self.btn_size:
                    return [i, 0]
                if self.extra_btns[0]:
                    for j in range(self.to_sys + 1):
                        bottom_line = self.btn_y - self.extrabtn_size * (j - 1)
                        if self.btn_y - self.extrabtn_size * j <= mouse_pos[1] <= bottom_line:
                            return [i, j]  # [номер по горизонтали, номер по вертикали (снизу)]
        return None

    def get_click(self, mouse_pos):
        btn = self.get_btn(mouse_pos)
        if btn == 'pause':
            self.is_pause = not self.is_pause
        elif btn and not self.is_pause:
            self.on_click(btn)

    def on_click(self, btn_xy):
        if not btn_xy[1]:
            if self.to_sys == 2:
                self.solution[btn_xy[0]] = '0' if int(self.solution[btn_xy[0]]) else '1'
            else:
                self.extra_btns = [True, btn_xy[0]] if self.extra_btns[1] != btn_xy[0] else [False, None]
        else:
            self.solution[btn_xy[0]] = self.alphabet[btn_xy[1] - 1]
            self.extra_btns = [False, None]

    def check_solution(self, to_system_numbs):  # постоянная проверка, не набрали ли правильное число
        if any(map(lambda el: el != '0', self.solution)):
            str_solution = ''.join(self.solution)
            while str_solution[0] == '0':
                str_solution = str_solution[1:]
            if str_solution in to_system_numbs:
                return to_system_numbs.index(str_solution)
        return None


class MovingObjects:
    def __init__(self, from_sys, to_sys, font_name):
        self.from_sys, self.to_sys = from_sys, to_sys
        self.font = font_name
        self.numb_list = []
        self.score = 0
        self.character = None
        self.fireworks = []
        self.firework_sprites, self.character_sprites = pygame.sprite.Group(), pygame.sprite.Group()
        self.star_sprites = pygame.sprite.Group()
        self.star_image = load_image("drawing.png", -1)

    def add_numb(self):
        n = random.randint(1, 255)
        while decimal_conversion(n, self.from_sys) in map(lambda lst: lst[1], self.numb_list):
            n = random.randint(1, 255)
        text = game_font(35, self.font).render(decimal_conversion(n, self.from_sys), True, (0, 0, 0))
        star_sprite = pygame.sprite.Sprite()
        star_sprite.image = pygame.transform.scale(self.star_image, (text.get_width() + 110, text.get_height() + 20))
        star_sprite.rect = star_sprite.image.get_rect()
        x_coord = random.randrange(9, WIDTH - text.get_width() - 115, 3)
        star_sprite.rect.x, star_sprite.rect.y = x_coord, 0
        self.star_sprites.add(star_sprite)
        self.numb_list.append([[x_coord, 0], decimal_conversion(n, self.to_sys), star_sprite, text])

    def render(self, surface, is_pause, t, btns_class_obj):
        if is_pause:
            self.pause(surface)
        else:
            excess_n = btns_class_obj.check_solution([el[1] for el in self.numb_list])   # пора delete n, тк его набрали
            numb_texts = []
            for i in range(len(self.numb_list)):
                self.numb_list[i][0][1] += t
                self.numb_list[i][2].rect.y = self.numb_list[i][0][1]
                x = self.numb_list[i][0][0] + 55
                y = self.numb_list[i][0][1] + 10
                numb_texts.append((self.numb_list[i][3], (x, y)))
            self.star_sprites.draw(surface)
            for text in numb_texts:  # отдельный цикл, чтобы текст размещался поверх картинок (а не наоборот)
                surface.blit(text[0], text[1])
            if excess_n or excess_n == 0:
                self.delete_excess(excess_n, btns_class_obj)

    def delete_excess(self, n, btns_class_obj):
        coords = self.numb_list[n][0]
        firework = AnimatedSprite(self.firework_sprites, load_image("effect_009.png", -1),
                                  5, 8, coords[0] + self.numb_list[n][3].get_width() // 2 - 40, coords[1] - 40)
        self.fireworks.append([firework, 0])
        self.numb_list[n][2].kill()
        del self.numb_list[n]
        self.score += 1
        btns_class_obj.solution = ['0'] * btns_class_obj.btns_n  # обнуление кнопочек

    def pause(self, surface):
        text = game_font(90, self.font).render("PAUSE", True, (61, 40, 89))
        x = WIDTH // 2 - text.get_width() // 2
        y = HEIGHT // 2 - text.get_height() // 2
        pygame.draw.rect(surface, (186, 172, 199), (x - 10, y - 50, text.get_width() + 20, text.get_height() - 7))
        pygame.draw.rect(surface, (61, 40, 89), (x - 10, y - 50, text.get_width() + 20, text.get_height() - 7), 4)
        surface.blit(text, (x, y - 50))
        if not self.character:
            self.character = AnimatedSprite(self.character_sprites,
                                            load_image("dancing.png", -1), 8, 1, WIDTH // 2 - 50, y + 75)

    def animate_fireworks(self, surface, clock):
        first_animation_end = False
        self.firework_sprites.draw(surface)
        if clock.tick(20):
            for firework in self.fireworks:
                if firework[1] < 40:
                    firework[0].update()
                    firework[1] += 1
                else:
                    first_animation_end = True
            if first_animation_end:
                del self.fireworks[0]

    def check_gameover(self):
        for i in range(len(self.numb_list)):
            if self.numb_list[i][0][1] >= HEIGHT - WIDTH // 10 - 76:
                return True
        return False


class GameOverScreen:
    def __init__(self, font_name):
        self.font = font_name
        replay_txt = game_font(WIDTH // 10, font_name).render('replay', True, (186, 172, 199))
        replay_btn_info = [WIDTH // 2 - replay_txt.get_width() // 2 - 10, HEIGHT // 1.7,  # x, y
                           replay_txt.get_width() + 18, replay_txt.get_height() - 10]  # width, height
        return_txt = game_font(WIDTH // 14, font_name).render('return to menu', True, (186, 172, 199))
        return_btn_info = [WIDTH // 2 - return_txt.get_width() // 2 - 10, HEIGHT // 1.3,  # x, y
                           return_txt.get_width() + 18, return_txt.get_height() - 10]
        self.texts = [replay_txt, return_txt]
        self.info = [replay_btn_info, return_btn_info]

    def render(self, surface, score):
        gameover_text = game_font(WIDTH // 10, self.font).render(f"GAME OVER", True, (1, 0, 28))
        score_text = game_font(WIDTH // 10, self.font).render(f"your score: {score}", True, (1, 0, 28))
        gameover_x = WIDTH // 2 - gameover_text.get_width() // 2
        score_x = WIDTH // 2 - score_text.get_width() // 2
        y = HEIGHT // 4 - gameover_text.get_height() // 2
        pygame.draw.rect(surface, (186, 172, 199), (WIDTH // 2 - (score_text.get_width() + 61) // 2, 101,
                                                    score_text.get_width() + 61, 158))
        pygame.draw.rect(surface, (61, 40, 89), (WIDTH // 2 - (score_text.get_width() + 61) // 2, 101,
                                                 score_text.get_width() + 61, 158), 4)
        surface.blit(gameover_text, (gameover_x, y - 40))
        surface.blit(score_text, (score_x, y + 40))
        self.draw_buttons(surface)

    def draw_buttons(self, surface):
        for i in range(2):
            info = self.info[i]
            pygame.draw.rect(surface, (1, 0, 28), (info[0], info[1], info[2], info[3]))
            pygame.draw.rect(surface, (255, 255, 255), (info[0], info[1], info[2], info[3]), 2)
            surface.blit(self.texts[i], (info[0] + 10, info[1] - 8))

    def get_btn(self, mouse_pos):
        if self.info[0][0] <= mouse_pos[0] <= self.info[0][0] + self.info[0][2] and \
                self.info[0][1] <= mouse_pos[1] <= self.info[0][1] + self.info[0][3]:
            return 'replay'
        elif self.info[1][0] <= mouse_pos[0] <= self.info[1][0] + self.info[1][2] and \
                self.info[1][1] <= mouse_pos[1] <= self.info[1][1] + self.info[1][3]:
            return 'return to menu'
        return None


class StoreScreen:
    def __init__(self):
        self.product = (0, 'background')
        self.backgrounds = ['asia', 'forest', 'green_street', 'house', 'idk', 'leaves', 'mountain', 'sky',
                            'night_forest', 'night_water', 'river', 'romantic_forest', 'street', 'sunset', 'sunrise']
        self.fonts = ['Mistral', 'Chiller', 'Jokerman', 'Harrington']
        self.sprites = self.current_sprite = None
        self.coin_img = load_image('lil_coins.png', -1)
        self.n_is_changed = False

    def render(self, screen):
        if not self.sprites:
            self.create_coin_sprites((40, 43), WIDTH - WIDTH * 0.08, HEIGHT * 0.03)
            self.create_coin_sprites((70, 75), WIDTH // 2 + WIDTH // 10, HEIGHT * 0.86)
        if self.n_is_changed or not self.current_sprite:
            if self.product[1] == 'background':
                self.create_background_sprite()
        self.sprites.draw(screen)
        self.draw_btns(screen)
        self.add_text(screen)

    def create_coin_sprites(self, img_size, x, y):
        if not self.sprites:
            self.sprites = pygame.sprite.Group()
        coin_sprite = pygame.sprite.Sprite()
        coin_sprite.image = pygame.transform.scale(self.coin_img, img_size)
        coin_sprite.rect = coin_sprite.image.get_rect()
        coin_sprite.rect.x, coin_sprite.rect.y = x, y
        self.sprites.add(coin_sprite)

    def create_background_sprite(self):
        if self.current_sprite:
            self.current_sprite.kill()
        self.current_sprite = pygame.sprite.Sprite()
        img = load_image(f'{self.backgrounds[self.product[0]]}.jpg')
        self.current_sprite.image = pygame.transform.scale(img, (SIDE * 0.7, SIDE * 0.7))
        self.current_sprite.rect = self.current_sprite.image.get_rect()
        self.current_sprite.rect.x, self.current_sprite.rect.y = WIDTH * 0.15, HEIGHT * 0.15
        self.sprites.add(self.current_sprite)

    def draw_btns(self, screen):
        if self.product[0] != 1:
            pygame.draw.rect(screen, (186, 172, 199), (20, HEIGHT - 70, 70, 50))
            pygame.draw.polygon(screen, (106, 92, 119), ((50, HEIGHT - 65), (30, HEIGHT - 45), (50, HEIGHT - 25),
                                                         (50, HEIGHT - 35), (80, HEIGHT - 35), (80, HEIGHT - 55),
                                                         (50, HEIGHT - 55)))
        if self.product[0] != len(self.backgrounds) - 1:
            pygame.draw.rect(screen, (186, 172, 199), (WIDTH - 90, HEIGHT - 70, 70, 50))
            pygame.draw.polygon(screen, (106, 92, 119), ((WIDTH - 50, HEIGHT - 65), (WIDTH - 30, HEIGHT - 45),
                                                         (WIDTH - 50, HEIGHT - 25), (WIDTH - 50, HEIGHT - 35),
                                                         (WIDTH - 80, HEIGHT - 35), (WIDTH - 80, HEIGHT - 55),
                                                         (WIDTH - 50, HEIGHT - 55)))

    def add_text(self, screen):
        text = game_font(90, 'Ink Free').render("100", True, (186, 172, 19))
        x = WIDTH // 2 - text.get_width()
        y = HEIGHT * 0.86
        pygame.draw.rect(screen, (61, 40, 89), (x - 10, y - 50, text.get_width() + 20, text.get_height() - 7), 4)
        screen.blit(text, (x, y - 50))

    def get_click(self, mouse_pos):
        pass

    def get_btn(self, mouse_pos):
        pass

    def on_click(self):
        pass


def terminate():
    pygame.quit()
    sys.exit()


def store():
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('Добро пожаловать в магазинчик!)')
    store_screen = StoreScreen()
    while True:
        fon = pygame.transform.scale(load_image('space.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                store_screen.get_click(event.pos)
        store_screen.render(screen)
        pygame.display.flip()


def gameover(surface, fon_img, score, font_name):
    pygame.display.set_caption('Ничто не вечно, и эта игра тоже)')
    gameover_screen = GameOverScreen(font_name)
    character_sprites = pygame.sprite.Group()
    img = random.choice(['happy1.png', 'happy2.png', 'happy3.png', 'happy4.png']) if score else 'calm_character.png'
    character = AnimatedSprite(character_sprites, load_image(img, -1), 8, 1, WIDTH // 2 - 55, HEIGHT // 2.6)
    character_clock = pygame.time.Clock()
    btn_is_chosen = info = False
    while True:
        fon = pygame.transform.scale(load_image(fon_img), (WIDTH, HEIGHT))
        surface.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                btn = gameover_screen.get_btn(event.pos)
                if btn == 'replay':
                    return True
                elif btn == 'return to menu':
                    return False
            if event.type == pygame.MOUSEMOTION:
                btn = gameover_screen.get_btn(event.pos)
                if btn:
                    btn_is_chosen = True
                    info = gameover_screen.info[0] if btn == 'replay' else gameover_screen.info[1]
                else:
                    btn_is_chosen = False
        gameover_screen.render(surface, score)
        character_sprites.draw(surface)
        if btn_is_chosen:
            pygame.draw.rect(surface, (32, 15, 128), (info[0], info[1], info[2], info[3]), 2)
        if character_clock.tick(7):
            character.update()
        pygame.display.flip()


def game(from_sys=16, to_sys=16, frequency=1000, speed=100, fon_img='romantic_forest.jpg', font_name='Ink Free'):
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Let's gooooo")
    MYEVENTTYPE = pygame.USEREVENT + 1  # каждые frequency миллисекунд падает новое число
    pygame.time.set_timer(MYEVENTTYPE, frequency)
    clock, firework_clock, character_clock = pygame.time.Clock(), pygame.time.Clock(), pygame.time.Clock()
    game_is_over = False
    btns = Buttons(to_sys, font_name)
    moving_objs = MovingObjects(from_sys, to_sys, font_name)
    while True:
        fon = pygame.transform.scale(load_image(fon_img), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                btns.get_click(event.pos)
            if event.type == MYEVENTTYPE and not (game_is_over + btns.is_pause):
                moving_objs.add_numb()
        if btns.is_pause:
            clock.tick()
            moving_objs.render(screen, True, 0, btns)
            btns.render(screen)
            moving_objs.character_sprites.draw(screen)
            if character_clock.tick(10):
                moving_objs.character.update()
        elif not game_is_over:
            t = speed * clock.tick() / 1000
            moving_objs.render(screen, False, t, btns)
            btns.render(screen)
            if moving_objs.fireworks:
                moving_objs.animate_fireworks(screen, firework_clock)
            game_is_over = moving_objs.check_gameover()
        else:
            replay = gameover(screen, fon_img, moving_objs.score, font_name)
            if replay:
                game_is_over = False
                btns = Buttons(to_sys, font_name)
                moving_objs = MovingObjects(from_sys, to_sys, font_name)
                clock.tick()
            else:
                return
        pygame.display.flip()


if __name__ == '__main__':
    # gameover(pygame.display.set_mode(SIZE), 'space.jpg', 7988, 'Ink Free')
    # game()
    store()
