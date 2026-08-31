# Resultados - Aula 03 (Sensores de Proximidade e Braitenberg)

## 1. Explicação simples dos resultados de cada exercício

**Lab 1 - Raycasting com 3 sensores**
O robô ganhou 3 "olhos" (esquerda, frente, direita) que enxergam
distância até obstáculos jogando um raio ponto a ponto até bater em
algo. Segui o mouse com o robô só pra testar melhor: quando ele se
aproxima de um retângulo vermelho, o raio correspondente fica amarelo
e mostra exatamente onde bateu. Funcionou de primeira, o código do
professor já estava certo.

**Lab 2 - Rotação in-place de 180°**
Aqui não tem sensor, é puramente cinemática. Calculei o tempo
necessário (`tempo = ângulo / velocidade_angular`) pra girar exatos
180° com `w = 45°/s`, dando 4 segundos. Simulei o `/cmd_vel` com uma
função que guarda o comando, o robô gira no lugar (x, y fixos) e ao
final do tempo eu mando velocidade zero pra ele parar de girar.
Confirmei no terminal que o `theta` final bateu certinho em 180°.

**Lab 3 - 5 sensores com ruído gaussiano**
Expandi de 3 pra 5 sensores em leque e adicionei ruído
(`np.random.normal(0, 2.0)`) em cima da distância real medida. Dá pra
ver na tela os números tremendo levemente mesmo com o robô parado,
que é exatamente o comportamento esperado de um sensor real (nunca
mede o valor "perfeito").

**Lab 4 - Veículo de Braitenberg (medo puro)**
Esse foi o que juntou todo o fluxo do diagrama do enunciado: sensor
→ lei reativa → cinemática inversa → movimento. A parte chave é a
fiação cruzada (sensor direito controla roda esquerda e vice-versa),
que faz o robô desviar de obstáculos sem nenhuma regra explícita de
"se tem parede, desvie" — o comportamento de desvio simplesmente
emerge da lei proporcional. Também coloquei uma regra extra de
"pânico" pra quando o sensor frontal detecta algo muito perto, porque
só a lei proporcional das laterais não reagia rápido o bastante
quando o obstáculo estava bem de frente.

**Lab 5 - Go-to-Goal com desvio**
O robô persegue um ponto clicado com o mouse usando um controlador
proporcional clássico (Modo 1), mas se algum sensor detecta obstáculo
muito perto, um torque repulsivo sobrepõe a velocidade angular
calculada (Modo 2) e reduz a velocidade linear, até o caminho ficar
livre de novo e o robô retomar a rota até o alvo. Ele para sozinho a
15px de distância do alvo.

## 2. Exercício de maior dificuldade

Pra mim o mais difícil foi o **Lab 5**. Não porque o código em si
seja mais complexo (o Lab 4 tem praticamente a mesma quantidade de
lógica), mas porque nele os dois comportamentos (ir até o alvo e
desviar do obstáculo) competem pelo controle do robô ao mesmo tempo,
e achar o equilíbrio certo entre os ganhos (`Kp_angular`,
`K_REPULSAO`, o quanto reduzir a velocidade durante o desvio) foi na
base da tentativa e erro. No Lab 4 o robô só tem um objetivo (não
bater), então a lei de Braitenberg sozinha já resolve; no Lab 5 tem
um "empate técnico" entre duas prioridades diferentes, e isso deixou
mais difícil prever o comportamento só olhando o código, precisei
mesmo rodar e ajustar os números várias vezes.

## 3. Impressões gerais sobre as dificuldades técnicas

No geral, a parte de matemática/cinemática (calcular `v`, `w`, e
integrar a pose) não foi tão complicada assim, é basicamente física
básica de movimento circular e retilíneo. A parte que mais exigiu de
mim foi entender a **lógica de controle reativo** do Braitenberg: no
começo eu queria escrever regras explícitas tipo "se sensor direito
< X, então vira pra esquerda", só que o professor deixa claro que a
ideia é não ter esse tipo de regra condicional explícita — o
comportamento deve nascer só da conexão (fiação) entre sensor e
atuador. Foi um "clique" mental entender que comportamento complexo
(desviar suavemente, contornar quinas) pode emergir de uma fórmula
bem simples sem nenhum "if" de decisão, e isso muda bastante a forma
de pensar em programação de robôs comparado com programação
"tradicional" cheia de condicionais.

Outra dificuldade foi calibrar os ganhos e limiares (`K`, distância
de pânico, distância de emergência) — não tem uma fórmula fechada
pra achar o valor "certo", é bastante ajuste empírico rodando o
simulador várias vezes e observando se o robô bate, oscila demais, ou
reage devagar demais.
