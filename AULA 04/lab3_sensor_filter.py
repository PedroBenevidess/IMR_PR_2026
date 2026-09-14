import math
import sys
import pygame
import numpy as np

LARGURA, ALTURA = 1000, 650
FPS = 60
DT = 1.0 / FPS

N_FEIXES = 7
FOV = math.pi  # 180 graus, de -90 a +90
DESVIO_PADRAO_RUIDO = 5.0
LIMIAR_MIN = 10.0
LIMIAR_MAX = 200.0
ALCANCE_RAYCAST = 420.0  # alcance fisico do raycast, antes do filtro

VEL_LINEAR = 120.0                 # px/s
VEL_ANGULAR = math.radians(120)    # rad/s


def construir_arena():
    margem = 40
    w, h = LARGURA - 320, ALTURA  # espaco reservado ao painel lateral
    return [
        ((margem, margem), (w, margem)),
        ((w, margem), (w, h - margem)),
        ((w, h - margem), (margem, h - margem)),
        ((margem, h - margem), (margem, margem)),
        # obstaculo interno retangular
        ((300, 200), (420, 200)),
        ((420, 200), (420, 320)),
        ((420, 320), (300, 320)),
        ((300, 320), (300, 200)),
    ]


def raio_intersecta_segmento(origem, angulo, segmento):
    ox, oy = origem
    dx, dy = math.cos(angulo), math.sin(angulo)
    (x1, y1), (x2, y2) = segmento
    v1x, v1y = ox - x1, oy - y1
    v2x, v2y = x2 - x1, y2 - y1
    v3x, v3y = -dy, dx
    denom = v2x * v3x + v2y * v3y
    if abs(denom) < 1e-9:
        return None
    t1 = (v2x * v1y - v2y * v1x) / denom
    t2 = (v1x * v3x + v1y * v3y) / denom
    if t1 >= 0.0 and 0.0 <= t2 <= 1.0:
        return t1
    return None


def distancia_real(origem, angulo, segmentos, alcance_max):
    menor = alcance_max
    for seg in segmentos:
        d = raio_intersecta_segmento(origem, angulo, seg)
        if d is not None and d < menor:
            menor = d
    return menor


def aplica_filtro(d_ruido):
    """Retorna (valido, distancia_filtrada)."""
    if d_ruido < LIMIAR_MIN:
        return False, None
    if d_ruido > LIMIAR_MAX:
        return True, LIMIAR_MAX
    return True, d_ruido


def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Exercicio 3 - Filtro de leitura de sensores")
    relogio = pygame.time.Clock()
    fonte = pygame.font.SysFont("consolas", 16)
    fonte_titulo = pygame.font.SysFont("consolas", 18, bold=True)

    segmentos = construir_arena()
    x, y, theta = 250.0, 400.0, -math.pi / 2

    angulos_relativos = [-FOV / 2 + i * (FOV / (N_FEIXES - 1)) for i in range(N_FEIXES)]

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP]:
            x += VEL_LINEAR * DT * math.cos(theta)
            y += VEL_LINEAR * DT * math.sin(theta)
        if teclas[pygame.K_DOWN]:
            x -= VEL_LINEAR * DT * math.cos(theta)
            y -= VEL_LINEAR * DT * math.sin(theta)
        if teclas[pygame.K_LEFT]:
            theta -= VEL_ANGULAR * DT
        if teclas[pygame.K_RIGHT]:
            theta += VEL_ANGULAR * DT

        
        leituras = []
        for ang_rel in angulos_relativos:
            ang_abs = theta + ang_rel
            d_real = distancia_real((x, y), ang_abs, segmentos, ALCANCE_RAYCAST)
            d_ruido = d_real + float(np.random.normal(0, DESVIO_PADRAO_RUIDO))
            valido, d_filtrado = aplica_filtro(d_ruido)
            leituras.append((ang_rel, d_ruido, valido, d_filtrado))

        tela.fill((24, 24, 28))
        for seg in segmentos:
            pygame.draw.line(tela, (150, 150, 160), seg[0], seg[1], 3)

        for ang_rel, d_ruido, valido, d_filtrado in leituras:
            ang_abs = theta + ang_rel
            fim_bruto = (x + d_ruido * math.cos(ang_abs), y + d_ruido * math.sin(ang_abs))
            pygame.draw.line(tela, (90, 90, 100), (x, y), fim_bruto, 1)

            if valido:
                fim_filt = (x + d_filtrado * math.cos(ang_abs), y + d_filtrado * math.sin(ang_abs))
                cor = (255, 200, 60) if d_filtrado >= LIMIAR_MAX else (80, 220, 120)
                pygame.draw.line(tela, cor, (x, y), fim_filt, 2)
                pygame.draw.circle(tela, cor, (int(fim_filt[0]), int(fim_filt[1])), 4)
            else:
                px, py = x + 14 * math.cos(ang_abs), y + 14 * math.sin(ang_abs)
                pygame.draw.line(tela, (240, 70, 70), (px - 4, py - 4), (px + 4, py + 4), 2)
                pygame.draw.line(tela, (240, 70, 70), (px - 4, py + 4), (px + 4, py - 4), 2)

        pygame.draw.circle(tela, (240, 240, 240), (int(x), int(y)), 9)
        frente = (x + 18 * math.cos(theta), y + 18 * math.sin(theta))
        pygame.draw.line(tela, (255, 90, 90), (x, y), frente, 3)

        
        painel_x = LARGURA - 300
        pygame.draw.rect(tela, (18, 18, 22), (painel_x, 0, 300, ALTURA))
        titulo = fonte_titulo.render("Bruto (ruido) x Filtrado", True, (255, 255, 255))
        tela.blit(titulo, (painel_x + 16, 16))

        for i, (ang_rel, d_ruido, valido, d_filtrado) in enumerate(leituras):
            y_texto = 55 + i * 34
            graus = math.degrees(ang_rel)
            linha1 = f"Feixe {i} ({graus:+.0f} graus)"
            if valido:
                linha2 = f"  bruto: {d_ruido:6.1f} px   filtrado: {d_filtrado:6.1f} px"
                cor2 = (150, 230, 170)
            else:
                linha2 = f"  bruto: {d_ruido:6.1f} px   filtrado: DESCARTADO"
                cor2 = (240, 120, 120)
            tela.blit(fonte.render(linha1, True, (200, 200, 210)), (painel_x + 16, y_texto))
            tela.blit(fonte.render(linha2, True, cor2), (painel_x + 16, y_texto + 16))

        ajuda = fonte.render("Setas: mover / girar o robo", True, (140, 140, 150))
        tela.blit(ajuda, (painel_x + 16, ALTURA - 30))

        pygame.display.flip()
        relogio.tick(FPS)


if __name__ == "__main__":
    main()
