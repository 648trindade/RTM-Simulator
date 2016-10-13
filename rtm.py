#!/usr/bin/python3

"""Package with classes that implement together a simulator of a Reversible Turing machine"""

class Machine:
    """Class representing a reversible Turing machine. It contains attributes with objects related to its components.
    To use it, its necessary:
     1. Define a tape alphabet (without blank symbol)
     2. Define a input alphabet (without blank symbol)
     8. Define a blank symbol (optional)
     3. Add state names
     4. Define a starter state
     5. Define final states
     6. Add transitions
     7. Specify an input tape text
     9. Lock machine
     10. Run it or execute step by step"""

    def __init__(self):
        self.states = {
            'A': dict(),
            'B': dict(),
            'C': dict()
        }
        self.tapeAlphabet = list()
        self.inputAlphabet = list()
        self.heads = [Machine.Head() for i in range(3)]
        self.tapes = {
            'input': self.heads[0].tape,
            'history': self.heads[1].tape,
            'output': self.heads[2].tape
        }
        self.starterState = None
        self.finalState = None
        self.blank = 'B'
        # variáveis de controle interno
        self.__locked = False
        self.__state = None

    def addState(self, name, final=False):
        if self.__locked:
            raise Exception('Machine Locked. An unlock is necessary for editing.')
        if self.states['A'].get(name) is not None:
            raise Exception('State {name} already registered on machine.'.format(name=name))
        
        self.states['A'][name] = Machine.State(name, final)
        self.finalState = name
    
    def addTransition(self, transition):
        if self.__locked:
            raise Exception('Machine Locked. An unlock is necessary for editing.')
        statesNames = self.states['A'].keys()
        if transition.stateFrom not in statesNames:
            raise Exception('Machine has no state {transition.stateFrom} registered'.format(transition=transition))
        if transition.stateTo not in statesNames:
            raise Exception('Machine has no state {transition.stateTo} registered'.format(transition=transition))
        checkResult = transition.checkAlphabet(self.tapeAlphabet)
        if len(self.tapeAlphabet) is 0:
            raise Exception('Tape alphabet is empty.')
        if not checkResult[0]:
            raise Exception('Symbol {s} not in tape alphabet.'.format(s=checkResult[1]))
        
        transition._objTo = self.states['A'][transition.stateTo]
        self.states['A'][transition.stateFrom].addTransition(transition)
    
    def setFinal(self, name):
        if self.__locked:
            raise Exception('Machine Locked. An unlock is necessary for editing.')
        if name not in self.states['A'].keys():
            raise Exception('Machine has no state {name} registered'.format(name=name))
        
        if not self.states['A'][name].final:
            self.states['A'][name].final = True
            self.finalState = name
    
    def setStarter(self, name):
        if self.__locked:
            raise Exception('Machine Locked. An unlock is necessary for editing.')
        if name not in self.states['A'].keys():
            raise Exception('Machine has no state {name} registered'.format(name=name))
        
        self.starterState = name

    def setInputTape(self, tape):
        if self.__locked:
            raise Exception('Machine Locked. An unlock is necessary for editing.')
        if len(self.inputAlphabet) is 0:
            raise Exception('Input alphabet is empty. Cannot verify tape content.')
        for s in str(tape):
            if s not in self.inputAlphabet:
                raise Exception('Input tape not accepted. Input alphabet has no symbol {s}'.format(s=s))
        
        self.tapes['input'].content = str(tape)
    
    def setInputAlphabet(self, alphabet):
        if type(alphabet) not in (str, list):
            raise Exception('Alphabet providade must be a string or a character list.')

        if type(alphabet) is str:
            self.inputAlphabet = alphabet
        else:
            self.inputAlphabet = ''.join(alphabet)
    
    def setTapeAlphabet(self, alphabet):
        if type(alphabet) not in (str, list):
            raise Exception('Alphabet providade must be a string or a character list.')

        if type(alphabet) is str:
            self.tapeAlphabet = alphabet + self.blank
        else:
            self.tapeAlphabet = ''.join(alphabet) + self.blank
    
    def setBlankSymbol(self, symbol):
        if self.__locked:
            raise Exception('Machine Locked. An unlock is necessary for editing.')
        if len(symbol.strip()) > 1:
            raise Exception("Blank symbol must consist of one alphanumeric character.", symbol.strip())
        
        symbol = symbol.strip()
        self.tapeAlphabet = self.tapeAlphabet.replace(self.blank, symbol)
        self.blank = symbol
        for obj in list(self.tapes.values()) + self.heads:
            obj.blank = self.blank

    def getCurrentState(self):
        return self.__state
    
    def step(self):
        if not self.__locked:
            raise Exception('Machine unlocked. A lock is necessary for stepping.')
        
        symbols = [head.read() for head in self.heads]
        transition = self.__state.matchedTransition(symbols)
        if transition is None:
            return 'Finished' if self.__state.final else 'Unfinished'
        for i in range(3):
            if transition.symbolsIn[i] == '/':
                self.heads[i].move(transition[i])
            else:
                self.heads[i].write(transition[i])
        self.__state = transition._objTo
        return 'Stepped'
    
    def run(self):
        if not self.__locked:
            raise Exception('Machine unlocked. A lock is necessary for running.')
        
        while True:
            result = self.step()
            if result != 'Stepped':
                print(result)
                break
    
    def lock(self):
        if len(self.tapeAlphabet) is 0:
            raise Exception('Tape alphabet is empty.')
        if self.starterState is None:
            raise Exception('Starter state not set.')
        if self.finalState is None:
            raise Exception('No final state.')

        if not self.__locked:
            self.states['B'].clear()
            self.states['C'].clear()
            self.__generateRetraceStates()
            self.__generateCopyStates()
            self.__state = self.states['A'][self.starterState]
            self.__locked = True
    
    def __generateRetraceStates(self):
        for name in self.states['A'].keys():
            self.states['C'][name] = Machine.State(name)
        self.states['C'][self.starterState].final = True
        for name, state in self.states['A'].items():
            for transition in state.transitions:
                r_transition = transition.getReverse()
                r_transition._objTo = self.states['C'][r_transition.stateTo]
                self.states['C'][r_transition.stateFrom].addTransition(r_transition)
    
    def __generateCopyStates(self):
        self.states['B']['-'] = Machine.State('-')
        self.states['B']['a'] = Machine.State('a')
        self.states['B']['A'] = Machine.State('A')
        self.states['B']['b'] = Machine.State('b')
        self.states['B']['+'] = Machine.State('+')
        # transitions to -
        name = self.finalState
        t = Transition(name, ['/', '/', self.blank], '-', [0, 0, self.blank])
        t._objTo = self.states['B']['-']
        self.states['A'][name].addTransition(t)
        # shift left and goes to a
        t = Transition('-', [self.blank, '/', '/'], 'a', [self.blank, 0, 0])
        t._objTo = self.states['B']['a']
        self.states['B']['-'].addTransition(t)
        t = Transition('-', ['/', '/', '/'], '-', [-1, 0, 0])
        t._objTo = self.states['B']['-']
        self.states['B']['-'].addTransition(t)
        # transitions from a
        t = Transition('a', ['/', '/', '/'], 'A', [1, 0, 1])
        t._objTo = self.states['B']['A']
        self.states['B']['a'].addTransition(t)
        # transitions from A
        t = Transition('A', [self.blank, '/', self.blank], 'b', [self.blank, 0, self.blank])
        t._objTo = self.states['B']['b']
        self.states['B']['A'].addTransition(t)
        for symbol in self.tapeAlphabet:
            t = Transition('A', [symbol, '/', self.blank], 'a', [symbol, 0, symbol])
            t._objTo = self.states['B']['a']
            self.states['B']['A'].addTransition(t)
        # shift one character left
        for symbol in self.tapeAlphabet[:-1]:
            t = Transition('b', [symbol, '/', self.blank], '+', [symbol, 0, symbol])
            t._objTo = self.states['B']['+']
            self.states['B']['b'].addTransition(t)
        t = Transition('b', ['/', '/', '/'], '+', [-1, 0, 0])
        t._objTo = self.states['B']['+']
        self.states['B']['b'].addTransition(t)
        t = Transition('+', ['/', '/', '/'], name, [0, 0, 0])
        t._objTo = self.states['C'][name]
        self.states['B']['+'].addTransition(t)
        # remove final properties of original states
        self.states['A'][name].final = False

    def unlock(self):
        self.states['A'][self.finalState].final = True
        self.__locked = False

    class Head:
        """Subclass that represents a head of a Turing machine."""

        def __init__(self, blank='B'):
            self.pos = 0
            self.blank = blank
            self.tape = Machine.Tape("")

        def move(self, value):
            self.pos += value
        
        def read(self):
            return self.tape.read(self.pos)
        
        def write(self, symbol):
            self.tape.write(self.pos, symbol)
            if self.pos < 0 and symbol != self.blank:
                self.pos = 0
    
    class Tape:
        """Subclass that represents a tape in a Turing machine."""
        
        def __init__(self, content, blank='B'):
            """Create a tape and define its content as the string representation of the content parameter."""
            
            self.content = str(content)
            self.blank = blank
        
        def read(self, index):
            """Returns the symbol contained in the position specified by the index parameter, relative to the current tape beginning."""
            
            if index in range(len(self.content)):
                return self.content[index]
            return self.blank
        
        def write(self, index, value):
            """Writes the specified value on the tape in the position specified by the index parameter, relative to the current tape beginning."""
            
            if len(value.strip()) > 1:
                raise Exception("Write value must contain only one alphanumeric character.", value.strip())

            _len = len(self.content)
            if index in range(_len):
                listSymbols = list(self.content)
                listSymbols[index] = value.strip()
                self.content = ''.join(listSymbols)
            elif value != self.blank:
                if index < 0:
                    self.content = value.ljust(abs(index), self.blank) + self.content
                else:
                    self.content += value.rjust(index-_len-1, self.blank)
        
        def __str__(self):
            return self.content

    class State:
        """Subclass that represents a state of a Turing machine."""

        def __init__(self, name, final=False):
            if len(name.strip()) > 1:
                raise Exception("State name must contain only one alphanumeric character.", name.strip())
            
            self.name = name.strip()
            self.transitions = list()
            self.final = final
        
        def matchedTransition(self, _list):
            for transition in self.transitions:
                if transition.matchInput(self.name, _list):
                    return transition
            return None
        def addTransition(self, transition):
            self.transitions.append(transition)

