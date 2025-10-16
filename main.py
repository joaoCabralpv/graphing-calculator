from collections.abc import Callable
from enum import Enum

class Operator:
    func:Callable
    n_arguments:int
    precedence:int

    def __init__(self,func:Callable,n_arguments,precedence):
        self.func=func
        self.n_arguments=n_arguments
        self.precedence=precedence

class SymbolType(Enum):
    NONE=0
    NUMBER=1
    OPERATOR=2
    
class Symbol:
    represented = None
    type = SymbolType.NONE

    def __init__(self,s,type:SymbolType):
        self.represented = s
        self.type=type

    def from_operator(op:Operator):
        return Symbol(op,SymbolType.OPERATOR)
    
    def from_float(f:float):
        return Symbol(f,SymbolType.NUMBER)


        

operators:dict[str,Operator] = {
    "+": Operator(lambda a: a[0]+a[1],2,1),
    "-": Operator(lambda a: a[0]-a[1],2,1),
    "*": Operator(lambda a: a[0]*a[1],2,2),
    "/": Operator(lambda a: a[0]/a[1],2,2),
    "u-":Operator(lambda a: -a[0],1,999)
}


rpn_stack:list[Symbol] =[Symbol.from_float(22),Symbol.from_operator(operators["u-"]),Symbol.from_float(3),Symbol.from_operator(operators["+"])]



def compute(rpn_stack):
    solve_stack:list = []

    for symbol in rpn_stack:
        if symbol.type == SymbolType.NUMBER:
            solve_stack.append(symbol.represented)
            continue

        if symbol.type == SymbolType.OPERATOR:
            operator = symbol.represented
            func = operator.func
            n_arguments = operator.n_arguments
            list_arguments = []

            for i in range(n_arguments):
                list_arguments.append(solve_stack.pop())

            list_arguments.reverse()
            solve_stack.append(func(list_arguments))
    return solve_stack[0]

print(compute(rpn_stack))