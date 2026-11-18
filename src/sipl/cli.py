import argparse
import json
from pathlib import Path
from pprint import pprint

from sipl.parser import parse_source
from sipl.interpreter.evaluator import SIPLInterpreter

def main():
    parser = argparse.ArgumentParser(description="SIPL Language Toolkit CLI")
    parser.add_argument("command", choices=["parse", "run", "trace"], help="Команда: parse (тільки AST), run (виконати), trace (покроковий звіт)")
    parser.add_argument("file", help="Шлях до файлу .sipl")
    parser.add_argument("--state", default="{}", help="Початковий стан у форматі JSON, наприклад: '{\"X\": 5, \"Y\": 2}'")

    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"Помилка: Файл {args.file} не знайдено!")
        return

    with open(path, 'r', encoding='utf-8') as f:
        code = f.read()

    try:
        ast = parse_source(code)
    except Exception as e:
        print(f"Помилка синтаксису: {e}")
        return

    if args.command == "parse":
        print("=== AST успішно побудовано ===")
        pprint(ast)
        return

    try:
        initial_state = json.loads(args.state)
    except json.JSONDecodeError:
        print("Помилка: Неправильний формат початкового стану (--state). Має бути валідний JSON.")
        return

    interpreter = SIPLInterpreter(initial_state)
    try:
        interpreter.evaluate(ast)
    except Exception as e:
        print(f"Помилка виконання: {e}")
        return

    if args.command == "run":
        print(f"Фінальний стан: {interpreter.state}")
        
    elif args.command == "trace":
        print(f"{'Рядок':<7} | {'Подія':<15} | {'Деталі':<22} | Стан")
        print("-" * 75)
        for event in interpreter.trace:
            line_str = f"Line {event['line']}"
            print(f"{line_str:<7} | {event['type']:<15} | {event['details']:<22} | {event['state']}")

if __name__ == "__main__":
    main()