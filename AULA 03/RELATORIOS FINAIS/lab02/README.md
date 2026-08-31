# Lab 02 - Rotação in-place de 180°

## O que eu fiz

Esse lab pedia pra validar a cinemática angular fazendo o robô girar
sobre o próprio eixo sem sair do lugar. Como aqui não temos ROS de
verdade rodando, criei uma função `publish_cmd_vel(v, w)` dentro da
classe do robô que faz o papel do tópico `/cmd_vel` — ela só guarda
os valores de velocidade linear e angular mais recentes, do mesmo
jeito que um publisher real faria.

O cálculo principal é bem direto:

```
tempo_necessario = angulo_alvo / velocidade_angular
```

Escolhi `w = 45°/s`, então pra girar 180° o tempo dá exatamente `4s`
(180 / 45 = 4). Enquanto o tempo não passa desse valor, o robô
recebe o comando `v=0, w=45°/s` (só gira, não anda pra frente).
Quando o tempo acaba, publico `v=0, w=0` pra zerar a velocidade —
isso é importante porque se eu esquecesse de mandar esse comando
final o robô ia continuar girando pra sempre.

## Resultado

Na janela do pygame o robô fica parado no centro, só a "seta"
vermelha (indicando o `theta`) gira lentamente até completar meia
volta. No terminal aparece:

```
[LAB02] Angulo alvo: 180 deg | w = 45 deg/s | tempo necessario = 4.00 s
[LAB02] Giro concluido! Theta final = 180.0 deg (variacao de 180.0 deg)
```

E na tela dá pra acompanhar em tempo real o ângulo atual e o tempo
decorrido, até aparecer "GIRO CONCLUIDO (parado)".

## O que eu entendi

A posição (x, y) do robô não muda em nenhum momento — só o `theta`.
Isso é meio óbvio pensando na fórmula da cinemática (x e y dependem
de `v`, e aqui `v = 0` o tempo todo), mas foi legal ver isso
"provado" visualmente: o círculo fica cravado no mesmo lugar e só a
orientação muda.
