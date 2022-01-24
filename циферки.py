import pygame
import random
import sys
fontt = 'Ink Free'  # ещё Mistral стильненько выглядит, Chiller как будто хоррор-игра,
# Harrington как что-то про средневековых королей, а Jokerman что-то просто очень весёленькое, вайбы Куми-Куми


def decimal_conversion(n, to_system):  # десятичное число(int) и сс, в которую надо перевести(int)
    result = []
    ALPHABET = '0123456789ABCDEF'
    while n >= to_system:
        new_n = n // to_system
        result.append(ALPHABET[n - (new_n * to_system)])
        n = new_n
    if n > 0:
        result.append(ALPHABET[n])
    return ''.join(result)[::-1]


pygame.init()
size = WIDTH, HEIGHT = 700, 700
screen = pygame.display.set_mode(size)
font = pygame.font.SysFont(fontt, 40)
TO_SYSTEM, FROM_SYSTEM = 16, 2  # в какую, из какой сс переводить


def terminate():
    pygame.quit()
    sys.exit()


class Buttons:
    def __init__(self, height, width, to_system):
        self.width, self.height = width, height
        self.to_system = to_system
        btns_dict = {16: 2, 8: 3, 4: 4, 2: 8}
        self.btns_n = btns_dict[to_system]
        self.btns_x = []
        self.btn_y = height - 80  # для всех кнопок одинаковое значение
        self.solution = ['0'] * self.btns_n
        self.extra_btns = [False, None]  # если True, второй элемент - номер кнопки
        self.alphabet = '123456789ABCDEF'
        self.btn_font = pygame.font.SysFont(fontt, 55)

    def render(self, screen, pause):
        pygame.draw.rect(screen, (186, 172, 199), (self.width - 52, 8, 44, 44))  # кнопка паузы
        if not pause:
            pygame.draw.line(screen, (106, 92, 119), (self.width - 36, 16), (self.width - 36, 42), 4)
            pygame.draw.line(screen, (106, 92, 119), (self.width - 26, 16), (self.width - 26, 42), 4)
        else:
            pygame.draw.polygon(screen, (106, 92, 119),
                                ((self.width - 39, 16), (self.width - 20, 29), (self.width - 39, 42)))
        if self.btns_x:
            for i in range(len(self.btns_x)):
                pygame.draw.rect(screen, (186, 172, 199), (self.btns_x[i], self.btn_y, 70, 70))
                numb = self.btn_font.render(self.solution[i], True, (61, 40, 89))
                x = self.btns_x[i] + 35 - numb.get_width() // 2
                y = self.btn_y + 35 - numb.get_height() // 2
                screen.blit(numb, (x, y))
                if self.extra_btns[0] and self.extra_btns[1] == i:
                    self.add_btns(i)
        else:
            for i in range(self.btns_n):
                btn_x = ((self.width - 70 * self.btns_n) / (self.btns_n + 1)) * (i + 1) + 70 * i
                self.btns_x.append(btn_x)

    def add_btns(self, i):
        add = self.to_system - 1
        bsize = 41 if self.to_system == 16 else 70
        bfont = pygame.font.SysFont(fontt, 30) if self.to_system == 16 else self.btn_font
        pygame.draw.rect(screen, (186, 172, 199), (self.btns_x[i], self.btn_y - bsize * add,
                                                   bsize, bsize * add))
        for j in range(add):
            pygame.draw.line(screen, (106, 92, 119), (self.btns_x[i], self.btn_y - bsize * (add - j - 1)),
                             (self.btns_x[i] + bsize, self.btn_y - bsize * (add - j - 1)), 3)
            new_numb = bfont.render(self.alphabet[j], True, (61, 40, 89))
            new_x = self.btns_x[i] + bsize // 2 - new_numb.get_width() // 2
            new_y = (self.btn_y + bsize // 2 - new_numb.get_height() // 2) - bsize * (j + 1)
            screen.blit(new_numb, (new_x, new_y))

    def get_btn(self, mouse_pos):  # если кликнули на кнопку, возвращает её номер, иначе None
        if self.width - 52 <= mouse_pos[0] <= self.width - 8 and 8 <= mouse_pos[1] <= 52:
            return 'pause'
        bsize = 41 if self.to_system == 16 else 70
        for i in range(len(self.btns_x)):
            if self.btns_x[i] <= mouse_pos[0] <= self.btns_x[i] + 70:
                for j in range(self.to_system):
                    bottom_line = self.btn_y - bsize * (j - 1) if j else self.btn_y + 70
                    if self.btn_y - bsize * j <= mouse_pos[1] <= bottom_line:
                        return [i, j]  # [номер по горизонтали, номер по вертикали (снизу)]
        return None

    def get_click(self, mouse_pos):
        global pause
        btn = self.get_btn(mouse_pos)
        if btn == 'pause':
            pause = not pause
        elif btn and not pause:
            self.on_click(btn)

    def on_click(self, btn_xy):
        if not btn_xy[1]:
            if self.to_system == 2:
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


class Numbers:
    def __init__(self, width, height, to_sys, from_sys):
        self.numb_list = []
        self.width, self.height = width, height
        self.to_sys, self.from_sys = to_sys, from_sys

    def add_numb(self):
        n = random.randint(1, 255)
        while decimal_conversion(n, FROM_SYSTEM) in map(lambda lst: lst[1], self.numb_list):
            n = random.randint(1, 255)
        self.numb_list.append([[random.randrange(5, self.width - 190, 3), 0],
                               decimal_conversion(n, self.from_sys), decimal_conversion(n, self.to_sys)])
        # self.numb_list[0] это список с координатами x, y; дальше 2 числа (которое переводят и в какое переводят)

    def render(self, screen, t):
        excess_n = btns.check_solution([el[2] for el in numbs.numb_list])  # число, которое пора удалить, тк его набрали
        for i in range(len(self.numb_list)):
            self.numb_list[i][0][1] += t
            if i == excess_n:
                pass  # надо наверно как-то красиво его убрать, не знаю пока как именно
            btn_txt = 'pause' if pause else self.numb_list[i][1]
            text = font.render(btn_txt, True, (61, 40, 89))
            pygame.draw.rect(screen, (186, 172, 199), (self.numb_list[i][0], (text.get_width() + 16, 60)))
            x = self.numb_list[i][0][0] + 8
            y = self.numb_list[i][0][1] + (60 // 2 - text.get_height() // 2)
            screen.blit(text, (x, y))
        if pause:
            text = pygame.font.SysFont(fontt, 93).render("PAUSE", True, (255, 255, 255))
            x = WIDTH // 2 - text.get_width() // 2
            y = HEIGHT // 2 - text.get_height() // 2
            screen.blit(text, (x, y))
            text = pygame.font.SysFont(fontt, 90).render("PAUSE", True, (56, 42, 69))
            x = WIDTH // 2 - text.get_width() // 2
            y = HEIGHT // 2 - text.get_height() // 2
            screen.blit(text, (x, y))
        if excess_n or excess_n == 0:
            del self.numb_list[excess_n]
            btns.solution = ['0'] * btns.btns_n  # это обнуление кнопочек, но мне не нравится, как быстро это происходит

    def check_gameover(self):
        for i in range(len(self.numb_list)):
            if self.numb_list[i][0][1] >= self.height - 140:
                return True
        return False


MYEVENTTYPE = pygame.USEREVENT + 1  # каждые х секунд падает новое число
MILLISECONDS = 5000  # частота падения в миллисекундах (x = MILLISECONDS / 1000)
pygame.time.set_timer(MYEVENTTYPE, MILLISECONDS)
clock = pygame.time.Clock()
gameover = pause = False
btns = Buttons(WIDTH, HEIGHT, TO_SYSTEM)
numbs = Numbers(WIDTH, HEIGHT, TO_SYSTEM, FROM_SYSTEM)

while True:
    screen.fill((135, 144, 67))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.MOUSEBUTTONDOWN:
            btns.get_click(event.pos)
        if event.type == MYEVENTTYPE and not (gameover + pause):
            numbs.add_numb()
    if pause:
        clock.tick()
        btns.render(screen, pause)
        numbs.render(screen, 0)
    elif not gameover:
        t = 40 * clock.tick() / 1000
        btns.render(screen, pause)
        numbs.render(screen, t)
        gameover = numbs.check_gameover()
    else:
        text = pygame.font.SysFont(fontt, 70).render("GAME OVER))", True, (102, 0, 0))
        x = WIDTH // 2 - text.get_width() // 2
        y = HEIGHT // 2 - text.get_height() // 2
        screen.blit(text, (x, y))
    pygame.display.flip()
