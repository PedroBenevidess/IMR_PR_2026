"""
Exercicio 5 - Centralizacao autonoma em corredor (Controle Proporcional)
Dois feixes laterais fixos (+-90 graus) medem a distancia ate as paredes.
erro e = d_esq - d_dir   ->   omega = Kp * e   (Kp = 0.01), v constante.
"""

import math
import random
import sys
import pygame

LARGURA, ALTURA = 1000, 500
FPS = 60
DT = 1.0 / FPS

KP = 0.01
V = 40.0                        # px/s, velocidade linear constante
ALCANCE_SENSOR = 600.0

Y_PAREDE_CIMA = 130.0
Y_PAREDE_BAIXO = 370.0
COMPRIMENTO_CORREDOR = 20000.0  # bem longo; a camera acompanha o robo

PAREDES = [
    ((-1000.0, Y_PAREDE_CIMA), (COMPRIMENTO_CORREDOR, Y_PAREDE_CIMA)),
    ((-1000.0, Y_PAREDE_BAIXO), (COMPRIMENTO_CORREDOR, Y_PAREDE_BAIXO)),
]


def raio_intersecta_segmento(origem, angulo, segmento, alcance_max):
    ox, oy = origem
    dx, dy = math.cos(angulo), math.sin(angulo)
    (x1, y1), (x2, y2) = segmento
    v1x, v1y = ox - x1, oy - y1
    v2x, v2y = x2 - x1, y2 - y1
    v3x, v3y = -dy, dx
    denom = v2x * v3x + v2y * v3y
    if abs(denom) < 1e-9:
        return alcance_max
    t1 = (v2x * v1y - v2y * v1x) / denom
    t2 = (v1x * v3x + v1y * v3y) / denom
    if t1 >= 0.0 and 0.0 <= t2 <= 1.0 and t1 <= alcance_max:
        return t1
    return alcance_max


def distancia_parede(origem, angulo):
    return min(raio_intersecta_segmento(origem, angulo, seg, ALCANCE_SENSOR) for seg in PAREDES)


def novo_estado_inicial():
    y0 = random.uniform(Y_PAREDE_CIMA + 40, Y_PAREDE_BAIXO - 40)
    theta0 = math.radians(random.uniform(-25, 25))
    return 0.0, y0, theta0


def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Exercicio 5 - Centralizacao em corredor (P)")
    relogio = pygame.time.Clock()
    fonte = pygame.font.SysFont("consolas", 17)

    x, y, theta = novo_estado_inicial()
    trilha = []

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    x, y, theta = novo_estado_inicial()
                    trilha = []
                if evento.key == pygame.K_UP:
                    y -= 40  # perturba manualmente para testar a correcao
                if evento.key == pygame.K_DOWN:
                    y += 40
                if evento.key == pygame.K_LEFT:
                    theta -= math.radians(15)
                if evento.key == pygame.K_RIGHT:
                    theta += math.radians(15)

        # -------- Sensores laterais fixos (+-90 graus) --------
        ang_esq = theta + math.pi / 2
        ang_dir = theta - math.pi / 2
        d_esq = distancia_parede((x, y), ang_esq)
        d_dir = distancia_parede((x, y), ang_dir)

        # -------- Controle proporcional --------
        erro = d_esq - d_dir
        w = KP * erro

        x += V * math.cos(theta) * DT
        y += V * math.sin(theta) * DT
        theta += w * DT

        trilha.append((x, y))
        if len(trilha) > 4000:
            trilha.pop(0)

        # -------- Camera acompanha o robo no eixo X --------
        cam_x = x - LARGURA * 0.3

        def tela_xy(px, py):
            return px - cam_x, py

        # -------- Desenho --------
        tela.fill((22, 22, 26))
        for (p1, p2) in PAREDES:
            pygame.draw.line(tela, (140, 140, 150), tela_xy(*p1), tela_xy(*p2), 4)

        if len(trilha) > 1:
            pontos = [tela_xy(px, py) for (px, py) in trilha]
            pygame.draw.lines(tela, (90, 170, 255), False, pontos, 2)

        y_centro = (Y_PAREDE_CIMA + Y_PAREDE_BAIXO) / 2
        pygame.draw.line(tela, (60, 60, 70), tela_xy(-1000, y_centro),
                          tela_xy(COMPRIMENTO_CORREDOR, y_centro), 1)

        rx, ry = tela_xy(x, y)
        pygame.draw.circle(tela, (240, 240, 240), (int(rx), int(ry)), 9)
        frente = (rx + 20 * math.cos(theta), ry + 20 * math.sin(theta))
        pygame.draw.line(tela, (255, 90, 90), (rx, ry), frente, 3)

        fe = (rx + d_esq * math.cos(ang_esq), ry + d_esq * math.sin(ang_esq))
        fd = (rx + d_dir * math.cos(ang_dir), ry + d_dir * math.sin(ang_dir))
        pygame.draw.line(tela, (120, 220, 140), (rx, ry), fe, 1)
        pygame.draw.line(tela, (255, 210, 90), (rx, ry), fd, 1)

        linhas = [
            f"d_esq = {d_esq:6.1f} px   d_dir = {d_dir:6.1f} px   e = {erro:+.1f}",
            f"omega = Kp*e = {w:+.4f} rad/s    v = {V:.0f} px/s",
            "Setas: perturbar manualmente | R: reiniciar em posicao aleatoria",
        ]
        for i, linha in enumerate(linhas):
            tela.blit(fonte.render(linha, True, (220, 220, 220)), (16, 16 + i * 20))

        pygame.display.flip()
        relogio.tick(FPS)


if __name__ == "__main__":
    main()
