import math
import sys
import pygame

LARGURA, ALTURA = 900, 600
FPS = 60
DT = 1.0 / FPS

V0 = 40.0          # velocidade base de cada roda [px/s]
ALPHA = 90.0       # ganho de excitacao do sensor
D_MAX = 220.0      # alcance maximo do sensor [px]
L_EIXO = 40.0      # distancia entre rodas [px]
ANG_SENSOR = math.radians(35)  # abertura dos sensores em relacao a frente

OBSTACULO_POS = (700, 300)
OBSTACULO_RAIO = 45

POSICAO_INICIAL = (100.0, 450.0, math.radians(-25))


def raio_intersecta_circulo(origem, angulo, centro, raio, alcance_max):
    ox, oy = origem
    dx, dy = math.cos(angulo), math.sin(angulo)
    cx, cy = centro
    fx, fy = ox - cx, oy - cy
    b = 2 * (fx * dx + fy * dy)
    c = fx * fx + fy * fy - raio * raio
    disc = b * b - 4 * c
    if disc < 0:
        return alcance_max
    raiz = math.sqrt(disc)
    t1 = (-b - raiz) / 2
    t2 = (-b + raiz) / 2
    candidatos = [t for t in (t1, t2) if t >= 0]
    if not candidatos:
        return alcance_max
    return min(min(candidatos), alcance_max)


def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Exercicio 4 - Braitenberg (conexao direta)")
    relogio = pygame.time.Clock()
    fonte = pygame.font.SysFont("consolas", 16)

    x, y, theta = POSICAO_INICIAL
    trilha = []

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                x, y, theta = POSICAO_INICIAL
                trilha = []

        
        ang_esq = theta + ANG_SENSOR
        ang_dir = theta - ANG_SENSOR
        d_esq = raio_intersecta_circulo((x, y), ang_esq, OBSTACULO_POS, OBSTACULO_RAIO, D_MAX)
        d_dir = raio_intersecta_circulo((x, y), ang_dir, OBSTACULO_POS, OBSTACULO_RAIO, D_MAX)

        
        vL = V0 + ALPHA * (1.0 - d_esq / D_MAX)
        vR = V0 + ALPHA * (1.0 - d_dir / D_MAX)

        
        v = (vL + vR) / 2.0
        w = (vR - vL) / L_EIXO
        x += v * math.cos(theta) * DT
        y += v * math.sin(theta) * DT
        theta += w * DT

        trilha.append((x, y))
        if len(trilha) > 3000:
            trilha.pop(0)

        
        tela.fill((26, 26, 30))
        pygame.draw.circle(tela, (230, 90, 90), OBSTACULO_POS, OBSTACULO_RAIO)

        if len(trilha) > 1:
            pygame.draw.lines(tela, (90, 170, 255), False, trilha, 2)

        fim_esq = (x + d_esq * math.cos(ang_esq), y + d_esq * math.sin(ang_esq))
        fim_dir = (x + d_dir * math.cos(ang_dir), y + d_dir * math.sin(ang_dir))
        pygame.draw.line(tela, (120, 220, 140), (x, y), fim_esq, 1)
        pygame.draw.line(tela, (255, 210, 90), (x, y), fim_dir, 1)

        pygame.draw.circle(tela, (240, 240, 240), (int(x), int(y)), 10)
        frente = (x + 20 * math.cos(theta), y + 20 * math.sin(theta))
        pygame.draw.line(tela, (255, 255, 255), (x, y), frente, 3)

        linhas = [
            f"d_esq = {d_esq:6.1f} px    d_dir = {d_dir:6.1f} px",
            f"vL = {vL:6.1f} px/s    vR = {vR:6.1f} px/s",
            f"omega = (vR-vL)/L = {w:+.3f} rad/s",
            "R: reiniciar posicao",
        ]
        for i, linha in enumerate(linhas):
            tela.blit(fonte.render(linha, True, (220, 220, 220)), (16, 16 + i * 20))

        pygame.display.flip()
        relogio.tick(FPS)


if __name__ == "__main__":
    main()
