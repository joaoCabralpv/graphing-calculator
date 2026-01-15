from collections.abc import Callable
from enum import Enum
from math import floor

class SymbolType(Enum):
    NONE=0
    NUMBER=1
    BINARY_OPERATOR=2
    OPEN_PARENTHESIS=4
    CLOSED_PARENTHESIS=5
    VARIABLE=6

class ParenthesisType(Enum):
    OPEN=0
    CLOSED=1

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

class Parenthesis:
    type:ParenthesisType
    precedence:int
    
    def __init__(self,type:ParenthesisType):
        self.precedence=0
        self.type=type

    def __str__(self):
        
        if self.type==ParenthesisType.OPEN:
            return "("
        if self.type==ParenthesisType.CLOSED:
            return ")"
        return "Secret third parenthesis type(something is wrong)"
        

class Variable:
    value:None
    name:None
    def __init__(self,name:str):
        self.name=name
        self.value=None
    def set_value(self,value:float):
        self.value=value
    def __float__(self):
        return self.value
    def __str__(self):
        return self.name
    
class Symbol:
    represented = None
    type = SymbolType.NONE

    def __init__(self,s,type:SymbolType):
        self.represented = s
        self.type=type

    def from_operator(op:Operator):
        return Symbol(op,SymbolType.BINARY_OPERATOR)
    
    def from_float(f:float):
        return Symbol(f,SymbolType.NUMBER)
    
    def open_parenthesis():
        return Symbol(Parenthesis(ParenthesisType.OPEN),SymbolType.OPEN_PARENTHESIS)
    
    def closed_parenthesis():
        return Symbol(Parenthesis(ParenthesisType.CLOSED),SymbolType.CLOSED_PARENTHESIS)
    
    def variable(name:str):
        return Symbol(Variable(name),SymbolType.VARIABLE)
    
    def __str__(self):
        return str(self.represented)


        

operators:dict[str,Operator] = {
    "+": Operator(lambda a: a[0]+a[1],2,1,"+"),
    "-": Operator(lambda a: a[0]-a[1],2,1,"-"),
    "*": Operator(lambda a: a[0]*a[1],2,2,"*"),
    "/": Operator(lambda a: a[0]/a[1],2,2,"/"),
    "^": Operator(lambda a: a[0]**a[1],2,3,"^"),
    "u-":Operator(lambda a: -a[0],1,999,"u-")
}




#rpn_stack:list[Symbol] =[Symbol.from_float(22),Symbol.from_operator(operators["u-"]),Symbol.from_float(3),Symbol.from_operator(operators["+"])]

def create_symbol_list(input:str):
    symbol_list:list[Symbol] = []
    i=0
    last_type=SymbolType.NONE

    variable_dict={}

    while i < len(input):

        if input[i].isnumeric() or input[i] == ".":
            chars=[]
            while i < len(input) and (input[i].isnumeric() or input[i] == "."):
                chars.append(input[i])
                i+=1
                joined="".join(chars)
            try:
                symbol_list.append(Symbol.from_float(float(joined)))
            except:
                return (f"Invalid number {joined} ",{})
            last_type=SymbolType.NUMBER
            continue

        if input[i] == "+":
            symbol_list.append(Symbol.from_operator(operators["+"]))
            i+=1
            last_type=SymbolType.BINARY_OPERATOR
            continue

        if input[i] == "*":
            symbol_list.append(Symbol.from_operator(operators["*"]))
            i+=1
            last_type=SymbolType.BINARY_OPERATOR
            continue

        if input[i] == "/":
            symbol_list.append(Symbol.from_operator(operators["/"]))
            i+=1
            last_type=SymbolType.BINARY_OPERATOR
            continue

        if input[i] == "-":
            if last_type==SymbolType.NUMBER or last_type==SymbolType.CLOSED_PARENTHESIS:
                symbol_list.append(Symbol.from_operator(operators["-"]))
                last_type=SymbolType.BINARY_OPERATOR
            else:
                symbol_list.append(Symbol.from_operator(operators["u-"]))
            i+=1
            continue

        if input[i] == "^":
            symbol_list.append(Symbol.from_operator(operators["^"]))
            i+=1
            last_type=SymbolType.BINARY_OPERATOR
            continue

        if input[i] == "(":
            i+=1
            symbol_list.append(Symbol.open_parenthesis())
            last_type=SymbolType.OPEN_PARENTHESIS
            continue

        if input[i] == ")":
            i+=1
            symbol_list.append(Symbol.closed_parenthesis())
            last_type=SymbolType.CLOSED_PARENTHESIS
            continue

        if input[i].isalpha():
            if input[i] in variable_dict.keys():
                symbol_list.append(variable_dict[input[i]])
            else:
                var=Symbol.variable(input[i])
                variable_dict.update({input[i]:var})
                symbol_list.append(var)
            i+=1
            continue
        

        return(f" Unknown symbol: {input[i]}",{})

    return (symbol_list,variable_dict)


