"""
LAB 02 - AULA 03
Rotacao in-place (giro de 180 graus sobre o proprio eixo).

Nao temos ROS instalado nesse ambiente, entao eu simulei o topico
/cmd_vel com uma funcao publish_cmd_vel(v, w) que guarda o comando
mais recente, exatamente como faria um publisher real. O "motor"
do robo (metodo update) le esse comando e integra a pose no tempo,
que e o que um driver real faria ao receber a mensagem.
"""

import pygame
import math

LARGURA, ALTURA = 700, 500
FPS = 60
COR_FUNDO = (20, 24, 30)
COR_ROBO = (0, 200, 255)


class Robo:
    def __init__(self, x, y, theta=0.0):
        self.x = float(x)
        self.y = float(y)
        self.theta = float(theta)  # rad
        self.v = 0.0   # velocidade linear (px/s)
        self.w = 0.0   # velocidade angular (rad/s)

    def publish_cmd_vel(self, v, w):
        """Simula a publicacao no topico /cmd_vel."""
        self.v = v
        self.w = w

    def update(self, dt):
        """Integra a pose a partir do comando de velocidade atual."""
        self.x += self.v * math.cos(self.theta) * dt
        self.y += self.v * math.sin(self.theta) * dt
        self.theta += self.w * dt


def main():
    pygame.init()
    screen = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("LAB 02 - Giro in-place de 180 graus")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 16)

    robo = Robo(LARGURA / 2, ALTURA / 2, theta=0.0)

    # --- calculo do giro ---
    angulo_alvo = math.pi          # 180 graus em radianos
    w_desejado = math.radians(45)  # velocidade angular: 45 graus/s
    tempo_necessario = angulo_alvo / w_desejado  # t = angulo / velocidade
    print(f"[LAB02] Angulo alvo: 180 deg | w = 45 deg/s | tempo necessario = {tempo_necessario:.2f} s")

    tempo_decorrido = 0.0
    girando = True
    theta_inicial = robo.theta

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if girando:
            if tempo_decorrido < tempo_necessario:
                # publica velocidade angular constante, sem velocidade linear
                # (posicao x,y fica fixa, so o theta muda)
                robo.publish_cmd_vel(v=0.0, w=w_desejado)
                tempo_decorrido += dt
            else:
                # zera a velocidade ao atingir o angulo desejado
                robo.publish_cmd_vel(v=0.0, w=0.0)
                girando = False
                print(f"[LAB02] Giro concluido! Theta final = {math.degrees(robo.theta):.1f} deg "
                      f"(variacao de {math.degrees(robo.theta - theta_inicial):.1f} deg)")

        robo.update(dt)

        screen.fill(COR_FUNDO)
        pos = (int(robo.x), int(robo.y))
        pygame.draw.circle(screen, COR_ROBO, pos, 20)
        fx = robo.x + 40 * math.cos(robo.theta)
        fy = robo.y + 40 * math.sin(robo.theta)
        pygame.draw.line(screen, (255, 60, 60), pos, (int(fx), int(fy)), 4)

        status = "GIRANDO..." if girando else "GIRO CONCLUIDO (parado)"
        textos = [
            f"Status: {status}",
            f"Theta atual: {math.degrees(robo.theta) % 360:.1f} graus",
            f"Posicao (x,y) fixa: ({robo.x:.1f}, {robo.y:.1f})",
            f"Tempo decorrido: {min(tempo_decorrido, tempo_necessario):.2f}s / {tempo_necessario:.2f}s",
        ]
        for i, t in enumerate(textos):
            screen.blit(font.render(t, True, (230, 230, 230)), (20, 20 + i * 22))

        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
