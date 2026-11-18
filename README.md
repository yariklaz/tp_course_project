# SIPL Toolkit (SImple Programming Language)

---

## Вибрані завдання та бали (трек «Interpreter + Debugger»)

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
| **Разом** | 

---

## Cтарт

### 1. Клонування репозиторію та налаштування середовища

```bash
git clone https://github.com/yariklaz/sipl-toolkit.git
cd sipl-toolkit

python -m venv .venv

.venv\Scripts\activate

pip install lark
```

### 2. Запуск через CLI

Парсити та запускати SIPL-програми можна напряму з консолі:

```bash
python run.py examples/example1.sipl --state "{\"X\": 5, \"Y\": 2}"
```

---

## VS Code Extension та Debugger (IDE-03)

У кореневій папці проєкту знаходиться готовий інсталяційний файл розширення: **`sipl-toolkit-0.1.0.vsix`**.

### Встановлення

1. Відкрийте вкладку Extensions (`Ctrl+Shift+X`).
2. Натисніть на три крапки у верхньому правому куті панелі й виберіть **Install from VSIX...**.
3. Виберіть файл `sipl-toolkit-0.1.0.vsix`.

### Тестування відлагодження

1. Відкрийте файл `examples/example1.sipl`.
2. Поставте брейкпоінт (червону крапку) на 3-му рядку (`while Y>0 do`).
3. Перейдіть у вкладку **Run and Debug**, виберіть конфігурацію **Debug SIPL** і натисніть **F5**.
4. Використовуйте покрокове виконання (`Step Over`, `Continue`), щоб спостерігати за зміною змінних (`X`, `Y`, `R`) у реальному часі.

---

## Тести (CORE-01)

У проєкті є набір автоматичних тестів для перевірки граматики:

- Позитивні тести: `tests/positive/` (10 файлів)
- Негативні тести: `tests/negative/` (10 файлів)

Генерація та перевірка тестової бази:

```bash
python generate_tests.py
```
