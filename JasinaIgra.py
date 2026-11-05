import sys
import math
import pygame

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# ИЗМЕНЕНО НАЗВАНИЕ ОКНА ТУТ:
pygame.display.set_caption("Бегающий курсор за мышкой")

clock = pygame.time.Clock()

# Координаты самолета
plane_x = WIDTH // 2
plane_y = HEIGHT // 2
PLANE_SPEED = 6

# Список для хранения точек дымового следа
trail_particles = []

# Функция для генерации детального самолета
def get_detailed_plane():
    surf = pygame.Surface((60, 60), pygame.SRCALPHA)
    
    BODY_COLOR = (200, 210, 220)      # Светло-серый фюзеляж
    WING_COLOR = (140, 155, 170)      # Темно-серые крылья
    COCKPIT_COLOR = (0, 180, 255)     # Голубое стекло кабины
    DECOR_COLOR = (220, 50, 50)       # Красные элементы

    # 1. Большие крылья
    pygame.draw.polygon(surf, WING_COLOR, [(30, 25), (5, 42), (10, 50), (30, 38)])
    pygame.draw.polygon(surf, WING_COLOR, [(30, 25), (55, 42), (50, 50), (30, 38)])
    
    # Красные законцовки крыльев
    pygame.draw.polygon(surf, DECOR_COLOR, [(5, 42), (0, 44), (3, 49), (10, 50)])
    pygame.draw.polygon(surf, DECOR_COLOR, [(55, 42), (60, 44), (57, 49), (50, 50)])

    # 2. Хвостовое оперение
    pygame.draw.polygon(surf, WING_COLOR, [(30, 50), (18, 56), (20, 59), (30, 56)])
    pygame.draw.polygon(surf, WING_COLOR, [(30, 50), (42, 56), (40, 59), (30, 56)])

    # 3. Фюзеляж
    body_points = [(30, 5), (35, 15), (34, 52), (30, 58), (26, 52), (25, 15)]
    pygame.draw.polygon(surf, BODY_COLOR, body_points)
    
    # Киль
    pygame.draw.line(surf, (100, 110, 120), (30, 48), (30, 58), 2)

    # 4. Кабина пилота
    pygame.draw.ellipse(surf, COCKPIT_COLOR, (27, 18, 6, 14))
    
    return surf

plane_original = get_detailed_plane()

# Главный цикл
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Логика движения
    mouse_x, mouse_y = pygame.mouse.get_pos()
    dx = mouse_x - plane_x
    dy = mouse_y - plane_y
    distance = math.hypot(dx, dy)

    if distance > 2:
        angle = math.degrees(math.atan2(-dy, dx)) - 90
        rotated_plane = pygame.transform.rotate(plane_original, angle)
        
        # Движение
        step_x = (dx / distance) * PLANE_SPEED
        step_y = (dy / distance) * PLANE_SPEED
        plane_x += step_x
        plane_y += step_y
        
        # Частица дыма из хвоста
        back_x = plane_x - (dx / distance) * 25
        back_y = plane_y - (dy / distance) * 25
        trail_particles.append([back_x, back_y, 255])
    else:
        rotated_plane = plane_original

    # Обновление частиц дыма
    for p in trail_particles[:]:
        p[2] -= 8
        if p[2] <= 0:
            trail_particles.remove(p)

    rect = rotated_plane.get_rect(center=(int(plane_x), int(plane_y)))

    # Отрисовка
    screen.fill((20, 30, 40))

    # Рисуем дымовой след
    for p in trail_particles:
        smoke_surf = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(smoke_surf, (255, 255, 255, p[2] // 3), (5, 5), 5)
        screen.blit(smoke_surf, (int(p[0] - 5), int(p[1] - 5)))

    # Рисуем самолет
    screen.blit(rotated_plane, rect)
    
    pygame.display.flip()

pygame.quit()
sys.exit()