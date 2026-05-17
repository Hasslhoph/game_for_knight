import pygame
import sys
import random
import math

# Инициализация Pygame
pygame.init()

# Константы экрана
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Цветовая палитра (в стиле Hollow Knight)
COLOR_BG_DARK = (10, 12, 16)           # Глубокий темный фон
COLOR_BG_GRADIENT = (20, 25, 35)       # Градиент фона
COLOR_PLATFORM_STONE = (45, 50, 60)    # Каменные платформы
COLOR_PLATFORM_HIGHLIGHT = (65, 70, 85)  # Светлые края камня
COLOR_PLATFORM_SHADOW = (25, 28, 35)   # Тени платформ
COLOR_PLAYER = (230, 235, 240)         # Бледный Саня
COLOR_CLOAK = (40, 45, 60)             # Темный плащ
COLOR_SWORD = (160, 180, 210)          # Сталь меча
COLOR_SWORD_GLOW = (200, 220, 255)     # Свечение меча
COLOR_GRANDMA = (90, 60, 75)           # Бабушка
COLOR_GRANDMA_SHAWL = (50, 35, 50)     # Платок
COLOR_BEER = (200, 140, 30)            # Янтарное пиво
COLOR_FOAM = (250, 245, 230)           # Пена
COLOR_LEAF = (50, 70, 60)              # Мрачная листва
COLOR_TEXT = (180, 190, 200)           # Текст интерфейса
COLOR_TEXT_DIM = (100, 110, 120)       # Тусклый текст
COLOR_TORCH_FIRE = (220, 140, 60)      # Огонь факела
COLOR_TORCH_GLOW = (255, 180, 100)     # Свечение факела
COLOR_DECORATION = (35, 40, 50)        # Декоративные элементы
COLOR_COLUMN = (55, 58, 68)            # Колонны
COLOR_STALACTITE = (50, 52, 62)        # Сталактиты

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Пьяный Саня: Hollow Edition")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 36)
font_large = pygame.font.SysFont("Arial", 72)
font_small = pygame.font.SysFont("Arial", 24)


