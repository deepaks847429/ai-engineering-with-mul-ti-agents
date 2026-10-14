"""
Phase 1 solutions — LLM basics.

Reference solutions for exercises.py. Try the exercises yourself first!
Run this file to see all checks pass:
    python solutions.py
"""
import math


# =========================================================== LESSON 2: TOKENS

# ---------------------------------------------------------------- exercise 1
def words_to_tokens(word_count):
    """Estimate the token count for English text with the rule of thumb:
    1 token is about 3/4 of a word. Return a whole number (use round()).

    words_to_tokens(3000) -> 4000
    words_to_tokens(75)   -> 100
    """
    return round(word_count / 0.75)


# ---------------------------------------------------------------- exercise 2
def most_frequent_pair(tokens):
    """BPE step 1: find the pair of NEIGHBOURING tokens that appears most often.
    Return it as a tuple. If two pairs tie, return the one that appears first.

    most_frequent_pair(["t", "h", "e", " ", "t", "h", "e", "n"]) -> ("t", "h")

    Hint: neighbours are tokens[i] and tokens[i + 1]. Count them in a dict.
    """
    counts = {}
    for i in range(len(tokens) - 1):
        pair = (tokens[i], tokens[i + 1])
        counts[pair] = counts.get(pair, 0) + 1
    return max(counts, key=counts.get)


# ---------------------------------------------------------------- exercise 3
def merge_pair(tokens, pair):
    """BPE step 2: glue every occurrence of `pair` into one token.
    Return a NEW list.

    merge_pair(["t", "h", "e", " ", "t", "h", "e", "n"], ("t", "h"))
        -> ["th", "e", " ", "th", "e", "n"]

    Hint: walk through the list with a while loop. When tokens[i] and
    tokens[i + 1] match the pair, append the glued token and jump 2 places.
    """
    merged = []
    i = 0
    while i < len(tokens):
        if i < len(tokens) - 1 and (tokens[i], tokens[i + 1]) == pair:
            merged.append(tokens[i] + tokens[i + 1])
            i += 2
        else:
            merged.append(tokens[i])
            i += 1
    return merged


# ============================================ LESSON 3: NEXT-TOKEN PREDICTION

# ---------------------------------------------------------------- exercise 4
def next_word_probs(sentences, prefix):
    """The "I drink chai" model from the lesson.

    Look at every sentence that STARTS with the words in `prefix` and has at
    least one more word after it. Count which word comes next, then turn the
    counts into probabilities (count / total). Split on spaces only.
    Return {} if no sentence continues the prefix.

    sentences = ["I drink chai", "I drink chai", "I drink chai", "I drink coffee"]
    next_word_probs(sentences, "I drink") -> {"chai": 0.75, "coffee": 0.25}
    """
    prefix_words = prefix.split()
    n = len(prefix_words)
    counts = {}
    for sentence in sentences:
        words = sentence.split()
        if words[:n] == prefix_words and len(words) > n:
            next_word = words[n]
            counts[next_word] = counts.get(next_word, 0) + 1
    total = sum(counts.values())
    return {word: count / total for word, count in counts.items()}


# ---------------------------------------------------------------- exercise 5
def greedy_pick(probs):
    """Greedy decoding: return the word with the highest probability.

    greedy_pick({"chai": 0.75, "coffee": 0.25}) -> "chai"
    """
    return max(probs, key=probs.get)


# ---------------------------------------------------------------- exercise 6
def softmax(logits):
    """Turn raw scores (logits) into probabilities that add up to 1.

    For each word:  probability = e^score / (sum of e^score for all words)
    Use math.exp(x) for e^x.

    softmax({"Paris": 5.0, "Lyon": 3.0, "banana": 0.0})
        -> {"Paris": 0.876, "Lyon": 0.118, "banana": 0.006}   (roughly)
    """
    exps = {word: math.exp(score) for word, score in logits.items()}
    total = sum(exps.values())
    return {word: e / total for word, e in exps.items()}


# ================================================== LESSON 6: THE SETTINGS

# ---------------------------------------------------------------- exercise 7
def apply_temperature(logits, temperature):
    """Divide every logit by the temperature, THEN apply softmax.
    Reuse your softmax() from exercise 6.

    Low temperature  -> the top word gets an even bigger share (sharper)
    High temperature -> the shares get more even (flatter)
    """
    return softmax({word: score / temperature for word, score in logits.items()})


