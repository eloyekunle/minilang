from AST_NODES import *
from error import error


def typecheck(ast, symtab):
    """
    Input : the AST of a mini program and its associated symbol table
    Output: an AST of the mini program, but with extra type
    information added inside expression nodes

    The typing rules of our small language are pretty simple:

    - We have two types, int and float
    - An int literal has type int
    - A float literal has type float
    - There is no automatic conversion from int to float (in fact, the
      language does not support conversions)
    - The two operands of an arithmetic operations must be of the same type
    - An expression can be assigned to a variable only if their types are equal
    """

    def check_stmt(stmt):
        if stmt["nodetype"] == AST_PRINT:
            typed_expr = check_expr(stmt["expr"])
            return astnode(AST_PRINT, expr=typed_expr)
        elif stmt["nodetype"] == AST_RETURN:
            typed_expr = check_expr(stmt["expr"])
            return astnode(AST_RETURN, expr=typed_expr)
        elif stmt["nodetype"] == AST_READ:
            return astnode(AST_READ, id=stmt["id"])
        elif stmt["nodetype"] == AST_ASSIGN:
            typed_rhs = check_expr(stmt["rhs"])
            if typed_rhs["type"] == symtab[stmt["lhs"]]:
                return astnode(AST_ASSIGN, lhs=stmt["lhs"], rhs=typed_rhs)
            else:
                error("expected %s, got %s" % (symtab[stmt["lhs"]], typed_rhs["type"]))
        elif stmt["nodetype"] == AST_WHILE:
            typed_expr = check_expr(stmt["expr"])
            if typed_expr["type"] != "int":
                error("loop condition must be an int")
            typed_body = [check_stmt(body_stmt) for body_stmt in stmt["body"]]
            return astnode(AST_WHILE, expr=typed_expr, body=typed_body)

    def check_expr(expr):
        if expr["nodetype"] == AST_INT:
            return astnode(AST_INT, value=expr["value"], type="int")
        elif expr["nodetype"] == AST_FLOAT:
            return astnode(AST_FLOAT, value=expr["value"], type="float")
        elif expr["nodetype"] == AST_ID:
            if expr["name"] not in symtab:
                error("undeclared variable: %s" % expr["name"])
            return astnode(AST_ID, name=expr["name"], type=symtab[expr["name"]])
        elif expr["nodetype"] == AST_BINOP:
            typed_e1 = check_expr(expr["lhs"])
            typed_e2 = check_expr(expr["rhs"])
            if typed_e1["type"] == typed_e2["type"]:
                return astnode(AST_BINOP, op=expr["op"], lhs=typed_e1, rhs=typed_e2, type=typed_e1["type"])
            else:
                error("operands must have the same type")

    updated_stmts = []
    for stmt in ast["stmts"]:
        updated_stmts.append(check_stmt(stmt))
    return {"decls": ast["decls"], "stmts": updated_stmts}
