from collections.abc import Callable
from enum import Enum

class Operator:
    func:Callable
    n_arguments:int
    precedence:int
    string:str

    def __init__(self,func:Callable,n_arguments,precedence,string):
        self.func=func
        self.n_arguments=n_arguments
        self.precedence=precedence
        self.string=string

    def __str__(self):
        return self.string

    

class SymbolType(Enum):
    NONE=0
    NUMBER=1
    OPERATOR=2
    OPEN_PARENTHESIS=3
    CLOSED_PARENTHESIS=4
    
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
    
    def open_parenthesis():
        return Symbol(None,SymbolType.OPEN_PARENTHESIS)
    
    def closed_parenthesis():
        return Symbol(None,SymbolType.CLOSED_PARENTHESIS)
    
    def __str__(self):
        return str(self.represented)


        

operators:dict[str,Operator] = {
    "+": Operator(lambda a: a[0]+a[1],2,1,"+"),
    "-": Operator(lambda a: a[0]-a[1],2,1,"-"),
    "*": Operator(lambda a: a[0]*a[1],2,2,"*"),
    "/": Operator(lambda a: a[0]/a[1],2,2,"/"),
    "u-":Operator(lambda a: -a[0],1,999,"u-")
}




rpn_stack:list[Symbol] =[Symbol.from_float(22),Symbol.from_operator(operators["u-"]),Symbol.from_float(3),Symbol.from_operator(operators["+"])]

def create_symbol_list(input:str):
    symbol_list:list[Symbol] = []
    i=0
    while i < len(input):

        if input[i].isnumeric() or input[i] == ".":
            chars=[]
            while i < len(input) and (input[i].isnumeric() or input[i] == "."):
                chars.append(input[i])
                i+=1
            try:
                symbol_list.append(Symbol.from_float(float("".join(chars))))    
            except:
                print(f"Innalid number f: {"".join(chars)}")
                return
            continue

        if input[i] == "+":
            symbol_list.append(Symbol.from_operator(operators["+"]))
            i+=1
            continue

        if input[i] == "*":
            symbol_list.append(Symbol.from_operator(operators["*"]))
            i+=1
            continue

        if input[i] == "/":
            symbol_list.append(Symbol.from_operator(operators["/"]))
            i+=1
            continue

        if input[i] == "-":
            symbol_list.append(Symbol.from_operator(operators["-"]))
            i+=1
            continue

        if input[i] == "(":
            i+=1
            symbol_list.append(Symbol.open_parenthesis())

        if input[i] == "(":
            i+=1
            symbol_list.append(Symbol.closed_parenthesis())
        

        print(f"Unknown symbol: {input[i]}")
        return

    return symbol_list


def create_rpn_stack(symbol_stack):
    holding_stack:list[Symbol]=[]
    output:list[Symbol]=[]

    if not symbol_stack:
        return

    for symbol in symbol_stack:
        if symbol.type == SymbolType.NUMBER:
            output.append(symbol)
            continue

        if symbol.type == SymbolType.OPERATOR:
            if len(holding_stack) == 0:
                holding_stack.append(symbol)
                continue
            #last=holding_stack[-1][0]
            while len(holding_stack) and holding_stack[-1].represented.precedence >= symbol.represented.precedence:
                output.append(holding_stack.pop())
            holding_stack.append(symbol)
            continue

    while holding_stack:
        output.append(holding_stack.pop())
    
    return output


def compute(rpn_stack):
    solve_stack:list = []

    if not rpn_stack:
        return

    for symbol in rpn_stack:
        if symbol.type == SymbolType.NUMBER:
            solve_stack.append(symbol.represented)
            continue

        if symbol.type == SymbolType.OPEN_PARENTHESIS:
            solve_stack.append("(")
            continue

        if symbol.type == SymbolType.CLOSED_PARENTHESIS:
            while len(rpn_stack) > 0 and rpn_stack[len(rpn_stack)].type != SymbolType.OPEN_PARENTHESIS:
                solve_stack.append()

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

"5*54+5.4-5+.6"
out=compute(create_rpn_stack(create_symbol_list("5*54+(5.4/5)+.6")))
print(out)
