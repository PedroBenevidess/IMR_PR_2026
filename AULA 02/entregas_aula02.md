# Entregas --- Aula 02

## 1. Estado do Robô e POSE 2D

O estado do robô pode ser representado por **(x, y, θ)**:

-   **x, y**: posição do robô no plano.
-   **θ**: orientação do robô.

A **POSE 2D** informa, portanto, onde o robô está e para qual direção
está apontando.

## 2. Cinemática Diferencial

Em um robô com duas rodas, o movimento depende das velocidades da roda
esquerda e direita.

-   Mesma velocidade nas duas rodas → movimento em linha reta.
-   Velocidades diferentes → robô faz uma curva.
-   Rodas em sentidos opostos → robô gira no próprio eixo.

As velocidades das rodas são convertidas em velocidade linear **v** e
velocidade angular **ω**.

## 3. Odometria Discreta

A odometria estima a nova pose do robô usando o movimento ocorrido
durante um pequeno intervalo de tempo **dt**.

A atualização é feita passo a passo:

-   **θ = θ + ω · dt**
-   **x = x + v · cos(θ) · dt**
-   **y = y + v · sin(θ) · dt**

Como o cálculo é repetido várias vezes, pequenos erros podem se
acumular.

## 4. Navegação "GO-TO-GOAL"

O objetivo é orientar o robô para um ponto alvo.

Primeiro, calcula-se a direção desejada:

**θ_desejado = atan2(y_alvo - y, x_alvo - x)**

Depois, calcula-se o erro:

**erro_θ = θ_desejado - θ**

Um controlador proporcional pode gerar a velocidade angular:

**ω = Kp · erro_θ**

Assim, quanto maior o erro, maior é a correção do robô. Quando o erro se
aproxima de zero, o robô fica apontado para o alvo.
