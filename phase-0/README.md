# Phase 0 — Absolute Beginner Foundations

> Goal: in 6 weeks, go from zero to writing a Python script that calls a real API,
> parses JSON, stores results in a database, and lives in a clean Git repo.
> That is the exit ticket to Phase 1 (LLM fundamentals).

## How each week works

1. Read `notes.md` in the week's folder — short lessons, no fluff.
2. Do `exercises.py` — type the code yourself. **Never copy-paste. Typing is the learning.**
3. Run the file. Exercises check themselves with `assert` — if it prints `ALL PASSED`, you're done.
4. Stuck for more than 20 minutes on one exercise? Ask Claude to *explain*, not to *solve*.
5. Commit your work at the end of every session (you'll learn Git in week 3 — until then, just save).

## Weekly plan

| Week | Folder | Topic | You can... |
|------|--------|-------|-----------|
| 1 | `week-01-python-basics` | Variables, types, strings, control flow, functions | write small programs that make decisions |
| 2 | `week-02-data-structures` | Lists, dicts, sets, tuples, comprehensions, files & JSON | model real data and save/load it |
| 3 | `week-03-git-and-terminal` | Terminal fluency, Git & GitHub, project layout, venv | work like a developer, not a notebook user |
| 4 | `week-04-oop-and-errors` | Classes, inheritance, exceptions, type hints | structure code the way PyTorch & FastAPI expect |
| 5 | `week-05-apis-and-http` | HTTP, REST, `requests`, API keys, `.env` files | call any public API and handle its failures |
| 6 | `week-06-capstone` | numpy/pandas taste + SQL basics + **capstone project** | ship the Phase 0 exit project |

## Phase 0 capstone (week 6)

**Weather Logger CLI** — a script that:
- takes a city name from the command line
- calls a free weather API (no credit card needed)
- parses the JSON response
- stores each lookup in SQLite with a timestamp
- can print a history table of past lookups
- lives in a Git repo with a README written by you

Every skill in weeks 1–5 is used by this build. When it works, Phase 0 is over.

## Rules of the road

- **Daily beats weekly.** 45 minutes every day beats 6 hours on Sunday.
- **Type everything.** Muscle memory is real for syntax.
- **Break things on purpose.** Change a line, predict what happens, run it, check. That loop is how programmers are made.
- **No tutorial hell.** These notes + exercises + the official Python docs are enough. Don't open a 14-hour YouTube course.
