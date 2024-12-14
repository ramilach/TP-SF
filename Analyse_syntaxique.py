from ply import yacc
from lexer import tokens

def p_diagram(p):
    """diagram : STARTUML elements ENDUML"""
    p[0] = {"type": "diagram", "elements": p[2]}

def p_elements(p):
    """elements : elements element
                | element"""
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_element(p):
    """element : actor
               | usecase
               | relation
               | package"""
    p[0] = p[1]

def p_actor(p):
    """actor : ACTOR ACTOR_TXT
             | ACTOR ACTOR_TXT AS ID
             | ACTOR ACTOR_TXT STEREO"""
    if len(p) == 3:
        p[0] = {"type": "actor", "name": p[2]}
    elif len(p) == 5:
        p[0] = {"type": "actor", "name": p[2], "alias": p[4]}
    elif len(p) == 4:
        p[0] = {"type": "actor", "name": p[2], "stereotype": p[3]}

def p_usecase(p):
    """usecase : USECASE USE_CASE_TXT
               | USECASE USE_CASE_TXT AS ID"""
    if len(p) == 3:
        p[0] = {"type": "usecase", "name": p[2]}
    elif len(p) == 5:
        p[0] = {"type": "usecase", "name": p[2], "alias": p[4]}

def p_relation(p):
    """relation : ACTOR_TXT RIGHT_ARROW_1 USE_CASE_TXT
                | ACTOR_TXT RIGHT_ARROW_2 USE_CASE_TXT
                | USE_CASE_TXT INHERIT USE_CASE_TXT
                | USE_CASE_TXT INCLUDES USE_CASE_TXT
                | USE_CASE_TXT EXTENDS USE_CASE_TXT"""
    if p[2] in {"-+>", ".>"}:
        p[0] = {"type": "relation", "from": p[1], "to": p[3], "arrow": p[2]}
    elif p[2] in {"includes", "extends"}:
        p[0] = {"type": "relation", "from": p[1], "to": p[3], "type": p[2]}
    elif p[2] == "<|--":
        p[0] = {"type": "inheritance", "from": p[3], "to": p[1]}

def p_package(p):
    """package : PACKAGE ID LBRACE elements RBRACE"""
    p[0] = {"type": "package", "name": p[2], "elements": p[4]}

def p_error(p):
    if p:
        print(f"Erreur syntaxique près de '{p.value}' à la ligne {p.lineno}")
    else:
        print("Erreur syntaxique : Fin inattendue du fichier")

parser = yacc.yacc()

if __name__ == "__main__":
    with open("usecase.plantuml") as f:
        data = f.read()
    result = parser.parse(data)
    print(result)
