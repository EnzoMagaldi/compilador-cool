p_reservadas = ["class", "else", "false", "fi", "if", "in", "inherits", "isvoid", "let", "loop", "pool", 
                "then", "while", "case", "esac", "new", "of", "not", "true"]

lst_read = None

coments = [False,False]


def lexico(arq):
    global lst_read
    global coments
    palavra = "" 

    if lst_read == ";":
        palavra += lst_read
        return palavra
    
    while True:
        c = arq.read(1)
        lst_read = c
        if not c:
            return palavra if palavra else None
            
        if c.isalpha():
            palavra += c
        
        elif c.isspace():
            if palavra:
                lst_read = None
                return palavra
            continue

        elif c == ";":
            if palavra:
                return palavra
            return ";"
        
        elif c == "-":
            c = arq.read(1)
            i = 0
            if c == "-":
                while True:



def main():
    with open("teste.txt", "r") as arquivo:
        # Primeira chamada
        p1 = lexico(arquivo)
        print(f"Token 1: {p1}")
        
        # Segunda chamada (continua de onde parou!)
        p2 = lexico(arquivo)
        print(f"Token 2: {p2}")
main()