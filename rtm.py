#!/usr/bin/python3

class RTM:
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
    pass