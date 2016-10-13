# RTM-Simulator
Simulador de uma máquina de turing reversível escrito em python 3

Para executá-lo, rode:

    python3 main.py

O programa espera as entradas vindas do _stdin_. A entrada se dá no seguinte formato:

A primeira linha apresenta números, que indicam: número de estados, número de símbolos no alfabeto de entrada, número de símbolos no alfabeto da fita e número de transições, respectivamente. A seguir, temos os estados, na próxima linha alfabeto de entrada e logo alfabeto da fita. Nas linhas sequentes temos as funções de transição. Depois da funcão de transição, segue uma entrada.

Você pode dizer ao programa para ler da entrada padrão, com o comando

    python3 main.py < arquivo.txt
