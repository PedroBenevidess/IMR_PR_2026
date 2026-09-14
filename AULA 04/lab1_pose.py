"""
Exercicio 1 - Validador de Pose em malha aberta (Cinematica Diferencial)
Calcula e simula a Pose (x, y, theta) de um robo diferencial apos uma
sequencia de comandos de velocidade (v, w) aplicados em malha aberta.
"""

import math
import sys
import pygame

# ---------------------------------------------------------------
# Parametros da simulacao
# ---------------------------------------------------------------
LARGURA, ALTURA = 900, 500
FPS = 60
DT = 1.0 / FPS
ESCALA = 60          # pixels por metro
ORIGEM = (100, ALTURA // 2)

# Sequencia de comandos: (v [m/s], w [rad/s], duracao [s])
SEQUENCIA = [
    (0.5, 0.0, 4.0),
    (0.0, math.pi / 4, 2.0),   # 0.7854 rad/s
    (0.4, 0.0, 3.0),
]


def pose_para_pixel(x, y):
    """Converte (x, y) em metros para coordenadas de tela em pixels."""
    px = ORIGEM[0] + x * ESCALA
    py = ORIGEM[1] - y * ESCALA
    return px, py


def integra_exato(x, y, theta, v, w, dt):
    """Integracao exata do modelo unicycle para v, w constantes em dt."""
    if abs(w) < 1e-9:
        x += v * dt * math.cos(theta)
        y += v * dt * math.sin(theta)
    else:
        x += (v / w) * (math.sin(theta + w * dt) - math.sin(theta))
        y += (v / w) * (-math.cos(theta + w * dt) + math.cos(theta))
        theta += w * dt
    return x, y, theta


def calcula_pose_teorica():
    """Aplica a sequencia inteira em um passo fechado por trecho."""
    x, y, theta = 0.0, 0.0, 0.0
    for v, w, t in SEQUENCIA:
        x, y, theta = integra_exato(x, y, theta, v, w, t)
    return x, y, theta


def main():
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Exercicio 1 - Pose em malha aberta")
    relogio = pygame.time.Clock()
    fonte = pygame.font.SysFont("consolas", 18)

    # Pose teorica (formula fechada, calculada de uma unica vez)
    x_teo, y_teo, th_teo = calcula_pose_teorica()

    # Pose simulada (integrada passo a passo, dt pequeno, junto do Pygame)
    x, y, theta = 0.0, 0.0, 0.0
    trilha = [pose_para_pixel(x, y)]

    indice_trecho = 0
    tempo_no_trecho = 0.0
    simulacao_ativa = True
    impresso = False

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if simulacao_ativa:
            v, w, dur = SEQUENCIA[indice_trecho]
            x, y, theta = integra_exato(x, y, theta, v, w, DT)
            trilha.append(pose_para_pixel(x, y))

            tempo_no_trecho += DT
            if tempo_no_trecho >= dur:
                indice_trecho += 1
                tempo_no_trecho = 0.0
                if indice_trecho >= len(SEQUENCIA):
                    simulacao_ativa = False

        if not simulacao_ativa and not impresso:
            print("=" * 55)
            print("POSE FINAL TEORICA  (formula fechada):")
            print(f"  x = {x_teo:.4f} m | y = {y_teo:.4f} m | "
                  f"theta = {th_teo:.4f} rad ({math.degrees(th_teo):.2f} graus)")
            print("POSE FINAL SIMULADA (integracao passo a passo, dt=1/60s):")
            print(f"  x = {x:.4f} m | y = {y:.4f} m | "
                  f"theta = {theta:.4f} rad ({math.degrees(theta):.2f} graus)")
            print("=" * 55)
            impresso = True

        # -------- Desenho --------
        tela.fill((30, 30, 35))

        if len(trilha) > 1:
            pygame.draw.lines(tela, (80, 160, 255), False, trilha, 2)

        px, py = pose_para_pixel(x, y)
        comprimento_seta = 25
        ponta = (px + comprimento_seta * math.cos(theta),
                 py - comprimento_seta * math.sin(theta))
        pygame.draw.circle(tela, (240, 240, 240), (px, py), 12)
        pygame.draw.line(tela, (255, 80, 80), (px, py), ponta, 3)

        linhas_hud = [
            f"Trecho atual: {min(indice_trecho + 1, len(SEQUENCIA))}/{len(SEQUENCIA)}",
            f"x = {x:.2f} m   y = {y:.2f} m   theta = {math.degrees(theta):.1f} graus",
            "Status: " + ("simulando..." if simulacao_ativa else "concluido (ver terminal)"),
        ]
        for i, linha in enumerate(linhas_hud):
            texto = fonte.render(linha, True, (230, 230, 230))
            tela.blit(texto, (20, 20 + i * 22))

        pygame.display.flip()
        relogio.tick(FPS)


if __name__ == "__main__":
    main()
