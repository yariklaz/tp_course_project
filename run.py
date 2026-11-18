import sys
from pathlib import Path
from sipl.parser import parse_source
from sipl.interpreter.evaluator import run_program

def main():
    example_path = Path('examples/example1.sipl')
    with open(example_path, 'r', encoding='utf-8') as f:
        code = f.read()
    
    print("Парсинг програми...")
    ast = parse_source(code)
    
    initial_state = {'X': 5, 'Y': 2}
    print(f"Початковий стан: {initial_state}")
    
    print("\nВиконання...")
    try:
        final_state = run_program(ast, initial_state)
        print(f"Фінальний стан:  {final_state}")
    except Exception as e:
        print(f"Помилка виконання: {e}")

if __name__ == '__main__':
    main()