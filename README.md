![image](https://github.com/user-attachments/assets/02ab7613-71a4-4f82-98fb-ea3f253f207f)
Início do projeto

![image](https://github.com/user-attachments/assets/77baea83-5aca-40b3-a9b1-f9f449d29b1b)
Tela cheia antigamente

![image](https://github.com/user-attachments/assets/a11e4b27-260e-423b-9118-dd639063f3a0)
![image](https://github.com/user-attachments/assets/5ac22801-8a12-4e9f-a418-ff76a871cf06)
![image](https://github.com/user-attachments/assets/1be0646b-441a-4d3e-ad26-f8d16b81337d)
![image](https://github.com/user-attachments/assets/e2d1eff5-d020-458d-aaef-89a46651bc0f)
Após fizemos a implementação de sprites com canos em movimento

![image](https://github.com/user-attachments/assets/39cdbbdf-eab7-4b09-998c-4f61c3aaec9f)
![image](https://github.com/user-attachments/assets/03ad4b9b-c8cb-408a-81c7-8d3933d91915)
Implementação dos outros powerups como o que aumenta o tamanho dos espaços entre os canos ou diminui o tamanho do personagem

![image](https://github.com/user-attachments/assets/63237a47-0e37-4925-a4fb-3f7dfec11034)
Canos com sprites de árvores

![image](https://github.com/user-attachments/assets/ae89973a-6cb2-4ecd-9edd-53c4cf7125cd)
Adicionado high score

![image](https://github.com/user-attachments/assets/78a69245-732b-4c7c-a26f-acfd1f549753)
![image](https://github.com/user-attachments/assets/188967ba-0336-4e2e-ad0f-362133e3879f)
Novos sprites para personagem, chão e nuvens, além dos powerups

![image](https://github.com/user-attachments/assets/3935433f-8600-499a-b446-e9fb77ec41a8)
Implementação do botão de pausa

Flappy Bird Enhanced - README
🎯 Visão Geral

Este projeto é uma versão aprimorada do clássico Flappy Bird, desenvolvido em Python com OpenGL e GLFW. Ele inclui recursos adicionais como power-ups, sistema de vidas, diferentes estados de jogo e um sistema de recordes.
🚀 Como Rodar o Projeto
Pré-requisitos

    Python 3.6+

    Bibliotecas necessárias (instaláveis via pip):

bash

pip install glfw PyOpenGL numpy pillow

Execução

    Clone o repositório

    Navegue até o diretório do projeto

    Execute o arquivo principal:

bash

python main.py

🎮 Controles

    ESPAÇO: Pular/Iniciar jogo

    R: Reiniciar após game over

    ESC: Fechar o jogo

🧠 Lógica do Jogo
Componentes Principais

    Jogador (Pássaro):

        Física de gravidade e impulso

        Sistema de animação por spritesheet

        Detecção de colisão com tubos e chão

    Obstáculos (Tubos):

        Geração procedural de pares de tubos

        Movimento contínuo da direita para a esquerda

        Sistema de pontuação ao passar pelos tubos

    Power-ups:

        Tipos: Invulnerabilidade, Speed Boost, Chainsaw, Heavy Jump, Shrink

        Spawn aleatório entre os tubos

        Efeitos temporários com duração específica

    Sistema de Jogo:

        Máquina de estados: Menu, Jogando, Game Over

        Pontuação baseada em tubos ultrapassados

        Sistema de vidas (padrão: 3 vidas)

Fluxo Principal

    Inicialização de recursos (texturas, janela)

    Loop principal:

        Atualização da física e estados (delta time)

        Renderização dos elementos

        Processamento de input

    Liberação de recursos ao sair
