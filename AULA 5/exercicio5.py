import math
from exercicio3 import controle_reativo
from exercicio4 import calcular_orientacao_alvo


def maquina_de_estados(x, y, theta, x_alvo, y_alvo, dist_frente, dist_esq, dist_dir):
    dist_alvo = math.sqrt((x_alvo - x) ** 2 + (y_alvo - y) ** 2)

    # Prioridade: objetivo > obstáculo > ir para o alvo
    if dist_alvo < 0.2:
        return 'OBJETIVO_ALCANÇADO', 0.0, 0.0

    if dist_frente < 0.5:
        # Entre 0.4 e 0.5 m o Ex. 3 mandaria avançar; para não ficar colado
        # na parede, forçamos a rotação no lugar durante este estado.
        v, omega = controle_reativo({'frente': min(dist_frente, 0.39),
                                     'esquerda': dist_esq,
                                     'direita': dist_dir})
        return 'DESVIAR_OBSTACULO', v, omega

    omega = calcular_orientacao_alvo(x, y, theta, x_alvo, y_alvo)
    return 'IR_PARA_ALVO', 0.5, omega


if __name__ == "__main__":
    print(maquina_de_estados(0, 0, 0, 3, 3, 2.0, 2.0, 2.0))
    print(maquina_de_estados(0, 0, 0, 3, 3, 0.45, 2.0, 1.0))
    print(maquina_de_estados(0, 0, 0, 0.1, 0.1, 2.0, 2.0, 2.0))