# ---------------------------------------------------------------- exercise 8
def top_k_filter(probs, k):
    """Keep only the k most likely words, then RE-NORMALISE so the kept
    probabilities add up to 1 again (divide each by their new total).

    top_k_filter({"chai": 0.5, "coffee": 0.3, "juice": 0.15, "petrol": 0.05}, 2)
        -> {"chai": 0.625, "coffee": 0.375}

    Hint: sorted(probs, key=probs.get, reverse=True) gives words from most to
    least likely.
    """
    kept = sorted(probs, key=probs.get, reverse=True)[:k]
    total = sum(probs[word] for word in kept)
    return {word: probs[word] / total for word in kept}


# ---------------------------------------------------------------- exercise 9
def top_p_filter(probs, p):
    """Nucleus sampling: go from most to least likely, keep adding words until
    their probabilities add up to AT LEAST p. Then re-normalise.

    top_p_filter({"chai": 0.5, "coffee": 0.3, "juice": 0.15, "petrol": 0.05}, 0.75)
        -> {"chai": 0.625, "coffee": 0.375}        (0.5 + 0.3 = 0.8 >= 0.75)
    top_p_filter({"Paris": 0.95, "Lyon": 0.05}, 0.8)
        -> {"Paris": 1.0}                          (confident -> keeps just 1)
    """
    kept = []
    running_total = 0
    for word in sorted(probs, key=probs.get, reverse=True):
        kept.append(word)
        running_total += probs[word]
        if running_total >= p:
            break
    return {word: probs[word] / running_total for word in kept}


# ======================================== LESSON 4: CONTEXT WINDOW

# --------------------------------------------------------------- exercise 10
def fits_in_context(input_tokens, max_output_tokens, context_window):
    """Return True if the prompt AND the full answer fit in the window together.

    fits_in_context(7900, 500, 8000) -> False   (the answer would be cut off)
    fits_in_context(2000, 500, 8000) -> True
    """
    return input_tokens + max_output_tokens <= context_window


# --------------------------------------------------------------- exercise 11
def trim_history(messages, budget):
    """Make a long chat fit. `messages` is a list of (text, token_count) tuples.
    The FIRST message is the system prompt: always keep it.
    Then keep the MOST RECENT messages that still fit in `budget` tokens.
    Return the kept messages in their original order.

    messages = [("system", 100), ("old", 500), ("mid", 300), ("new", 200)]
    trim_history(messages, 650) -> [("system", 100), ("mid", 300), ("new", 200)]

    Hint: walk backwards through messages[1:], stop when the next one won't fit.
    """
    system = messages[0]
    used = system[1]
    kept = []
    for message in reversed(messages[1:]):
        if used + message[1] > budget:
            break
        kept.append(message)
        used += message[1]
    return [system] + list(reversed(kept))


# ======================================== LESSON 9: PRICING

# --------------------------------------------------------------- exercise 12
def request_cost(input_tokens, output_tokens, input_price_per_m, output_price_per_m):
    """Cost in dollars of one request. Prices are per 1,000,000 tokens.

    request_cost(2000, 500, 3, 15) -> 0.0135
    """
    input_cost = input_tokens / 1_000_000 * input_price_per_m
    output_cost = output_tokens / 1_000_000 * output_price_per_m
    return input_cost + output_cost


# ==================================== BOSS LEVEL: YOUR OWN MINI LLM LOOP

