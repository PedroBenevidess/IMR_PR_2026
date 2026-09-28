def controle_reativo(distancias, d_critica=0.4, v_livre=0.5,
                     omega_giro=1.0, k=0.5, omega_max=1.0, d_max=5.0):
    # distancias = {'frente': float, 'esquerda': float, 'direita': float}
    frente = distancias['frente']
    esq = min(distancias['esquerda'], d_max)   # inf -> d_max
    dir_ = min(distancias['direita'], d_max)

    # Trava de segurança: freia e gira para o lado mais livre
    if frente < d_critica:
        omega = omega_giro if esq >= dir_ else -omega_giro  # + = anti-horário (esquerda)
        return 0.0, omega

    # Frente livre: avança e corrige omega pela diferença lateral
    omega = k * (esq - dir_)                   # esquerda mais livre -> vira à esquerda
    omega = max(-omega_max, min(omega_max, omega))
    return v_livre, omega


if __name__ == "__main__":
    print(controle_reativo({'frente': 0.3, 'esquerda': 2.0, 'direita': 1.0}))  # (0.0, 1.0)
    print(controle_reativo({'frente': 2.0, 'esquerda': 2.0, 'direita': 1.0}))  # (0.5, 0.5)