def create_rpn_stack(symbol_stack):
    if isinstance(symbol_stack,str):
        return symbol_stack
    holding_stack:list[Symbol]=[]
    output:list[Symbol]=[]

    if not symbol_stack:
        return (None,{})

    for symbol in symbol_stack:
        if symbol.type == SymbolType.NUMBER or symbol.type == SymbolType.VARIABLE:
            output.append(symbol)
            continue

        if symbol.type == SymbolType.BINARY_OPERATOR:
            if len(holding_stack) == 0:
                holding_stack.append(symbol)
                continue
            #last=holding_stack[-1][0]
            while len(holding_stack) and holding_stack[-1].represented.precedence >= symbol.represented.precedence:
                output.append(holding_stack.pop())
            holding_stack.append(symbol)
            continue

        if symbol.type==SymbolType.OPEN_PARENTHESIS:
            holding_stack.append(symbol)
        
        if symbol.type==SymbolType.CLOSED_PARENTHESIS:
            
            while True:
                if len(holding_stack)==0:
                    return(" Unmatched parenthesis",{})
                
                last=holding_stack.pop()
                if last.type==SymbolType.BINARY_OPERATOR:
                    output.append(last)

                if last.type==SymbolType.OPEN_PARENTHESIS:
                    break

    while holding_stack:
        output.append(holding_stack.pop())
    
    return output


def compute(rpn_stack):
    if isinstance(rpn_stack,str):
        return rpn_stack
    solve_stack:list = []

    if not rpn_stack:
        return "Empty expression"

    for symbol in rpn_stack:
        if symbol.type == SymbolType.NUMBER:
            solve_stack.append(symbol.represented)
            continue
    
        if symbol.type ==SymbolType.VARIABLE:
            value=symbol.represented.value
            solve_stack.append(value)

        if symbol.type == SymbolType.OPEN_PARENTHESIS:
            solve_stack.append("(")
            continue

        if symbol.type == SymbolType.CLOSED_PARENTHESIS:
            while len(rpn_stack) > 0 and rpn_stack[len(rpn_stack)].type != SymbolType.OPEN_PARENTHESIS:
                solve_stack.append()

        if symbol.type == SymbolType.BINARY_OPERATOR:
            operator = symbol.represented
            func = operator.func
            n_arguments = operator.n_arguments
            list_arguments = []

            for i in range(n_arguments):
                try:
                    list_arguments.append(solve_stack.pop())
                except:
                    return ("Operator with missing arguments")

            list_arguments.reverse()
            try:
                solve_stack.append(func(list_arguments))
            except:
                return " Math error"

    if len(solve_stack) != 1:
        return " Stack size is not 1 at the end"
    
    result=solve_stack[0]
    if floor(result) == result:
        result = int(result)
    return result

def solve(s):
    symbols,_ = create_symbol_list(s)
    return compute(create_rpn_stack(symbols))

def create_rpn_stack_for_function(string):
    symbols, variables = create_symbol_list(string)
    rpn_stack = create_rpn_stack(symbols)
    return (lambda: compute(rpn_stack), variables)

if __name__ == "__main__":
    func, variables = create_rpn_stack_for_function("2*x*x+2+4*x+3")
    variables["x"].represented.set_value(4)
    print(func())
    variables["x"].represented.set_value(5)
    print(func())
