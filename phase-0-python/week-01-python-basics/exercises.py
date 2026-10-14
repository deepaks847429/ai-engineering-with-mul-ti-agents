"""
Week 1 exercises — Python basics.

HOW THIS WORKS
--------------
1. Each exercise is a function with a TODO. Replace the line that says
       raise NotImplementedError
   with your own code.
2. Run this file from the terminal:
       python exercises.py
3. The checks at the bottom test your answers. Fix errors until you see:
       ALL PASSED - week 1 complete!
4. Do them IN ORDER. They get harder. No copy-paste from notes — type it.

Rule: if you're stuck > 20 minutes, ask for a HINT, not the answer.
"""

# ---------------------------------------------------------------- exercise 1
def greet(name):
    """Return (not print!) the string: Hello, <name>!

    greet("Deepak") -> "Hello, Deepak!"
    """
    raise NotImplementedError


# ---------------------------------------------------------------- exercise 2
def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit and return it.

    Formula: F = C * 9/5 + 32
    celsius_to_fahrenheit(0) -> 32.0
    """
    raise NotImplementedError


# ---------------------------------------------------------------- exercise 3
def is_even(number):
    """Return True if number is even, False if odd.

    Hint: the % operator gives the remainder of a division.
    """
    raise NotImplementedError


# ---------------------------------------------------------------- exercise 4
def weather_advice(temperature):
    """Return advice based on temperature:

    above 35            -> "stay inside"
    26 to 35 (inclusive)-> "warm day"
    16 to 25 (inclusive)-> "pleasant"
    15 or below         -> "take a jacket"
    """
    raise NotImplementedError


# ---------------------------------------------------------------- exercise 5
def count_vowels(text):
    """Return how many vowels (a, e, i, o, u) appear in text.

    Count both uppercase and lowercase.
    count_vowels("AI Engineering") -> 7
    Hint: loop over the string; "for ch in text:" visits each character.
    """
    raise NotImplementedError


# ---------------------------------------------------------------- exercise 6
def sum_to_n(n):
    """Return the sum 1 + 2 + ... + n using a loop.

    sum_to_n(5) -> 15
    (Yes, there's a formula. Use the loop anyway - it's loop practice.)
    """
    raise NotImplementedError


# ---------------------------------------------------------------- exercise 7
def fizzbuzz(n):
    """The classic interview question. Return a string for one number n:

    divisible by 3 and 5 -> "FizzBuzz"
    divisible by 3 only  -> "Fizz"
    divisible by 5 only  -> "Buzz"
    otherwise            -> the number itself, as a string, e.g. "7"

    Careful with the ORDER of your if/elif checks.
    """
    raise NotImplementedError


# ---------------------------------------------------------------- exercise 8
def clean_name(raw):
    """Normalize a messy user-typed name.

    - remove surrounding whitespace
    - make it lowercase, then capitalize the first letter
      (there is a string method that does exactly lowercase-then-capitalize)

    clean_name("   dEEPAK  ") -> "Deepak"
    """
    raise NotImplementedError


# ---------------------------------------------------------------- exercise 9
def make_prompt(task, text, style="concise"):
    """Build a prompt string - your first prompt template!

    Return EXACTLY this (with real newlines, using an f-string):

    You are a helpful assistant.
    Task: <task>
    Style: <style>

    <text>

    Example:
    make_prompt("summarize", "Long article here")
    -> "You are a helpful assistant.\nTask: summarize\nStyle: concise\n\nLong article here"
    """
    raise NotImplementedError


# ---------------------------------------------------------------- exercise 10
def password_strength(password):
    """Rate a password. Return one of: "weak", "medium", "strong".

    Rules:
    - shorter than 8 characters            -> "weak"
    - 8+ characters                        -> "medium"
    - 12+ characters AND contains at least
      one digit (0-9)                      -> "strong"

    Hint: ch.isdigit() tells you if a character is a digit.
    password_strength("abc")            -> "weak"
    password_strength("abcdefgh")       -> "medium"
    password_strength("abcdefgh1234")   -> "strong"
    password_strength("abcdefghijkl")   -> "medium"  (12+ but no digit)
    """
    raise NotImplementedError


# ============================================================================
# CHECKS - do not edit below this line
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
