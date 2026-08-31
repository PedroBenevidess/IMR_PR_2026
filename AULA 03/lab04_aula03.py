"""
LAB 04 - AULA 03
Veiculo de Braitenberg - comportamento de "medo puro".

Sem alvo, sem mapa. O robo so reage ao que os 3 sensores enxergam
no exato instante, usando fiacao CRUZADA (sensor da direita manda
na roda esquerda e vice-versa). Isso faz o robo desviar do obstaculo
virando pra longe dele, em vez de virar de encontro.
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

RAIO_ROBO = 14
SENSOR_RANGE = 130.0
V_CRUZEIRO = 60.0        # px/s, velocidade base de cruzeiro
GANHO_K = 90.0           # ganho da lei de desvio diferencial
DIST_PANICO = 35.0       # abaixo disso o sensor frontal forca giro no proprio eixo
EIXO_ENTRE_RODAS = 24.0  # "L" da cinematica diferencial


class VeiculoBraitenberg:
    def __init__(self, x, y, theta=0.0):
        self.x = float(x)
        self.y = float(y)
        self.theta = float(theta)
        self.sensor_angles = [-math.pi / 4, 0.0, math.pi / 4]  # Esq, Frente, Dir
        self.sensor_range = SENSOR_RANGE
        self.sensor_readings = [self.sensor_range] * 3
        self.v_l = 0.0
        self.v_r = 0.0

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

    def lei_braitenberg(self):
        """Lei de desvio diferencial (fiacao cruzada = medo/covarde)."""
        d_esq, d_frente, d_dir = self.sensor_readings

        # se o sensor frontal detectar obstaculo muito perto -> panico,
        # gira no proprio eixo em vez de seguir a lei proporcional
        if d_frente < DIST_PANICO:
            self.v_l = V_CRUZEIRO
            self.v_r = -V_CRUZEIRO
            return

        # quanto mais perto o obstaculo da DIREITA, mais rapido a roda ESQUERDA
        # quanto mais perto o obstaculo da ESQUERDA, mais rapido a roda DIREITA
        prox_dir = max(0.0, (self.sensor_range - d_dir) / self.sensor_range)
        prox_esq = max(0.0, (self.sensor_range - d_esq) / self.sensor_range)

        self.v_l = V_CRUZEIRO + GANHO_K * prox_dir
        self.v_r = V_CRUZEIRO + GANHO_K * prox_esq

    def cinematica_inversa(self, dt):
        """A partir de v_l, v_r calcula v e w, e integra a pose."""
        v = (self.v_r + self.v_l) / 2.0
        w = (self.v_r - self.v_l) / EIXO_ENTRE_RODAS

        novo_x = self.x + v * math.cos(self.theta) * dt
        novo_y = self.y + v * math.sin(self.theta) * dt

        # nao deixa sair da tela (evita ficar preso na parede)
        if RAIO_ROBO < novo_x < LARGURA - RAIO_ROBO:
            self.x = novo_x
        if RAIO_ROBO < novo_y < ALTURA - RAIO_ROBO:
            self.y = novo_y
        self.theta += w * dt

    def draw(self, surface, font):
        for i, beta in enumerate(self.sensor_angles):
            angle = self.theta + beta
            dist = self.sensor_readings[i]
            rx = self.x + dist * math.cos(angle)
            ry = self.y + dist * math.sin(angle)
            cor = COR_RAIO_COLISAO if dist < self.sensor_range - 1 else COR_RAIO_LIVRE
            pygame.draw.line(surface, cor, (int(self.x), int(self.y)), (int(rx), int(ry)), 2)

        pos = (int(self.x), int(self.y))
        pygame.draw.circle(surface, COR_ROBO, pos, RAIO_ROBO)
        fx = self.x + 24 * math.cos(self.theta)
        fy = self.y + 24 * math.sin(self.theta)
        pygame.draw.line(surface, (255, 50, 50), pos, (int(fx), int(fy)), 3)


def main():
    pygame.init()
    screen = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("LAB 04 - Braitenberg (medo puro)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 14)

    robo = VeiculoBraitenberg(100, 100, theta=math.radians(20))

    # sala fechada com obstaculos fixos (paredes + moveis no meio)
    obstacles = [
        pygame.Rect(0, 0, LARGURA, 15),               # parede topo
        pygame.Rect(0, ALTURA - 15, LARGURA, 15),      # parede baixo
        pygame.Rect(0, 0, 15, ALTURA),                 # parede esquerda
        pygame.Rect(LARGURA - 15, 0, 15, ALTURA),      # parede direita
        pygame.Rect(300, 150, 60, 250),
        pygame.Rect(550, 350, 200, 60),
        pygame.Rect(650, 100, 60, 180),
        pygame.Rect(150, 400, 180, 60),
    ]

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        robo.cast_rays(obstacles)
        robo.lei_braitenberg()
        robo.cinematica_inversa(dt)

        screen.fill(COR_FUNDO)
        for obs in obstacles:
            pygame.draw.rect(screen, COR_OBSTACULO, obs)
        robo.draw(screen, font)

        textos = [
            f"v_L = {robo.v_l:6.1f}  v_R = {robo.v_r:6.1f}",
            f"Sensores (Esq/Frente/Dir): {robo.sensor_readings[0]:5.1f} / "
            f"{robo.sensor_readings[1]:5.1f} / {robo.sensor_readings[2]:5.1f}",
        ]
        for i, t in enumerate(textos):
            screen.blit(font.render(t, True, (220, 220, 220)), (20, 20 + i * 18))

        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
