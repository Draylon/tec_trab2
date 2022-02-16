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

def build_to_left(id):
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
    return [
        MachineStructure(id,'#','*','r',id+"_drag_start"),
        MachineStructure(id+"_drag_start",'*','*','r',id+"_drag_start"),
        MachineStructure(id+"_drag_start",'$','*','*',id+"_drag"),

        MachineStructure(id+"_drag",'0','_','r',id+"_drag_0"),
        MachineStructure(id+"_drag",'1','_','r',id+"_drag_1"),
        MachineStructure(id+"_drag",'$','_','r',id+"_drag_$"),
        MachineStructure(id+"_drag",'_','_','r',id+"_drag__"),
        MachineStructure(id+"_drag",'B','_','r',id+"_drag_B"),
        MachineStructure(id+"_drag",'X','_','r',id+"_drag_X"),
        
        MachineStructure(id+"_drag",'#','*','r',id),
        
        MachineStructure(id+"_drag_$",'*','$','l',id+"_drag_b"),
        MachineStructure(id+"_drag_0",'*','0','l',id+"_drag_b"),
        MachineStructure(id+"_drag_1",'*','1','l',id+"_drag_b"),
        MachineStructure(id+"_drag__",'*','_','l',id+"_drag_b"),
        MachineStructure(id+"_drag_X",'*','X','l',id+"_drag_b"),

        MachineStructure(id+"_drag_b",'*','*','l',id+"_drag")
    ]



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
                additions = additions + build_to_left(x.current_state)

        default = '''; # = inicio da fita
; $ = final da fita

start * * r start
start _ $ r pull


;começa a puxar pra direita
pull 0 _ r pull_0
pull 1 _ r pull_1
pull $ _ r pull_$
pull # * r pull
pull _ _ l pull__

pull__ _ # r 0
pull__ $ $ r pull_$
pull__ 0 _ r pull_0
pull__ 1 _ r pull_1

;bota #|0|1|x na fita e volta
pull_$ * $ l pull
pull_0 * 0 l pull
pull_1 * 1 l pull


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