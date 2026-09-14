"""
Exercicio 2 - Calculadora de giro Ackermann vs. Diferencial
O usuario controla v (velocidade linear) e phi (angulo de esterco) via
teclado e observa a trajetoria de um veiculo com tracao Ackermann,
comparando-a com as capacidades de um robo diferencial.
"""

import math
import sys
import pygame

LARGURA, ALTURA = 900, 600
FPS = 60
DT = 1.0 / FPS
ESCALA = 40          # pixels por metro
L = 2.0              # entre-eixos [m]
PHI_MAX = math.radians(30)
V_MAX = 3.0
V_ACC = 1.5          # m/s^2 ao acelerar
PHI_VEL = math.radians(45)  # velocidade de esterco [rad/s]

CENTRO = (LARGURA // 2, ALTURA // 2)


def mundo_para_tela(x, y):
    return CENTRO[0] + x * ESCALA, CENTRO[1] - y * ESCALA


def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Exercicio 2 - Ackermann x Diferencial")
    relogio = pygame.time.Clock()
    fonte_peq = pygame.font.SysFont("consolas", 15)

    x, y, theta = 0.0, 0.0, 0.0
    v = 0.0
    phi = 0.0
    trilha = []

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                x, y, theta, v, phi = 0.0, 0.0, 0.0, 0.0, 0.0
                trilha = []

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            v = min(V_MAX, v + V_ACC * DT)
        elif teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            v = max(-V_MAX, v - V_ACC * DT)
        else:
            v *= 0.98  # atrito leve

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            phi = min(PHI_MAX, phi + PHI_VEL * DT)
        elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            phi = max(-PHI_MAX, phi - PHI_VEL * DT)
        else:
            if phi > 0:
                phi = max(0.0, phi - PHI_VEL * DT)
            elif phi < 0:
                phi = min(0.0, phi + PHI_VEL * DT)

        # ---- Cinematica Ackermann (modelo bicicleta) ----
        w = (v / L) * math.tan(phi)
        x += v * math.cos(theta) * DT
        y += v * math.sin(theta) * DT
        theta += w * DT

        trilha.append(mundo_para_tela(x, y))
        if len(trilha) > 2000:
            trilha.pop(0)

        raio = L / math.tan(phi) if abs(phi) > 1e-4 else None

        # -------------------- Desenho --------------------
        tela.fill((28, 28, 34))

        if len(trilha) > 1:
            pygame.draw.lines(tela, (90, 170, 255), False, trilha, 2)

        px, py = mundo_para_tela(x, y)
        comprimento = 22
        frente = (px + comprimento * math.cos(theta), py - comprimento * math.sin(theta))
        pygame.draw.circle(tela, (240, 240, 240), (px, py), 10)
        pygame.draw.line(tela, (255, 90, 90), (px, py), frente, 3)

        # roda dianteira indicando o angulo de esterco phi
        ang_roda = theta + phi
        ponta_roda = (frente[0] + 14 * math.cos(ang_roda), frente[1] - 14 * math.sin(ang_roda))
        pygame.draw.line(tela, (255, 220, 90), frente, ponta_roda, 4)

        # centro da curva, quando o raio e pequeno o bastante para caber na tela
        if raio is not None and abs(raio) < 60:
            cx = x - raio * math.sin(theta)
            cy = y + raio * math.cos(theta)
            ccx, ccy = mundo_para_tela(cx, cy)
            pygame.draw.circle(tela, (120, 255, 150), (ccx, ccy), 4)

        linhas = [
            f"v = {v:+.2f} m/s        phi = {math.degrees(phi):+.1f} graus  (max +-30)",
            f"L (entre-eixos) = {L:.1f} m",
            f"omega = (v/L)*tan(phi) = {w:+.3f} rad/s",
            "R = L / tan(phi) = " + ("infinito (reto)" if raio is None else f"{raio:.2f} m"),
            "",
            "Diferencial: consegue R = 0 (gira no proprio eixo, v=0, w<>0)",
            "Ackermann : com v=0, w=(v/L)*tan(phi)=0 sempre -> nunca gira no lugar",
            "",
            "Setas/WASD: acelerar e estercar | R: reiniciar",
        ]
        for i, linha in enumerate(linhas):
            if i in (5, 6):
                cor = (170, 220, 170)
            elif i < 4:
                cor = (230, 230, 230)
            else:
                cor = (150, 150, 155)
            texto = fonte_peq.render(linha, True, cor)
            tela.blit(texto, (16, 16 + i * 20))

        pygame.display.flip()
        relogio.tick(FPS)


if __name__ == "__main__":
    main()
