from AST_NODES import *
from error import error


curr_tmp = 0


def tac_gen(ast, symtab):
    """
    Input : the AST and symbol table of a mini program
    Output: an equivalent TAC program
    """

    def new_temp():
        """Return a new, unique temporary variable name."""
        global curr_tmp
        curr_tmp += 1
        return "t" + str(curr_tmp)

    def gen_stmt(stmt):
        if stmt["nodetype"] == AST_ASSIGN:
            if stmt["lhs"] not in symtab:
                error("undeclared variable: %s" % stmt["lhs"])
            expr_loc = gen_expr(stmt["rhs"])
            print("%s = %s;" % (stmt["lhs"], expr_loc))
        elif stmt["nodetype"] == AST_PRINT:
            expr_loc = gen_expr(stmt["expr"])
            if stmt["expr"]["type"] == "int":
                flag = "d"
            else:
                flag = "f"
            print('printf("%%%s\\n", %s);' % (flag, expr_loc))
        elif stmt["nodetype"] == AST_RETURN:
            expr_loc = gen_expr(stmt["expr"])
            print('\nreturn %s;' % expr_loc)
        elif stmt["nodetype"] == AST_READ:
            id = stmt["id"]["value"]
            if symtab[id] == "int":
                flag = "d"
            else:
                flag = "f"
            print('scanf("%%%s", &%s);' % (flag, id))
        elif stmt["nodetype"] == AST_WHILE:
            expr_loc = gen_expr(stmt["expr"])
            print("\nwhile (%s) { " % expr_loc)
            for body_stmt in stmt["body"]:
                gen_stmt(body_stmt)
            gen_expr(stmt["expr"], expr_loc)
            print("}")

    def gen_expr(expr, loc_name=None):
        if expr["nodetype"] in (AST_INT, AST_FLOAT):
            loc = loc_name or new_temp()
            print("%s = %s;" % (loc, expr["value"]))
            return loc
        elif expr["nodetype"] == AST_ID:
            return expr["name"]
        elif expr["nodetype"] == AST_BINOP:
            lhs_loc = gen_expr(expr["lhs"])
            rhs_loc = gen_expr(expr["rhs"])
            loc = new_temp()
            print("%s = %s %s %s;" % (loc, lhs_loc, expr["op"], rhs_loc))
            return loc

    # Add the C statements to the main function.
    for stmt in ast["stmts"]:
        gen_stmt(stmt)
