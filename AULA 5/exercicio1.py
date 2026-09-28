def converter_cmd_vel(v, omega, L=0.3, max_wheel_speed=1.5):
    # 1. Cinemática diferencial (velocidades brutas)
    v_e = v - omega * L / 2.0
    v_d = v + omega * L / 2.0

    # 2. Maior módulo entre as rodas
    maior = max(abs(v_e), abs(v_d))

    # 3. Saturação proporcional: mesma escala nas duas rodas
    #    (preserva a curvatura da trajetória, v/omega)
    if maior > max_wheel_speed:
        escala = max_wheel_speed / maior
        v_e *= escala
        v_d *= escala

    return v_e, v_d


if __name__ == "__main__":
    print(converter_cmd_vel(1.2, 3.0))  # (0.68, 1.5)
