from lex import lexico

#Estrutura dos nós das árvores:
class Node: pass

class ClassNode(Node):
    def __init__(self, name, parent, features):
        self.name = name
        self.parent = parent
        self.features = features # Métodos e Atributos

class MethodNode(Node):
    def __init__(self, name, formal_params, return_type, body):
        self.name = name
        self.params = formal_params
        self.return_type = return_type
        self.body = body # Uma expressão


#Parser para o analisador sintático
class CoolParser:
    def __init__(self, arquivo):
        self.arquivo = arquivo
        self.token_completo = None # Guarda a tupla (linha, tipo, valor)
        self.linha_atual = 1
        self.tipo_atual = None
        self.valor_atual = None
        
        self.proximo_token() # "Carrega o buffer" com o primeiro token

    def proximo_token(self):
        """Atualiza o estado do parser com o próximo token do léxico."""
        self.token_completo = lexico(self.arquivo)
        
        if self.token_completo:
            self.linha_atual, self.tipo_atual, self.valor_atual = self.token_completo
        else:
            self.tipo_atual = "EOF"
            self.valor_atual = None

    def erro(self, mensagem):
        raise Exception(f"Erro Sintático na linha {self.linha_atual}: {mensagem}. "
                        f"Encontrado: {self.tipo_atual} ('{self.valor_atual}')")

    def eat(self, tipo_esperado, valor_esperado=None):
        """
        Consome o token se o TIPO coincidir. 
        Se valor_esperado for passado, verifica o conteúdo também (útil para ';' ou 'class').
        """
        if self.tipo_atual == tipo_esperado:
            if valor_esperado and self.valor_atual != valor_esperado:
                self.erro(f"Esperava valor '{valor_esperado}'")
            
            # Se deu tudo certo, avança para o próximo
            self.proximo_token()
        else:
            self.erro(f"Esperava tipo {tipo_esperado}")

    # --- Regras da Gramática (Exemplos) ---

    def parse_program(self):
        """Regra: program ::= [class;]+"""
        classes = []
        while self.tipo_atual != "EOF":
            classes.append(self.parse_class())
        print("Análise sintática concluída com sucesso!")
        return classes

    def parse_class(self):
        """Regra: class TYPE [inherits TYPE] { [feature;]* } ;"""
        # Verifica se o valor é 'class' (case-insensitive como manda o manual de COOL)
        if self.valor_atual.lower() != "class":
            self.erro("Declaração de classe deve começar com 'class'")
        
        self.eat("RESERVADA") # Consome 'class'
        
        nome_classe = self.valor_atual
        self.eat("IDENTIFICADOR")
        
        pai = "Object"
        if self.tipo_atual == "RESERVADA" and self.valor_atual.lower() == "inherits":
            self.eat("RESERVADA")
            pai = self.valor_atual
            self.eat("IDENTIFICADOR")
            
        self.eat("SIMBOLO", "{")
        # Aqui viria o loop de parse_features()
        self.eat("SIMBOLO", "}")
        self.eat("SIMBOLO", ";")
        
        return f"Classe {nome_classe} (pai: {pai}) processada."

 #Para rodar:
def main():
    with open("teste.txt", "r") as arq:
        parser = CoolParser(arq)
        parser.parse_program()