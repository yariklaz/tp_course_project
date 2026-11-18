# src/sipl/interpreter/evaluator.py
from sipl.sipl_ast import *

class SIPLInterpreter:
    def __init__(self, initial_state=None):
        self.state = initial_state.copy() if initial_state is not None else {}
        self.step_limit = 10000 
        self.trace = []  

    def log_event(self, event_type: str, node: ASTNode, details: str = ""):
        """Записує крок виконання для подальшого дебагу"""
        if getattr(node, 'line', None) is not None:
            self.trace.append({
                "line": node.line,
                "type": event_type,
                "details": details,
                "state": self.state.copy()  
            })

    def evaluate(self, node: ASTNode):
        if isinstance(node, Program):
            self.log_event("start", node, "Початок програми")
            self.evaluate(node.body)
            self.log_event("end", node, "Завершення програми")
            
        elif isinstance(node, Block):
            for stm in node.statements:
                self.evaluate(stm)
                
        elif isinstance(node, Assign):
            self.log_event("before_stm", node, f"Присвоєння {node.var}")
            value = self.evaluate(node.expr)
            self.state[node.var] = value
            self.log_event("after_stm", node, f"{node.var} = {value}")
            
        elif isinstance(node, IfElse):
            self.log_event("before_stm", node, "Перевірка умови If")
            cond = self.evaluate(node.condition)
            self.log_event("cond_eval", node.condition, f"Умова If: {cond}")
            if cond:
                self.evaluate(node.then_branch)
            else:
                self.evaluate(node.else_branch)
                
        elif isinstance(node, WhileDo):
            self.log_event("before_stm", node, "Початок циклу While")
            steps = 0
            while True:
                cond = self.evaluate(node.condition)
                self.log_event("cond_eval", node.condition, f"Умова While: {cond}")
                if not cond:
                    break
                self.evaluate(node.body)
                steps += 1
                if steps > self.step_limit:
                    raise RuntimeError("Перевищено ліміт кроків (нескінченний цикл)")
                    
        elif isinstance(node, Skip):
            self.log_event("statement", node, "Skip")
        
        elif isinstance(node, BinOp):
            left = self.evaluate(node.left)
            right = self.evaluate(node.right)
            if node.op == 'add': return left + right
            elif node.op == 'sub': return left - right
            elif node.op == 'mult': return left * right
            elif node.op == 'gr': return left > right
            elif node.op == 'eq': return left == right
            elif node.op == 'or': return left or right
            
        elif isinstance(node, UnaryOp):
            if node.op == 'neg': return not self.evaluate(node.expr)
        elif isinstance(node, Number):
            return node.value
        elif isinstance(node, Variable):
            if node.name not in self.state:
                raise ValueError(f"Змінна '{node.name}' не ініціалізована!")
            return self.state[node.name]

        return self.state

def run_program(ast: Program, initial_state: dict = None):
    interpreter = SIPLInterpreter(initial_state)
    interpreter.evaluate(ast)
    return interpreter.state, interpreter.trace