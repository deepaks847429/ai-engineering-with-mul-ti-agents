# Phase 1 — LLM Basics: Revision Notes

These are the notes from our lessons, in the same simple language and examples.
Read a lesson, then try to explain it out loud **without looking**. If you can't,
read it again.

Study order: **notes.md** → **exercises.py** → **INTERVIEW_QUESTIONS.md**

Every lesson ends with a 🎤 **Interview soundbite**, a short answer to learn
by heart.

---

## Lesson 1 — What is an LLM?

### The idea in one line

> **An LLM takes some text and predicts what comes next.**

It's like your phone keyboard: type "I'm on my..." and it suggests "way". It
learned which word usually comes next. An LLM is **the same idea, much bigger**.

| | Phone keyboard | LLM |
|---|---|---|
| Looks back at | The last 1–2 words | Up to hundreds of thousands of words |
| Learned from | Your own messages | Trillions of words (internet, books, code) |
| Size | Tiny | **Billions** of parameters |
| Writes | One suggestion | Whole essays and programs |

### The name

- **Large**: billions of **parameters**. A parameter is a number the model learned.
  Everything the model "knows" is stored in these numbers.
- **Language**: it works with text (newer models also handle images and audio).
- **Model**: a big maths function: text in → prediction of the next piece out.

### How it learned

It read a huge amount of text and played one game trillions of times:
**cover the next word → guess → check → adjust a little**. To get good at
guessing, it had to pick up grammar, facts, reasoning and coding along the way.
Nobody programmed in "Paris is the capital of France". It learned the pattern.

### ❌ Misconception: "it looks things up in a database"

There is **no database inside**. "Paris" is just the most likely next word,
based on what it read. That's why it can sound confident and still be wrong.

### LLMs can't really calculate

"2 + 2 = 4" works because that pattern was seen thousands of times.
"48,273 × 9,381" was probably never seen, so the model guesses digits that
*look* right, and they're often wrong.

**The fix is a calculator tool:**

```
You:  "What is 48,273 × 9,381?"
LLM:  writes a request → calculator("48273 * 9381")
App:  normal Python code computes 452849013   ✅ exact
LLM:  "48,273 × 9,381 = 452,849,013"
```

The LLM decides **when** to use the tool (a language skill). Real code does the
**maths** (a precision skill). This is called **tool use / function calling** (Phase 6).
The raw API has no tools unless **you** give them.

🎤 *"An LLM is a Transformer neural network trained on a huge amount of text to
predict the next token. Everything it does, like chatting, coding or summarising,
comes from repeating that prediction. It doesn't look facts up or calculate. For
exact maths we give it a calculator tool through function calling."*

---

## Lesson 2 — Tokens

### What's a token?

LLMs don't read words or letters. They read **tokens**: chunks of text.

```
"I love unbelievable pizza!"
→ "I" | " love" | " un" | "believ" | "able" | " pizza" | "!"     = 7 tokens, 5 words
```

- Common words = 1 token. Rare words = several pieces.
- The space usually sticks to the front of a token (`" love"`).
- Each token has an **ID number**. The model only ever sees numbers.
- **Vocabulary** = the list of all tokens the model knows (about 50k–200k).
- **Tokenizer** = the program that cuts text into tokens.

### Why not words? Why not letters?

| Option | Problem |
|---|---|
| **Whole words** | The vocabulary would be endless (names, typos, slang, every language). A new word like "Zeptomart" **can't be represented**: it becomes `[UNK]` and its meaning is lost |
| **Single letters** | Everything becomes 4–5× longer, so it's **slower, more expensive, and uses up the context window** |
| **Sub-word tokens** ✅ | The balance: common words are short, rare and new words are built from pieces |

### Rule of thumb

> **1 token ≈ ¾ of an English word ≈ 4 characters**
> **100 tokens ≈ 75 words.** 3,000 words ≈ 3,000 ÷ 0.75 = **4,000 tokens**

### Why engineers care

💰 **Cost** is per token. 📏 **Limits** are in tokens. ⏱️ **Speed** is one token at a time.

### How tokenizers are built: BPE (Byte Pair Encoding)

1. Start with single characters.
2. Find the **pair that appears together most often** in the training text.
3. **Glue it** into one new token.
4. Repeat thousands of times.

