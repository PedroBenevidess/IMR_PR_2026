# Lab 05 - Go-to-Goal com desvio reativo

## O que eu fiz

Esse foi de longe o mais trabalhoso, porque precisa combinar dois
comportamentos diferentes no mesmo robô: perseguir um alvo E desviar
de obstáculo, sem que um atrapalhe o outro.

**Modo 1 (atração ao alvo):** é um controlador proporcional clássico.
Calculo o ângulo entre a direção atual do robô e a direção do alvo
(`erro_ang`), e a velocidade angular é proporcional a esse erro:

```python
w = Kp_angular * erro_ang
v = Kp_linear * distancia_ate_o_alvo   # limitado em V_MAX
```

Isso sozinho já faz o robô ir reto até o alvo e ir freando conforme
se aproxima (porque `v` cai junto com a distância).

**Modo 2 (desvio de emergência):** só entra em ação quando algum dos
5 sensores acusa uma distância menor que 55px. Nesse caso eu calculo
um "torque repulsivo" somando a contribuição de cada sensor que está
muito perto, com sinal oposto ao lado de onde veio o obstáculo (se o
obstáculo está do lado direito do robô, o torque empurra pra
esquerda, e vice-versa). Esse torque **sobrepõe** o `w` do modo 1
completamente enquanto durar a emergência, e eu também reduzo a
velocidade linear pra 30% — não faz sentido acelerar em direção ao
alvo se tem alguma coisa quase colidindo do lado.

Assim que os sensores voltam a ficar livres, a lógica volta sozinha
pro modo 1 e o robô retoma o caminho até o alvo.

O robô para quando fica a menos de 15px do alvo clicado.

## Resultado

Ao rodar o script, o robô começa parado no canto superior esquerdo.
Clicando em qualquer lugar da tela aparece uma marcação amarela (o
alvo) e o robô sai perseguindo. Se no caminho ele encontra um dos
retângulos vermelhos, dá pra ver claramente ele "desviando" (virando
mais forte) perto do obstáculo e depois voltando a apontar pro alvo
assim que passa por ele. Quando chega perto o suficiente do alvo, o
texto muda pra "ALVO ATINGIDO" e ele para de vez.

## O que eu entendi

A parte mais difícil de acertar foi o **peso relativo** entre os dois
modos — se o ganho de repulsão (`K_REPULSAO`) for baixo demais, o
robô ignora o obstáculo e bate; se for alto demais, ele fica
"vibrando" entre desviar e voltar pro alvo sem nunca progredir de
verdade. Tive que ir testando os valores até achar um equilíbrio
razoável (55px de distância de emergência e reduzir a velocidade
linear pra 30% durante o desvio ajudou bastante a estabilizar).
