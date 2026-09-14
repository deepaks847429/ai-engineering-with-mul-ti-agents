"""
Week 1 solutions — Python basics.

Reference solutions for exercises.py. Try the exercises yourself first!
Run this file to see all checks pass:
    python solutions.py
"""

# ---------------------------------------------------------------- exercise 1
def greet(name):
    """Return (not print!) the string: Hello, <name>!

    greet("Deepak") -> "Hello, Deepak!"
    """
    return f"Hello, {name}!"


# ---------------------------------------------------------------- exercise 2
def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit and return it.

    Formula: F = C * 9/5 + 32
    celsius_to_fahrenheit(0) -> 32.0
    """
    return celsius * 9 / 5 + 32


# ---------------------------------------------------------------- exercise 3
def is_even(number):
    """Return True if number is even, False if odd."""
    return number % 2 == 0


# ---------------------------------------------------------------- exercise 4
def weather_advice(temperature):
    """Return advice based on temperature:

    above 35            -> "stay inside"
    26 to 35 (inclusive)-> "warm day"
    16 to 25 (inclusive)-> "pleasant"
    15 or below         -> "take a jacket"
    """
    if temperature > 35:
        return "stay inside"
    elif temperature >= 26:
        return "warm day"
    elif temperature >= 16:
        return "pleasant"
    else:
        return "take a jacket"


# ---------------------------------------------------------------- exercise 5
def count_vowels(text):
    """Return how many vowels (a, e, i, o, u) appear in text.

    Count both uppercase and lowercase.
    count_vowels("AI Engineering") -> 7
    """
    count = 0
    for ch in text.lower():
        if ch in "aeiou":
            count += 1
    return count


# ---------------------------------------------------------------- exercise 6
def sum_to_n(n):
    """Return the sum 1 + 2 + ... + n using a loop.

    sum_to_n(5) -> 15
    """
    total = 0
    for i in range(1, n + 1):
        total += i
    return total


# ---------------------------------------------------------------- exercise 7
def fizzbuzz(n):
    """The classic interview question. Return a string for one number n:

    divisible by 3 and 5 -> "FizzBuzz"
    divisible by 3 only  -> "Fizz"
    divisible by 5 only  -> "Buzz"
    otherwise            -> the number itself, as a string, e.g. "7"
    """
    if n % 3 == 0 and n % 5 == 0:
        return "FizzBuzz"
    elif n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    else:
        return str(n)


# ---------------------------------------------------------------- exercise 8
def clean_name(raw):
    """Normalize a messy user-typed name.

    clean_name("   dEEPAK  ") -> "Deepak"
    """
    return raw.strip().capitalize()


# ---------------------------------------------------------------- exercise 9
def make_prompt(task, text, style="concise"):
    """Build a prompt string - your first prompt template!

    make_prompt("summarize", "Long article here")
    -> "You are a helpful assistant.\nTask: summarize\nStyle: concise\n\nLong article here"
    """
    return f"You are a helpful assistant.\nTask: {task}\nStyle: {style}\n\n{text}"


# ---------------------------------------------------------------- exercise 10
def password_strength(password):
    """Rate a password. Return one of: "weak", "medium", "strong".

    - shorter than 8 characters            -> "weak"
    - 8+ characters                        -> "medium"
    - 12+ characters AND contains at least
      one digit (0-9)                      -> "strong"
    """
    if len(password) < 8:
        return "weak"

    has_digit = False
    for ch in password:
        if ch.isdigit():
            has_digit = True

    if len(password) >= 12 and has_digit:
        return "strong"
    else:
        return "medium"


# ============================================================================
# CHECKS - same as exercises.py
# ============================================================================
def _run_checks():
    checks = []

    def check(label, actual, expected):
        ok = actual == expected
        checks.append(ok)
        mark = "PASS" if ok else "FAIL"
        print(f"[{mark}] {label}: got {actual!r}, expected {expected!r}")

    try:
        check("1. greet", greet("Deepak"), "Hello, Deepak!")
        check("2. celsius 0", celsius_to_fahrenheit(0), 32.0)
        check("2. celsius 31.5", round(celsius_to_fahrenheit(31.5), 1), 88.7)
        check("3. is_even 4", is_even(4), True)
        check("3. is_even 7", is_even(7), False)
        check("4. weather 40", weather_advice(40), "stay inside")
        check("4. weather 30", weather_advice(30), "warm day")
        check("4. weather 20", weather_advice(20), "pleasant")
        check("4. weather 5", weather_advice(5), "take a jacket")
        check("4. weather 35 edge", weather_advice(35), "warm day")
        check("5. vowels", count_vowels("AI Engineering"), 7)
        check("5. vowels caps", count_vowels("AEIOU aeiou"), 10)
        check("6. sum_to_n 5", sum_to_n(5), 15)
        check("6. sum_to_n 100", sum_to_n(100), 5050)
        check("7. fizzbuzz 15", fizzbuzz(15), "FizzBuzz")
        check("7. fizzbuzz 9", fizzbuzz(9), "Fizz")
        check("7. fizzbuzz 10", fizzbuzz(10), "Buzz")
        check("7. fizzbuzz 7", fizzbuzz(7), "7")
        check("8. clean_name", clean_name("   dEEPAK  "), "Deepak")
        check("9. make_prompt",
              make_prompt("summarize", "Long article here"),
              "You are a helpful assistant.\nTask: summarize\nStyle: concise\n\nLong article here")
        check("9. make_prompt style",
              make_prompt("translate", "Hola", style="formal"),
              "You are a helpful assistant.\nTask: translate\nStyle: formal\n\nHola")
        check("10. password weak", password_strength("abc"), "weak")
        check("10. password medium", password_strength("abcdefgh"), "medium")
        check("10. password strong", password_strength("abcdefgh1234"), "strong")
        check("10. password 12 no digit", password_strength("abcdefghijkl"), "medium")
    except NotImplementedError:
        done = sum(checks)
        print(f"\n{done} check(s) passed so far.")
        print("Stopped at the first unfinished exercise - keep going!")
        return

    if all(checks):
        print(f"\nALL PASSED - week 1 complete! ({len(checks)} checks)")
        print("Commit your work, take a break, then start week 2.")
    else:
        failed = len(checks) - sum(checks)
        print(f"\n{failed} check(s) failing - read the FAIL lines above and fix them.")


if __name__ == "__main__":
    _run_checks()