class Transition:
    """Class that represents a transition between states on a Turing machine."""

    def __init__(self, stateFrom, symbolsIn, stateTo, symbolsOut):
        if (len(symbolsIn) is not 3) or (len(symbolsOut) is not 3):
            raise Exception("Lengths of arrays of symbols must be 3.")
        for i in range(3):
            if (symbolsIn[i] == '/') and (symbolsOut[i] not in (-1,0,1)):
                raise Exception("/ operations require a pair with value -1, 0 or 1. Found {s}.".format(s=symbolsOut[i]))

        self.stateFrom = stateFrom
        self.symbolsIn = symbolsIn
        self.stateTo = stateTo
        self.symbolsOut = symbolsOut
        self._objTo = None
    
    def matchInput(self, state, symbols):
        if self.stateFrom != state:
            return False
        for i in range(3):
            if (symbols[i] != self.symbolsIn[i]) and (self.symbolsIn[i] != '/'):
                return False
        return True

    def __getitem__(self, index):
        return self.symbolsOut[index]
    
    def checkAlphabet(self, alphabet):
        for symbol in [self.symbolsIn[0], self.symbolsOut[0]]:
            if symbol not in ('/',-1,0,1):
                if symbol not in alphabet:
                    return [False, symbol]
        return [True]

    def getReverse(self):
        r_in = list()
        r_out = list()
        for i in range(3):
            if self.symbolsIn[i] != '/':
                r_in.append(self.symbolsOut[i])
                r_out.append(self.symbolsIn[i])
            else:
                r_in.append('/')
                r_out.append(- self.symbolsOut[i])
        return Transition(self.stateTo, r_in, self.stateFrom, r_out)

