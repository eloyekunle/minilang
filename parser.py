from AST_NODES import *
from TOKEN_TYPES import *
from error import error


def parse(toks):
    """
    Input : a list of tokens
    Output: a list of statement nodes

    parse(toks) is a predictive, recursive-descent parser that will
    return a list of AST nodes (declarations and statements) from the
    token stream computer by lex() above.  We parse the tokens
    according to the following grammar.  Every non-terminal (left-hand
    side of a ::=) has its own local function definition.

        program  ::=  decls stmts
        decls    ::=  decl decls
                   |  ε
        decl     ::=  'var' ident ':' type ';'
        stmts    ::=  stmt stmts
                   |  ε
        stmt     ::=  ident '=' expr ';'
                   |  'read' ident ';'
                   |  'print' expr ';'
                   |  'while' expr 'do' stmts 'done'
        expr     ::=  term { '+' expr }
                   |  term { '-' expr }
                   |  term
        term     ::=  factor { '*' term }
                   |  factor { '-' term }
                   |  factor
        factor   ::=  '(' expr ')'
                   |  ident
                   |  int
                   |  float

    The AST nodes are represented with dicts as follows:
    - Declarations
        - var id: type         : { "nodetype": AST_DECL, "id": id, "type": type }

    - Statements
        - id = expr            : { "nodetype": AST_ASSIGN, "lhs": id, "rhs": expr }
        - print expr           : { "nodetype": AST_PRINT, "expr": expr }
        - read id              : { "nodetype": AST_READ, "id": id }
        - while e do stmts done: { "nodetype": AST_WHILE, "expr": e, "body": stmts }

    - Expressions
        - int                  : { "nodetype": AST_INT, "value": int }
        - float                : { "nodetype": AST_FLOAT, "value": float }
        - id                   : { "nodetype": AST_ID, "name": id }
        - e1 + e2              : { "nodetype": AST_BINOP, op: "+", "lhs": e1, "rhs": e2 }

    For example, here is a simple statement and its AST representation:

        x = 3 + y

        {
          "nodetype": AST_ASSIGN,
          "lhs": "x",
          "rhs": {
            "nodetype": AST_BINOP,
            "op": "+",
            "lhs": { "nodetype": AST_INT, "value": 3 },
            "rhs": { "nodetype": AST_ID, "name": "y" }
          }
        }
    """

    def consume(tok_type):
        if tok_type == toks[0]["toktype"]:
            t = toks.pop(0)
            return t
        else:
            error("expected %d, found %d" % (tok_type, toks[0]["toktype"]))

    def peek():
        if toks:
            return toks[0]["toktype"]
        else:
            return None

    def program():
        ds = decls()
        sts = stmts()
        return {
            "decls": ds,
            "stmts": sts,
        }

    def decls():
        decls = []
        while peek() == TOK_VAR:
            decls.append(decl())
        return decls

    def decl():
        if peek() == TOK_VAR:
            consume(TOK_VAR)
            id = consume(TOK_ID)
            consume(TOK_COLON)
            ty = consume(TOK_TYPE)
            consume(TOK_SEMI)
            return astnode(AST_DECL, id=id["value"], type=ty["value"])
        else:
            error("not a valid declaration")

    def stmts():
        stmts = []
        while peek() in (TOK_PRINT, TOK_RETURN, TOK_READ, TOK_ID, TOK_WHILE):
            stmts.append(stmt())
        return stmts

    def stmt():
        next_tok = peek()
        if next_tok == TOK_ID:
            id = consume(TOK_ID)
            consume(TOK_EQ)
            e = expr()
            consume(TOK_SEMI)
            return astnode(AST_ASSIGN, lhs=id["value"], rhs=e)
        elif next_tok == TOK_PRINT:
            consume(TOK_PRINT)
            e = expr()
            consume(TOK_SEMI)
            return astnode(AST_PRINT, expr=e)
        elif next_tok == TOK_RETURN:
            consume(TOK_RETURN)
            e = expr()
            consume(TOK_SEMI)
            return astnode(AST_RETURN, expr=e)
        elif next_tok == TOK_READ:
            consume(TOK_READ)
            id = consume(TOK_ID)
            consume(TOK_SEMI)
            return astnode(AST_READ, id=id)
        elif next_tok == TOK_WHILE:
            consume(TOK_WHILE)
            e = expr()
            consume(TOK_DO)
            body = stmts()
            consume(TOK_DONE)
            return astnode(AST_WHILE, expr=e, body=body)
        else:
            error("illegal statement")

    def expr():
        t = term()
        next_tok = peek()
        while next_tok in (TOK_PLUS, TOK_MINUS):
            if next_tok == TOK_PLUS:
                consume(TOK_PLUS)
                t2 = term()
                t = astnode(AST_BINOP, op="+", lhs=t, rhs=t2)
            elif next_tok == TOK_MINUS:
                consume(TOK_MINUS)
                t2 = term()
                t = astnode(AST_BINOP, op="-", lhs=t, rhs=t2)
            next_tok = peek()
        return t

    def term():
        f = factor()
        next_tok = peek()
        while next_tok in (TOK_STAR, TOK_SLASH, TOK_GTHAN, TOK_LTHAN):
            if next_tok == TOK_STAR:
                consume(TOK_STAR)
                f2 = factor()
                f = astnode(AST_BINOP, op="*", lhs=f, rhs=f2)
            elif next_tok == TOK_SLASH:
                consume(TOK_SLASH)
                f2 = factor()
                f = astnode(AST_BINOP, op="/", lhs=f, rhs=f2)
            elif next_tok == TOK_GTHAN:
                consume(TOK_GTHAN)
                f2 = factor()
                f = astnode(AST_BINOP, op=">", lhs=f, rhs=f2)
            elif next_tok == TOK_LTHAN:
                consume(TOK_LTHAN)
                f2 = factor()
                f = astnode(AST_BINOP, op="<", lhs=f, rhs=f2)
            next_tok = peek()
        return f

    def factor():
        next_tok = peek()
        if next_tok == TOK_LPAREN:
            consume(TOK_LPAREN)
            e = expr()
            consume(TOK_RPAREN)
            return e
        elif next_tok == TOK_INT:
            tok = consume(TOK_INT)
            return astnode(AST_INT, value=tok["value"])
        elif next_tok == TOK_FLOAT:
            tok = consume(TOK_FLOAT)
            return astnode(AST_FLOAT, value=tok["value"])
        elif next_tok == TOK_ID:
            tok = consume(TOK_ID)
            return astnode(AST_ID, name=tok["value"])
        else:
            error("illegal token %d" % next_tok)

    return program()
