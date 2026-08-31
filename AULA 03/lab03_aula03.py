"""
LAB 03 - AULA 03
Percepcao com multiplos sensores de feixe (5 sensores) + ruido gaussiano.

5 raios abrindo em leque na frente do robo, alcance maximo de 200px.
Cada leitura recebe ruido gaussiano (media 0, desvio padrao 2.0) pra
simular a imprecisao de um sensor real.
"""

import pygame
import math
import numpy as np

LARGURA, ALTURA = 900, 650
FPS = 60
COR_FUNDO = (20, 24, 30)
COR_ROBO = (0, 200, 255)
COR_OBSTACULO = (180, 50, 50)
COR_RAIO_LIVRE = (0, 255, 100)
COR_RAIO_COLISAO = (255, 200, 0)

ALCANCE_MAX = 200.0
RUIDO_MEDIA = 0.0
RUIDO_DESVIO = 2.0


class RoboMultiSensor:
    def __init__(self, x, y, theta=0.0):
        self.x = float(x)
        self.y = float(y)
        self.theta = float(theta)
        # 5 feixes abrindo em leque: -60, -30, 0, 30, 60 graus
        self.sensor_angles = [math.radians(a) for a in (-60, -30, 0, 30, 60)]
        self.sensor_range = ALCANCE_MAX
        self.sensor_readings = [self.sensor_range] * 5

    def cast_rays(self, obstacles):
        leituras = []
        for beta in self.sensor_angles:
            angle = self.theta + beta
            min_dist = self.sensor_range

            for step in range(5, int(self.sensor_range), 3):
                rx = self.x + step * math.cos(angle)
                ry = self.y + step * math.sin(angle)

                if rx <= 0 or rx >= LARGURA or ry <= 0 or ry >= ALTURA:
                    min_dist = float(step)
                    break

                hit = False
                for obs in obstacles:
                    if obs.collidepoint(rx, ry):
                        min_dist = float(step)
                        hit = True
                        break
                if hit:
                    break

            # adiciona ruido gaussiano simulado na medicao
            ruido = np.random.normal(RUIDO_MEDIA, RUIDO_DESVIO)
            leitura_ruidosa = float(np.clip(min_dist + ruido, 0.0, self.sensor_range))
            leituras.append(leitura_ruidosa)

        self.sensor_readings = leituras

    def draw(self, surface, font):
        for i, beta in enumerate(self.sensor_angles):
            angle = self.theta + beta
            dist = self.sensor_readings[i]
            rx = self.x + dist * math.cos(angle)
            ry = self.y + dist * math.sin(angle)
            cor = COR_RAIO_COLISAO if dist < self.sensor_range - 1 else COR_RAIO_LIVRE
            pygame.draw.line(surface, cor, (int(self.x), int(self.y)), (int(rx), int(ry)), 2)
            pygame.draw.circle(surface, cor, (int(rx), int(ry)), 4)

            # mostra o valor numerico ao lado da ponta do raio
            label = font.render(f"{dist:.0f}", True, (255, 255, 255))
            surface.blit(label, (int(rx) + 6, int(ry) - 6))

        pos = (int(self.x), int(self.y))
        pygame.draw.circle(surface, COR_ROBO, pos, 16)
        fx = self.x + 24 * math.cos(self.theta)
        fy = self.y + 24 * math.sin(self.theta)
        pygame.draw.line(surface, (255, 50, 50), pos, (int(fx), int(fy)), 3)


def main():
    pygame.init()
    screen = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("LAB 03 - 5 sensores com ruido gaussiano")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 14)

    robo = RoboMultiSensor(150, 325, 0.0)
    obstacles = [
        pygame.Rect(350, 150, 100, 350),
        pygame.Rect(600, 100, 150, 100),
        pygame.Rect(600, 400, 150, 150),
    ]

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        mx, my = pygame.mouse.get_pos()
        dx, dy = mx - robo.x, my - robo.y
        robo.theta = math.atan2(dy, dx)
        robo.x += dx * 0.03
        robo.y += dy * 0.03

        robo.cast_rays(obstacles)

        screen.fill(COR_FUNDO)
        for obs in obstacles:
            pygame.draw.rect(screen, COR_OBSTACULO, obs)
            pygame.draw.rect(screen, (255, 100, 100), obs, 2)

        robo.draw(screen, font)

        nomes = ["S1(-60)", "S2(-30)", "S3(0)", "S4(30)", "S5(60)"]
        for i, (nome, dist) in enumerate(zip(nomes, robo.sensor_readings)):
            screen.blit(
                font.render(f"{nome}: {dist:6.1f} px", True, (220, 220, 220)),
                (20, 20 + i * 18),
            )

        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