```
"t" + "h" → "th"     then     "th" + "e" → "the"
```

(You'll code one merge step in exercises 2–3.)

### The strawberry problem 🍓

"How many r's in strawberry?" Older models often said 2. The model sees
`"str" | "aw" | "berry"` as **3 ID numbers**. The letters are **hidden inside**.
It's like being asked to count the r's inside three sealed boxes.

### Hindi and Tamil cost more tokens

Tokenizers were trained mostly on **English**, so English pairs got glued into
whole-word tokens. Hindi and Tamil appeared less, so their words stay in **many
small pieces**.

```
English: "Hello"  → 1 token          Hindi: "नमस्ते" → several tokens
```

So the same message in Hindi means **higher cost, less fits in context, and slower answers**.

🎤 *"A token is the unit a model reads, usually a word or sub-word, made by a
tokenizer such as BPE. Sub-words balance vocabulary size against sequence
length. Cost, limits and speed are all measured in tokens. It also explains quirks
like letter-counting, and why non-English text needs more tokens."*

---

## Lesson 3 — Next-token prediction

### The fill-in-the-blank game

> "India ki capital ______ hai."

Your brain: think of options → give each a chance → pick the best. **An LLM does
exactly this**, one blank at a time.

### Where do the chances come from?

From what it read. If it read only these sentences:

```
"I drink chai."  "I drink chai."  "I drink chai."  "I drink coffee."
```

then for **"I drink ___"**: chai = 3/4 = **75%**, coffee = 1/4 = **25%**, banana = **0%**.

(A real LLM learns *patterns*, not literal counts, which is why it can handle
sentences it has never seen. But "it learned what usually comes next" is the
right mental model.)

### One step, with the official names

```
text → tokens → [model] → a score for EVERY token → softmax → % chances → pick one
                           (these are "logits")             ("probability distribution")
```

| Simple words | Official name |
|---|---|
| Raw score for each token, can be any number | **Logits** |
| Formula that turns scores into % that add up to 100 | **Softmax** |
| The list of chances (Paris 88%, Lyon 11%...) | **Probability distribution** |
| Filling one blank, adding it, repeating | **Autoregressive generation** |

Softmax example: logits Paris 5, Lyon 3, banana 0 → **88% / 12% / 0.6%**.
A gap of only 2 points became 7× the probability. Softmax **exaggerates the gaps**.

### Picking a token

- **Greedy**: always take the top one, so the same answer every time.
- **Sampling**: a lucky draw. 88 chits say "Paris", 11 say "Lyon". That's why
  **asking twice can give different answers**.

### The loop

```
Turn 1: "The capital of France is"          → " Paris"
Turn 2: "The capital of France is Paris"    → "."
Turn 3: ...                                  → <END>
```

It stops on an **end token**, at **max tokens**, or at a **stop sequence**.

### 3 consequences (interview favourites)

1. **Output is slower and costs more than input.** The prompt is read all at once
   (in parallel). The answer is written one token at a time. That's why output tokens cost 3–5× more.
   *Reading a page is fast. Writing one is slow.*
2. **It can't go back and edit.** A wrong early token ("capital of Australia is
   Sydney") gets built on. This is one reason "think step by step" helps.
3. **Two speed numbers:** **time to first token** (TTFT) and **tokens per second**.
   That's why chat apps **stream** the answer.

🎤 *"At each step the model outputs a logit for every token in the vocabulary.
Softmax turns them into probabilities, and a decoding strategy like greedy or
sampling picks one. That token is appended and the loop repeats until an end
token, stop sequence or max tokens. This is autoregressive generation. It's why
output is slower and pricier than input, and why early mistakes compound."*

---

## Lesson 4 — The context window

### The one-sheet exam

The **context window** is the most the model can read at once, measured in
tokens. Like being allowed **one sheet of notes** in an exam.

```
┌──────────────── one sheet (the context window) ────────────────┐
│ instructions │ old chat messages │ your question │ the answer │
└─────────────────────────────────────────────────────────────────┘
```

**The answer has to fit on the same sheet.** Window 8,000 and question 7,900
leaves only 100 tokens (about 75 words), so the answer **gets cut off**.

### 🤯 The model has NO memory

It forgets everything after each reply. The API is **stateless**.
ChatGPT "remembers" your name because **the app re-sends the whole conversation every time**:

```
Turn 2 sends: [Hi, my name is Deepak] [Hello Deepak!] [What is my name?]
```

*Like talking to someone who loses their memory every minute: you hand them a
notebook of everything said so far.* In Phase 4, **your code** does this.

### When the chat gets too long

- ❌ An error ("too many tokens"), or ✂️ the answer is cut off
- 🧹 The app cleans up: **delete the oldest messages**, **summarise** old ones, or
  send **only the relevant parts** (RAG, Phase 9)

### Why not always use a huge window?

💰 You pay for every token on **every** request. 🐢 It's slower to start answering.
😵 **"Lost in the middle"**: models notice the start and end best and can miss the middle.

🎤 *"The context window is the maximum tokens per request, input plus output.
The model is stateless, so the app re-sends history each turn and must trim,
summarise or retrieve when it grows. Long contexts cost more, add latency, and
models can miss information in the middle."*

---

## Lesson 5 — How an LLM is trained (3 stages)

```
📚 Stage 1: Pretraining  →  👩‍🏫 Stage 2: SFT         →  👍 Stage 3: RLHF / DPO
read the whole internet      learn from example Q&A       learn from human preferences
      BASE MODEL                INSTRUCT MODEL               CHAT MODEL (ChatGPT/Claude)
```

### Stage 1: Pretraining (school: reading everything)

- Trillions of words, the "guess the next word" game.
- No human labels: the text is its own answer key, so it's **self-supervised**.
- **The most expensive stage by far:** thousands of GPUs, weeks to months, crores of rupees.
- Gives a **base model**: knows a lot, but **only continues text**. Ask "What is the
  capital of France?" and it may continue "What is the capital of Germany?..."

### Stage 2: SFT / instruction tuning (an internship)

- Humans **write** example conversations: question → good answer.
- The model learns the **format** of being an assistant: answer, follow instructions, stop.

### Stage 3: RLHF / DPO (manager feedback)

- The model writes **two answers**. A human **compares** them and picks the better one.
- After thousands of comparisons, the model learns **what humans prefer**: helpful,
  honest, polite, and refusing harmful requests.
- **RLHF** = Reinforcement Learning from Human Feedback (trains a *reward model*,
  then uses reinforcement learning). **DPO** = Direct Preference Optimization (newer and
  simpler: learns from the pairs directly, with no reward model).

| Stage | The human... | The model gets |
|---|---|---|
| Pretraining | Does nothing (just text) | **Knowledge** |
| SFT | **Writes** answers | **How to answer** |
| RLHF / DPO | **Compares** answers | **Which answers are better** |

(Bonus: **reasoning models** add extra reinforcement learning on maths and code
problems with checkable answers, which teaches them to "think" before answering.)

🎤 *"Pretraining is self-supervised next-token prediction on trillions of
tokens. It's the most expensive stage and gives a base model that only
continues text. Supervised fine-tuning on human-written instruction-response pairs
teaches it to act as an assistant. Preference tuning with RLHF or DPO, where humans
compare answers, aligns it to be helpful, honest and safe."*

---

## Lesson 6 — The settings you control

### Temperature: the creativity knob

It changes the chits in the lucky-draw box **before** the draw.

```
Original:        chai 70%   coffee 20%   juice 10%
Low  (0.1)  🧊:  chai 99%   coffee  1%   juice  0%    ← safe, same every time
High (1.5)  🔥:  chai 45%   coffee 32%   juice 23%    ← creative, more random
```

(Technically: divide the logits by the temperature, then softmax.)
**Temperature 0 = greedy** (always the top token).

| Task | Temperature |
|---|---|
| Extract amount from a bank statement / invoice | **0** |
| Classify spam / not spam | **0** |
| Write code | **0–0.3** |
| Normal chatbot | **0.5–0.8** |
| Brainstorm names, poems, stories | **0.9–1.0** |

> **One correct answer → low. Many good answers → high.**

⚠️ **Myths:**
1. "Temperature 0 = exactly the same output every time." **Almost**, but not guaranteed.
2. "Temperature 0 = no mistakes." **Wrong.** It always picks the **top guess**, and
   the top guess can be wrong (Sydney 55% vs Canberra 40%).
   **Temperature controls randomness, not correctness.**

### Top-k: only the top k words can win

```
k = 2:   chai 50% ✅   coffee 30% ✅   juice 15% ❌   petrol 5% ❌
```

This stops silly picks. `k = 1` = greedy.

### Top-p (nucleus sampling): keep words until p% is covered

```
p = 0.8:  chai 50% ✅ (50%)  coffee 30% ✅ (80%, stop)  juice ❌  petrol ❌
```

**It adapts:** the model is sure (Paris 95%) → keeps 1 word. The model is unsure
(4 colours × 20%) → keeps 4 words. Top-k always keeps exactly k.

> Change **temperature OR top-p, not both**. They do similar jobs, and changing
> both makes behaviour hard to predict.

### Max tokens: the teacher takes your paper ✂️

A hard limit on **output** length. It **cuts** the answer off. It doesn't make the
answer shorter. For short answers, **ask in the prompt** ("answer in one sentence").
Always check the API's **stop reason** (e.g. `"max_tokens"`) so you don't show a
cut-off answer as complete.

### Stop sequences: a STOP sign 🛑

Generation ends as soon as a given string appears (e.g. `"###"` or `"User:"`).
This stops the model inventing extra text, such as a fake next user message.

🎤 *"Temperature scales the logits before softmax: low is sharper and more
deterministic, high is flatter and more creative. Top-k keeps the k most likely
tokens. Top-p keeps the smallest set reaching probability p, so it adapts to the
model's confidence. Tune one of temperature or top-p. Max tokens truncates output,
so check the stop reason. Stop sequences end generation at a given string."*

---

## Lesson 7 — Hallucination 🤥

**Confident, fluent, false.** Fake book titles, made-up functions, fake court
cases (a US lawyer was fined in 2023 for citing ChatGPT's invented cases).

### Why it happens

1. **Trained to sound *likely*, not to be *true*.** It fills the blank. It doesn't check facts.
   *Like a student in a viva who confidently says something that sounds right.*
2. **No database.** Common facts (France → Paris) are solid. Rare facts (founding year
   of a small Pune startup) are fuzzy, so it guesses.
3. **It always has to say something.** Confident answers were far more common in
   training than "I don't know".
4. **It can't go back.** One wrong word, then more invented words to match.

### Can't easily fix

- "Don't hallucinate!" in the prompt helps only a little.
- Temperature 0 doesn't fix it (top guess ≠ true).

### How engineers reduce it

| Fix | Idea | Phase |
|---|---|---|
| **RAG** | Put real documents in the prompt: "answer ONLY from these". An **open-book exam** | 9 |
| **Ask for sources** | "Quote the line you used" | 9 |
| **Allow "I don't know"** | Permit refusing when unsure | 3 |
| **Tools** | Search, calculator, database instead of guessing | 6 |
| **Validate with code** | Check format and facts automatically | 6 |
| **Evals** | Measure the hallucination rate on many test questions | 23 |

Example: a **college admissions chatbot** → give it the official rules document
(RAG), tell it to answer only from it, quote the rule, and say "I don't know" otherwise.

🎤 *"Hallucination is confident but false output. It happens because LLMs
generate likely text, not verified text, store fuzzy compressed patterns rather than
facts, and always produce an answer. You can't prompt it away, and temperature 0
doesn't fix it. You reduce it with RAG grounding, citations, allowing 'I don't
know', tools, and measuring it with evals."*

---

## Lesson 8 — Knowledge cutoff 📰

The **date the training data ends**. *Like a person who fell asleep in January
2025: they know nothing after it.*

Ask about something after the cutoff and the model either says it doesn't know ✅,
or **guesses from old info**, which is a hallucination ❌ (e.g. calling an old iPhone
"the latest").

4 facts:
1. The cutoff is usually **months before release** (testing and safety take time).
2. The **last months before the cutoff are thin**: the internet hadn't written much yet.
3. The model **doesn't know today's date**. Apps add "Today's date is ..." to the prompt.
4. The model doesn't know what it doesn't know, so it may present old info as current.

**Fixes:** RAG, web search tools, or put the facts in the prompt.
❌ **Not** "retrain every week": pretraining costs crores and takes months.

🎤 *"The knowledge cutoff is when the training data ends. The model knows nothing
after it, recent events before it are thin, and it doesn't know the current date
unless told. For fresh information we use retrieval, search tools or the prompt,
not retraining."*

---

## Lesson 9 — The model landscape 🗺️

### Closed vs open-weight

| | 🔒 Closed: rent it (Ola/Uber) | 🔓 Open-weight: buy it (own car) |
|---|---|---|
| Examples | OpenAI **GPT**, Anthropic **Claude**, Google **Gemini** | Meta **Llama**, **Mistral**, Alibaba **Qwen**, **DeepSeek**, Google **Gemma** |
| Access | API only, pay per token | Download the weights, run on your servers |
| Quality | Usually the best | Close, often slightly behind |
| Setup | Easy: an API key | Hard: GPUs, ops work |
| Privacy | Data goes to the company | **Data stays with you** |
| Customise | Limited | Full control, can fine-tune |

Open-weight suits **banks, hospitals, government** (private data) or very high volume.
⚠️ Open-weight ≠ open source (no training data or code), and **check the licence**.

### Tiers (sizes)

| Tier | Claude example | Use for | Cost |
|---|---|---|---|
| 🦁 Large | **Opus** | Hardest problems, complex code, agents | 💰💰💰 |
| 🐺 Medium | **Sonnet** | Most tasks, the default | 💰💰 |
| 🐇 Small | **Haiku** | Simple, high-volume, fast | 💰 |

**Router:** easy questions → small model, hard ones → large model. Saves lots of money.
*(A hospital doesn't send every cold to the senior surgeon.)*

### Reasoning ("thinking") models 🧠

They think step by step before answering. **Better at maths, logic, hard code and planning.**
**Slower and costlier** (you pay for thinking tokens). Don't use one to say hello.

### Multimodal 🖼️🎤

Image input (photo of a bill), PDFs, audio (speech ↔ text), image generation.

### Pricing 💰

Priced **per 1 million tokens**, input and output separately; output costs more.

```
$3 / 1M input,  $15 / 1M output     (illustrative)
2,000 input  → 2,000 / 1,000,000 × 3  = $0.006
  500 output →   500 / 1,000,000 × 15 = $0.0075
Total = $0.0135 per request (~₹1.1)
× 1,00,000 requests/day = $1,350/day (~₹1.1 lakh/day) 😱
```

Savers (Phase 21): **caching** a repeated prompt prefix, and **batch** (about half price if you can wait).

### Model card and benchmarks

A **model card** is the spec sheet: context window, max output, cutoff, inputs, price,
benchmarks, limitations, licence. **Benchmarks** are standard tests, but a model can ace
them and still fail **your** task (like memorising past papers). The real test is
**your own evals** (Phase 23).

### Choosing checklist

1. How hard is it? → large or reasoning vs small
2. How fast must it be? → small or medium for real-time
3. What's the budget? → small model or a router
4. Is the data private? → open-weight, self-hosted
5. Images or audio? → multimodal
6. **Test on your own examples**

🎤 *"I pick by task difficulty, latency, cost, context window and privacy.
Closed APIs give top quality with no hosting. Open-weight gives privacy and
control. I default to a mid-tier model, route easy traffic to a small one, use
reasoning models only for hard problems, and confirm with evals on our own data."*

---

## The whole phase on one screen

```
Text ─tokenizer─► token IDs ─model─► logits ─softmax─► probabilities
                                                              │
                     temperature / top-k / top-p ◄────────────┘
                                     │
                             pick ONE token ─► append ─► repeat
                                     │
                  stop: end token / stop sequence / max tokens
```

- **LLM** = next-token predictor. No database, no calculator.
- **Token** ≈ ¾ word. Cost, limits and speed are counted in tokens. BPE builds the vocabulary.
- **Context window** = input + output. Stateless, so the app re-sends history.
- **Training** = pretraining (most expensive) → SFT (humans write) → RLHF/DPO (humans compare).
- **Temperature** = randomness, not correctness. Top-p adapts. Max tokens cuts.
- **Hallucination** = likely ≠ true. Fix with RAG, citations, tools, evals.
- **Cutoff** = no new knowledge. Fix with retrieval and tools, not retraining.
- **Model choice** = difficulty × speed × cost × privacy, proven with evals.

**Next:** Phase 2, first API calls, where you'll see all of this in real code.
