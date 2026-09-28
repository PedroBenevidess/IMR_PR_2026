import math


def processar_scan(leituras_lidar, r_min=0.1, r_max=5.0):
    # leituras_lidar: lista/array com 360 floats (índice = ângulo em graus)
    leituras = list(leituras_lidar)

    def menor_valida(indices):
        validas = [leituras[i] for i in indices
                   if math.isfinite(leituras[i]) and r_min <= leituras[i] <= r_max]
        return min(validas) if validas else float('inf')

    idx_frente = list(range(345, 360)) + list(range(0, 16))  # 345° a 15° (cruza o zero)
    idx_esq = range(45, 136)                                  # 45° a 135°
    idx_dir = range(225, 316)                                 # 225° a 315°

    return {
        'frente': menor_valida(idx_frente),
        'esquerda': menor_valida(idx_esq),
        'direita': menor_valida(idx_dir),
    }


if __name__ == "__main__":
    scan = [3.0] * 360
    for i in range(0, 5):
        scan[i] = 0.0            # ruído nulo
    scan[10] = 0.3               # obstáculo à frente
    scan[100] = float('inf')     # fora do alcance
    scan[90] = 1.2               # obstáculo à esquerda
    print(processar_scan(scan))
