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


# ==============================
# Classe do Robô
# ==============================

class DiffDriveRobot:
    def __init__(self, x, y, theta=0.0,
                 wheelbase=30.0, radius=15.0):

        # Estado do robô
        self.x = float(x)
        self.y = float(y)
        self.theta = float(theta)

        # Parâmetros físicos
        self.L = float(wheelbase)
        self.radius = float(radius)

        # Velocidades
        self.v = 0.0
        self.omega = 0.0

        # Histórico da trajetória
        self.history = []

    def set_direct_velocity(self, v, omega):
        self.v = v
        self.omega = omega

    def update(self, dt):

        # Atualiza orientação
        self.theta += self.omega * dt

        # Normaliza o ângulo
        self.theta = (
            (self.theta + math.pi)
            % (2 * math.pi)
            - math.pi
        )

        # Atualiza posição
        self.x += self.v * math.cos(self.theta) * dt
        self.y += self.v * math.sin(self.theta) * dt

        # Salva trajetória
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

        # Desenha trajetória
        if len(self.history) > 1:
            pygame.draw.lines(
                surface,
                COR_TRAJETORIA,
                False,
                self.history,
                2
            )

        # Corpo do robô
        pos_int = (int(self.x), int(self.y))

        pygame.draw.circle(
            surface,
            COR_ROBO,
            pos_int,
            int(self.radius)
        )

        # Direção do robô
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
            (
                int(linha_frente_x),
                int(linha_frente_y)
            ),
            3
        )


# ==============================
# Estados da Máquina
# ==============================

FRENTE = 0
GIRAR = 1
FINALIZADO = 2


# ==============================
# Programa Principal
# ==============================

def main():

    pygame.init()

    screen = pygame.display.set_mode(
        (LARGURA_TELA, ALTURA_TELA)
    )

    pygame.display.set_caption(
        "Exercício 2 - Quadrado em Malha Aberta"
    )

    clock = pygame.time.Clock()

    font = pygame.font.SysFont(
        "monospace",
        16
    )

    # Cria o robô
    robot = DiffDriveRobot(
        x=LARGURA_TELA // 2,
        y=ALTURA_TELA // 2,
        theta=0.0
    )

    # ------------------------------
    # Configuração do movimento
    # ------------------------------

    VELOCIDADE_LINEAR = 100.0      # pixels/s

    # Para girar 90 graus em 1 segundo:
    VELOCIDADE_ANGULAR = math.pi / 2

    TEMPO_FRENTE = 2.0
    TEMPO_GIRO = 1.0

    # ------------------------------
    # Máquina de Estados
    # ------------------------------

    estado = FRENTE

    tempo_estado = 0.0

    lado = 0

    running = True

    while running:

        # Delta time
        dt = clock.tick(FPS) / 1000.0

        # Eventos
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

        # Atualiza o tempo do estado atual
        tempo_estado += dt

        # ==============================
        # ESTADO: MOVER PARA FRENTE
        # ==============================

        if estado == FRENTE:

            robot.set_direct_velocity(
                VELOCIDADE_LINEAR,
                0.0
            )

            # Após 2 segundos, começa a girar
            if tempo_estado >= TEMPO_FRENTE:

                estado = GIRAR

                tempo_estado = 0.0


        # ==============================
        # ESTADO: GIRAR 90 GRAUS
        # ==============================

        elif estado == GIRAR:

            robot.set_direct_velocity(
                0.0,
                VELOCIDADE_ANGULAR
            )

            # Após 1 segundo, termina o giro
            if tempo_estado >= TEMPO_GIRO:

                lado += 1

                tempo_estado = 0.0

                # Se completou 4 lados
                if lado >= 4:

                    estado = FINALIZADO

                else:

                    estado = FRENTE


        # ==============================
        # ESTADO: FINALIZADO
        # ==============================

        elif estado == FINALIZADO:

            robot.set_direct_velocity(
                0.0,
                0.0
            )

        # Atualiza a cinemática
        robot.update(dt)

        # ==============================
        # Renderização
        # ==============================

        screen.fill(COR_FUNDO)

        robot.draw(screen)

        # Nome do estado
        if estado == FRENTE:
            nome_estado = "FRENTE"

        elif estado == GIRAR:
            nome_estado = "GIRANDO"

        else:
            nome_estado = "FINALIZADO"

        # Telemetria
        info_txt = [

            f"Estado: {nome_estado}",

            f"Lado atual: {lado + 1}/4",

            f"Tempo do estado: "
            f"{tempo_estado:.2f} s",

            f"X: {robot.x:.1f} | "
            f"Y: {robot.y:.1f}",

            f"Theta: "
            f"{math.degrees(robot.theta):.1f} graus"

        ]

        for i, txt in enumerate(info_txt):

            rendered = font.render(
                txt,
                True,
                (220, 220, 220)
            )

            screen.blit(
                rendered,
                (15, 15 + i * 25)
            )

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()