class ParallaxBackground:
    """Фон с параллаксом для главного меню"""
    def __init__(self):
        self.layers = []
        # Создаем несколько слоев для параллакса
        for i in range(5):
            speed = 0.02 + i * 0.01
            elements = []
            num_elements = 8 + i * 4
            for _ in range(num_elements):
                x = random.randint(0, SCREEN_WIDTH)
                y = random.randint(0, SCREEN_HEIGHT)
                size = random.randint(20, 80 - i * 10)
                alpha = 30 + i * 15
                elements.append({'x': x, 'y': y, 'size': size, 'alpha': alpha})
            self.layers.append({'speed': speed, 'elements': elements, 'offset': 0})

    def update(self, mouse_x):
        for layer in self.layers:
            layer['offset'] = (mouse_x * layer['speed']) % SCREEN_WIDTH

    def draw(self, surface):
        for i, layer in enumerate(self.layers):
            color_val = 15 + i * 8
            color = (color_val, color_val + 5, color_val + 12)
            for elem in layer['elements']:
                x = (elem['x'] - layer['offset']) % SCREEN_WIDTH
                # Рисуем размытые пятна для атмосферы
                surf = pygame.Surface((elem['size'], elem['size']), pygame.SRCALPHA)
                pygame.draw.circle(surf, (*color, elem['alpha']), 
                                   (elem['size']//2, elem['size']//2), elem['size']//2)
                surface.blit(surf, (x - elem['size']//2, elem['y']))


class FloatingMug:
    """Кружки пива на главном экране"""
    def __init__(self):
        self.reset()
        self.y = random.randint(-100, SCREEN_HEIGHT)

    def reset(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = -50
        self.speed_y = random.uniform(0.5, 2)
        self.speed_x = random.uniform(-0.5, 0.5)
        self.angle = random.randint(0, 360)
        self.rot_speed = random.uniform(-1, 1)
        self.size = random.uniform(0.7, 1.3)

    def update(self):
        self.y += self.speed_y
        self.x += self.speed_x
        self.angle += self.rot_speed
        if self.y > SCREEN_HEIGHT + 50:
            self.reset()

    def draw(self, surface):
        scale = int(40 * self.size)
        mug_surf = pygame.Surface((scale, int(50 * self.size)), pygame.SRCALPHA)
        rect_h = int(35 * self.size)
        foam_h = int(12 * self.size)
        
        # Тело кружки
        pygame.draw.rect(mug_surf, COLOR_BEER, 
                        (int(5*self.size), int(15*self.size), 
                         int(30*self.size), rect_h), 
                        border_bottom_left_radius=5, border_bottom_right_radius=5)
        # Пена
        pygame.draw.rect(mug_surf, COLOR_FOAM, 
                        (int(5*self.size), int(5*self.size), 
                         int(30*self.size), foam_h), 
                        border_top_left_radius=5, border_top_right_radius=5)
        # Ручка
        handle_x = int(30 * self.size)
        handle_y = int(18 * self.size)
        handle_w = int(10 * self.size)
        handle_h = int(20 * self.size)
        pygame.draw.arc(mug_surf, COLOR_FOAM, 
                       (handle_x, handle_y, handle_w, handle_h), 
                       -math.pi/2, math.pi/2, int(3*self.size))

        rot_surf = pygame.transform.rotate(mug_surf, self.angle)
        new_rect = rot_surf.get_rect(center=(self.x, self.y))
        surface.blit(rot_surf, new_rect.topleft)


class Particle:
    """Частицы для атмосферы"""
    def __init__(self, particle_type='leaf'):
        self.particle_type = particle_type
        self.reset()

    def reset(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(-50, SCREEN_HEIGHT)
        self.vx = random.uniform(-1, -0.3)
        self.vy = random.uniform(0.3, 1)
        self.size = random.randint(3, 8)
        self.time = random.uniform(0, 100)
        self.alpha = random.randint(50, 150)

    def update(self):
        self.time += 0.03
        current_vx = self.vx + math.sin(self.time) * 0.3
        self.x += current_vx
        self.y += self.vy
        if self.y > SCREEN_HEIGHT or self.x < -20:
            self.reset()

    def draw(self, surface):
        if self.particle_type == 'leaf':
            color = COLOR_LEAF
        else:
            color = COLOR_DECORATION
        surf = pygame.Surface((int(self.size * 1.5), int(self.size)), pygame.SRCALPHA)
        pygame.draw.ellipse(surf, (*color, self.alpha), 
                           (0, 0, int(self.size * 1.5), int(self.size)))
        surface.blit(surf, (self.x, self.y))


class Torch:
    """Факел для освещения"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.flame_timer = 0
        self.flame_offset = random.uniform(0, math.pi * 2)
        self.base_size = 15

    def update(self, timer):
        self.flame_timer = timer

    def draw(self, surface):
        # Деревянная основа
        pygame.draw.rect(surface, (60, 40, 30), 
                        (self.x - 3, self.y, 6, 25))
        
        # Пламя (анимированное)
        flicker = math.sin(self.flame_timer * 3 + self.flame_offset) * 3
        flame_height = self.base_size + flicker
        flame_width = 10 + math.cos(self.flame_timer * 5 + self.flame_offset) * 2
        
        # Внешнее свечение
        glow_surf = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.ellipse(glow_surf, (*COLOR_TORCH_GLOW, 80), 
                           (0, 0, 40, 40))
        surface.blit(glow_surf, (self.x - 20, self.y - flame_height - 10))
        
        # Ядро пламени
        pygame.draw.ellipse(surface, COLOR_TORCH_FIRE, 
                           (self.x - flame_width//2, self.y - flame_height, 
                            flame_width, flame_height))
        pygame.draw.ellipse(surface, COLOR_TORCH_GLOW, 
                           (self.x - flame_width//3, self.y - flame_height + 5, 
                            flame_width//1.5, flame_height//1.5))


class Player:
    def __init__(self, x, y):
        self.initial_w = 40
        self.initial_h = 60
        self.rect = pygame.Rect(x, y, self.initial_w, self.initial_h)
        
        # Физика
        self.vx = 0
        self.vy = 0
        self.speed = 5
        self.jump_power = -14
        self.gravity = 0.6
        self.on_ground = False
        
        # Состояния
        self.is_crouching = False
        self.direction = 1
        self.health = 6
        self.max_health = 6
        
        # Атака
        self.is_attacking = False
        self.attack_timer = 0
        self.attack_cooldown = 20
        self.attack_duration = 10
        self.sword_angle = 0

    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        self.vx = 0
        if keys[pygame.K_a]:
            self.vx = -self.speed
            self.direction = -1
        if keys[pygame.K_d]:
            self.vx = self.speed
            self.direction = 1

        if keys[pygame.K_s]:
            if not self.is_crouching:
                self.is_crouching = True
                self.rect.height = self.initial_h // 2
                self.rect.y += self.initial_h // 2
        else:
            if self.is_crouching:
                self.is_crouching = False
                self.rect.y -= self.initial_h // 2
                self.rect.height = self.initial_h

        if keys[pygame.K_w] and self.on_ground:
            self.vy = self.jump_power
            self.on_ground = False

        if keys[pygame.K_SPACE] and self.attack_timer == 0:
            self.is_attacking = True
            self.attack_timer = self.attack_cooldown

    def update(self, platforms):
        self.vy += self.gravity
        if self.vy > 15:
            self.vy = 15

        self.rect.x += self.vx
        for p in platforms:
            if self.rect.colliderect(p):
                if self.vx > 0:
                    self.rect.right = p.left
                elif self.vx < 0:
                    self.rect.left = p.right

        self.rect.y += self.vy
        self.on_ground = False
        for p in platforms:
            if self.rect.colliderect(p):
                if self.vy > 0:
                    self.rect.bottom = p.top
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:
                    self.rect.top = p.bottom
                    self.vy = 0

        if self.attack_timer > 0:
            self.attack_timer -= 1
            if self.attack_timer > self.attack_cooldown - self.attack_duration:
                # Активная фаза атаки
                range_x = 55
                sword_height = 45
                if self.direction == 1:
                    self.attack_rect = pygame.Rect(
                        self.rect.right, 
                        self.rect.y + 5, 
                        range_x, 
                        sword_height
                    )
                    self.sword_angle = 0
                else:
                    self.attack_rect = pygame.Rect(
                        self.rect.left - range_x, 
                        self.rect.y + 5, 
                        range_x, 
                        sword_height
                    )
                    self.sword_angle = 0
            else:
                self.is_attacking = False
        else:
            self.is_attacking = False

    def draw(self, surface):
        # Плащ/тело
        cloak_rect = self.rect.copy()
        pygame.draw.rect(surface, COLOR_CLOAK, cloak_rect, border_radius=8)
        
        # Голова (маска в стиле Hollow Knight)
        head_h = 25 if not self.is_crouching else 15
        head_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, head_h)
        pygame.draw.ellipse(surface, COLOR_PLAYER, head_rect)
        
        # Детали маски
        eye_y = self.rect.y + int(head_h * 0.4)
        eye_w, eye_h = 7, 12
        if self.direction == 1:
            pygame.draw.ellipse(surface, COLOR_BG_DARK, 
                              (self.rect.x + 20, eye_y, eye_w, eye_h))
            pygame.draw.ellipse(surface, COLOR_BG_DARK, 
                              (self.rect.x + 30, eye_y, eye_w, eye_h))
        else:
            pygame.draw.ellipse(surface, COLOR_BG_DARK, 
                              (self.rect.x + 8, eye_y, eye_w, eye_h))
            pygame.draw.ellipse(surface, COLOR_BG_DARK, 
                              (self.rect.x + 18, eye_y, eye_w, eye_h))

        # Прямой меч
        if self.is_attacking and self.attack_timer > self.attack_cooldown - self.attack_duration:
            sword_length = 50
            sword_width = 8
            
            if self.direction == 1:
                # Меч направлен вправо
                sword_rect = pygame.Rect(
                    self.rect.right - 5,
                    self.rect.y + 15,
                    sword_length,
                    sword_width
                )
            else:
                # Меч направлен влево
                sword_rect = pygame.Rect(
                    self.rect.left - sword_length + 5,
                    self.rect.y + 15,
                    sword_length,
                    sword_width
                )
            
            # Лезвие меча
            pygame.draw.rect(surface, COLOR_SWORD, sword_rect, border_radius=3)
            pygame.draw.rect(surface, COLOR_SWORD_GLOW, sword_rect, 2, border_radius=3)
            
            # Рукоять
            handle_x = sword_rect.left if self.direction == 1 else sword_rect.right - 10
            pygame.draw.rect(surface, (80, 60, 50), 
                           (handle_x, self.rect.y + 12, 12, 14), border_radius=2)
            
            # Гарда (защита руки)
            guard_x = sword_rect.left if self.direction == 1 else sword_rect.right - 5
            pygame.draw.rect(surface, COLOR_SWORD, 
                           (guard_x, self.rect.y + 8, 8, 22), border_radius=2)


class GrandmaEnemy:
    def __init__(self, x, y, patrol_range=100):
        self.rect = pygame.Rect(x, y, 45, 65)
        self.start_x = x
        self.patrol_range = patrol_range
        self.health = 3
        self.speed = 1.2
        self.shoot_cooldown = 0
        self.detect_radius = 350
        self.direction = 1
        self.patrol_direction = 1

    def update(self, player, projectiles):
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)

        if distance < self.detect_radius:
            # Патрулирование или преследование
            if abs(dx) > 50:
                if dx > 0:
                    self.rect.x += self.speed
                    self.direction = 1
                else:
                    self.rect.x -= self.speed
                    self.direction = -1
            
            # Ограничение патруля
            if self.rect.x < self.start_x - self.patrol_range:
                self.rect.x = self.start_x - self.patrol_range
                self.patrol_direction = 1
            elif self.rect.x > self.start_x + self.patrol_range:
                self.rect.x = self.start_x + self.patrol_range
                self.patrol_direction = -1

            # Бросок кружки
            if self.shoot_cooldown == 0 and abs(dx) < 300:
                proj_dir = 1 if dx > 0 else -1
                projectiles.append(BeerMugProjectile(self.rect.centerx, self.rect.y + 15, proj_dir))
                self.shoot_cooldown = 90

    def draw(self, surface):
        # Тело бабушки
        pygame.draw.rect(surface, COLOR_GRANDMA, self.rect, 
                        border_top_left_radius=15, border_top_right_radius=15)
        
        # Платок
        shawl_points = [
            (self.rect.left, self.rect.top),
            (self.rect.right, self.rect.top),
            (self.rect.centerx, self.rect.top + 25)
        ]
        pygame.draw.polygon(surface, COLOR_GRANDMA_SHAWL, shawl_points)
        
        # Лицо
        pygame.draw.circle(surface, (220, 180, 160), 
                          (self.rect.centerx, self.rect.y + 22), 13)
        
        # Очки
        pygame.draw.circle(surface, (255, 255, 255), 
                          (self.rect.centerx - 6, self.rect.y + 20), 5, 2)
        pygame.draw.circle(surface, (255, 255, 255), 
                          (self.rect.centerx + 6, self.rect.y + 20), 5, 2)
        # Дужки очков
        pygame.draw.line(surface, (255, 255, 255), 
                        (self.rect.centerx - 6, self.rect.y + 20), 
                        (self.rect.centerx + 6, self.rect.y + 20), 2)


class BeerMugProjectile:
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x - 10, y, 20, 25)
        self.speed = 5 * direction
        self.rotation = 0
        self.rot_speed = random.uniform(-5, 5)

    def update(self):
        self.rect.x += self.speed
        self.rotation += self.rot_speed

    def draw(self, surface):
        mug_surf = pygame.Surface((25, 30), pygame.SRCALPHA)
        pygame.draw.rect(mug_surf, COLOR_BEER, (3, 8, 19, 22), border_radius=3)
        pygame.draw.rect(mug_surf, COLOR_FOAM, (3, 0, 19, 10), border_radius=3)
        pygame.draw.arc(mug_surf, COLOR_FOAM, (18, 8, 8, 15), -math.pi/2, math.pi/2, 3)
        
        rot_surf = pygame.transform.rotate(mug_surf, self.rotation)
        new_rect = rot_surf.get_rect(center=self.rect.center)
        surface.blit(rot_surf, new_rect.topleft)


class Game:
    def __init__(self):
        self.state = "MENU"
        self.has_died = False
        
        # Фон меню
        self.parallax_bg = ParallaxBackground()
        self.menu_mugs = [FloatingMug() for _ in range(12)]
        
        # Частицы уровня
        self.particles = [Particle('leaf') for _ in range(30)]
        self.particles += [Particle('dust') for _ in range(15)]
        
        # Факелы
        self.torches = []
        
        self.init_level()

    def init_level(self):
        """Создание расширенного уровня с каменным ландшафтом"""
        self.player = Player(80, 600)
        
        # Враги с разными паттернами патрулирования
        self.enemies = [
            GrandmaEnemy(400, 585, patrol_range=80),
            GrandmaEnemy(700, 585, patrol_range=100),
            GrandmaEnemy(1100, 435, patrol_range=120),
            GrandmaEnemy(1500, 285, patrol_range=90),
            GrandmaEnemy(1900, 435, patrol_range=110),
        ]
        self.projectiles = []
        
        # Расширенная карта платформ (каменный ландшафт)
        self.platforms = [
            # Стартовая платформа
            pygame.Rect(0, 650, 300, 118),
            
            # Нижний уровень (основной путь)
            pygame.Rect(350, 650, 400, 118),
            pygame.Rect(800, 650, 450, 118),
            pygame.Rect(1300, 650, 400, 118),
            pygame.Rect(1750, 650, 500, 118),
            
            # Средний ярус
            pygame.Rect(200, 500, 180, 40),
            pygame.Rect(450, 500, 220, 40),
            pygame.Rect(750, 500, 200, 40),
            pygame.Rect(1050, 500, 250, 40),
            pygame.Rect(1400, 500, 200, 40),
            pygame.Rect(1700, 500, 220, 40),
            
            # Верхний ярус
            pygame.Rect(100, 350, 200, 40),
            pygame.Rect(400, 350, 250, 40),
            pygame.Rect(750, 350, 200, 40),
            pygame.Rect(1050, 350, 280, 40),
            pygame.Rect(1450, 350, 220, 40),
            pygame.Rect(1800, 350, 250, 40),
            
            # Платформы-островки
            pygame.Rect(300, 250, 100, 30),
            pygame.Rect(600, 250, 120, 30),
            pygame.Rect(950, 250, 100, 30),
            pygame.Rect(1300, 250, 120, 30),
            pygame.Rect(1650, 250, 100, 30),
            
            # Финишная платформа
            pygame.Rect(2100, 500, 300, 268),
        ]
        
        # Факелы для освещения
        self.torches = [
            Torch(150, 620),
            Torch(500, 620),
            Torch(950, 620),
            Torch(1450, 620),
            Torch(1950, 620),
            Torch(300, 470),
            Torch(850, 470),
            Torch(1200, 470),
            Torch(1600, 470),
            Torch(200, 320),
            Torch(600, 320),
            Torch(1150, 320),
            Torch(1700, 320),
        ]
        
        # Декорации (сталактиты, колонны, камни)
        self.decorations = {
            'stalactites': [
                {'x': 250, 'y': 0, 'w': 20, 'h': 60},
                {'x': 550, 'y': 0, 'w': 25, 'h': 80},
                {'x': 900, 'y': 0, 'w': 18, 'h': 50},
                {'x': 1250, 'y': 0, 'w': 22, 'h': 70},
                {'x': 1600, 'y': 0, 'w': 20, 'h': 55},
                {'x': 1950, 'y': 0, 'w': 24, 'h': 75},
            ],
            'columns': [
                {'x': 320, 'y': 500, 'w': 30, 'h': 150},
                {'x': 770, 'y': 500, 'w': 30, 'h': 150},
                {'x': 1280, 'y': 500, 'w': 30, 'h': 150},
                {'x': 1720, 'y': 500, 'w': 30, 'h': 150},
            ],
            'rocks': [
                {'x': 180, 'y': 630, 'w': 40, 'h': 20},
                {'x': 620, 'y': 630, 'w': 35, 'h': 20},
                {'x': 1050, 'y': 630, 'w': 45, 'h': 20},
                {'x': 1550, 'y': 630, 'w': 38, 'h': 20},
                {'x': 2050, 'y': 630, 'w': 42, 'h': 20},
            ],
            'plants': [
                {'x': 50, 'y': 625, 'w': 15, 'h': 25},
                {'x': 280, 'y': 625, 'w': 12, 'h': 25},
                {'x': 720, 'y': 625, 'w': 18, 'h': 25},
                {'x': 1180, 'y': 625, 'w': 14, 'h': 25},
                {'x': 1680, 'y': 625, 'w': 16, 'h': 25},
                {'x': 2150, 'y': 625, 'w': 15, 'h': 25},
            ]
        }
        
        self.anim_timer = 0
        self.camera_x = 0

    def draw_menu(self):
        mouse_x, _ = pygame.mouse.get_pos()
        self.parallax_bg.update(mouse_x)
        
        # Градиентный фон
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(COLOR_BG_DARK[0] + (COLOR_BG_GRADIENT[0] - COLOR_BG_DARK[0]) * ratio)
            g = int(COLOR_BG_DARK[1] + (COLOR_BG_GRADIENT[1] - COLOR_BG_DARK[1]) * ratio)
            b = int(COLOR_BG_DARK[2] + (COLOR_BG_GRADIENT[2] - COLOR_BG_DARK[2]) * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Параллакс слои
        self.parallax_bg.draw(screen)
        
        # Летающие кружки
        for mug in self.menu_mugs:
            mug.update()
            mug.draw(screen)
        
        # Заголовок в стиле Hollow Knight
        title_y = 150
        title_text = font_large.render("ПЬЯНЫЙ САНЯ", True, COLOR_TEXT)
        title_shadow = font_large.render("ПЬЯНЫЙ САНЯ", True, COLOR_BG_DARK)
        
        # Тень текста
        screen.blit(title_shadow, (SCREEN_WIDTH // 2 - title_shadow.get_width() // 2 + 3, title_y + 3))
        # Основной текст
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, title_y))
        
        # Декоративная линия под заголовком
        line_y = title_y + 80
        pygame.draw.line(screen, COLOR_SWORD, 
                        (SCREEN_WIDTH // 2 - 150, line_y), 
                        (SCREEN_WIDTH // 2 + 150, line_y), 3)
        
        # Орнамент по бокам от линии
        pygame.draw.circle(screen, COLOR_SWORD, (SCREEN_WIDTH // 2 - 160, line_y), 6)
        pygame.draw.circle(screen, COLOR_SWORD, (SCREEN_WIDTH // 2 + 160, line_y), 6)
        
        # Подзаголовок
        subtitle = font_small.render("Hollow Knight Edition", True, COLOR_TEXT_DIM)
        screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, line_y + 15))
        
        # Кнопки
        play_label = "Начать заново" if self.has_died else "Новая игра"
        self.btn_play_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 380, 300, 60)
        self.btn_exit_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 470, 300, 60)

        for btn, label in [(self.btn_play_rect, play_label), (self.btn_exit_rect, "Выход")]:
            mouse_pos = pygame.mouse.get_pos()
            is_hovered = btn.collidepoint(mouse_pos)
            
            # Цвет кнопки
            base_color = COLOR_PLATFORM_HIGHLIGHT if is_hovered else COLOR_PLATFORM_STONE
            border_color = COLOR_SWORD_GLOW if is_hovered else COLOR_SWORD
            
            pygame.draw.rect(screen, base_color, btn, border_radius=8)
            pygame.draw.rect(screen, border_color, btn, 3, border_radius=8)
            
            text = font.render(label, True, COLOR_TEXT)
            screen.blit(text, (btn.centerx - text.get_width() // 2, 
                             btn.centery - text.get_height() // 2))
        
        # Управление внизу
        controls_text = font_small.render("WASD - Движение | SPACE - Атака", True, COLOR_TEXT_DIM)
        screen.blit(controls_text, (SCREEN_WIDTH // 2 - controls_text.get_width() // 2, 
                                   SCREEN_HEIGHT - 50))

    def draw_interface(self):
        """Интерфейс здоровья"""
        for i in range(self.player.max_health):
            x = 30 + i * 38
            y = 30
            if i < self.player.health:
                # Целая маска
                pygame.draw.circle(screen, COLOR_PLAYER, (x, y), 14)
                pygame.draw.circle(screen, COLOR_BG_DARK, (x - 5, y - 3), 3)
                pygame.draw.circle(screen, COLOR_BG_DARK, (x + 5, y - 3), 3)
                # Обводка
                pygame.draw.circle(screen, COLOR_SWORD, (x, y), 14, 2)
            else:
                # Разбитая маска
                pygame.draw.circle(screen, COLOR_PLATFORM_SHADOW, (x, y), 14, 2)

    def draw_platform(self, surface, rect):
        """Рисует каменную платформу с деталями"""
        # Основная масса
        pygame.draw.rect(surface, COLOR_PLATFORM_STONE, rect, border_radius=5)
        
        # Верхняя грань (светлее)
        top_rect = pygame.Rect(rect.x, rect.y, rect.width, 8)
        pygame.draw.rect(surface, COLOR_PLATFORM_HIGHLIGHT, top_rect, 
                        border_top_left_radius=5, border_top_right_radius=5)
        
        # Нижняя тень
        bottom_rect = pygame.Rect(rect.x, rect.bottom - 8, rect.width, 8)
        pygame.draw.rect(surface, COLOR_PLATFORM_SHADOW, bottom_rect, 
                        border_bottom_left_radius=5, border_bottom_right_radius=5)
        
        # Текстура камня (точки/неровности)
        random.seed(int(rect.x * 1000 + rect.y))
        for _ in range(5):
            px = rect.x + random.randint(10, rect.width - 10)
            py = rect.y + random.randint(15, rect.height - 15)
            pygame.draw.circle(surface, COLOR_PLATFORM_HIGHLIGHT, (px, py), 2)

    def run(self):
        running = True
        while running:
            self.anim_timer += 0.05
            
            # Обновление факелов
            for torch in self.torches:
                torch.update(self.anim_timer)
            
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN and self.state == "MENU":
                    if self.btn_play_rect.collidepoint(event.pos):
                        self.init_level()
                        self.state = "PLAYING"
                    elif self.btn_exit_rect.collidepoint(event.pos):
                        running = False

            if self.state == "MENU":
                self.draw_menu()
            
            elif self.state == "PLAYING":
                # Ввод и обновление игрока
                self.player.handle_input()
                self.player.update(self.platforms)
                
                # Камера следует за игроком
                target_camera_x = self.player.rect.centerx - SCREEN_WIDTH // 2
                target_camera_x = max(0, min(target_camera_x, 2400 - SCREEN_WIDTH))
                self.camera_x += (target_camera_x - self.camera_x) * 0.1

                # Проверка смерти
                if self.player.health <= 0:
                    self.has_died = True
                    self.state = "MENU"

                # Очистка экрана
                screen.fill(COLOR_BG_DARK)
                
                # Сохраняем состояние поверхности для камеры
                game_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                game_surface.fill(COLOR_BG_DARK)

                # Частицы на заднем плане
                for p in self.particles:
                    p.update()
                    p.draw(game_surface)

                # Сталактиты (на заднем плане)
                for stal in self.decorations['stalactites']:
                    points = [
                        (stal['x'], stal['y']),
                        (stal['x'] + stal['w'], stal['y']),
                        (stal['x'] + stal['w'] // 2, stal['y'] + stal['h'])
                    ]
                    pygame.draw.polygon(game_surface, COLOR_STALACTITE, points)

                # Платформы
                for plat in self.platforms:
                    self.draw_platform(game_surface, plat)

                # Колонны
                for col in self.decorations['columns']:
                    col_rect = pygame.Rect(col['x'], col['y'], col['w'], col['h'])
                    pygame.draw.rect(game_surface, COLOR_COLUMN, col_rect, border_radius=5)
                    # Вертикальные линии на колонне
                    for i in range(3):
                        line_x = col['x'] + col['w'] // 4 * (i + 1)
                        pygame.draw.line(game_surface, COLOR_PLATFORM_HIGHLIGHT,
                                       (line_x, col['y']), (line_x, col['y'] + col['h']), 2)

                # Камни
                for rock in self.decorations['rocks']:
                    rock_rect = pygame.Rect(rock['x'], rock['y'], rock['w'], rock['h'])
                    pygame.draw.ellipse(game_surface, COLOR_PLATFORM_STONE, rock_rect)

                # Растения
                sway = math.sin(self.anim_timer) * 3
                for plant in self.decorations['plants']:
                    points = [
                        (plant['x'], plant['y'] + plant['h']),
                        (plant['x'] + plant['w'], plant['y'] + plant['h']),
                        (plant['x'] + plant['w'] // 2 + sway, plant['y'])
                    ]
                    pygame.draw.polygon(game_surface, COLOR_LEAF, points)

                # Факелы
                for torch in self.torches:
                    torch.draw(game_surface)

                # Враги
                for enemy in self.enemies[:]:
                    enemy.update(self.player, self.projectiles)
                    
                    # Проверка атаки игрока
                    if self.player.is_attacking and \
                       self.player.attack_timer > self.player.attack_cooldown - self.player.attack_duration:
                        if self.player.attack_rect.colliderect(enemy.rect):
                            enemy.health -= 1
                            # Отталкивание врага
                            enemy.rect.x += 20 * self.player.direction
                            if enemy.health <= 0:
                                self.enemies.remove(enemy)
                    
                    enemy.draw(game_surface)

                # Снаряды
                for proj in self.projectiles[:]:
                    proj.update()
                    proj.draw(game_surface)
                    
                    if proj.rect.colliderect(self.player.rect):
                        self.player.health -= 1
                        if proj in self.projectiles:
                            self.projectiles.remove(proj)
                    
                    if proj.rect.x < self.camera_x - 50 or proj.rect.x > self.camera_x + SCREEN_WIDTH + 50:
                        if proj in self.projectiles:
                            self.projectiles.remove(proj)

                # Игрок
                self.player.draw(game_surface)

                # Применяем камеру
                screen.blit(game_surface, (-self.camera_x, 0))
                
                # Интерфейс (поверх камеры)
                self.draw_interface()
                
                # Мини-карта / прогресс
                progress_text = font_small.render(f"Врагов: {len(self.enemies)}", True, COLOR_TEXT_DIM)
                screen.blit(progress_text, (SCREEN_WIDTH - 150, 30))

            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