# --------------------------------------------------------------- exercise 13
def generate(sentences, start, max_tokens, stop=None):
    """The autoregressive loop from Lesson 3, using your exercise 4 and 5.

    Start with the text `start`. Repeat:
      1. probs = next_word_probs(sentences, text)
      2. if probs is empty          -> return (text, "end")
      3. word = greedy_pick(probs)
      4. if word == stop            -> return (text, "stop_sequence")  (don't add it)
      5. add the word to text (with a space)
      6. if you've added max_tokens words -> return (text, "max_tokens")

    sentences = ["I drink chai every morning", "I drink chai every morning",
                 "I drink coffee at night"]
    generate(sentences, "I", 10)              -> ("I drink chai every morning", "end")
    generate(sentences, "I", 2)               -> ("I drink chai", "max_tokens")
    generate(sentences, "I", 10, stop="every") -> ("I drink chai", "stop_sequence")
    """
    text = start
    added = 0
    while True:
        probs = next_word_probs(sentences, text)
        if not probs:
            return text, "end"
        word = greedy_pick(probs)
        if word == stop:
            return text, "stop_sequence"
        text = text + " " + word
        added += 1
        if added == max_tokens:
            return text, "max_tokens"


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

    def rounded(d, places=3):
        return {k: round(v, places) for k, v in d.items()}

    chai = ["I drink chai", "I drink chai", "I drink chai", "I drink coffee"]
    virat = ["Virat Kohli plays cricket", "Virat Kohli plays cricket",
             "Virat Kohli plays football", "Virat Kohli plays cricket"]
    story = ["I drink chai every morning", "I drink chai every morning",
             "I drink coffee at night"]
    drinks = {"chai": 0.5, "coffee": 0.3, "juice": 0.15, "petrol": 0.05}
    logits = {"Paris": 5.0, "Lyon": 3.0, "banana": 0.0}
    chat = [("system", 100), ("old", 500), ("mid", 300), ("new", 200)]
    the_then = ["t", "h", "e", " ", "t", "h", "e", "n"]

    try:
        check("1. 3000 words", words_to_tokens(3000), 4000)
        check("1. 75 words", words_to_tokens(75), 100)
        check("2. most frequent pair", most_frequent_pair(the_then), ("t", "h"))
        check("2. tie -> first seen", most_frequent_pair(["a", "b", "c", "d"]), ("a", "b"))
        check("3. merge th", merge_pair(the_then, ("t", "h")),
              ["th", "e", " ", "th", "e", "n"])
        check("3. merge again", merge_pair(["th", "e", " ", "th", "e", "n"], ("th", "e")),
              ["the", " ", "the", "n"])
        check("4. chai", next_word_probs(chai, "I drink"), {"chai": 0.75, "coffee": 0.25})
        check("4. virat", next_word_probs(virat, "Virat Kohli plays"),
              {"cricket": 0.75, "football": 0.25})
        check("4. nothing follows", next_word_probs(chai, "I drink chai"), {})
        check("5. greedy", greedy_pick({"chai": 0.75, "coffee": 0.25}), "chai")
        check("6. softmax", rounded(softmax(logits)),
              {"Paris": 0.876, "Lyon": 0.118, "banana": 0.006})
        check("6. softmax sums to 1", round(sum(softmax(logits).values()), 6), 1.0)
        check("7. temperature 1 = softmax",
              rounded(apply_temperature(logits, 1)), rounded(softmax(logits)))
        check("7. low temp is sharper",
              apply_temperature(logits, 0.5)["Paris"] > softmax(logits)["Paris"], True)
        check("7. high temp is flatter",
              apply_temperature(logits, 2)["Paris"] < softmax(logits)["Paris"], True)
        check("8. top-k 2", rounded(top_k_filter(drinks, 2)), {"chai": 0.625, "coffee": 0.375})
        check("8. top-k 1 = greedy", top_k_filter(drinks, 1), {"chai": 1.0})
        check("9. top-p 0.75", rounded(top_p_filter(drinks, 0.75)),
              {"chai": 0.625, "coffee": 0.375})
        check("9. top-p confident", top_p_filter({"Paris": 0.95, "Lyon": 0.05}, 0.8),
              {"Paris": 1.0})
        check("9. top-p unsure keeps 4",
              len(top_p_filter({"red": 0.2, "blue": 0.2, "green": 0.2,
                                "yellow": 0.2, "pink": 0.2}, 0.8)), 4)
        check("10. 7900 + 500 in 8000", fits_in_context(7900, 500, 8000), False)
        check("10. 2000 + 500 in 8000", fits_in_context(2000, 500, 8000), True)
        check("10. exactly full", fits_in_context(7500, 500, 8000), True)
        check("11. trim", trim_history(chat, 650), [("system", 100), ("mid", 300), ("new", 200)])
        check("11. everything fits", trim_history(chat, 5000), chat)
        check("11. only system", trim_history(chat, 150), [("system", 100)])
        check("12. one request", round(request_cost(2000, 500, 3, 15), 6), 0.0135)
        check("12. 1 lakh requests",
              round(request_cost(2000, 500, 3, 15) * 100_000, 2), 1350.0)
        check("13. runs to the end", generate(story, "I", 10),
              ("I drink chai every morning", "end"))
        check("13. max tokens", generate(story, "I", 2), ("I drink chai", "max_tokens"))
        check("13. stop sequence", generate(story, "I", 10, stop="every"),
              ("I drink chai", "stop_sequence"))
    except NotImplementedError:
        done = sum(checks)
        print(f"\n{done} check(s) passed so far.")
        print("Stopped at the first unfinished exercise - keep going!")
        return

    if all(checks):
        print(f"\nALL PASSED - Phase 1 complete! ({len(checks)} checks)")
        print("You just built tokenizer merges, softmax, temperature, top-k, top-p")
        print("and a tiny autoregressive generator. Now do INTERVIEW_QUESTIONS.md.")
    else:
        failed = len(checks) - sum(checks)
        print(f"\n{failed} check(s) failing - read the FAIL lines above and fix them.")


if __name__ == "__main__":
    _run_checks()
