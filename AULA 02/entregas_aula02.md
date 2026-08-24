# Entregas — Aula 02 - Pedro e Rodrigo

## 1. Estado do Robô e POSE 2D

O estado de um robô pode ser representado por **(x, y, θ)**. Nesse caso, **x e y** representam a posição do robô no plano, enquanto **θ** indica a sua orientação.

Ou seja, a POSE 2D mostra basicamente **onde o robô está e para qual direção ele está apontando**.

## 2. Cinemática Diferencial

Em um robô com duas rodas, o movimento acontece de acordo com a velocidade de cada roda.

Quando as duas rodas possuem a mesma velocidade, o robô segue em linha reta. Se uma roda estiver mais rápida que a outra, ele faz uma curva. Já quando as rodas giram em sentidos opostos, o robô consegue girar no próprio eixo.

Essas velocidades são utilizadas para calcular a velocidade linear **v** e a velocidade angular **ω**.

## 3. Odometria Discreta

A odometria serve para estimar a nova posição do robô após um pequeno intervalo de tempo, chamado de **dt**.

A atualização da posição acontece utilizando as seguintes equações:

* **θ = θ + ω · dt**
* **x = x + v · cos(θ) · dt**
* **y = y + v · sin(θ) · dt**

Como esse processo é realizado várias vezes durante o movimento, pequenos erros podem acabar se acumulando ao longo do percurso.

## 4. Navegação GO-TO-GOAL

O objetivo dessa navegação é fazer com que o robô se desloque até um ponto determinado.

Primeiro, calculamos a direção que o robô precisa seguir:

**θ_desejado = atan2(y_alvo - y, x_alvo - x)**

Depois, calculamos a diferença entre a direção atual do robô e a direção desejada:

**erro_θ = θ_desejado - θ**

A partir desse erro, podemos calcular a velocidade angular usando um controlador proporcional:

**ω = Kp · erro_θ**

Dessa forma, quanto maior for o erro, maior será a correção feita pelo robô. Conforme ele vai se aproximando da direção correta, o erro diminui e o robô fica apontado para o alvo.
