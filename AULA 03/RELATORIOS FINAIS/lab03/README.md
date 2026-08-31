# Lab 03 - Múltiplos sensores + ruído gaussiano

## O que eu fiz

Aumentei o lab 1 de 3 pra **5 sensores**, abrindo em leque na frente
do robô: -60°, -30°, 0°, +30° e +60°, todos com alcance máximo de
200px (aumentei um pouco em relação ao lab 1 porque com 5 feixes dava
pra "enxergar" mais coisa ao redor).

A parte nova de verdade foi o ruído. Depois de calcular a distância
"real" (a mesma lógica de raymarch do lab 1), eu somo um valor
aleatório vindo de uma distribuição gaussiana:

```python
ruido = np.random.normal(0, 2.0)
leitura_ruidosa = distancia_real + ruido
```

Ou seja, em média o ruído é zero (não desloca a leitura pra nenhum
lado sistematicamente), mas cada medida individual pode variar uns
2px pra cima ou pra baixo — igualzinho um sensor ultrassônico de
verdade, que nunca dá o valor "perfeito", sempre balança um pouco.
Usei `np.clip` pra garantir que a leitura não fique negativa nem
passe do alcance máximo depois de somar o ruído.

Também coloquei o valor numérico de cada sensor escrito do lado da
ponta do raio na tela, como pedido.

## Resultado

A janela mostra o robô com 5 raios saindo dele. Quando o raio bate
em algum obstáculo fica amarelo, quando não bate fica verde. Do lado
de cada ponta aparece o número da distância (em px), e esse número
fica "tremendo" levemente frame a frame mesmo com o robô parado —
isso é o ruído gaussiano em ação. No canto superior esquerdo tem a
lista com todos os 5 sensores nomeados (S1 a S5).

## O que eu entendi

Antes desse lab eu tratava a leitura do sensor como se fosse um
valor exato. Aqui ficou claro que isso não é realista: qualquer
sensor físico tem incerteza, e é por isso que os algoritmos de
robótica geralmente não confiam 100% numa única leitura (por isso
existem filtros tipo Kalman, mas isso acho que é assunto pra mais
pra frente).
