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
        """Создание расширенного уровня с каменным ландшафтом (6000px)"""
        self.player = Player(80, 600)
        
        # Враги распределены по всему уровню с разными паттернами
        self.enemies = [
            # Зона 1: Начальная область (обучение)
            GrandmaEnemy(400, 585, patrol_range=80),
            GrandmaEnemy(650, 585, patrol_range=60),
            
            # Зона 2: Средний ярус
            GrandmaEnemy(900, 435, patrol_range=100),
            GrandmaEnemy(1200, 435, patrol_range=80),
            
            # Зона 3: Верхние платформы
            GrandmaEnemy(1550, 285, patrol_range=90),
            GrandmaEnemy(1850, 285, patrol_range=70),
            
            # Зона 4: Глубокая пещера
            GrandmaEnemy(2200, 585, patrol_range=120),
            GrandmaEnemy(2500, 585, patrol_range=100),
            GrandmaEnemy(2800, 435, patrol_range=90),
            
            # Зона 5: Забытый храм
            GrandmaEnemy(3200, 285, patrol_range=110),
            GrandmaEnemy(3550, 285, patrol_range=80),
            GrandmaEnemy(3900, 435, patrol_range=100),
            
            # Зона 6: Подход к боссу
            GrandmaEnemy(4300, 585, patrol_range=90),
            GrandmaEnemy(4650, 435, patrol_range=120),
            
            # Босс: Прабабушка (усиленная версия)
            GrandmaEnemy(5200, 550, patrol_range=200),
        ]
        self.projectiles = []
        
        # Расширенная карта платформ на 6000 пикселей
        self.platforms = [
            # === ЗОНА 1: СТАРТ (0-800px) ===
            pygame.Rect(0, 650, 350, 118),      # Стартовая площадка
            pygame.Rect(400, 650, 300, 118),    # Первый прыжок
            
            # Зона 1 - средний ярус
            pygame.Rect(150, 500, 120, 35),
            pygame.Rect(350, 500, 150, 35),
            pygame.Rect(550, 500, 120, 35),
            
            # Зона 1 - верхний ярус
            pygame.Rect(100, 350, 100, 30),
            pygame.Rect(300, 350, 130, 30),
            pygame.Rect(500, 350, 100, 30),
            
            # === ЗОНА 2: ПЕРВЫЙ ПОДЪЕМ (800-1600px) ===
            pygame.Rect(750, 650, 350, 118),
            pygame.Rect(1150, 650, 300, 118),
            
            # Лестница вверх
            pygame.Rect(850, 520, 100, 35),
            pygame.Rect(1000, 450, 100, 35),
            pygame.Rect(1150, 380, 120, 35),
            pygame.Rect(1350, 320, 100, 35),
            
            # Верхняя зона 2
            pygame.Rect(1500, 320, 250, 35),
            pygame.Rect(1600, 220, 150, 30),
            
            # === ЗОНА 3: ГЛУБОКАЯ ПЕЩЕРА (1600-2800px) ===
            pygame.Rect(1800, 650, 400, 118),
            pygame.Rect(2250, 650, 350, 118),
            pygame.Rect(2650, 650, 300, 118),
            
            # Средний ярус зоны 3
            pygame.Rect(1900, 500, 150, 35),
            pygame.Rect(2150, 500, 180, 35),
            pygame.Rect(2450, 500, 150, 35),
            pygame.Rect(2700, 500, 120, 35),
            
            # Островки
            pygame.Rect(2000, 380, 80, 28),
            pygame.Rect(2200, 380, 90, 28),
            pygame.Rect(2400, 380, 80, 28),
            pygame.Rect(2600, 380, 90, 28),
            
            # === ЗОНА 4: ЗАБЫТЫЙ ХРАМ (2800-4000px) ===
            pygame.Rect(2950, 650, 350, 118),
            pygame.Rect(3350, 650, 400, 118),
            pygame.Rect(3800, 650, 350, 118),
            
            # Храмовые платформы
            pygame.Rect(3050, 520, 120, 35),
            pygame.Rect(3250, 450, 140, 35),
            pygame.Rect(3500, 380, 160, 35),
            pygame.Rect(3750, 450, 140, 35),
            pygame.Rect(3950, 520, 120, 35),
            
            # Верх храма
            pygame.Rect(3150, 280, 100, 30),
            pygame.Rect(3400, 250, 120, 30),
            pygame.Rect(3650, 280, 100, 30),
            pygame.Rect(3850, 320, 130, 30),
            
            # === ЗОНА 5: ТЕМНЫЙ ПЕРЕХОД (4000-5000px) ===
            pygame.Rect(4150, 650, 300, 118),
            pygame.Rect(4500, 650, 350, 118),
            pygame.Rect(4900, 650, 300, 118),
            
            # Сложные прыжки
            pygame.Rect(4250, 520, 80, 30),
            pygame.Rect(4450, 450, 70, 30),
            pygame.Rect(4650, 380, 80, 30),
            pygame.Rect(4850, 450, 70, 30),
            pygame.Rect(5050, 520, 80, 30),
            
            # === ЗОНА 6: АРЕНА БОССА (5000-6000px) ===
            pygame.Rect(5200, 600, 600, 168),   # Большая арена
            pygame.Rect(5300, 450, 150, 35),    # Платформы на арене
            pygame.Rect(5550, 450, 150, 35),
            pygame.Rect(5425, 320, 150, 30),    # Верхняя платформа
            
            # Финишная зона после босса
            pygame.Rect(5850, 500, 150, 268),   # Выход
        ]
        
        # Факелы для освещения (распределены по всему уровню)
        self.torches = [
            # Зона 1
            Torch(100, 620),
            Torch(350, 620),
            Torch(550, 470),
            Torch(200, 320),
            Torch(450, 320),
            # Зона 2
            Torch(800, 620),
            Torch(1100, 620),
            Torch(900, 490),
            Torch(1200, 420),
            Torch(1400, 290),
            Torch(1550, 290),
            # Зона 3
            Torch(1850, 620),
            Torch(2300, 620),
            Torch(2700, 620),
            Torch(2000, 470),
            Torch(2500, 470),
            Torch(2100, 350),
            Torch(2650, 350),
            # Зона 4
            Torch(3000, 620),
            Torch(3400, 620),
            Torch(3850, 620),
            Torch(3150, 490),
            Torch(3550, 420),
            Torch(3800, 490),
            Torch(3300, 250),
            Torch(3700, 250),
            # Зона 5
            Torch(4200, 620),
            Torch(4550, 620),
            Torch(4950, 620),
            Torch(4350, 490),
            Torch(4750, 420),
            Torch(5000, 490),
            # Зона 6 - Арена босса
            Torch(5250, 570),
            Torch(5750, 570),
            Torch(5400, 420),
            Torch(5600, 420),
            Torch(5500, 290),
        ]
        
        # Декорации (сталактиты, колонны, камни, растения) - распределены по зонам
        self.decorations = {
            'stalactites': [
                # Зона 1
                {'x': 200, 'y': 0, 'w': 20, 'h': 50},
                {'x': 450, 'y': 0, 'w': 25, 'h': 60},
                # Зона 2
                {'x': 850, 'y': 0, 'w': 22, 'h': 55},
                {'x': 1100, 'y': 0, 'w': 18, 'h': 45},
                {'x': 1400, 'y': 0, 'w': 24, 'h': 65},
                # Зона 3
                {'x': 1900, 'y': 0, 'w': 20, 'h': 50},
                {'x': 2200, 'y': 0, 'w': 26, 'h': 70},
                {'x': 2550, 'y': 0, 'w': 22, 'h': 55},
                {'x': 2800, 'y': 0, 'w': 20, 'h': 60},
                # Зона 4
                {'x': 3100, 'y': 0, 'w': 24, 'h': 65},
                {'x': 3450, 'y': 0, 'w': 20, 'h': 50},
                {'x': 3750, 'y': 0, 'w': 26, 'h': 70},
                {'x': 3950, 'y': 0, 'w': 22, 'h': 55},
                # Зона 5
                {'x': 4300, 'y': 0, 'w': 20, 'h': 50},
                {'x': 4600, 'y': 0, 'w': 24, 'h': 60},
                {'x': 4900, 'y': 0, 'w': 22, 'h': 55},
                # Зона 6
                {'x': 5300, 'y': 0, 'w': 28, 'h': 75},
                {'x': 5600, 'y': 0, 'w': 24, 'h': 65},
            ],
            'columns': [
                # Зона 1
                {'x': 280, 'y': 500, 'w': 30, 'h': 150},
                # Зона 2
                {'x': 950, 'y': 380, 'w': 30, 'h': 120},
                {'x': 1300, 'y': 320, 'w': 25, 'h': 100},
                # Зона 3
                {'x': 2050, 'y': 500, 'w': 30, 'h': 150},
                {'x': 2500, 'y': 500, 'w': 30, 'h': 150},
                # Зона 4
                {'x': 3200, 'y': 450, 'w': 35, 'h': 180},
                {'x': 3600, 'y': 380, 'w': 30, 'h': 150},
                # Зона 5
                {'x': 4400, 'y': 500, 'w': 30, 'h': 150},
                {'x': 4800, 'y': 450, 'w': 25, 'h': 120},
                # Зона 6
                {'x': 5350, 'y': 450, 'w': 35, 'h': 150},
                {'x': 5650, 'y': 450, 'w': 35, 'h': 150},
            ],
            'rocks': [
                # Зона 1
                {'x': 120, 'y': 630, 'w': 35, 'h': 18},
                {'x': 380, 'y': 630, 'w': 40, 'h': 20},
                {'x': 600, 'y': 630, 'w': 32, 'h': 16},
                # Зона 2
                {'x': 900, 'y': 630, 'w': 38, 'h': 18},
                {'x': 1200, 'y': 630, 'w': 42, 'h': 20},
                {'x': 1500, 'y': 300, 'w': 30, 'h': 15},
                # Зона 3
                {'x': 1950, 'y': 630, 'w': 40, 'h': 20},
                {'x': 2350, 'y': 630, 'w': 45, 'h': 22},
                {'x': 2750, 'y': 630, 'w': 38, 'h': 18},
                {'x': 2100, 'y': 480, 'w': 28, 'h': 14},
                # Зона 4
                {'x': 3100, 'y': 630, 'w': 42, 'h': 20},
                {'x': 3500, 'y': 630, 'w': 40, 'h': 20},
                {'x': 3900, 'y': 630, 'w': 38, 'h': 18},
                {'x': 3350, 'y': 430, 'w': 30, 'h': 15},
                # Зона 5
                {'x': 4250, 'y': 630, 'w': 35, 'h': 18},
                {'x': 4600, 'y': 630, 'w': 40, 'h': 20},
                {'x': 5000, 'y': 630, 'w': 38, 'h': 18},
                # Зона 6
                {'x': 5300, 'y': 580, 'w': 45, 'h': 22},
                {'x': 5650, 'y': 580, 'w': 45, 'h': 22},
            ],
            'plants': [
                # Зона 1
                {'x': 80, 'y': 625, 'w': 14, 'h': 25},
                {'x': 320, 'y': 625, 'w': 12, 'h': 22},
                {'x': 520, 'y': 625, 'w': 15, 'h': 25},
                # Зона 2
                {'x': 850, 'y': 625, 'w': 16, 'h': 28},
                {'x': 1250, 'y': 625, 'w': 14, 'h': 25},
                {'x': 1450, 'y': 295, 'w': 12, 'h': 20},
                # Зона 3
                {'x': 1900, 'y': 625, 'w': 15, 'h': 25},
                {'x': 2400, 'y': 625, 'w': 18, 'h': 28},
                {'x': 2800, 'y': 625, 'w': 14, 'h': 25},
                {'x': 2200, 'y': 475, 'w': 12, 'h': 20},
                # Зона 4
                {'x': 3050, 'y': 625, 'w': 16, 'h': 25},
                {'x': 3500, 'y': 625, 'w': 15, 'h': 25},
                {'x': 3900, 'y': 625, 'w': 14, 'h': 22},
                {'x': 3600, 'y': 355, 'w': 12, 'h': 20},
                # Зона 5
                {'x': 4250, 'y': 625, 'w': 14, 'h': 25},
                {'x': 4650, 'y': 625, 'w': 16, 'h': 28},
                {'x': 5050, 'y': 625, 'w': 14, 'h': 25},
                # Зона 6
                {'x': 5350, 'y': 575, 'w': 18, 'h': 28},
                {'x': 5700, 'y': 575, 'w': 16, 'h': 25},
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
            px = rect.x + random.randint(10, max(11, rect.width - 10))
            if rect.height >= 30:
                py = rect.y + random.randint(15, rect.height - 15)
            else:
                py = rect.y + rect.height // 2
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
