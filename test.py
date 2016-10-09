from rtm import Machine, Transition

# configurando maquina
m = Machine()
m.setInputAlphabet('01#')
m.setTapeAlphabet('01#x')
m.setBlankSymbol('˽')
for i in range(1,5):
    m.addState(str(i))
m.setStarter('1')
m.setFinal('4')

t = Transition('1', ['0','˽','˽'], '2', ['x','0','˽'])
m.addTransition(t)
t = Transition('2', ['/','/','˽'], '3', [1,1,'˽'])
m.addTransition(t)
t = Transition('3', ['0','˽','˽'], '4', ['x','0','˽'])
m.addTransition(t)

m.setInputTape('00')
m.lock()

# printando passo a passo
print('Stand by. At 1')
while True:
    a = input()
    print('Fitas: {a} | {b} | {c}'.format(
        a=m.tapes['input'],
        b=m.tapes['history'],
        c=m.tapes['output']
    ))
    print('Pos:',' '.join([str(head.pos) for head in m.heads]))
    t = m.getCurrentState().matchedTransition([head.read() for head in m.heads])
    if t is not None:
        print (t.stateFrom,t.symbolsIn,'->',t.stateTo,t.symbolsOut)
    step = m.step()
    print(step,'. At',m.getCurrentState().name)
    if (step == 'Finished'):
        break