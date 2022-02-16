import sys

class MachineStructure:
    def __init__(self,current_state,current_symbol,new_symbol,direction,new_state):
        self.current_state=current_state
        self.current_symbol=current_symbol
        self.new_symbol=new_symbol
        self.direction=direction
        self.new_state=new_state
    def __repr__(self):
        #return f"s{self.current_state}:{self.current_symbol}>s{self.new_state}"
        
        return f"{self.current_state} {self.current_symbol} {self.new_symbol} {self.direction} {self.new_state}"
        #return f"<{self.current_state}> <{self.current_symbol}> <{self.new_symbol}> <{self.direction}> <{self.new_state}>"
        
        #return "<"+self.current_state+"> <"+self.current_symbol+"> <"+self.new_symbol+"> <"+self.direction+"> <"+self.new_state+">"
        
    def exprt(self):
        return f"{self.current_state} {self.current_symbol} {self.new_symbol} {self.direction} {self.new_state}"
    
def build_to_right(id):
    #;special_to_right
    #0 $ * * 0_push_end
    #0_push_end $ _ r 0_push_end
    #0_push_end _ $ l 0
    return [
        MachineStructure(id,'$','*','*',id+"_push_end"),
        MachineStructure(id+"_push_end",'$','_','r',id+"_push_end"),
        MachineStructure(id+"_push_end",'_','$','l',id)
    ]

def build_to_left(id,machine):
    #;special_to_left
    #1 # * r 1_drag_start
    #1_drag_start * * r 1_drag_start
    #1_drag_start $ * * 1_drag
    #1_drag 0 _ r 1_drag_0
    #1_drag 1 _ r 1_drag_1
    #1_drag $ _ r 1_drag_$
    #1_drag _ _ r 1_drag__
    #1_drag # * r 1 ; SAIDA
    #1_drag_$ * $ l 1_drag_b
    #1_drag_0 * 0 l 1_drag_b
    #1_drag_1 * 1 l 1_drag_b
    #1_drag__ * _ l 1_drag_b
    #1_drag_b * * l 1_drag

    allsymbols = list(get_all_symbols(id,machine))

    listreturn = [
        MachineStructure(id,'#','*','r',id+"_drag_start"),
        MachineStructure(id+"_drag_start",'*','*','r',id+"_drag_start"),
        MachineStructure(id+"_drag_start",'$','*','*',id+"_drag"),
        MachineStructure(id+"_drag",'#','*','r',id),
        MachineStructure(id+"_drag_@",'*','*','l',id+"_drag")
    ]
    for sym in allsymbols:
        listreturn.append(
            MachineStructure(id+"_drag",sym,'_','r',id+"_drag_"+sym)
        )
        listreturn.append(
            MachineStructure(id+"_drag_"+sym,'*',sym,'l',id+"_drag_@")
        )
    return listreturn

def get_all_symbols(id,machineList):
    symbols = set()
    for x in machineList:
        if x.current_state == id:
            if x.current_symbol != '*' and x.current_symbol != '#':
                symbols.add(x.current_symbol)
            if x.new_symbol != '*' and x.new_symbol != '#':
                symbols.add(x.new_symbol)
    symbols.add('$')
    return symbols


if __name__ == "__main__":
    filename = sys.argv[1:2][0]
    if not filename:
        print("missing file")
        exit()
    else:
        #machine = [MachineStructure(0,0,0,0,0)]
        machine = list()
        additions = list()
        r_defined = list()
        l_defined = list()
        file = open(filename, "r")
        for line in file:
            if len(line) <= 1 or line == "" or line == '\n':
                continue
            line = str.rstrip(line)
            line=str.split(line," ")
            machine.append(MachineStructure(line[0],line[1],line[2],line[3],line[4]))
        
        file.close()

        for x in machine:
            if x.direction == 'l' and x.current_state not in l_defined:
                l_defined.append(x.current_state)
                additions = additions + build_to_right(x.current_state)
            elif x.direction == 'r' and x.current_state not in r_defined:
                r_defined.append(x.current_state)
                additions = additions + build_to_left(x.current_state,machine)

        default = '''; # = inicio da fita
; $ = final da fita

_|start|_ * * r _|start|_
_|start|_ _ $ r _|pull|_


;começa a puxar pra direita
_|pull|_ 0 _ r _|pull|__0
_|pull|_ 1 _ r _|pull|__1
_|pull|_ $ _ r _|pull|__$
_|pull|_ # * r _|pull|_
_|pull|_ _ _ l _|pull|___

_|pull|___ _ # r 0
_|pull|___ $ $ r _|pull|__$
_|pull|___ 0 _ r _|pull|__0
_|pull|___ 1 _ r _|pull|__1

;bota #|0|1|x na fita e volta
_|pull|__$ * $ l _|pull|_
_|pull|__0 * 0 l _|pull|_
_|pull|__1 * 1 l _|pull|_


;=============================
;=============================
;=============================

; Regra original

'''
        exp_file = open(file.name+".txt",'w+')
        exp_file.write(default+'\n')
        
        for x in machine:
            exp_file.write(x.exprt()+'\n')

        exp_file.write('''\n;=============================
;=============================
;=============================\n''')

        exp_file.write("; Adicoes a maquina\n\n")

        for x in additions:
            exp_file.write(x.exprt()+'\n')

        exp_file.close()