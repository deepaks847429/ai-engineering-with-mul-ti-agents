# Transformers From Scratch: Vectors → Attention → Feed-Forward Network

> Goal for today: understand **exactly** what happens inside a Transformer, by hand and in code.
> No magic, no hand-waving. Every idea is built only on the ones that come before it.

**How to use this file**
1. Read one section at a time. Don't skip ahead.
2. Do every calculation by hand with pen and paper **before** you look at the answer.
3. Run the Python code and check that it gives the same numbers you got by hand.
4. Do the exercises at the end of each part. If you can't do them, re-read the part.

**What you need:** Python + `numpy` (`pip install numpy`). School maths (add, multiply, square root). That's it.

---

## Table of Contents

- [Part 0 — The Big Picture (read this first)](#part-0--the-big-picture-read-this-first)
- [Part 1 — Vectors](#part-1--vectors)
- [Part 2 — Attention](#part-2--attention)
- [Part 3 — Feed-Forward Neural Network (FFNN)](#part-3--feed-forward-neural-network-ffnn)
- [Part 4 — Putting It Together: One Transformer Block](#part-4--putting-it-together-one-transformer-block)
- [Final Checklist](#final-checklist)

---

## Part 0 — The Big Picture (read this first)

A Transformer (the thing inside ChatGPT, Claude, etc.) does one job:

> **Given some words, predict the next word.**

It does this in 4 steps:

```
"the cat sat"
     │
     ▼
1. Split into tokens        → ["the", "cat", "sat"]
2. Turn each token into a   → [0.2, 0.9, ...], [0.7, 0.1, ...], [0.5, 0.5, ...]
   list of numbers (VECTOR)
3. Pass through N Transformer blocks. Each block has:
      a) ATTENTION  → words look at each other and share information
      b) FFNN       → each word "thinks" on its own about what it now knows
4. Turn the final vector into a probability for every possible next word → "on"
```

So the three topics for today are **the three core ingredients**:

| Topic | Role in one sentence |
|---|---|
| **Vectors** | How a computer represents the *meaning* of a word as numbers. |
| **Attention** | How each word *collects information from other words* in the sentence. |
| **FFNN** | How each word *processes* that collected information. |

Keep this picture in your head. Everything below is just zooming in on it.

---

## Part 1 — Vectors

### 1.1 What is a vector?

A vector is just **an ordered list of numbers**.

```
v = [3, 4]          ← a 2-dimensional (2D) vector
w = [1, 0, -2, 5]   ← a 4-dimensional (4D) vector
```

The number of values is called its **dimension**.
Order matters: `[3, 4]` is not the same as `[4, 3]`.

**Picture it:** a 2D vector `[3, 4]` is an arrow from the origin `(0,0)` to the point `(3,4)`.

```
  y
  4 |        • (3,4)
  3 |      /
  2 |    /
  1 |  /
  0 +--------------- x
    0  1  2  3
```

It has a **direction** (where it points) and a **length** (how long the arrow is).

### 1.2 Why do we need vectors for words?

Computers can't understand the word "cat". They only understand numbers.

**Bad idea:** give each word an ID. `cat = 1`, `dog = 2`, `car = 3`.
Problem: this says `dog` is "between" `cat` and `car`, which means nothing. Numbers like these carry no meaning.

**Good idea:** give each word a **vector**, where each number describes some property.

Imagine (for learning) 3 hand-made dimensions: `[is_animal, is_big, is_vehicle]`

```
cat   = [0.9, 0.2, 0.0]
dog   = [0.9, 0.4, 0.0]
lion  = [0.9, 0.9, 0.0]
car   = [0.0, 0.6, 0.9]
truck = [0.0, 0.9, 0.9]
```

Now similar words have similar numbers. `cat` and `dog` are close. `cat` and `truck` are far.

In real models:
- The vectors have **hundreds or thousands** of dimensions (e.g. 768, 4096).
- Nobody hand-picks what each dimension means. The model **learns** the numbers during training.
- This word → vector lookup is called an **embedding**. The vector is the word's **embedding**.

### 1.3 Operation 1: Adding vectors and scaling vectors

**Addition:** add position by position.
```
[1, 2, 3] + [4, 5, 6] = [1+4, 2+5, 3+6] = [5, 7, 9]
```

**Scaling (multiply by a single number):** multiply every value.
```
2 × [1, 2, 3] = [2, 4, 6]
0.5 × [4, 6]  = [2, 3]
```

> Remember this: **attention's output is a weighted sum of vectors** = scaling some vectors and adding them up. That's all it is.

### 1.4 Operation 2: Length (magnitude)

The length of a vector (Pythagoras):

```
|v| = sqrt(v1² + v2² + ... + vn²)

|[3, 4]| = sqrt(9 + 16) = sqrt(25) = 5
```

### 1.5 Operation 3: The dot product ⭐ (MOST IMPORTANT)

Multiply position by position, then add everything up. The result is **one number**.

```
a = [1, 2, 3]
b = [4, 5, 6]

a · b = (1×4) + (2×5) + (3×6) = 4 + 10 + 18 = 32
```

**What does it mean?** The dot product measures **how much two vectors point in the same direction**.

| Dot product | Meaning |
|---|---|
| Big positive | Point the same way → **similar** |
| Around 0 | At right angles → **unrelated** |
| Negative | Point opposite ways → **opposite** |

Check with our word vectors:
```
cat · dog   = 0.9×0.9 + 0.2×0.4 + 0.0×0.0 = 0.81 + 0.08 + 0     = 0.89  (high → similar)
cat · truck = 0.9×0.0 + 0.2×0.9 + 0.0×0.9 = 0    + 0.18 + 0     = 0.18  (low  → different)
```

> **Attention is built entirely on dot products.** When a word "asks" which other words are relevant, it computes a dot product with each one. Big number = relevant.

### 1.6 Cosine similarity

The dot product also grows when vectors are just *longer*. To measure only direction, divide by both lengths:

```
cos_sim(a, b) = (a · b) / (|a| × |b|)
```

Result is always between **-1** (opposite) and **+1** (identical direction).

```
a = [1,2,3], b = [4,5,6]
a · b = 32
|a| = sqrt(1+4+9)   = sqrt(14) ≈ 3.742
|b| = sqrt(16+25+36)= sqrt(77) ≈ 8.775
cos_sim = 32 / (3.742 × 8.775) = 32 / 32.83 ≈ 0.975   → very similar
```

### 1.7 Matrices and matrix multiplication

A **matrix** is a grid of numbers = a stack of vectors.

```
W = [[1, 2],
     [0, 1],
     [3, 0]]     ← shape (3, 2): 3 rows, 2 columns
```

**Vector × Matrix:** each output value is a dot product of the vector with one **column** of the matrix.

```
x = [1, 0, 1]      shape (3,)
W shape (3, 2)

output[0] = x · column0 = 1×1 + 0×0 + 1×3 = 4
output[1] = x · column1 = 1×2 + 0×1 + 1×0 = 2

x @ W = [4, 2]     shape (2,)
```

**Shape rule (memorise this):**
```
(a, b) @ (b, c) → (a, c)
        ↑    ↑
   these must match
```

**Why it matters:** multiplying by a matrix **transforms** a vector into a new vector (possibly of a different size). In Transformers, "learned weights" are just matrices, and "the model learns" means "the numbers in these matrices get adjusted".

If you stack many vectors as rows, you can transform all of them at once:
```
X shape (3 words, 4 dims) @ W shape (4, 2) → shape (3 words, 2 dims)
```

### 1.8 Code: Vectors in numpy

```python
import numpy as np

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print(a + b)                 # [5 7 9]
print(2 * a)                 # [2 4 6]
print(np.linalg.norm(a))     # 3.7416...  (length)
print(a @ b)                 # 32         (dot product)
print(np.dot(a, b))          # 32         (same thing)

cos = (a @ b) / (np.linalg.norm(a) * np.linalg.norm(b))
print(cos)                   # 0.9746...

x = np.array([1, 0, 1])
W = np.array([[1, 2],
              [0, 1],
              [3, 0]])
print(x @ W)                 # [4 2]
print(W.shape)               # (3, 2)
```

### ✏️ Exercises — Part 1
1. By hand: `[2, -1, 3] · [1, 4, 0]` = ?
2. By hand: length of `[6, 8]` = ?
3. Using the word vectors above, compute `lion · car` and `car · truck`. Which pair is more similar?
4. What is the shape of `(5, 8) @ (8, 3)`? Can you do `(5, 8) @ (5, 3)`? Why not?
5. Code: write a function `cosine_similarity(a, b)` from scratch (only use `sum`, `**`, loops — no numpy). Test it against numpy.

<details><summary>Answers</summary>

1. `2 - 4 + 0 = -2`
2. `sqrt(36 + 64) = 10`
3. `lion·car = 0 + 0.54 + 0 = 0.54`, `car·truck = 0 + 0.54 + 0.81 = 1.35` → car/truck more similar
4. `(5, 3)`. No — the inner numbers (8 and 5) don't match.
</details>

---

## Part 2 — Attention

### 2.1 The problem attention solves

Look at these two sentences:

> "I sat by the river **bank**."
> "I deposited money at the **bank**."

After Part 1, the word "bank" gets **the same vector** in both sentences. But the meaning is different!
The meaning of a word depends on **the other words around it (its context)**.

Another one:
> "The **animal** didn't cross the street because **it** was too tired."

What does "it" mean? The animal. To know that, "it" must **look at** the other words and figure out which one is relevant.

**Attention = a way for each word to look at every other word, decide how relevant each one is, and pull in information from the relevant ones.**

After attention, the vector for "bank" is updated to include information from "river" (or "money"). Now it's a **context-aware** vector.

### 2.2 The intuition: Query, Key, Value (library analogy)

Think of a search in a library:

| Name | Question it answers | Analogy |
|---|---|---|
| **Query (Q)** | "What am I looking for?" | What you type in the search box |
| **Key (K)** | "What do I contain / what am I about?" | The title/label on each book |
| **Value (V)** | "What information do I actually give?" | The content inside the book |

Every word plays **all three roles**:
- As a **Query**, it asks: "which words are relevant to me?"
- As a **Key**, it advertises: "here is what I'm about."
- As a **Value**, it provides: "here's the information you get if you pay attention to me."

Match = **dot product of Query with Key** (Part 1.5! similar → big number).

### 2.3 Step 0: Softmax (a tool we need first)

Softmax turns any list of numbers into **percentages that add up to 1**. Bigger numbers get bigger shares.

```
softmax(x_i) = e^(x_i) / sum of all e^(x_j)
```
(`e ≈ 2.718`. `e^x` is always positive and grows fast.)

Example: `softmax([2, 1, 0.1])`
```
e^2   = 7.389
e^1   = 2.718
e^0.1 = 1.105
sum   = 11.212

→ [7.389/11.212, 2.718/11.212, 1.105/11.212]
→ [0.659, 0.242, 0.099]      (adds up to 1.0 ✓)
```

These are the **attention weights**: "spend 65.9% of your attention here, 24.2% there...".

### 2.4 The attention formula

The whole thing, in one line (from the famous 2017 paper *"Attention Is All You Need"*):

```
Attention(Q, K, V) = softmax( Q · Kᵀ / sqrt(d_k) ) · V
```

Don't panic. It's 5 simple steps:

| Step | Operation | Plain English |
|---|---|---|
| 1 | `Q = X·W_Q`, `K = X·W_K`, `V = X·W_V` | Make a query, key and value vector for every word |
| 2 | `scores = Q · Kᵀ` | Dot product of every query with every key → how relevant is each word to each other word |
| 3 | `scores / sqrt(d_k)` | Shrink the numbers so softmax doesn't get too extreme |
| 4 | `weights = softmax(scores)` | Turn scores into percentages (per row) |
| 5 | `output = weights · V` | Each word's new vector = weighted mix of all value vectors |

`d_k` = the dimension of the key vectors. `Kᵀ` = K "transposed" (rows become columns) so the dot products line up.

### 2.5 Worked example by hand ⭐

Sentence: **"the cat sat"**. Let's compute the new vector for **"sat"**.
To keep maths easy, use 2D vectors and assume steps 1 is already done:

```
Queries:          Keys:             Values:
                  the = [0, 1]      the = [1, 0]
sat = [1, 0]      cat = [1, 0]      cat = [0, 2]
                  sat = [1, 1]      sat = [1, 1]
d_k = 2
```

**Step 2 — scores (query of "sat" · each key):**
```
sat · the = 1×0 + 0×1 = 0
sat · cat = 1×1 + 0×0 = 1
sat · sat = 1×1 + 0×1 = 1
scores = [0, 1, 1]
```

**Step 3 — scale by sqrt(2) ≈ 1.414:**
```
[0/1.414, 1/1.414, 1/1.414] = [0, 0.707, 0.707]
```

**Step 4 — softmax:**
```
e^0     = 1.000
e^0.707 = 2.028
e^0.707 = 2.028
sum     = 5.056
weights = [0.198, 0.401, 0.401]
```
"sat" pays ~20% attention to "the", ~40% to "cat", ~40% to itself. Makes sense: *who* sat? The cat.

**Step 5 — weighted sum of values:**
```
0.198 × [1, 0] = [0.198, 0.000]
0.401 × [0, 2] = [0.000, 0.802]
0.401 × [1, 1] = [0.401, 0.401]
                 ---------------
new "sat"      = [0.599, 1.203]
```

That's it. The new vector for "sat" now contains information from "cat". **This is attention.**
In the real thing, this is done for every word at the same time using matrices.

### 2.6 Where do Q, K, V come from? (Step 1)

Each word starts with just one vector `x` (its embedding). We create Q, K, V by multiplying it by three **learned matrices**:

```
Q = X @ W_Q
K = X @ W_K
V = X @ W_V
```

`X` has shape `(num_words, d_model)`. The model learns `W_Q, W_K, W_V` during training.
Why three different matrices? Because "what I'm looking for" (Q), "what I'm about" (K) and "what I give" (V) are **different jobs**, so they need different transformations.

### 2.7 Why divide by sqrt(d_k)?

With big vectors (say 512 dims), dot products become huge numbers (like 40, 60). Softmax of huge numbers gives something like `[0.0000, 1.0000, 0.0000]` — all attention on one word, and the model stops learning well. Dividing by `sqrt(d_k)` keeps the numbers in a sensible range.

### 2.8 Causal mask (for GPT-style models)

When predicting the next word, a word **must not look at future words** (that's cheating — the future is what we're predicting).
So before softmax, we set the scores for future words to `-infinity`. Since `e^(-inf) = 0`, they get 0% attention.

```
           the   cat   sat
the     [  ok   -inf  -inf ]
cat     [  ok    ok   -inf ]
sat     [  ok    ok    ok  ]
```

### 2.9 Multi-head attention

One attention computation can only focus on one "kind" of relationship at a time. But language has many:
- grammar (which noun does this verb belong to?)
- meaning (what does "it" refer to?)
- position (what word came just before?)

**Solution:** run attention several times in parallel (e.g. 8 or 12 "heads"), each with its own `W_Q, W_K, W_V`. Each head is smaller (`d_model / num_heads` dims). Then **concatenate** (glue) all head outputs together and multiply by one more matrix `W_O`.

```
head_i = Attention(X·W_Q_i, X·W_K_i, X·W_V_i)
MultiHead(X) = concat(head_1, ..., head_h) · W_O
```

### 2.10 Code: Attention from scratch

```python
import numpy as np

def softmax(x):
    # subtract max for numerical stability (doesn't change the result)
    e = np.exp(x - x.max(axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)

def attention(Q, K, V, mask=None):
    d_k = Q.shape[-1]
    scores = Q @ K.T / np.sqrt(d_k)          # (n, n)
    if mask is not None:
        scores = np.where(mask, scores, -np.inf)
    weights = softmax(scores)                # (n, n), each row sums to 1
    return weights @ V, weights              # (n, d_v)

# --- Check our hand example ---
K = np.array([[0, 1], [1, 0], [1, 1]], dtype=float)  # the, cat, sat
V = np.array([[1, 0], [0, 2], [1, 1]], dtype=float)
Q_sat = np.array([[1, 0]], dtype=float)
out, w = attention(Q_sat, K, V)
print(w.round(3))    # [[0.198 0.401 0.401]]
print(out.round(3))  # [[0.599 1.203]]

# --- Full self-attention with learned-style weights ---
np.random.seed(0)
n_words, d_model = 3, 4
X = np.random.randn(n_words, d_model)       # word embeddings
W_Q = np.random.randn(d_model, d_model)
W_K = np.random.randn(d_model, d_model)
W_V = np.random.randn(d_model, d_model)

Q, K, V = X @ W_Q, X @ W_K, X @ W_V
causal_mask = np.tril(np.ones((n_words, n_words), dtype=bool))
out, w = attention(Q, K, V, mask=causal_mask)
print(w.round(2))    # upper triangle is 0 → no looking into the future
print(out.shape)     # (3, 4) → same shape as X
```

**Notice:** the output has the **same shape** as the input. Attention doesn't change the number of words or dimensions; it just updates each word's vector with context.

### ✏️ Exercises — Part 2
1. By hand: `softmax([1, 1, 1])` = ? Why does that make sense?
2. By hand: repeat the worked example (2.5), but for query **"the" = [0, 1]**. Which word gets the most attention?
3. In the causal mask, how much attention can the **first** word pay to itself? Why?
4. Code: implement `multi_head_attention(X, num_heads)` using the `attention` function above. Split `d_model` into `num_heads` pieces, run attention per head, concatenate.
5. Explain in your own words (2–3 lines): what are Q, K and V?

<details><summary>Answers</summary>

1. `[0.333, 0.333, 0.333]` — equal scores → equal attention.
2. scores `[1, 0, 1]` → scaled `[0.707, 0, 0.707]` → weights `[0.401, 0.198, 0.401]`. "the" and "sat" tie.
3. 100% (weight = 1.0) — it's the only word it's allowed to see.
</details>

---

## Part 3 — Feed-Forward Neural Network (FFNN)

### 3.1 Why do we need it?

Attention **moves information between words**. But look at what it actually computes: a weighted **average** of value vectors. Averages are simple — they mix, they don't really "think".

The FFNN is where each word **processes** what it gathered. Researchers have found that FFN layers act a lot like the model's **memory of facts** ("Paris" → "capital of France").

Rule to remember:
> **Attention = words talk to each other.**
> **FFNN = each word thinks by itself.** (same network, applied to every word separately)

### 3.2 A single neuron

The smallest unit. It takes a vector, and outputs one number:

```
output = activation( w · x + b )
```

- `x` = input vector
- `w` = weights (a vector, learned) → how important each input is
- `b` = bias (a number, learned) → a shift
- `w · x` = dot product (Part 1.5 again!)
- `activation` = a simple non-linear function (next section)

Example: `x = [1, 2]`, `w = [0.5, -1]`, `b = 1`
```
w · x + b = 0.5×1 + (-1)×2 + 1 = 0.5 - 2 + 1 = -0.5
```

### 3.3 Activation functions (why non-linearity matters)

**ReLU** — the simplest: keep positives, turn negatives into 0.
```
ReLU(x) = max(0, x)

ReLU(3)    = 3
ReLU(-0.5) = 0
```

Transformers usually use **GELU**, which is a smooth version of ReLU. Same idea.

**Why do we need it at all?** Without it, stacking layers is useless:
```
(x @ W1) @ W2 = x @ (W1 @ W2) = x @ W_single
```
Two matrix multiplications in a row = one matrix multiplication. You'd only ever be able to learn straight-line relationships.
Putting a non-linear function in between breaks this, and lets the network learn curved, complex patterns.

### 3.4 A layer = many neurons at once = a matrix

Put many neurons side by side and you get a **layer**. Their weight vectors become the columns of a matrix:

```
layer(x) = activation( x @ W + b )
```

(This is exactly the vector × matrix from Part 1.7.)

### 3.5 The FFNN inside a Transformer

It's just **two layers**: expand, activate, shrink back.

```
FFN(x) = ReLU(x @ W1 + b1) @ W2 + b2

x     : (d_model,)            e.g. 512
W1    : (d_model, d_ff)       e.g. 512 → 2048   (expand 4×)
W2    : (d_ff, d_model)       e.g. 2048 → 512   (shrink back)
output: (d_model,)            same size as input ✓
```

Why expand to 4× bigger? More room in the middle = more "neurons" = more patterns and facts it can detect and store. Then it compresses back so the next block receives the same size.

### 3.6 Worked example by hand ⭐

```
x  = [1, 2]

W1 = [[1, -1,  0],        b1 = [0, 0, 0]
      [0,  1, -1]]        (2 → 3, expand)

W2 = [[1, 0],             b2 = [0, 0]
      [0, 1],             (3 → 2, shrink)
      [1, 1]]
```

**Layer 1:** `x @ W1`
```
col0: 1×1  + 2×0  =  1
col1: 1×-1 + 2×1  =  1
col2: 1×0  + 2×-1 = -2
→ [1, 1, -2]
```
**ReLU:** `[1, 1, 0]`   ← the -2 became 0: that neuron "didn't fire"

**Layer 2:** `[1, 1, 0] @ W2`
```
col0: 1×1 + 1×0 + 0×1 = 1
col1: 1×0 + 1×1 + 0×1 = 1
→ [1, 1]
```
Input `[1, 2]` → output `[1, 1]`. Same size. ✓

### 3.7 How does it learn? (short version)

1. Start with random weights.
2. Make a prediction (e.g. next word).
3. Measure how wrong it was → a number called the **loss**.
4. Calculus (**backpropagation**) tells us, for every weight, "nudge it up or down to reduce the loss?"
5. Nudge all weights a tiny bit (**gradient descent**). Repeat billions of times.

That's how `W_Q, W_K, W_V, W1, W2` and the embeddings all get their values. You don't need the calculus today — just know this loop exists.

### 3.8 Code: FFNN from scratch

```python
import numpy as np

def relu(x):
    return np.maximum(0, x)

def ffn(x, W1, b1, W2, b2):
    return relu(x @ W1 + b1) @ W2 + b2

# --- Check the hand example ---
x  = np.array([1, 2], dtype=float)
W1 = np.array([[1, -1, 0], [0, 1, -1]], dtype=float)
b1 = np.zeros(3)
W2 = np.array([[1, 0], [0, 1], [1, 1]], dtype=float)
b2 = np.zeros(2)
print(ffn(x, W1, b1, W2, b2))     # [1. 1.]

# --- Applied to every word at once (rows = words) ---
X = np.random.randn(3, 2)          # 3 words, 2 dims
print(ffn(X, W1, b1, W2, b2).shape)  # (3, 2) → each word processed separately
```

### ✏️ Exercises — Part 3
1. By hand: `ReLU([-3, 0, 2.5, -0.1])` = ?
2. By hand: run the example in 3.6 with `x = [2, 1]`.
3. If `d_model = 768` and `d_ff = 3072`, how many numbers are in `W1`? In `W2`? (This is why models have billions of parameters.)
4. Code: verify with numpy that `(x @ W1) @ W2` equals `x @ (W1 @ W2)` for random matrices. Then add ReLU in the middle and show it's no longer equal.

<details><summary>Answers</summary>

1. `[0, 0, 2.5, 0]`
2. `x@W1 = [2, -1, -1]` → ReLU `[2, 0, 0]` → `@W2 = [2, 0]`
3. `768 × 3072 = 2,359,296` each.
</details>

---

## Part 4 — Putting It Together: One Transformer Block

### 4.1 Two small extras

**Residual connection ("skip connection"):** add the input back to the output.
```
x = x + Attention(x)
```
Meaning: "keep what you already knew, and **add** the new info on top." Without this, deep models forget the original word and are very hard to train.

**Layer Normalization:** rescale each word's vector so its values have mean 0 and standard deviation 1. It keeps the numbers from exploding or shrinking as they pass through many layers.

**Positional encoding:** attention by itself has no idea of word order ("cat sat" vs "sat cat" look the same to it). So we add a position vector to each word embedding at the start: `x = embedding(word) + position_vector(index)`.

### 4.2 The full block

```
input X  (n_words, d_model)
   │
   ├─────────────┐
   ▼             │
LayerNorm        │
   ▼             │
Multi-Head       │
Attention        │
   ▼             │
   + ◄───────────┘   residual
   │
   ├─────────────┐
   ▼             │
LayerNorm        │
   ▼             │
  FFNN           │
   ▼             │
   + ◄───────────┘   residual
   │
output X  (n_words, d_model)   ← same shape, now smarter
```

GPT-style models stack this block many times (GPT-2 small: 12 blocks, big models: 80+).

### 4.3 Code: one full block

```python
import numpy as np

def softmax(x):
    e = np.exp(x - x.max(axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)

def layer_norm(x, eps=1e-5):
    mean = x.mean(axis=-1, keepdims=True)
    std  = x.std(axis=-1, keepdims=True)
    return (x - mean) / (std + eps)

def attention(Q, K, V, mask):
    scores = Q @ K.T / np.sqrt(Q.shape[-1])
    scores = np.where(mask, scores, -np.inf)
    return softmax(scores) @ V

def transformer_block(X, p):
    n = X.shape[0]
    mask = np.tril(np.ones((n, n), dtype=bool))

    # 1) Attention sub-layer: words talk to each other
    h = layer_norm(X)
    X = X + attention(h @ p["W_Q"], h @ p["W_K"], h @ p["W_V"], mask) @ p["W_O"]

    # 2) FFNN sub-layer: each word thinks alone
    h = layer_norm(X)
    X = X + np.maximum(0, h @ p["W1"] + p["b1"]) @ p["W2"] + p["b2"]
    return X

np.random.seed(42)
n_words, d_model, d_ff = 3, 8, 32
p = {
    "W_Q": np.random.randn(d_model, d_model) * 0.1,
    "W_K": np.random.randn(d_model, d_model) * 0.1,
    "W_V": np.random.randn(d_model, d_model) * 0.1,
    "W_O": np.random.randn(d_model, d_model) * 0.1,
    "W1":  np.random.randn(d_model, d_ff) * 0.1,
    "b1":  np.zeros(d_ff),
    "W2":  np.random.randn(d_ff, d_model) * 0.1,
    "b2":  np.zeros(d_model),
}
X = np.random.randn(n_words, d_model)   # pretend these are word embeddings
out = transformer_block(X, p)
print(out.shape)   # (3, 8)
```

You've now written the core of a GPT in ~30 lines. The real ones are the same thing, with bigger numbers, multi-head attention, and trained weights.

---

## Final Checklist

Tick these off only when you can **explain them out loud without looking**:

**Vectors**
- [ ] What a vector is, and why words are turned into vectors (embeddings)
- [ ] How to compute a dot product by hand, and what a big/small/negative value means
- [ ] Cosine similarity and why we divide by the lengths
- [ ] Matrix multiplication and the shape rule `(a,b) @ (b,c) → (a,c)`

**Attention**
- [ ] The problem it solves (context: "river bank" vs "money bank")
- [ ] What Q, K, V are (library analogy)
- [ ] The formula `softmax(QKᵀ / sqrt(d_k)) V` — each of the 5 steps
- [ ] Softmax by hand
- [ ] Why we scale by `sqrt(d_k)`, why the causal mask exists, why multiple heads

**FFNN**
- [ ] A neuron: `activation(w·x + b)`
- [ ] Why we need a non-linear activation (ReLU/GELU)
- [ ] The expand → activate → shrink structure, and that it runs on each word separately
- [ ] Attention = talk, FFNN = think

**Block**
- [ ] Residual connections, LayerNorm, positional encoding — one line each
- [ ] Draw the Transformer block from memory

---

## Interview practice
Once the checklist is done, test yourself with [INTERVIEW_QUESTIONS.md](INTERVIEW_QUESTIONS.md) (100 questions with answers).

## Where to go next
- **Watch:** 3Blue1Brown — *"But what is a GPT?"* and *"Attention in transformers, visually explained"* (YouTube)
- **Read:** Jay Alammar — *"The Illustrated Transformer"*
- **Paper:** Vaswani et al., 2017 — *"Attention Is All You Need"* (read it after this file; it'll make sense now)
- **Build:** Andrej Karpathy — *"Let's build GPT: from scratch, in code, spelled out"* (YouTube)
