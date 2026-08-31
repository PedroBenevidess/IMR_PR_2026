"""
LAB 05 - AULA 03
Navegador reativo Go-to-Goal com desvio de obstaculos.

Clique com o mouse em qualquer lugar da tela pra definir o alvo.
- Modo 1 (Atracao): controlador proporcional classico ate o alvo.
- Modo 2 (Desvio de emergencia): se algum sensor detectar obstaculo
  muito perto, a velocidade angular do modo 1 e sobreposta por um
  torque repulsivo calculado a partir dos sensores.
"""

import pygame
import math

LARGURA, ALTURA = 900, 650
FPS = 60
COR_FUNDO = (20, 24, 30)
COR_ROBO = (0, 200, 255)
COR_OBSTACULO = (180, 50, 50)
COR_RAIO_LIVRE = (0, 255, 100)
COR_RAIO_COLISAO = (255, 200, 0)
COR_ALVO = (255, 215, 0)

SENSOR_RANGE = 140.0
DIST_EMERGENCIA = 55.0     # abaixo disso entra o modo de desvio
DIST_PARADA_ALVO = 15.0    # o robo para quando chega perto assim do alvo

KP_LINEAR = 1.4
KP_ANGULAR = 3.0
K_REPULSAO = 55.0

V_MAX = 90.0
W_MAX = 3.5


class NavegadorGoToGoal:
    def __init__(self, x, y, theta=0.0):
        self.x = float(x)
        self.y = float(y)
        self.theta = float(theta)
        self.sensor_angles = [-math.pi / 3, -math.pi / 6, 0.0, math.pi / 6, math.pi / 3]
        self.sensor_range = SENSOR_RANGE
        self.sensor_readings = [self.sensor_range] * len(self.sensor_angles)
        self.v = 0.0
        self.w = 0.0
        self.chegou = False

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
            leituras.append(min_dist)
        self.sensor_readings = leituras

    def controlador(self, goal):
        if goal is None:
            self.v, self.w = 0.0, 0.0
            return

        # ---------- MODO 1: atracao ao alvo (proporcional) ----------
        gx, gy = goal
        dx, dy = gx - self.x, gy - self.y
        dist_alvo = math.hypot(dx, dy)

        if dist_alvo < DIST_PARADA_ALVO:
            self.v, self.w = 0.0, 0.0
            self.chegou = True
            return
        self.chegou = False

        angulo_alvo = math.atan2(dy, dx)
        erro_ang = (angulo_alvo - self.theta + math.pi) % (2 * math.pi) - math.pi

        v_atracao = min(KP_LINEAR * dist_alvo, V_MAX)
        w_atracao = KP_ANGULAR * erro_ang

        # ---------- MODO 2: desvio de emergencia ----------
        w_repulsivo = 0.0
        emergencia = False
        for beta, dist in zip(self.sensor_angles, self.sensor_readings):
            if dist < DIST_EMERGENCIA:
                emergencia = True
                # quanto mais perto, maior o torque; sinal contrario ao
                # angulo do sensor pra "empurrar" o robo pro lado oposto
                intensidade = (DIST_EMERGENCIA - dist) / DIST_EMERGENCIA
                w_repulsivo += -math.copysign(1.0, beta if beta != 0 else 1.0) * K_REPULSAO * intensidade

        if emergencia:
            # o desvio sobrepoe o w do modo 1 e reduz a velocidade linear
            self.w = max(-W_MAX, min(W_MAX, w_repulsivo * 0.05))
            self.v = v_atracao * 0.3
        else:
            self.v = v_atracao
            self.w = max(-W_MAX, min(W_MAX, w_atracao))

    def update(self, dt):
        self.x += self.v * math.cos(self.theta) * dt
        self.y += self.v * math.sin(self.theta) * dt
        self.theta += self.w * dt

    def draw(self, surface):
        for i, beta in enumerate(self.sensor_angles):
            angle = self.theta + beta
            dist = self.sensor_readings[i]
            rx = self.x + dist * math.cos(angle)
            ry = self.y + dist * math.sin(angle)
            cor = COR_RAIO_COLISAO if dist < self.sensor_range - 1 else COR_RAIO_LIVRE
            pygame.draw.line(surface, cor, (int(self.x), int(self.y)), (int(rx), int(ry)), 2)

        pos = (int(self.x), int(self.y))
        pygame.draw.circle(surface, COR_ROBO, pos, 14)
        fx = self.x + 22 * math.cos(self.theta)
        fy = self.y + 22 * math.sin(self.theta)
        pygame.draw.line(surface, (255, 50, 50), pos, (int(fx), int(fy)), 3)


def main():
    pygame.init()
    screen = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("LAB 05 - Go-to-Goal com desvio reativo (clique pra definir o alvo)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 14)

    robo = NavegadorGoToGoal(80, 80, theta=0.0)
    goal = None

    obstacles = [
        pygame.Rect(0, 0, LARGURA, 15),
        pygame.Rect(0, ALTURA - 15, LARGURA, 15),
        pygame.Rect(0, 0, 15, ALTURA),
        pygame.Rect(LARGURA - 15, 0, 15, ALTURA),
        pygame.Rect(350, 150, 80, 300),
        pygame.Rect(550, 400, 220, 60),
        pygame.Rect(600, 100, 60, 200),
    ]

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                goal = event.pos

        robo.cast_rays(obstacles)
        robo.controlador(goal)
        robo.update(dt)

        screen.fill(COR_FUNDO)
        for obs in obstacles:
            pygame.draw.rect(screen, COR_OBSTACULO, obs)

        if goal is not None:
            pygame.draw.circle(screen, COR_ALVO, goal, 8)
            pygame.draw.circle(screen, COR_ALVO, goal, 15, 2)

        robo.draw(screen)

        status = "ALVO ATINGIDO" if robo.chegou else ("SEM ALVO (clique na tela)" if goal is None else "NAVEGANDO...")
        textos = [
            f"Status: {status}",
            f"v = {robo.v:6.1f}  w = {robo.w:6.2f}",
        ]
        for i, t in enumerate(textos):
            screen.blit(font.render(t, True, (230, 230, 230)), (20, 20 + i * 18))

        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
