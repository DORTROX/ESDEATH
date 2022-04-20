def addition(query):
    add = 0
    x = query[7:]
    x = x.split('and ')
    for i in x:
        i = int(i)
        add += i
    return add

def subtract(query):
    sub = 0
    x = query[9:]
    x = x.split('and ')
    for i in x:
        i = int(i)
        sub -= i
    return sub

def divide(query):
    div = 0
    x = query[7:]
    x = x.split('and ')
    for i in x:
        i = int(i)
        div //= i
    return div

def multiply(query):
    mul = 0
    x = query[9:]
    x = x.split('and ')
    for i in x:
        i = int(i)
        mul //= i
    return mul