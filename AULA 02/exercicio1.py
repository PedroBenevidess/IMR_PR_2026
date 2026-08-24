# Se for executar no VSCode, executar:
# 1. Criar e ativar o ambiente virtual
# python ou python3 -m venv venv_robotica
# source venv_robotica/bin/activate     # No Linux
# venv_robotica\Scripts\activate        # No Windows
#
# 2. Instalar as dependências leves
# pip install pygame numpy

#Se for rodar no Colab, executar i código diretamente


import pygame
import math
import numpy as np

# Constantes de Configuração
LARGURA_TELA = 800
ALTURA_TELA = 600
FPS = 60

COR_FUNDO = (30, 30, 30)
COR_ROBO = (0, 180, 255)
COR_DIRECAO = (255, 50, 50)
COR_TRAJETORIA = (100, 200, 100)


class DiffDriveRobot:
    def __init__(self, x, y, theta=0.0, wheelbase=30.0, radius=15.0):
        # Estado do robô: [x, y, theta]
        self.x = float(x)
        self.y = float(y)
        self.theta = float(theta)

        # Parâmetros físicos
        self.L = float(wheelbase)
        self.radius = float(radius)

        # Entradas de controle
        self.v = 0.0
        self.omega = 0.0

        # Histórico de posições
        self.history = []

    def set_wheel_velocities(self, v_left, v_right):
        """Converte velocidade das rodas em velocidade linear e angular."""
        self.v = (v_right + v_left) / 2.0
        self.omega = (v_right - v_left) / self.L

    def set_direct_velocity(self, v, omega):
        """Comando direto de velocidade linear e angular."""
        self.v = v
        self.omega = omega

    def update(self, dt):
        """Integração numérica da cinemática diferencial."""

        # Atualização angular
        self.theta += self.omega * dt

        # Normaliza o ângulo
        self.theta = (self.theta + math.pi) % (2 * math.pi) - math.pi

        # Atualização de posição
        self.x += self.v * math.cos(self.theta) * dt
        self.y += self.v * math.sin(self.theta) * dt

        # Guarda histórico para desenhar o rastro
        if (
            len(self.history) == 0
            or np.hypot(
                self.x - self.history[-1][0],
                self.y - self.history[-1][1]
            ) > 5
        ):
            self.history.append((self.x, self.y))

            if len(self.history) > 500:
                self.history.pop(0)

    def draw(self, surface):
        # Desenha o rastro
        if len(self.history) > 1:
            pygame.draw.lines(
                surface,
                COR_TRAJETORIA,
                False,
                self.history,
                2
            )

        # Desenha o robô
        pos_int = (int(self.x), int(self.y))
        pygame.draw.circle(
            surface,
            COR_ROBO,
            pos_int,
            int(self.radius)
        )

        # Linha indicadora da direção
        linha_frente_x = (
            self.x +
            (self.radius + 10) * math.cos(self.theta)
        )

        linha_frente_y = (
            self.y +
            (self.radius + 10) * math.sin(self.theta)
        )

        pygame.draw.line(
            surface,
            COR_DIRECAO,
            pos_int,
            (int(linha_frente_x), int(linha_frente_y)),
            3
        )


def main():
    pygame.init()

    screen = pygame.display.set_mode(
        (LARGURA_TELA, ALTURA_TELA)
    )

    pygame.display.set_caption(
        "Exercício 1: Controle por Rodas"
    )

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 14)

    robot = DiffDriveRobot(
        x=LARGURA_TELA // 2,
        y=ALTURA_TELA // 2,
        theta=0.0
    )

    running = True

    while running:

        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # ==========================================
        # CONTROLE INDIVIDUAL DAS RODAS
        # ==========================================

        keys = pygame.key.get_pressed()

        # Velocidade da roda esquerda
        v_left = 0.0

        # Velocidade da roda direita
        v_right = 0.0

        # ------------------------------------------
        # RODA ESQUERDA
        # ------------------------------------------

        if keys[pygame.K_w]:
            v_left = 100.0

        if keys[pygame.K_s]:
            v_left = -100.0

        # ------------------------------------------
        # RODA DIREITA
        # ------------------------------------------

        if keys[pygame.K_i]:
            v_right = 100.0

        if keys[pygame.K_k]:
            v_right = -100.0

        # Aplica as velocidades individuais das rodas
        robot.set_wheel_velocities(
            v_left,
            v_right
        )

        # Atualiza a física do robô
        robot.update(dt)

        # ==========================================
        # RENDERIZAÇÃO
        # ==========================================

        screen.fill(COR_FUNDO)

        robot.draw(screen)

        # Painel de telemetria
        info_txt = [
            f"Pose X: {robot.x:.1f} px | "
            f"Y: {robot.y:.1f} px | "
            f"Theta: {math.degrees(robot.theta):.1f} deg",

            f"Roda esquerda: {v_left:.1f} px/s | "
            f"Roda direita: {v_right:.1f} px/s",

            f"v = {robot.v:.1f} px/s | "
            f"omega = {robot.omega:.2f} rad/s",

            "W/S: Roda Esquerda | I/K: Roda Direita"
        ]

        for i, txt in enumerate(info_txt):
            rendered = font.render(
                txt,
                True,
                (220, 220, 220)
            )

            screen.blit(
                rendered,
                (15, 15 + i * 20)
            )

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()