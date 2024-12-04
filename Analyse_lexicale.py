import ply.lex as lex


tokens = [
    'STARTUML',     
    'ENDUML',       
    'IDENTIFIER',   
    'ACTOR',        
    'USECASE',      
    'PACKAGE',      
    'COLON',        
    'LPAREN',       
    'RPAREN',       
    'AS',           
    'STEREOTYPE',   
    'INCLUDES',     
    'EXTENDS',      
    'ARROW',        
    'INHERITANCE',  
    'DOT',          
    'STRING',       
]


t_STARTUML = r'@startuml'
t_ENDUML = r'@enduml'
t_ACTOR = r'actor'
t_USECASE = r'usecase'
t_PACKAGE = r'package'
t_AS = r'as'
t_COLON = r':'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_STEREOTYPE = r'<<.*?>>'
t_ARROW = r'-->|\.>'
t_INHERITANCE = r'<\|--'
t_INCLUDES = r':\s*includes'
t_EXTENDS = r':\s*extends'
t_DOT = r'\.'

# Identifier les chaînes et les identifiants
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_STRING(t):
    r'\".*?\"'
    return t


t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f"Caractère non reconnu : {t.value[0]} à la ligne {t.lexer.lineno}")
    t.lexer.skip(1)


lexer = lex.lex()

# Test du lexer
if __name__ == "__main__":
    data = '''
    @startuml System
    actor :User:
    usecase (Define travel) as DT
    :User: --> (Define travel)
    @enduml
    '''
    lexer.input(data)
    for tok in lexer:
        print(tok)
