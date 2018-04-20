# -*- coding: utf-8 -*-

# Copyright (c) 2014-2015 Vincent Foley-Bourgon

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import sys
from lexical_analyzer import lex
from parser import parse
from build_symbol_table import build_symtab
from typecheck import typecheck
from codegen import codegen


def main():
    src = sys.stdin.read()
    toks = lex(src)  # source -> tokens
    ast = parse(toks)  # tokens -> AST
    symtab = build_symtab(ast)  # AST -> symbol table
    typed_ast = typecheck(ast, symtab)  # AST * symbol table -> Typed AST
    codegen(typed_ast, symtab)  # Typed AST * symbol table -> C code


if __name__ == "__main__":
    main()
