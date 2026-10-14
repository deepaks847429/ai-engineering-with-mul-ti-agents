# 100 Interview Questions: Vectors, Attention, FFNN & Transformers

> Companion to [README.md](README.md). Finish the README first, then use this file for practice.

**How to practise**
1. Read the question and **answer it out loud** (or on paper) as if you were in the interview.
2. Only then open the answer and compare.
3. Mark the ones you got wrong and come back to them tomorrow.

**Difficulty:** 🟢 Easy (every candidate must know) · 🟡 Medium (asked for ML/AI engineer roles) · 🔴 Hard (senior roles and research labs)

| Section | Questions |
|---|---|
| [A. Vectors & Embeddings](#a-vectors--embeddings-125) | 1–25 |
| [B. Attention](#b-attention-2665) | 26–65 |
| [C. Feed-Forward Networks](#c-feed-forward-networks-6682) | 66–82 |
| [D. The Full Transformer & Practical Questions](#d-the-full-transformer--practical-questions-83100) | 83–100 |

---

## A. Vectors & Embeddings (1–25)

**1. 🟢 What is a vector, and why do ML models represent data as vectors?**
<details><summary>Answer</summary>

An ordered list of numbers, which you can picture as a point or arrow in n-dimensional space. Models can only do arithmetic, so all data (words, images, users) must become numbers. Vectors let us measure similarity (dot product, distance) and transform data (matrix multiplication), and that is all a neural net does.
</details>

**2. 🟢 What is the difference between one-hot encoding and a dense embedding?**
<details><summary>Answer</summary>

One-hot: a vector as long as the vocabulary, all zeros except a single 1. It is huge and sparse, and every pair of words is equally different (dot product = 0), so it carries no meaning.
Dense embedding: a short vector (e.g. 768 dims) of learned real numbers where similar words end up close together.
</details>

**3. 🟢 What is a dot product, and what do its sign and size tell you?**
<details><summary>Answer</summary>

`a·b = Σ aᵢbᵢ` = `|a||b|cos θ`. Large positive = the vectors point the same way (similar). About 0 = at right angles (unrelated). Negative = opposite. The size also grows with the vectors' lengths.
</details>

**4. 🟢 Dot product vs cosine similarity: when do you use which?**
<details><summary>Answer</summary>

Cosine = dot product divided by both lengths, so it measures **direction only** and always lies in [-1, 1]. Use cosine when length is noise (e.g. comparing documents of different sizes). Use the raw dot product when length carries signal, or when vectors are already normalised (then the two are identical and the dot product is cheaper). Attention uses the raw, scaled dot product.
</details>

**5. 🟡 How does Euclidean distance relate to cosine similarity?**
<details><summary>Answer</summary>

For unit-length vectors: `‖a − b‖² = 2 − 2·cos(a, b)`. So once vectors are normalised, ranking by Euclidean distance and ranking by cosine similarity give the **same order**.
</details>

**6. 🟢 What is the shape rule for matrix multiplication? What is the shape of `(B, T, C) @ (C, H)`?**
<details><summary>Answer</summary>

`(a, b) @ (b, c) → (a, c)`. The inner dimensions must match. For batched tensors the last dimension is multiplied out: `(B, T, C) @ (C, H) → (B, T, H)`.
</details>

**7. 🟢 What is an embedding layer and how is it implemented?**
<details><summary>Answer</summary>

A learned matrix `E` of shape `(vocab_size, d_model)`. For token ID `i` you take row `i`. Mathematically that equals `one_hot(i) @ E`, but in practice it is a fast table lookup (indexing).
</details>

**8. 🟢 How are embeddings learned?**
<details><summary>Answer</summary>

They start random and are updated by backpropagation along with every other weight, to minimise the training loss (e.g. next-token prediction). Words used in similar contexts receive similar gradient updates, so they drift close together.
</details>

**9. 🟡 Word2Vec: what is the difference between CBOW and Skip-gram?**
<details><summary>Answer</summary>

CBOW predicts the centre word from the surrounding words. It is faster and good for frequent words.
Skip-gram predicts the surrounding words from the centre word. It is slower but better for rare words.
Both are shallow networks whose learned weights are the embeddings.
</details>

**10. 🟡 Why does `king − man + woman ≈ queen` work?**
<details><summary>Answer</summary>

Training makes consistent relationships show up as consistent **directions** in the space. The "male → female" offset is roughly the same vector for many word pairs, so adding it to "king" lands near "queen". This works approximately, not perfectly.
</details>

**11. 🟡 Static vs contextual embeddings?**
<details><summary>Answer</summary>

Static (Word2Vec, GloVe) gives one vector per word regardless of context, so "bank" is the same in "river bank" and "bank account".
Contextual (BERT, GPT hidden states) gives a vector that depends on the surrounding sentence. Attention is what makes them contextual.
</details>

**12. 🟡 What is tokenization, and why do modern models use subword tokens (BPE, WordPiece)?**
<details><summary>Answer</summary>

Tokenization splits text into units that each get an ID. Whole-word vocabularies are huge and cannot handle unseen words. Character-level vocabularies make sequences very long. Subwords are the middle ground: frequent words are single tokens, and rare words split into pieces (`"unhappiness" → "un", "happi", "ness"`), so there is never an unknown word.
</details>

**13. 🟢 How does vocabulary size affect model size?**
<details><summary>Answer</summary>

The embedding matrix has `V × d` parameters (and the output layer has another `V × d` unless the two are tied). With V = 50k and d = 4096 that is about 205M parameters per matrix. A bigger vocabulary means shorter sequences but more parameters and a costlier softmax.
</details>

**14. 🟡 What is weight tying?**
<details><summary>Answer</summary>

Using the same matrix for the input embedding and the output (unembedding) projection. It saves `V × d` parameters and often improves results, since both layers map between tokens and the same vector space.
</details>

**15. 🟡 How do you choose the embedding dimension?**
<details><summary>Answer</summary>

It is a trade-off. Bigger means more capacity to encode nuance, but more parameters, compute and risk of overfitting on small data. In transformers `d_model` scales with model size (768 for GPT-2 small, 12288 for GPT-3). Pick it empirically and with scaling laws.
</details>

**16. 🔴 Why are random high-dimensional vectors almost orthogonal, and why does that matter?**
<details><summary>Answer</summary>

For random unit vectors in d dimensions, the cosine similarity concentrates around 0 with standard deviation about `1/√d`. In high dimensions you can therefore fit far more "nearly independent" directions than there are dimensions. This lets models store many features in superposition, and it also means that distances between random points become less informative (the curse of dimensionality).
</details>

**17. 🟡 What does multiplying a vector by a matrix do geometrically?**
<details><summary>Answer</summary>

It applies a linear transformation: rotating, scaling, stretching, projecting or changing dimension. `W_Q`, `W_K` and `W_V` project the same embedding into different "views" of it.
</details>

**18. 🟢 Why do transformers need positional encodings?**
<details><summary>Answer</summary>

Self-attention treats its input as a **set**: shuffle the words and each word gets the same output, just in the shuffled order (permutation-equivariance). Without position information, "dog bites man" and "man bites dog" would look identical. So we inject position information into the vectors.
</details>

**19. 🟡 How does the sinusoidal positional encoding work?**
<details><summary>Answer</summary>

`PE(pos, 2i) = sin(pos / 10000^(2i/d))` and `PE(pos, 2i+1) = cos(pos / 10000^(2i/d))`, added to the embeddings. Each dimension pair oscillates at a different frequency (like the hands of a clock). It has no learned parameters, and `PE(pos + k)` is a linear function of `PE(pos)`, which makes relative offsets easy to learn.
</details>

**20. 🔴 Learned absolute vs relative positional encodings (RoPE, ALiBi)?**
<details><summary>Answer</summary>

Learned absolute: one trained vector per position (GPT-2, BERT). It is simple but cannot handle positions longer than it saw in training.
Relative: encodes the *distance* between tokens rather than their absolute index. RoPE rotates Q and K. ALiBi adds a distance-based penalty to the attention scores. Both generalise to longer contexts better, and most modern LLMs use RoPE.
</details>

**21. 🔴 How does RoPE (Rotary Position Embedding) work?**
<details><summary>Answer</summary>

It splits Q and K into 2D pairs and rotates each pair by an angle of `position × frequency`. The dot product of two rotated vectors depends only on the **difference** in their rotation angles, so the attention score depends on relative position `m − n`. It is applied to Q and K only, never to V.
</details>

**22. 🟡 How do you get one embedding for a whole sentence from a transformer?**
<details><summary>Answer</summary>

Common options: mean-pool all the token vectors; use a special `[CLS]` token's vector (BERT); or use the last token's vector (decoder models). Models fine-tuned with a contrastive loss (Sentence-BERT, E5 and similar) produce much better sentence embeddings than raw pooling.
</details>

**23. 🔴 What is anisotropy in embeddings?**
<details><summary>Answer</summary>

Raw transformer embeddings often occupy a narrow cone, so even unrelated sentences have high cosine similarity (e.g. 0.7 or more). This hurts similarity search. Fixes include contrastive fine-tuning, whitening, and subtracting the mean vector.
</details>

**24. 🟡 How do you search millions of embeddings quickly?**
<details><summary>Answer</summary>

Use Approximate Nearest Neighbour (ANN) indexes such as HNSW (graph-based), IVF (clustering) or product quantisation, via libraries like FAISS or vector databases. They trade a little accuracy for large speed-ups over brute-force O(N) comparison.
</details>

**25. 🟢 Why normalise embeddings before a similarity search?**
<details><summary>Answer</summary>

After L2-normalisation the dot product equals cosine similarity, so you can use fast dot-product (maximum inner product) search. It also stops long vectors from dominating the results.
</details>

---

## B. Attention (26–65)

**26. 🟢 What problem does attention solve compared with RNNs?**
<details><summary>Answer</summary>

An RNN squeezes the whole past into one fixed-size hidden state, updated one step at a time. Information from far back fades (vanishing gradients), and the steps can't run in parallel. Attention lets every token look **directly** at every other token in one step, so long-range dependencies are easy and all positions are computed in parallel.
</details>

**27. 🟢 Explain Query, Key and Value intuitively.**
<details><summary>Answer</summary>

Think of a library. **Query** = what I'm looking for. **Key** = the label that says what each token is about. **Value** = the content a token hands over. The score between a query and a key decides *how much* of each value you take.
</details>

**28. 🟢 Write the scaled dot-product attention formula and explain each part.**
<details><summary>Answer</summary>

`Attention(Q, K, V) = softmax(QKᵀ / √d_k) V`
`QKᵀ` gives every query–key similarity, an `(n, n)` matrix. `/√d_k` keeps the scale sensible. `softmax` turns each row into weights that sum to 1. `@ V` takes the weighted average of the value vectors.
</details>

**29. 🟡 Why divide by √d_k? Derive it.**
<details><summary>Answer</summary>

If the entries of q and k are independent with mean 0 and variance 1, then `q·k` is a sum of d_k terms each with variance 1, so `Var(q·k) = d_k` and the standard deviation is `√d_k`. Large scores push softmax into saturation (almost one-hot), where gradients are tiny. Dividing by `√d_k` brings the variance back to 1.
</details>

**30. 🟢 What does softmax do? Why not just divide each score by the sum?**
<details><summary>Answer</summary>

It turns any real numbers into positive weights that sum to 1. Plain division breaks with negative scores (and when the sum is zero). The exponential makes everything positive, emphasises the largest scores, and is differentiable everywhere.
</details>

**31. 🟡 Why do implementations subtract the max before the softmax exponential?**
<details><summary>Answer</summary>

`e^1000` overflows to infinity. Since `softmax(x) = softmax(x − c)` for any constant c, subtracting `max(x)` makes the largest exponent `e^0 = 1`, which prevents overflow without changing the result.
</details>

**32. 🟡 Why use separate W_Q, W_K, W_V instead of the embeddings directly?**
<details><summary>Answer</summary>

Using X directly gives `XXᵀ`, which is symmetric (A attends to B exactly as much as B to A), and every token attends most to itself. Separate projections allow **asymmetric** relationships (a verb looking for its subject is different from the subject looking for its verb). They also separate "what I search for" from "what I advertise" and "what I pass on".
</details>

**33. 🟢 Self-attention vs cross-attention?**
<details><summary>Answer</summary>

In self-attention, Q, K and V all come from the same sequence. In cross-attention, Q comes from one sequence and K, V come from another (e.g. a translation decoder attending to the source sentence, or text attending to image features).
</details>

**34. 🟢 What is causal (masked) attention, and how is it implemented?**
<details><summary>Answer</summary>

In a decoder, token i may only attend to tokens ≤ i, so it can't peek at the answer during training. Before the softmax, set the scores above the diagonal to `−∞`. Since `e^(−∞) = 0`, those positions get zero weight. It is implemented with a lower-triangular boolean mask.
</details>

**35. 🟡 Padding mask vs causal mask?**
<details><summary>Answer</summary>

A padding mask hides the `[PAD]` tokens added to make sequences in a batch the same length. It depends on the data. A causal mask hides future positions and is always the same triangle. Decoders in batched training usually apply both.
</details>

**36. 🟢 What is multi-head attention, and why use it?**
<details><summary>Answer</summary>

It runs h attention operations in parallel, each with its own smaller `W_Q`, `W_K`, `W_V`, then concatenates the results and applies `W_O`. Different heads can specialise (syntax, coreference, previous token and so on), whereas a single softmax can only express one weighting pattern per token.
</details>

**37. 🟡 With d_model = 512 and 8 heads, what is each head's dimension? Is multi-head attention more expensive than single-head?**
<details><summary>Answer</summary>

`512 / 8 = 64` per head. The total parameters and FLOPs are about the same as one head of size 512. You split the same dimensions into several heads rather than adding more.
</details>

**38. 🟡 What does the output projection W_O do?**
<details><summary>Answer</summary>

After concatenation, each head's output sits in its own slice of the vector. `W_O` (`d_model × d_model`) mixes information across heads and maps the result back into the residual stream's space.
</details>

**39. 🟡 What are the time and memory complexity of self-attention?**
<details><summary>Answer</summary>

Time is `O(n² · d)`: every one of n tokens is compared with every other. Memory is `O(n²)` for the attention matrix (per head). This quadratic cost in sequence length n is the main bottleneck for long contexts.
</details>

**40. 🟢 Why can attention be parallelised when RNNs can't?**
<details><summary>Answer</summary>

An RNN's step t needs the hidden state from step t−1, which forces sequential computation. In attention, every output is computed from the same input matrices with big matrix multiplications, and GPUs are built for exactly that. (During training, the causal mask keeps this parallel even for decoders.)
</details>

**41. 🔴 Is self-attention permutation-invariant or permutation-equivariant?**
<details><summary>Answer</summary>

Equivariant: permute the input tokens and the outputs are permuted in the same way. (Invariant would mean the output doesn't change at all, which is true only after pooling.) This is why positional information must be added.
</details>

**42. 🟢 What shape is the attention weight matrix, and what property do its rows have?**
<details><summary>Answer</summary>

`(n_queries, n_keys)` per head, `(n, n)` for self-attention. Each row sums to 1 and every entry is ≥ 0. Row i is how token i spreads its attention.
</details>

**43. 🔴 Can attention weights be used to explain a model's decisions?**
<details><summary>Answer</summary>

Only with caution. Research ("Attention is not Explanation", among others) shows that different attention patterns can give the same prediction, and the weights ignore the value vector norms, the later layers and the FFN contributions. They are a useful hint, not a faithful explanation. Gradient-based or causal methods are more reliable.
</details>

**44. 🟡 Additive (Bahdanau) vs multiplicative (dot-product) attention?**
<details><summary>Answer</summary>

Additive: `score = vᵀ tanh(W₁q + W₂k)`, a small neural network. Multiplicative: `score = q·k`. Dot-product attention is much faster and more memory-efficient because it is one big matrix multiplication. With scaling by `√d_k` it performs as well, so transformers use it.
</details>

**45. 🟡 What is the KV cache and why does it speed up inference?**
<details><summary>Answer</summary>

When generating token t, the keys and values of tokens 1…t−1 haven't changed. The KV cache stores them so each new step computes Q, K, V for the new token only and attends over the cached K and V. Without it, each step would recompute the whole prefix, which is quadratic waste.
</details>

**46. 🔴 How much memory does the KV cache use?**
<details><summary>Answer</summary>

`2 (K and V) × n_layers × n_kv_heads × d_head × seq_len × batch × bytes_per_value`.
Example: 32 layers, 32 heads, d_head 128, 4k tokens, fp16 gives `2·32·32·128·4096·2` bytes ≈ **2 GB per sequence**. That is why MQA and GQA exist.
</details>

**47. 🔴 Multi-Query Attention (MQA) vs Grouped-Query Attention (GQA)?**
<details><summary>Answer</summary>

MQA: all query heads share **one** K/V head, which shrinks the KV cache by a factor of h but can lose some quality.
GQA: query heads are split into g groups, each sharing one K/V head. It is the middle ground and is used in Llama 2/3, Mistral and others.
</details>

**48. 🔴 What is FlashAttention?**
<details><summary>Answer</summary>

An exact (not approximate) attention algorithm that is aware of the GPU memory hierarchy. It tiles Q, K and V into blocks that fit in fast on-chip SRAM, computes the softmax incrementally ("online softmax"), and never writes the full `n × n` matrix to slow GPU memory (HBM). The result is the same output, much faster, with memory linear in n.
</details>

**49. 🔴 What are sparse, local and sliding-window attention?**
<details><summary>Answer</summary>

Each token attends only to a subset of positions: a window of the last w tokens (Mistral, Longformer), plus some global tokens or strided patterns (BigBird, Sparse Transformer). The cost drops from `O(n²)` to `O(n·w)`. Stacking layers still lets information travel far.
</details>

**50. 🔴 What is linear attention?**
<details><summary>Answer</summary>

It replaces `softmax(QKᵀ)V` with `φ(Q)(φ(K)ᵀV)` for some feature map φ. Computing `φ(K)ᵀV` first gives a `d × d` matrix, so the cost is `O(n·d²)`, linear in n. The trade-off is usually some loss in quality. Related ideas appear in RNN-like models (RetNet, and state-space models such as Mamba).
</details>

**51. 🟢 What happens if all attention scores for a query are equal?**
<details><summary>Answer</summary>

The softmax gives uniform weights `1/n`, so the output is the plain **average** of all value vectors.
</details>

**52. 🟡 What would happen if you removed the softmax?**
<details><summary>Answer</summary>

The weights would no longer be positive or sum to 1. Outputs could grow without bound as sequences get longer, training becomes unstable, and you lose the "pick the relevant tokens" behaviour. (Linear attention removes it deliberately and compensates with feature maps and normalisation.)
</details>

**53. 🔴 What is an "attention sink"?**
<details><summary>Answer</summary>

Trained LLMs often put a large amount of attention on the first token(s), even when they are meaningless. Because softmax must sum to 1, heads that have "nothing to attend to" dump their weight there. Evicting those tokens from the KV cache breaks generation, which is why StreamingLLM keeps them.
</details>

**54. 🟡 Encoder-only vs decoder-only vs encoder-decoder: what attention does each use?**
<details><summary>Answer</summary>

Encoder-only (BERT): bidirectional self-attention, with no causal mask. Good for understanding and classification.
Decoder-only (GPT, Llama, Claude-style LLMs): causal self-attention. Good for generation.
Encoder-decoder (T5, the original Transformer): a bidirectional encoder, plus a decoder with causal self-attention and cross-attention to the encoder.
</details>

**55. 🟡 In cross-attention, where do Q, K and V come from?**
<details><summary>Answer</summary>

Q comes from the decoder (what I'm generating needs...), and K and V come from the encoder output (...information from the source). The output has one row per decoder token.
</details>

**56. 🟡 How many parameters does one multi-head attention layer have?**
<details><summary>Answer</summary>

`W_Q`, `W_K`, `W_V` and `W_O` are each `d × d`, giving **4d²** (plus 4d biases if they are used). This doesn't depend on the number of heads. For d = 768 that is about 2.36M.
</details>

**57. 🟢 How does attention handle sequences of different lengths?**
<details><summary>Answer</summary>

Attention itself works for any n, since there are no weights tied to position. In batches, shorter sequences are padded, and a padding mask gives the pads zero attention.
</details>

**58. 🟡 What is the context window, and what limits it?**
<details><summary>Answer</summary>

It is the maximum number of tokens the model can attend over. The limits are the `O(n²)` compute and memory, the size of the KV cache, positional encodings that don't extrapolate beyond the training lengths, and a lack of long training data.
</details>

**59. 🟡 Why mask with −∞ rather than setting the weight to 0 after the softmax?**
<details><summary>Answer</summary>

Masking before the softmax with `−∞` makes those positions exactly 0 **and** re-normalises the remaining weights to sum to 1. Zeroing after the softmax leaves rows summing to less than 1, and the future tokens have already influenced the normalisation. (In practice a large negative number such as −1e9 is used to avoid NaNs.)
</details>

**60. 🟡 What does a temperature T in the softmax do?**
<details><summary>Answer</summary>

`softmax(x / T)`. With T < 1 the distribution is sharper and approaches one-hot. With T > 1 it is flatter and approaches uniform. The `√d_k` scaling is effectively a fixed temperature. At sampling time, temperature controls how random the generated text is.
</details>

**61. 🔴 What are induction heads?**
<details><summary>Answer</summary>

A two-head circuit found by Anthropic's interpretability research. A "previous-token" head plus an induction head implement the rule "if A was followed by B earlier, and I now see A again, predict B". They are thought to be a key mechanism behind in-context learning.
</details>

**62. 🟡 Coding: implement scaled dot-product attention in numpy.**
<details><summary>Answer</summary>

```python
def attention(Q, K, V, mask=None):
    s = Q @ K.T / np.sqrt(Q.shape[-1])
    if mask is not None: s = np.where(mask, s, -1e9)
    s = s - s.max(-1, keepdims=True)
    w = np.exp(s); w /= w.sum(-1, keepdims=True)
    return w @ V
```
Interviewers check: the scaling, max-subtraction, the mask applied before the softmax, and the axis the softmax runs over (keys, the last axis).
</details>

**63. 🔴 Coding: implement multi-head attention with reshape/transpose (no Python loop over heads).**
<details><summary>Answer</summary>

```python
# X: (B, T, D)
q = (X @ Wq).reshape(B, T, h, D//h).transpose(0, 2, 1, 3)  # (B, h, T, dh)
k = (X @ Wk).reshape(B, T, h, D//h).transpose(0, 2, 1, 3)
v = (X @ Wv).reshape(B, T, h, D//h).transpose(0, 2, 1, 3)
s = q @ k.transpose(0, 1, 3, 2) / np.sqrt(D//h)            # (B, h, T, T)
out = softmax(s) @ v                                        # (B, h, T, dh)
out = out.transpose(0, 2, 1, 3).reshape(B, T, D) @ Wo
```
</details>

**64. 🔴 What is attention entropy collapse, and how is it prevented?**
<details><summary>Answer</summary>

During training, the QK logits can grow so large that attention becomes nearly one-hot (very low entropy). Training then becomes unstable, with loss spikes. Fixes include QK-normalisation (LayerNorm or RMSNorm on Q and K), logit soft-capping, lower learning rates and careful initialisation.
</details>

**65. 🟡 How would you inspect or debug attention in a trained model?**
<details><summary>Answer</summary>

Plot the attention matrices as heatmaps per layer and head (tools such as BertViz), check the entropy of each head, ablate heads to see whether performance changes, and look for known patterns (previous-token, attention to punctuation or BOS tokens, induction). Then confirm hypotheses with interventions, because patterns alone can mislead.
</details>

---

## C. Feed-Forward Networks (66–82)

**66. 🟢 What is a single neuron (perceptron)?**
<details><summary>Answer</summary>

`y = activation(w·x + b)`: a weighted sum of the inputs plus a bias, passed through a non-linear function. A layer is many neurons in parallel, which is `activation(xW + b)`.
</details>

**67. 🟢 Why do neural networks need non-linear activations?**
<details><summary>Answer</summary>

Without them, stacked layers collapse into one: `(xW₁)W₂ = x(W₁W₂)`. The whole network could then only learn linear functions. Non-linearity lets it approximate curved, complex functions.
</details>

**68. 🟡 ReLU vs GELU vs SiLU/Swish?**
<details><summary>Answer</summary>

ReLU = `max(0, x)`: simple and fast, but has a sharp corner and outputs 0 for all negative inputs.
GELU = `x·Φ(x)`: a smooth version that lets small negative values through. Used in BERT and GPT-2.
SiLU/Swish = `x·sigmoid(x)`: also smooth. Used inside SwiGLU in Llama.
Smooth activations tend to train slightly better in large transformers.
</details>

**69. 🟡 What is the "dying ReLU" problem?**
<details><summary>Answer</summary>

If a neuron's input is always negative, its output and its gradient are always 0, so it never updates again and is "dead". Causes include large learning rates and bad initialisation. Fixes include Leaky ReLU, GELU and careful initialisation.
</details>

**70. 🟢 Describe the FFN inside a transformer block. Why expand to 4× d_model?**
<details><summary>Answer</summary>

`FFN(x) = act(xW₁ + b₁)W₂ + b₂`, going `d → 4d → d`. The wide hidden layer gives more neurons, meaning more features and patterns the block can detect and store. Projecting back to d keeps the residual stream the same size. The factor 4 is an empirical choice from the original paper.
</details>

**71. 🟢 What does "position-wise" feed-forward mean?**
<details><summary>Answer</summary>

The **same** FFN (same weights) is applied to each token's vector **independently**. Tokens don't interact inside the FFN; all mixing between tokens happens in attention.
</details>

**72. 🟡 How many parameters does the FFN have? Which has more, attention or the FFN?**
<details><summary>Answer</summary>

`2 · d · d_ff`, which is `8d²` when `d_ff = 4d`. Attention has `4d²`. So the FFN holds about **two thirds** of each block's parameters.
</details>

**73. 🔴 What is SwiGLU, and why do Llama models use d_ff ≈ 8/3·d?**
<details><summary>Answer</summary>

`SwiGLU(x) = (SiLU(xW₁) ⊙ xW₃) W₂`: a gated FFN where one projection controls ("gates") the other. It performs better than ReLU or GELU. It uses **three** matrices instead of two, so the hidden size is scaled from `4d` to about `8/3·d` to keep the parameter count the same (`3 · d · 8d/3 = 8d²`).
</details>

**74. 🔴 What role do FFN layers play in what a transformer "knows"?**
<details><summary>Answer</summary>

Research (Geva et al., "Transformer Feed-Forward Layers Are Key-Value Memories") shows that the rows of `W₁` act like **keys** that detect input patterns, and the rows of `W₂` act like **values** that write the associated information into the residual stream. Much factual knowledge seems to be stored in FFNs, which is why fact-editing methods such as ROME edit FFN weights.
</details>

**75. 🟡 What is the universal approximation theorem?**
<details><summary>Answer</summary>

A network with one hidden layer, a non-linear activation and enough neurons can approximate any continuous function on a bounded domain to any accuracy. It says such a network *exists*, but not that training will find it or that it will be efficiently sized. Depth is usually far more efficient than width.
</details>

**76. 🔴 What is a Mixture of Experts (MoE), and how does it change the FFN?**
<details><summary>Answer</summary>

It replaces the single FFN with N expert FFNs plus a small **router** that picks the top-k experts (e.g. 2) for each token. The model can have many total parameters while each token uses only a few, which gives more capacity at roughly the same compute. The challenges are load balancing, routing instability and memory. Mixtral and DeepSeek-V3 use this.
</details>

**77. 🟢 Explain backpropagation simply.**
<details><summary>Answer</summary>

Run a forward pass and compute the loss. Then use the chain rule to work backwards layer by layer, computing how much each weight contributed to the error (its gradient). Then gradient descent nudges every weight in the direction that reduces the loss: `w ← w − lr · ∂L/∂w`.
</details>

**78. 🟡 What are vanishing and exploding gradients, and how do transformers avoid them?**
<details><summary>Answer</summary>

Over many layers, gradients get multiplied many times and can shrink to 0 or blow up. Transformers mitigate this with **residual connections** (a direct path for gradients), **LayerNorm**, careful initialisation, learning-rate warm-up and gradient clipping.
</details>

**79. 🟡 Why not initialise all weights to zero?**
<details><summary>Answer</summary>

Every neuron in a layer would compute the same output and receive the same gradient, so they would stay identical forever (the symmetry problem). Random initialisation breaks the symmetry. Its scale is chosen (Xavier/Glorot, He/Kaiming) to keep activations and gradients at a stable variance.
</details>

**80. 🟢 What is dropout, and where is it used in a transformer?**
<details><summary>Answer</summary>

During training, randomly set a fraction p of activations to zero (and scale the rest by `1/(1−p)`). It reduces overfitting by preventing co-dependence between neurons. It is applied to the attention weights, after the attention and FFN sub-layers, and to the embeddings. Many large LLMs pretrain with dropout set to 0.
</details>

**81. 🟡 Why isn't attention alone enough? Why also have an FFN?**
<details><summary>Answer</summary>

Attention output is a weighted **average** of linearly projected values, and the only non-linearity is in how the weights are chosen. The FFN adds per-token non-linear processing and most of the model's parameters and stored knowledge. Removing FFNs badly hurts performance. The roles are: attention moves information between tokens, and the FFN processes it within each token.
</details>

**82. 🟢 Coding: implement a transformer FFN in PyTorch.**
<details><summary>Answer</summary>

```python
class FFN(nn.Module):
    def __init__(self, d, mult=4, p=0.1):
        super().__init__()
        self.net = nn.Sequential(nn.Linear(d, mult*d), nn.GELU(),
                                 nn.Linear(mult*d, d), nn.Dropout(p))
    def forward(self, x):          # x: (B, T, d)
        return self.net(x)         # nn.Linear acts on the last dim → position-wise
```
</details>

---

## D. The Full Transformer & Practical Questions (83–100)

**83. 🟢 Walk me through a transformer block from input to output.**
<details><summary>Answer</summary>

Input `X (n, d)` → LayerNorm → multi-head self-attention → add the residual (`X + attn`) → LayerNorm → FFN → add the residual. The output has the same shape `(n, d)`. That is Pre-LN, used by modern LLMs. The whole model is embeddings + positions → N blocks → final LayerNorm → linear layer to the vocabulary → softmax.
</details>

**84. 🟢 Why use residual (skip) connections?**
<details><summary>Answer</summary>

`x = x + f(x)`. Each sub-layer only has to learn a *change* to its input, and gradients flow straight through the addition to early layers, which makes deep networks trainable. It also creates a "residual stream" that every layer reads from and writes to.
</details>

**85. 🟡 LayerNorm vs BatchNorm: why do transformers use LayerNorm?**
<details><summary>Answer</summary>

BatchNorm normalises each feature across the **batch**, so it depends on batch statistics and struggles with variable-length sequences, small batches and autoregressive inference. LayerNorm normalises across the **features of one token**, so it is independent of the batch and behaves the same at training and inference time.
</details>

**86. 🔴 Pre-LN vs Post-LN?**
<details><summary>Answer</summary>

Post-LN (the original paper) computes `LN(x + f(x))`. It can reach good final quality but is unstable in deep models and needs learning-rate warm-up.
Pre-LN computes `x + f(LN(x))`. It gives a clean residual path, is much more stable, and is used by GPT-2 onwards and most modern LLMs. Pre-LN needs a final LayerNorm before the output layer.
</details>

**87. 🟡 What is RMSNorm?**
<details><summary>Answer</summary>

LayerNorm without the mean subtraction: `x / RMS(x) · g`, where `RMS(x) = sqrt(mean(x²))`. It is cheaper and works just as well in practice. Llama, Mistral and many others use it.
</details>

**88. 🟢 How does a decoder model turn its final vectors into next-token probabilities?**
<details><summary>Answer</summary>

Take the last position's hidden vector `(d,)` → final norm → multiply by the unembedding matrix `(d, V)` to get **logits** `(V,)` → softmax gives a probability for every token in the vocabulary → sample or pick the next token.
</details>

**89. 🟡 What is the training objective of a GPT-style model?**
<details><summary>Answer</summary>

Next-token prediction with **cross-entropy loss**: `−log P(correct next token)`, averaged over every position. Thanks to the causal mask, a sequence of n tokens gives n training examples in one parallel forward pass. Feeding the true previous tokens during training (rather than the model's own outputs) is called teacher forcing.
</details>

**90. 🔴 Roughly how many parameters does a decoder-only transformer have?**
<details><summary>Answer</summary>

Per block there are `4d²` (attention) + `8d²` (FFN) = `12d²`. The total is about `12 · L · d² + V · d`. For GPT-3: `12 · 96 · 12288² ≈ 174B`, plus embeddings, which gives the stated 175B.
</details>

**91. 🟢 Why did transformers replace RNNs and LSTMs?**
<details><summary>Answer</summary>

Parallel training (much faster on GPUs), direct long-range connections (no information bottleneck, no vanishing gradients over time), and very good scaling: performance keeps improving predictably with more data, parameters and compute.
</details>

**92. 🟡 BERT vs GPT?**
<details><summary>Answer</summary>

BERT is encoder-only with bidirectional attention, trained with masked language modelling (predicting hidden words). It is best for understanding tasks (classification, NER, embeddings).
GPT is decoder-only with causal attention, trained on next-token prediction. It is best for generation, and at scale it is general-purpose.
</details>

**93. 🟡 Explain the decoding strategies: greedy, beam search, top-k, top-p, temperature.**
<details><summary>Answer</summary>

Greedy: always take the most likely token. Deterministic, but often repetitive.
Beam search: keep the b best partial sequences. Good for translation, dull for open-ended chat.
Temperature: sharpens or flattens the distribution.
Top-k: sample only from the k most likely tokens.
Top-p (nucleus): sample from the smallest set of tokens whose probabilities add up to at least p.
</details>

**94. 🔴 What are the prefill and decode phases of inference, and which bottleneck does each have?**
<details><summary>Answer</summary>

Prefill processes the whole prompt in parallel. It is **compute-bound** (big matrix multiplications) and determines time-to-first-token.
Decode generates one token at a time, reading all the weights and the KV cache for each token. It is **memory-bandwidth-bound**. Batching many requests, the KV cache, GQA and quantisation mainly help the decode phase.
</details>

**95. 🔴 Approximately how many FLOPs does it take to train a transformer?**
<details><summary>Answer</summary>

About **6 · N · D**, where N = parameters and D = training tokens (2N for the forward pass, 4N for the backward pass, per token). Inference is about 2N FLOPs per token (plus the attention cost for long contexts). This is used in scaling-law and compute-budget calculations (e.g. Chinchilla: D ≈ 20N).
</details>

**96. 🟢 Explain a transformer to a non-technical person.**
<details><summary>Answer</summary>

"It reads all the words at once. For each word, it asks which other words help it understand this one, and takes clues from them (attention). Then each word thinks about what it learned (the feed-forward part). It repeats this many times, then guesses the most likely next word, over and over, to write text."
</details>

**97. 🟡 What are the main limitations of transformers?**
<details><summary>Answer</summary>

Quadratic cost in context length; large memory use (the KV cache); limited context and poor extrapolation beyond the training lengths; hallucination (confident wrong answers); needing huge amounts of data and compute; weak exact arithmetic and counting without tools; and being hard to interpret.
</details>

**98. 🔴 How would you extend the context length of an already-trained model?**
<details><summary>Answer</summary>

With RoPE-based models, scale the positions or frequencies (position interpolation, NTK-aware scaling, YaRN), then fine-tune briefly on long sequences. Add efficient attention (FlashAttention, sliding windows) and reduce KV-cache memory (GQA, quantised caches). Evaluate with long-context benchmarks such as needle-in-a-haystack tests.
</details>

**99. 🔴 What are mixed precision and quantisation, and how do they affect transformers?**
<details><summary>Answer</summary>

Mixed precision trains in bf16/fp16 while keeping fp32 master weights and accumulations, which roughly halves memory and gives large speed-ups on tensor cores.
Quantisation stores weights (and sometimes activations or the KV cache) in int8 or int4 for inference, cutting memory 2–4× with a small loss in quality (GPTQ, AWQ). Outlier activations in transformers are the main difficulty.
</details>

**100. 🔴 Design task: build a tiny GPT from scratch. What components do you need, in what order?**
<details><summary>Answer</summary>

1. A tokenizer (characters or BPE) and a dataset of token IDs.
2. A token embedding plus positional embedding.
3. N blocks, each: LayerNorm → causal multi-head attention → residual → LayerNorm → FFN → residual.
4. A final LayerNorm and a linear layer to the vocabulary (optionally tied to the embedding).
5. Training: a cross-entropy loss on shifted targets, the AdamW optimiser, a warm-up and cosine learning-rate schedule, and gradient clipping.
6. Generation: a loop that feeds the output back in, with temperature/top-k sampling and a KV cache.
(Karpathy's nanoGPT follows exactly this recipe.)
</details>

---

## Sources

These questions were compiled and extended from common interview-prep resources, including:

- [Top 32 LLMs & Transformers Interview Questions (2026) — DataInterview](https://www.datainterview.com/blog/llms-and-transformers-interview-questions)
- [Top 16 Interview Questions on Transformer — Analytics Vidhya](https://www.analyticsvidhya.com/blog/2022/11/top-6-interview-questions-on-transformer/)
- [Transformer Interview Questions — purepisces (GitHub)](https://github.com/purepisces/Wenqing-Machine_Learning_Blog/blob/main/Machine-Learning-Interview-Questions/Transformer-Interview-Question.md)
- [Transformers Interview Questions and Answers — Sanjay Kumar PhD (Medium)](https://skphd.medium.com/transformers-interview-questions-and-answers-d7248f43fbe8)
- [Interview Questions on Embedding Models — Sanjay Kumar PhD (Medium)](https://skphd.medium.com/interview-questions-and-answers-on-embedding-models-be0c73ec0730)
- [Interview Questions on Transformers — OpenGenus](https://iq.opengenus.org/interview-questions-on-transformers/)
- [Transformer LLMs: Roadmap and Interview Preparation — MentorCruise](https://mentorcruise.com/blog/transformer-llms-roadmap-and-interview-preparation-guide/)
- [LLM Interview Questions and Answers — InterviewBit](https://www.interviewbit.com/llm-interview-questions-answers/)
- [The LLM Interview Cheat Sheet — DEV Community](https://dev.to/thousand_miles_ai/the-llm-interview-cheat-sheet-10-questions-that-actually-come-up-5faa)
- [Understanding and Coding Self-Attention, Multi-Head, Causal and Cross-Attention — Sebastian Raschka](https://magazine.sebastianraschka.com/p/understanding-and-coding-self-attention)
- [Explain a Transformer in an AI/ML Interview — FACE Prep](https://faceprep.in/article/how-to-explain-transformer-in-ai-ml-interview-2026/)
