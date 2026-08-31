# Lab 04 - Veículo de Braitenberg (medo puro)

## O que eu fiz

Esse foi o lab que juntou tudo: sensores + lei de controle reativo +
cinemática inversa + movimento real, exatamente o fluxo que tá no
diagrama do enunciado.

A parte mais importante é a **fiação cruzada**. Em vez de o sensor da
direita controlar a roda direita, ele controla a roda **esquerda**
(e vice-versa). Fiz assim:

```python
prox_dir = (alcance - dist_sensor_direito) / alcance   # 0 a 1
prox_esq = (alcance - dist_sensor_esquerdo) / alcance

v_L = v_cruzeiro + K * prox_dir   # obstaculo na DIREITA acelera roda ESQUERDA
v_R = v_cruzeiro + K * prox_esq   # obstaculo na ESQUERDA acelera roda DIREITA
```

Isso faz o robô virar pra **longe** do obstáculo (por isso "medo" —
ele foge, diferente da fiação direta que faria ele virar de encontro
ao obstáculo, tipo "agressão"). Também botei uma regra de pânico: se
o sensor da frente detectar algo a menos de 35px, esqueço a fórmula
proporcional e mando `v_L = +V, v_R = -V`, o que faz o robô girar
puro no próprio eixo até desviar — sem isso ele às vezes ficava preso
"cutucando" a parede de frente porque a lei proporcional sozinha não
reage rápido o suficiente quando o obstáculo tá bem na cara dele.

Depois disso é só a cinemática diferencial padrão:

```
v = (v_R + v_L) / 2
w = (v_R - v_L) / L        # L = distancia entre rodas
```

E integro `x, y, theta` com esse `v` e `w`.

## Resultado

O robô começa perto do canto superior esquerdo da sala fechada e vai
navegando sozinho entre os móveis (retângulos vermelhos) sem eu
mexer em nada — só clico em rodar o script. Ele desvia suavizado
quando o obstáculo está de lado, e faz um giro mais brusco quando
algo aparece bem na frente. Consegue circular pela sala inteira sem
bater, embora às vezes passe bem raspando perto de quinas.

## O que eu entendi

O que mais me surpreendeu foi perceber que **não existe nenhum "se
obstáculo então desviar" explícito** no código pra desviar de
obstáculos que não estão bem na frente — o desvio pras laterais
"emerge" sozinho só de eu ter cruzado os fios entre sensor e roda.
Isso é exatamente a ideia do Braitenberg: comportamento complexo
saindo de uma regra bem simples, sem mapa e sem planejamento.
