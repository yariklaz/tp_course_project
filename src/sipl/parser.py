import os
from pathlib import Path
from lark import Lark, Transformer, v_args
from sipl.sipl_ast import *
from pprint import pprint  

GRAMMAR_PATH = Path(__file__).parent.parent.parent / 'grammar' / 'sipl.lark'

with open(GRAMMAR_PATH, 'r', encoding='utf-8') as f:
    sipl_grammar = f.read()

sipl_parser = Lark(sipl_grammar, start='prog', parser='lalr', propagate_positions=True)

@v_args(inline=True, meta=True)
class SIPLTransformer(Transformer):
    def prog(self, meta, stms):
        return Program(meta.line, meta.column, body=stms)
    
    def block(self, meta, *stms):
        return Block(meta.line, meta.column, statements=list(stms))
        
    def block_stm(self, meta, stms):
        return stms
    
    def assign(self, meta, var, expr):
        var_name = str(var.children[0])
        return Assign(meta.line, meta.column, var=var_name, expr=expr)
    
    def if_else(self, meta, condition, then_branch, else_branch):
        return IfElse(meta.line, meta.column, condition=condition, then_branch=then_branch, else_branch=else_branch)
    
    def while_do(self, meta, condition, body):
        return WhileDo(meta.line, meta.column, condition=condition, body=body)
    
    def skip(self, meta):
        return Skip(meta.line, meta.column)
        
    def add(self, meta, left, right): return BinOp(meta.line, meta.column, left, 'add', right)
    def sub(self, meta, left, right): return BinOp(meta.line, meta.column, left, 'sub', right)
    def mul(self, meta, left, right): return BinOp(meta.line, meta.column, left, 'mult', right)
    def greater(self, meta, left, right): return BinOp(meta.line, meta.column, left, 'gr', right)
    def equal(self, meta, left, right): return BinOp(meta.line, meta.column, left, 'eq', right)
    def or_op(self, meta, left, right): return BinOp(meta.line, meta.column, left, 'or', right)
    def not_op(self, meta, expr): return UnaryOp(meta.line, meta.column, 'neg', expr)
    
    def number(self, meta, n):
        return Number(meta.line, meta.column, value=int(n))
        
    def variable(self, meta, var):
        var_name = str(var.children[0])
        return Variable(meta.line, meta.column, name=var_name)
        
    def parens(self, meta, expr): return expr
    def bparens(self, meta, expr): return expr

def parse_source(source_code: str) -> Program:
    """Парсить текст коду і повертає AST."""
    tree = sipl_parser.parse(source_code)
    return SIPLTransformer().transform(tree)

if __name__ == '__main__':
    example_path = Path(__file__).parent.parent.parent / 'examples' / 'example1.sipl'
    
    if example_path.exists():
        with open(example_path, 'r', encoding='utf-8') as f:
            code = f.read()
            
        print("Текст програми")
        print(code)
        
        try:
            ast = parse_source(code)
            print("\nПобудоване AST")
            pprint(ast) 
        except Exception as e:
            print("Помилка синтаксису:", e)
    else:
        print(f"Не знайдено файл {example_path}")