from error import error


def build_symtab(ast):
    """
    Input : the AST of a mini program
    Output: a dictionary mapping variable names to types

    This procedure iterates over the declarations and adds them to a
    symbol table (here, a dictionary that maps variable names to their
    declared type).  If a variable is declared more than once, we
    report an error.
    """
    symtab = {}
    for decl in ast["decls"]:
        if decl["id"] in symtab:
            error("%s is already declared" % decl["id"])
        else:
            symtab[decl["id"]] = decl["type"]
    return symtab
