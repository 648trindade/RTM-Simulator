import rtm

numEstados, tamAlfEntr, tamAlfFita, numTrans = [int(i.strip()) for i in input().strip().split(' ')]

m = rtm.Machine()

estados = input().strip().split(' ')
for i in range(numEstados):
    m.addState(estados[i])

alfabetoEntrada = input().strip().split(' ')
m.setInputAlphabet(alfabetoEntrada[:tamAlfEntr])

alfabetoFita = input().replace('B','').strip().split(' ')
m.setTapeAlphabet(alfabetoFita[:tamAlfFita])

m.setStarter(estados[0])
m.setFinal(estados[numEstados-1])

for i in range(numTrans):
    _in, _out = input().strip().split('=')
    _in = _in.strip('()').split(',')
    _out = _out.strip('()').split(',')
    for i in range(1,len(_out)):
        if _in[i] == '/':
            if _out[i] == 'D':
                _out[i] = 1
            elif _out[i] == 'E':
                _out[i] = -1
            elif _out[i] == 'P':
                _out[i] = 0
    t = rtm.Transition(_in[0], _in[1:], _out[0], _out[1:])
    m.addTransition(t)

m.setInputTape(input().strip())
m.lock()
m.run()

print(m.tapes['input'])
print(m.tapes['history'])
print(m.tapes['output'])