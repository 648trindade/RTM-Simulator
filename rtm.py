#!/usr/bin/python3

"""Pacote com classes que implementam em conjunto um simulador de uma máquina
de turing reversível"""

class RTM:
    """Classe representando uma máquina de turing reversível. Contém atributos
    com objetos referentes a seus componentes"""
    def __init__(self):
        self.estados = {
            'A': [],
            'B': [],
            'C': []
        }
        self.alfabeto_entrada = []
        self.alfabeto_fita = []

    def criarEstados(self, n):
        self.estados['A'] = [ Estado(i) for i in range (n) ]

class Estado:
    def __init__(self, nome):
        self.nome = nome
        self.transicoes = []

    def addTransicao(self, transicao):
        self.transicoes.append(transicao)
    
    def temTransicao(self, transicao):
        return transicao in self.transicoes


class Fita:
    def __init__(self, conteudo):
        self.conteudo = conteudo
    
    def le(self, index):
        if index in range(len(self.conteudo)):
            return self.conteudo[index]
        return 'B'
    
    def escreve(self, index, value):
        _len = len(self.conteudo)
        if index in range(_len):
            listChars = list(self.conteudo)
            listChars[index] = value
            self.conteudo = ''.join(listChars)
        elif value != 'B':
            if index < 0:
                self.conteudo = value.ljust(abs(index), 'B') + self.conteudo
            else:
                self.conteudo += value.rjust(index-len-1, 'B')
    
    def __str__(self):
        return self.conteudo

class Transicao:
    def __init__(self, origem, fitas_in, destino, fitas_out):
        self.origem = origem
        self.fitas_in = fitas_in
        self.destino = destino
        self.fitas_out = fitas_out
    
    def __eq__(self, fita):
        return self.fitas_in == fita
    
    def __getitem__(self, index):
        return self.fitas_out[i]
    

class Cabecote:
    def __init__(self):
        self.pos = 0
        self.fita = Fita("")

    def moveRight(self):
        self.pos += 1
    
    def moveLeft(self):
        self.pos -= 1
    
    def read(self):
        return self.fita.le(self.pos)
    
    def write(self, symbol):
        self.fita.escreve(self, symbol)
        if self.pos < 0 and symbol != 'B':
            self.pos = 0

"""uashdusahduashduashduashduashdu asudh asudhasu hasueh saueh uahe uasr hfuasrh asur fhauhriw uhfaiwurh iawu h"""

