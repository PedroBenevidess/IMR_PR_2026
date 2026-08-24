import pygame
import math
import numpy as np

# ==============================
# Constantes de Configuração
# ==============================

LARGURA_TELA = 800
ALTURA_TELA = 600
FPS = 60

COR_FUNDO = (30, 30, 30)
COR_ROBO = (0, 180, 255)
COR_DIRECAO = (255, 50, 50)
COR_TRAJETORIA = (100, 200, 100)
COR_ALVO = (255, 255, 0)


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

        # Normaliza o ângulo entre [-pi, pi]
        self.theta = (
            (self.theta + math.pi)
            % (2 * math.pi)
            - math.pi
        )

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

        # Desenha o corpo do robô
        pos_int = (int(self.x), int(self.y))

        pygame.draw.circle(
            surface,
            COR_ROBO,
            pos_int,
            int(self.radius)
        )

        # Linha indicadora da direção
        linha_frente_x = (
            self.x
            + (self.radius + 10)
            * math.cos(self.theta)
        )

        linha_frente_y = (
            self.y
            + (self.radius + 10)
            * math.sin(self.theta)
        )

        pygame.draw.line(
            surface,
            COR_DIRECAO,
            pos_int,
            (
                int(linha_frente_x),
                int(linha_frente_y)
            ),
            3
        )


def main():

    pygame.init()

    screen = pygame.display.set_mode(
        (LARGURA_TELA, ALTURA_TELA)
    )

    pygame.display.set_caption(
        "Exercício 3: Controle Proporcional para um Ponto"
    )

    clock = pygame.time.Clock()

    font = pygame.font.SysFont(
        "monospace",
        14
    )

    # Cria o robô
    robot = DiffDriveRobot(
        x=LARGURA_TELA // 2,
        y=ALTURA_TELA // 2,
        theta=0.0
    )

    # ==============================
    # VARIÁVEIS DO CONTROLADOR
    # ==============================

    alvo = None

    # Ganho proporcional
    Kp = 3.0

    running = True

    while running:

        dt = clock.tick(FPS) / 1000.0

        # ==============================
        # EVENTOS
        # ==============================

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            # Clique do mouse define o alvo
            if event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:

                    alvo = event.pos

        # ==============================
        # CONTROLE LINEAR
        # ==============================

        keys = pygame.key.get_pressed()

        v_cmd = 0.0

        if keys[pygame.K_w]:
            v_cmd = 120.0

        if keys[pygame.K_s]:
            v_cmd = -80.0

        # ==============================
        # CONTROLE PROPORCIONAL ANGULAR
        # ==============================

        omega_cmd = 0.0
        theta_desejado = 0.0
        erro_theta = 0.0

        if alvo is not None:

            x_alvo, y_alvo = alvo

            # Calcula o ângulo desejado
            theta_desejado = math.atan2(
                y_alvo - robot.y,
                x_alvo - robot.x
            )

            # Calcula o erro angular
            erro_theta = (
                theta_desejado
                - robot.theta
            )

            # Normaliza o erro entre -pi e pi
            erro_theta = (
                (erro_theta + math.pi)
                % (2 * math.pi)
                - math.pi
            )

            # Controlador proporcional
            omega_cmd = Kp * erro_theta

        # ==============================
        # APLICA O CONTROLE
        # ==============================

        robot.set_direct_velocity(
            v_cmd,
            omega_cmd
        )

        robot.update(dt)

        # ==============================
        # RENDERIZAÇÃO
        # ==============================

        screen.fill(COR_FUNDO)

        # Desenha o alvo
        if alvo is not None:

            pygame.draw.circle(
                screen,
                COR_ALVO,
                alvo,
                8
            )

            pygame.draw.circle(
                screen,
                COR_ALVO,
                alvo,
                15,
                2
            )

        # Desenha o robô
        robot.draw(screen)

        # ==============================
        # TELEMETRIA
        # ==============================

        info_txt = [

            f"Pose X: {robot.x:.1f} px | "
            f"Y: {robot.y:.1f} px",

            f"Theta atual: "
            f"{math.degrees(robot.theta):.1f} deg",

            f"Theta desejado: "
            f"{math.degrees(theta_desejado):.1f} deg",

            f"Erro angular: "
            f"{math.degrees(erro_theta):.1f} deg",

            f"Omega: {robot.omega:.2f} rad/s",

            "Clique com o mouse para definir o alvo",

            "W/S: Movimento linear"
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