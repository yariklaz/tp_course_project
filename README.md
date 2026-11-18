# SIPL Toolkit (SImple Programming Language)

Інструментарій для мови програмування **SIPL**, розроблений у межах курсового проєкту з дисципліни **«Теорія програмування»**. Проєкт включає формальну граматику, парсер, інтерпретатор, систему трасування, розширення для VS Code із повноцінним дебагером (DAP), а також набір тестів і CI/CD конвеєр.

---

## Вибрані завдання

| ID | Завдання | 
| :--- | :--- | 
| **CORE-01** | Формальна специфікація SIPL (Lark граматика, 10+ позитивних і 10+ негативних тестів) | 
| **CORE-02** | Парсер та типізоване AST з позиціями у вихідному тексті | 
| **CORE-03** | Інтерпретатор SIPL (стан, присвоєння, умови, цикли, begin/end, skip) |
| **CORE-04** | Подієва модель виконання та trace (Before/AfterStatement, зміна змінних) |
| **CORE-05** | CLI: parse, run, trace; структурований режим | 
| **IDE-03** | Debug Adapter Protocol (breakpoints, continue, step, variables) |
| **REL-01** | CI: перевірка коду та генерація тестів через GitHub Actions |
| **REL-02** | GitHub Releases + CHANGELOG | 
| **REL-04** | Публікація VS Code extension у вигляді інсталяційного `.vsix` пакета |

---

## Cтарт та встановлення

### 1. Клонування репозиторію та настановлення середовища
```bash
git clone [https://github.com/yariklaz/sipl-toolkit.git](https://github.com/yariklaz/sipl-toolkit.git)
cd sipl-toolkit

# Створення та активація віртуального середовища
python -m venv .venv

.venv\Scripts\activate

# Встановлення залежностей
pip install lark
