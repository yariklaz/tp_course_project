from dataclasses import dataclass
from typing import List

@dataclass
class ASTNode:
    line: int
    column: int

@dataclass
class Number(ASTNode):
    value: int

@dataclass
class Variable(ASTNode):
    name: str

@dataclass
class BinOp(ASTNode):
    left: ASTNode
    op: str
    right: ASTNode

@dataclass
class UnaryOp(ASTNode):
    op: str
    expr: ASTNode

@dataclass
class Statement(ASTNode):
    pass

@dataclass
class Assign(Statement):
    var: str
    expr: ASTNode

@dataclass
class IfElse(Statement):
    condition: ASTNode
    then_branch: Statement
    else_branch: Statement

@dataclass
class WhileDo(Statement):
    condition: ASTNode
    body: Statement

@dataclass
class Block(Statement):
    statements: List[Statement]

@dataclass
class Skip(Statement):
    pass

@dataclass
class Program(ASTNode):
    body: Block