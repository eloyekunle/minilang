AST_DECL = 0
AST_ASSIGN = 1
AST_PRINT = 2
AST_INT = 3
AST_FLOAT = 4
AST_ID = 5
AST_BINOP = 6
AST_WHILE = 7
AST_READ = 8


def astnode(nodetype, **args):
    return dict(nodetype=nodetype, **args)
