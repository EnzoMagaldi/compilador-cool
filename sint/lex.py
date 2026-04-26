p_reservadas = ["class", "else", "false", "fi", "if", "in", "inherits", "isvoid", "let", "loop", "pool", 
                "then", "while", "case", "esac", "new", "of", "not", "true"]

operador = ["+", "-", "*", "/", "=", "<"]

tipos = {
    "RESERVADA": "RESERVADA",
    "INTEIRO": "INTEIRO",
    "STRING": "STRING",
    "IDENTIFICADOR": "IDENTIFICADOR",
    "SIMBOLO" : "SIMBOLO",
    "OPERADOR": "OPERADOR",
}

identificador = []

lst_read = None
dentro_string = False
linha = 1

def pega_char(arq):
    global lst_read
    if lst_read:
        res = lst_read
        lst_read = None
        return res
    return arq.read(1)

def lexico(arq):
    global lst_read, dentro_string, identificador, linha
    palavra = "" 
    
    while True:
        c = pega_char(arq)
        if not c:
            return palavra if palavra else None

        if c == "\n":
            linha += 1

        if c == '"':
            if palavra:
                lst_read = '"'
                return (linha, tipos["IDENTIFICADOR"], palavra)
            # Consome tudo até o próximo '"' e retorna como STRING
            conteudo = ""
            while True:
                ch = arq.read(1)
                if not ch or ch == '"':
                    break
                if ch == '\n':
                    linha += 1
                conteudo += ch
            return (linha, tipos["STRING"], conteudo)
        
        if dentro_string:
            proximo = arq.read(1)
            if proximo == '"':
                palavra += c
                if proximo:
                    arq.seek(arq.tell() - 1)
                return (linha, tipos["STRING"], palavra)
            else:
                if proximo:
                    arq.seek(arq.tell() - 1)
                palavra += c
                continue
            
        if c.isalpha() or c.isdigit() or c == "_" or c == ".":
            palavra += c
            continue
        
        if c.isspace():
            if palavra.lower() in p_reservadas:
                return (linha, tipos["RESERVADA"],palavra)
            if palavra.isdigit():
                return (linha, tipos["INTEIRO"], palavra)
            elif palavra:
                if palavra not in identificador:
                    identificador.append(palavra)
                return (linha, tipos["IDENTIFICADOR"], palavra)
            continue
        
        if c == "(":
            proximo = pega_char(arq)
            if proximo == "*":
                while True:
                    char_com = arq.read(1)
                    if not char_com: break
                    if char_com == "*":
                        if arq.read(1) == ")": break
                    if palavra: return palavra
                    else: continue
            else:
                if palavra: #Caso não seja comentário
                    lst_read = "(" 
                    if proximo:
                        arq.seek(arq.tell() - 1) 
                    return (linha, tipos["IDENTIFICADOR"], palavra)
                if proximo:
                    arq.seek(arq.tell() - 1)
                return (linha, tipos["SIMBOLO"], "(")
        

        if c == "-":
            proximo = pega_char(arq)
            if proximo == "-":
                while True:
                    char_com = arq.read(1)
                    if not char_com: break
                    if char_com == "\n": break
                    if palavra: return palavra
                    else: continue
                    
        if c == "<":
            if palavra:
                lst_read = "<"
                return palavra
            proximo = pega_char(arq)
            if proximo == "-" : return (linha, tipos["SIMBOLO"] ,"<-")
            else:
                lst_read = proximo
                return (linha, tipos["OPERADOR"], c)
            
        if c == "=":
            if palavra:
                lst_read = "="
                return palavra
            proximo = pega_char(arq)
            if proximo == ">" : return (linha, tipos["SIMBOLO"] ,"=>")
            else:
                lst_read = proximo
                return (linha, tipos["OPERADOR"], c)

        if c in operador:
            return (linha, tipos["OPERADOR"], c)

        #Retorna um simbolo caso não seja uma palavra ou um caractere que requer atenção 
        return (linha, tipos["SIMBOLO"], c)


'''        
def main():
    with open("teste.txt", "r") as arquivo:

        p = lexico(arquivo)
        while(p):
            print(p)
            p = lexico(arquivo)
        
main()
'''