operators = {
    "+": lambda a, b : a + b ,
    "*": lambda a, b : a * b ,
    "-": lambda a, b : a - b ,
    "/": lambda a, b : a / b
}

input:list =[float(input("n1: ")),float(input("n2: ")),input("op: ")]

print(operators[input[2]](input[0],input[1]))