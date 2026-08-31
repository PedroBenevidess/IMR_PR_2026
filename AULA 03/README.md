# Lab 01 - Raycasting com 3 sensores

## O que eu fiz

Peguei o código que o professor deu pronto, rodei local pra ver se dava
algum erro (não deu, só troquei o nome do arquivo pra `lab01_aula03.py`
e ajeitei uns comentários pra ficar mais claro pra mim depois).

A ideia do lab é simples: o robô tem 3 "raios" saindo dele, um pra
esquerda (-45°), um de frente (0°) e um pra direita (+45°). Cada raio
vai "andando" em passos de 4 pixels até bater em alguma parede da
tela ou em algum dos retângulos vermelhos (obstáculos). Quando bate,
ele guarda a distância percorrida até ali. Isso é basicamente o
raycasting que sensores tipo sonar/laser fazem na vida real, só que
simplificado em 2D.

Pra testar, deixei o robô seguindo o mouse (não pedia isso no
enunciado, mas ajuda bastante a ver os sensores reagindo em tempo
real quando ele se aproxima dos obstáculos).

## Resultado

Rodando o script abre uma janela 900x650 com fundo escuro. O robô
(bolinha azul) segue o cursor do mouse. Os 3 raios ficam **verdes**
quando não encontram nada (leitura = alcance máximo, 150px) e ficam
**amarelos** quando encontram um obstáculo, mostrando um pontinho no
local exato da colisão. No canto superior esquerdo aparece o valor
numérico de cada sensor (Esq / Frente / Dir) atualizando a cada frame.

Print da tela (comportamento observado) descrito no
`resultados_aula03.md` da pasta principal.

## O que eu entendi

O ponto central aqui é que o sensor não "sabe" onde está o obstáculo
de forma mágica — ele descobre isso testando ponto por ponto ao longo
do raio até achar uma colisão. Isso é bem diferente de um sensor de
verdade (que mede tempo de voo da luz/som), mas serve pra simular o
mesmo resultado: uma distância até o obstáculo mais próximo naquela
direção.
