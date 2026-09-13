# Week 1 — Python Basics

Work through each lesson, then do the matching exercises in `exercises.py`.
Run code as you read: open a terminal in this folder and type `python`, then experiment.

---

## Lesson 1 — Running Python

Two ways to run Python:

1. **Interactive shell (REPL)** — type `python` in the terminal. Great for experiments. Type `exit()` to leave.
2. **Script file** — write code in a `.py` file, run it with `python filename.py`. This is how real programs run.

```python
print("Hello, AI Engineer")
```

`print()` displays things. You will use it constantly to see what your program is doing.

---

## Lesson 2 — Variables and types

A variable is a **name for a value**.

```python
city = "Delhi"          # str  — text
temperature = 31.5      # float — decimal number
humidity = 62           # int  — whole number
is_raining = False      # bool — True or False
```

- No type declarations — Python figures it out. This is called *dynamic typing*.
- Names use `snake_case` — lowercase words joined by underscores. This is the Python convention; follow it always.
- Check any value's type: `type(temperature)` → `<class 'float'>`.

### Converting between types

```python
age = int("25")        # string → int  ... "25" becomes 25
price = float("9.99")  # string → float
label = str(42)        # int → string  ... 42 becomes "42"
```

This matters because **everything that comes from a user or an API arrives as a string.**

---

## Lesson 3 — Strings (you will use these more than anything)

```python
name = "Deepak"
greeting = f"Hello, {name}! You have {3 + 4} new messages."
```

That `f"..."` is an **f-string** — put any expression in `{}` and it becomes part of the text.
In AI work, *prompts are strings*. Building prompts = building strings. Master this.

Useful string operations:

```python
s = "  AI Engineering  "
s.strip()          # "AI Engineering"     — remove surrounding spaces
s.lower()          # "  ai engineering  " — lowercase
s.upper()          # "  AI ENGINEERING  "
s.replace("AI", "ML")   # swap text
"eng" in s.lower()      # True — substring check
len(s)             # 18 — length in characters
s.split()          # ["AI", "Engineering"] — split into a list of words
"-".join(["a", "b", "c"])  # "a-b-c" — glue a list into one string
s.startswith("  AI")   # True
```

Multi-line strings use triple quotes — this is exactly how prompts are written:

```python
prompt = """You are a helpful assistant.

Summarize the following text in one sentence:
"""
```

---

## Lesson 4 — Numbers and operators

```python
7 + 3    # 10
7 - 3    # 4
7 * 3    # 21
7 / 3    # 2.3333...  — division ALWAYS gives a float
7 // 3   # 2          — floor division (throw away the remainder)
7 % 3    # 1          — modulo (the remainder itself)
7 ** 2   # 49         — power
```

Comparisons produce booleans:

```python
5 > 3     # True
5 == 5    # True   — equality is DOUBLE equals (single = is assignment)
5 != 4    # True   — not equal
```

Combine conditions with `and`, `or`, `not`:

```python
temp = 31
is_summer = True
temp > 30 and is_summer    # True
```

---

## Lesson 5 — Control flow: `if` / `elif` / `else`

Programs make decisions:

```python
temperature = 31

if temperature > 35:
    print("Too hot, stay inside")
elif temperature > 25:
    print("Warm day")
else:
    print("Pleasant")
```

Two things Python is strict about:

1. **The colon `:`** at the end of the condition line.
2. **Indentation** — the indented block *is* the body. Python uses indentation instead of `{}` braces. Use 4 spaces, always.

---

## Lesson 6 — Loops

### `for` — repeat over a sequence

```python
for word in ["prompt", "model", "token"]:
    print(word)

for i in range(5):      # 0, 1, 2, 3, 4  (starts at 0, stops BEFORE 5)
    print(i)
```

### `while` — repeat until a condition changes

```python
count = 3
while count > 0:
    print(count)
    count = count - 1   # forget this line → infinite loop (Ctrl+C to escape)
```

### Loop controls

```python
for i in range(10):
    if i == 3:
        continue    # skip the rest of THIS iteration
    if i == 6:
        break       # exit the loop entirely
    print(i)        # prints 0 1 2 4 5
```

---

## Lesson 7 — Functions

A function is a **named, reusable block of code with inputs and an output**.

```python
def celsius_to_fahrenheit(celsius):
    fahrenheit = celsius * 9 / 5 + 32
    return fahrenheit

result = celsius_to_fahrenheit(31.5)   # 88.7
```

- `def name(parameters):` defines it; calling `name(arguments)` runs it.
- `return` sends a value back to the caller. Without `return`, the function returns `None`.
- **`print` shows a value to a human; `return` hands a value to code.** Beginners confuse these — burn the difference in now.

Default values and keyword arguments:

```python
def make_prompt(text, style="concise", language="English"):
    return f"Rewrite the following in a {style} style, in {language}:\n\n{text}"

make_prompt("hello world")                          # uses both defaults
make_prompt("hello world", style="formal")          # override one, by name
```

This *exact* pattern — a function that assembles a prompt string from parameters — is
what "prompt templates" are in every AI framework. You just learned Module 3's core trick.

---

## Lesson 8 — Getting input

```python
name = input("What is your name? ")   # ALWAYS returns a string
age = int(input("Your age: "))        # convert if you need a number
```

---

## What "good" looks like this week

You should be able to close the notes and, from memory, write a function that
takes a number and returns a string decision based on `if`/`elif`/`else`, and a
loop that calls it over a list of values. That's exercise territory — go do them.

**Next:** open `exercises.py`, follow the instructions at the top.
