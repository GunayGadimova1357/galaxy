
import pygame
from PIL import Image
import math
import random


WINDOW_SIZE = 800
SAMPLE_AMOUNT = 300
THRESHOLD = 80
SWITCH_INTERVAL_MS = 7000  


images = ["gal1.jpg", "gal.jpg", "gal3.jpg"]
current_index = 0

def load_image(path):
    img = Image.open(path).convert("RGB")
    img = img.resize((SAMPLE_AMOUNT, SAMPLE_AMOUNT))
    return img.load()

pixels = load_image(images[current_index])


pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Galaxy Visualizer 2.0")
clock = pygame.time.Clock()


try:
    pygame.mixer.init()
    pygame.mixer.music.load("space.mp3")
    pygame.mixer.music.play(-1)
except:
    print("⚠️ Музыка не найдена — продолжаем без звука.")


center = WINDOW_SIZE // 2
angle = 0
zoom_base = 1.0
last_switch = pygame.time.get_ticks()

running = True
while running:
    screen.fill((0, 0, 0))
    angle += 0.01
    zoom = math.sin(pygame.time.get_ticks() * 0.001) * 0.3 + zoom_base

    for y in range(SAMPLE_AMOUNT):
        for x in range(SAMPLE_AMOUNT):
            r, g, b = pixels[x, y]
            brightness = 0.299 * r + 0.587 * g + 0.114 * b

            if brightness > THRESHOLD:
                rel_x = x - SAMPLE_AMOUNT / 2
                rel_y = y - SAMPLE_AMOUNT / 2
                offset_angle = math.hypot(rel_x, rel_y) * 0.015
                final_angle = angle + offset_angle

                rot_x = rel_x * math.cos(final_angle) - rel_y * math.sin(final_angle)
                rot_y = rel_x * math.sin(final_angle) + rel_y * math.cos(final_angle)

                draw_x = int(center + rot_x * (WINDOW_SIZE / SAMPLE_AMOUNT) * zoom)
                draw_y = int(center + rot_y * (WINDOW_SIZE / SAMPLE_AMOUNT) * zoom)

                radius = int(brightness / 120)
                radius = max(1, min(radius, 3))

                pygame.draw.circle(screen, (r, g, b), (draw_x, draw_y), radius)


    for _ in range(10):
        fx = random.randint(0, WINDOW_SIZE)
        fy = random.randint(0, WINDOW_SIZE)
        pygame.draw.circle(screen, (255, 255, 255), (fx, fy), 1)

    pygame.display.flip()


    current_time = pygame.time.get_ticks()
    if current_time - last_switch > SWITCH_INTERVAL_MS:
        current_index = (current_index + 1) % len(images)
        new_pixels = load_image(images[current_index])

        for alpha in range(0, 256, 12):
            screen.fill((0, 0, 0))
            for y in range(SAMPLE_AMOUNT):
                for x in range(SAMPLE_AMOUNT):
                    r1, g1, b1 = pixels[x, y]
                    r2, g2, b2 = new_pixels[x, y]

                    r = int(r1 + (r2 - r1) * (alpha / 255))
                    g = int(g1 + (g2 - g1) * (alpha / 255))
                    b = int(b1 + (b2 - b1) * (alpha / 255))

                    brightness = 0.299 * r + 0.587 * g + 0.114 * b
                    if brightness > THRESHOLD:
                        rel_x = x - SAMPLE_AMOUNT / 2
                        rel_y = y - SAMPLE_AMOUNT / 2
                        offset_angle = math.hypot(rel_x, rel_y) * 0.015
                        final_angle = angle + offset_angle

                        rot_x = rel_x * math.cos(final_angle) - rel_y * math.sin(final_angle)
                        rot_y = rel_x * math.sin(final_angle) + rel_y * math.cos(final_angle)

                        draw_x = int(center + rot_x * (WINDOW_SIZE / SAMPLE_AMOUNT) * zoom)
                        draw_y = int(center + rot_y * (WINDOW_SIZE / SAMPLE_AMOUNT) * zoom)

                        pygame.draw.circle(screen, (r, g, b), (draw_x, draw_y), 2)

            pygame.display.flip()
            clock.tick(60)

        pixels = new_pixels
        last_switch = current_time  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                pygame.image.save(screen, "screenshot.png")
                print("📸 Сохранено: screenshot.png")

            elif event.key == pygame.K_SPACE:
                current_index = (current_index + 1) % len(images)
                new_pixels = load_image(images[current_index])

                for alpha in range(0, 256, 12):
                    screen.fill((0, 0, 0))
                    for y in range(SAMPLE_AMOUNT):
                        for x in range(SAMPLE_AMOUNT):
                            r1, g1, b1 = pixels[x, y]
                            r2, g2, b2 = new_pixels[x, y]

                            r = int(r1 + (r2 - r1) * (alpha / 255))
                            g = int(g1 + (g2 - g1) * (alpha / 255))
                            b = int(b1 + (b2 - b1) * (alpha / 255))

                            brightness = 0.299 * r + 0.587 * g + 0.114 * b
                            if brightness > THRESHOLD:
                                rel_x = x - SAMPLE_AMOUNT / 2
                                rel_y = y - SAMPLE_AMOUNT / 2
                                offset_angle = math.hypot(rel_x, rel_y) * 0.015
                                final_angle = angle + offset_angle

                                rot_x = rel_x * math.cos(final_angle) - rel_y * math.sin(final_angle)
                                rot_y = rel_x * math.sin(final_angle) + rel_y * math.cos(final_angle)

                                draw_x = int(center + rot_x * (WINDOW_SIZE / SAMPLE_AMOUNT) * zoom)
                                draw_y = int(center + rot_y * (WINDOW_SIZE / SAMPLE_AMOUNT) * zoom)

                                pygame.draw.circle(screen, (r, g, b), (draw_x, draw_y), 2)

                    pygame.display.flip()
                    clock.tick(60)

                pixels = new_pixels
                last_switch = pygame.time.get_ticks()  

    clock.tick(60)

pygame.quit()
