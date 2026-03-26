p_reservadas = ["class", "else", "false", "fi", "if", "in", "inherits", "isvoid", "let", "loop", "pool", 
                "then", "while", "case", "esac", "new", "of", "not", "true"]

simbolos = [";", ")", "*", "+", "-"]

lst_read = None

def pega_char(arq):
    global lst_read
    if lst_read:
        res = lst_read
        lst_read = None
        return res
    return arq.read(1)

def lexico(arq):
    global lst_read
    palavra = "" 

    if lst_read in simbolos:
        palavra += lst_read
        return palavra
    
    while True:
        c = pega_char(arq)
        if not c:
            return palavra if palavra else None
            
        if c.isalpha():
            palavra += c

        elif c in simbolos:
            if palavra:
                lst_read = c
                return palavra
            return c
        
        if c.isspace():
            if palavra:
                return palavra
            continue
        
        elif c == "(":
            proximo = pega_char(arq)
            if c == "*":
                while True:
                    char_com = arq.read(1)
                    if not char_com: break
                    if char_com == "*":
                        if arq.read(1) == ")": break
                    if palavra: return palavra
                    continue
            else:
                lst_read = proximo
                if palavra:
                    lst_read = "("
                    return palavra
                return "("



def main():
    with open("teste.txt", "r") as arquivo:

        p1 = lexico(arquivo)
        print(f"Token 1: {p1}")
        
        p2 = lexico(arquivo)
        print(f"Token 2: {p2}")
main()
