# Phase 1 Interview Questions: LLM Basics

> Companion to [notes.md](notes.md). Finish the notes and `exercises.py` first.

**How to practise**
1. Read the question and **answer it out loud** (or on paper), as if you were in the interview.
2. Only then open the answer and compare.
3. Mark the ones you got wrong and come back to them tomorrow.

**Difficulty:** 🟢 Easy (every candidate must know) · 🟡 Medium (asked for AI engineer roles) · 🔴 Hard (senior roles, follow-up questions)

Questions marked 💬 are the ones we discussed in our lessons.

| Section | Questions |
|---|---|
| [A. What is an LLM](#a-what-is-an-llm-17) | 1–7 |
| [B. Tokens](#b-tokens-816) | 8–16 |
| [C. Next-token prediction](#c-next-token-prediction-1726) | 17–26 |
| [D. Context window](#d-context-window-2734) | 27–34 |
| [E. Training stages](#e-training-stages-3543) | 35–43 |
| [F. Sampling settings](#f-sampling-settings-4454) | 44–54 |
| [G. Hallucination](#g-hallucination-5560) | 55–60 |
| [H. Knowledge cutoff](#h-knowledge-cutoff-6164) | 61–64 |
| [I. Model landscape](#i-model-landscape-6575) | 65–75 |
| [J. Scenario questions](#j-scenario-questions-7680) | 76–80 |

---

## A. What is an LLM (1–7)

**1. 🟢 What is a Large Language Model, in one or two sentences?**
<details><summary>Answer</summary>

A neural network (a Transformer) trained on a huge amount of text to predict the next token. Everything it does, like chatting, coding or summarising, comes from repeating that next-token prediction.
</details>

**2. 🟢 💬 If an LLM only predicts what comes next, how can it answer "What is 2 + 2?"**
<details><summary>Answer</summary>

After the text "2 + 2 =", the most likely next token is "4", because the model saw that pattern thousands of times in training. The answer falls out of next-token prediction. It isn't calculating anything.
</details>

**3. 🟢 💬 What are the main differences between a phone keyboard's autocomplete and an LLM?**
<details><summary>Answer</summary>

Same idea (next-word prediction), much bigger scale:
- **Context:** the keyboard looks at 1–2 words. An LLM looks at up to hundreds of thousands of tokens.
- **Training data:** your messages vs trillions of tokens.
- **Size:** tiny vs billions of parameters.
- **Output:** one suggestion vs whole essays and programs.
</details>

**4. 🟢 💬 True or false: "ChatGPT looks up facts in a database when you ask it something."**
<details><summary>Answer</summary>

False. There is no database inside. It generates the most likely next tokens based on patterns learned in training. That's also why it can sound confident and still be wrong.
</details>

**5. 🟢 What is a "parameter"?**
<details><summary>Answer</summary>

A number inside the model that was learned during training. An LLM has billions of them, and all its "knowledge" is stored in them. "70B model" means about 70 billion parameters.
</details>

**6. 🟡 💬 Why do LLMs get large multiplications wrong, and how do production apps fix it?**
<details><summary>Answer</summary>

The model doesn't calculate. It predicts digits that *look* plausible. "48,273 × 9,381" was almost certainly never in the training data, so there's no pattern to copy, and it often gets the middle digits wrong. The fix is **function calling / tool use**: the model decides to call a calculator or code tool, real code computes the exact answer, and the model uses that result. The LLM decides *when* and *what*. Code does the precise work.
</details>

**7. 🟡 What architecture do almost all modern LLMs use, and what is its key idea?**
<details><summary>Answer</summary>

The **Transformer** (from the 2017 paper "Attention Is All You Need"). Its key idea is **attention**: for each position, the model works out which earlier tokens matter most for predicting the next one, and it can process the input tokens in parallel.
</details>

---

## B. Tokens (8–16)

**8. 🟢 What is a token?**
<details><summary>Answer</summary>

The unit of text a model reads and writes, usually a word, part of a word, or punctuation. Each token maps to an ID number. The model only sees numbers.
</details>

**9. 🟢 💬 Why don't LLMs use whole words as tokens? Why not single letters?**
<details><summary>Answer</summary>

- **Whole words:** the vocabulary would be endless (names, typos, slang, every language), and a new word can't be represented. It becomes `[UNK]` and its meaning is lost.
- **Single letters:** sequences become 4–5× longer, which is slower, more expensive and uses up more of the context window. The model also has to work harder to learn meaning.
- **Sub-word tokens** balance the two: common words are one token, and rare or new words are built from pieces.
</details>

**10. 🟢 💬 A document has about 3,000 English words. Roughly how many tokens is that?**
<details><summary>Answer</summary>

About **4,000 tokens** (3,000 ÷ 0.75). Rule of thumb: 1 token ≈ ¾ of a word ≈ 4 characters. The token count is always bigger than the word count.
</details>

**11. 🟢 Why should an AI engineer care about tokens?**
<details><summary>Answer</summary>

Cost is charged per token, limits (the context window, max output, rate limits) are counted in tokens, and latency depends on tokens, because output is generated one token at a time.
</details>

**12. 🟡 💬 Why is "how many r's are in strawberry?" hard for an LLM?**
<details><summary>Answer</summary>

The model sees something like `"str" | "aw" | "berry"` as three ID numbers. The letters are hidden inside the tokens, so it can't simply count characters. It has to remember which letters each token contains. The same reason explains trouble with spelling backwards and counting characters.
</details>

**13. 🟡 Explain how Byte Pair Encoding (BPE) builds a vocabulary.**
<details><summary>Answer</summary>

Start with single characters (or bytes). Repeatedly find the most frequent adjacent pair in the training text and merge it into a new token. Repeat until the vocabulary reaches the target size (say 50k–200k). Frequent words become single tokens, and rare words stay split into pieces. Because it can fall back to bytes, it never meets a truly unknown input.
</details>

**14. 🟡 💬 Why does Hindi or Tamil text need more tokens than English for the same meaning? What's the practical impact?**
<details><summary>Answer</summary>

Tokenizers are trained mostly on English text, so English character pairs get merged into whole-word tokens. Hindi and Tamil appear less, so their words stay split into many small pieces. Impact: the same content costs 2–4× more, fills the context window faster, and generates more slowly. This matters when building apps for Indian-language users.
</details>

**15. 🟡 What is a vocabulary, and what's the trade-off in choosing its size?**
<details><summary>Answer</summary>

The set of all tokens a model knows. Bigger vocabulary means fewer tokens per text (shorter sequences, cheaper inference), but a bigger embedding table and output layer, with rare tokens seen less in training. Smaller vocabulary means the opposite. Modern LLMs use roughly 32k–200k.
</details>

**16. 🔴 Why can the same text have a different token count on different models?**
<details><summary>Answer</summary>

Each model family has its own tokenizer, trained on different data with a different vocabulary size. So token counts, and therefore costs and context usage, aren't directly comparable across providers. Always count tokens with that model's own tokenizer or token-counting API.
</details>

---

## C. Next-token prediction (17–26)

**17. 🟢 💬 What exactly does the model output in one step?**
<details><summary>Answer</summary>

Not a word. It outputs a **score (logit) for every token in the vocabulary**. Softmax turns these into a probability distribution, and a sampling strategy picks one token.
</details>

**18. 🟢 💬 What's the difference between logits and probabilities? What turns one into the other?**
<details><summary>Answer</summary>

Logits are raw scores. They can be any number, even negative, and don't add up to anything. **Softmax** turns them into probabilities: all positive, summing to 1. Softmax also exaggerates gaps: logits 5 vs 3 become about 88% vs 12%.
</details>

**19. 🟢 💬 A model read: "Virat Kohli plays cricket" (3 times) and "Virat Kohli plays football" (once). What does it predict after "Virat Kohli plays"?**
<details><summary>Answer</summary>

cricket = 3/4 = **75%**, football = 1/4 = **25%**. Greedy decoding picks **cricket**. Real LLMs learn patterns rather than literal counts, but this is the right intuition for where the probabilities come from.
</details>

**20. 🟢 💬 Why can you get a different answer when you ask the same question twice?**
<details><summary>Answer</summary>

The model usually **samples** from the probability distribution instead of always taking the top token. Like a lucky draw with 88 "Paris" chits and 12 "Lyon" chits, a less likely token sometimes wins, and the rest of the answer then changes too.
</details>

**21. 🟢 What is autoregressive generation?**
<details><summary>Answer</summary>

Generating one token at a time, where each new token is appended to the input and fed back in to predict the next. The model uses its own previous outputs as input. It stops at an end token, a stop sequence, or max tokens.
</details>

**22. 🟡 💬 Why are output tokens more expensive (and slower) than input tokens?**
<details><summary>Answer</summary>

The input (prompt) is processed all at once, in parallel. The output must be generated **one token at a time**, each step depending on the previous one, so it needs much more compute time per token. That's why providers charge roughly 3–5× more for output. *Reading a page is fast. Writing one is slow.*
</details>

**23. 🟡 💬 The model wrote "Sydney" as the capital of Australia in its first sentence. Why can't it fix that on its own later?**
<details><summary>Answer</summary>

Generation is autoregressive: once a token is chosen it's fixed and becomes part of the input, and the model has no "edit" step. Later tokens are predicted to be *consistent* with "Sydney", so it often builds more wrong details on top. This is one reason "think step by step" helps: the reasoning comes before the final answer is committed.
</details>

**24. 🟡 What are "time to first token" and "tokens per second"? Why do chat apps stream responses?**
<details><summary>Answer</summary>

TTFT is the delay before the first output token appears. It grows with prompt length. Tokens per second is generation speed after that. Streaming shows tokens as they're generated, so users see something after the TTFT instead of waiting for the whole answer, which feels much faster.
</details>

**25. 🟡 What's the difference between greedy decoding and sampling?**
<details><summary>Answer</summary>

Greedy always picks the highest-probability token: deterministic and focused, but it can be repetitive or bland. Sampling picks randomly, weighted by probability: more varied and natural, but it can pick worse tokens. Temperature, top-k and top-p control how the sampling behaves.
</details>

**26. 🔴 If the model only predicts the next token, how can it "plan" a long answer?**
<details><summary>Answer</summary>

Internally, the representations used to predict the next token carry information about likely future content (research shows models encode some plans ahead, for example rhymes). Explicit reasoning helps further: chain-of-thought and reasoning models write intermediate steps as tokens, so the plan becomes part of the context they condition on. But each step is still one next-token prediction.
</details>

---

## D. Context window (27–34)

**27. 🟢 What is the context window?**
<details><summary>Answer</summary>

The maximum number of tokens the model can handle in a single request, **input and output together**: system prompt, chat history, documents, question and the answer.
</details>

**28. 🟢 💬 Does an LLM remember your previous messages by itself? If not, how does ChatGPT remember your name?**
<details><summary>Answer</summary>

No. The model and API are **stateless**: each request starts from zero. The **app re-sends the whole conversation every time**, so the model reads your name again in the earlier messages. In your own chatbot, your code must do this.
</details>

**29. 🟢 💬 The context window is 8,000 tokens and your question is 7,900. What problem do you face?**
<details><summary>Answer</summary>

Only about 100 tokens (roughly 75 words) are left for the answer, so it gets **cut off** mid-sentence (or the API rejects the request if you asked for more output than fits).
</details>

**30. 🟢 💬 A chat is getting very long. What can the app do so it still fits?**
<details><summary>Answer</summary>

- **Drop the oldest messages** (keep the system prompt and the recent ones)
- **Summarise** older history into a short note
- **Retrieve** only the relevant parts of documents or history (RAG)
</details>

**31. 🟡 Why doesn't a long chat get cheaper over time? Why does it get *more* expensive per message?**
<details><summary>Answer</summary>

Because the whole history is re-sent with every request, and you pay for all those input tokens every time. Message 50 carries messages 1–49 with it. (Prompt caching, Phase 21, reduces this cost.)
</details>

**32. 🟡 Why not just always use the largest context window available?**
<details><summary>Answer</summary>

Cost (you pay for every input token on every call), latency (longer prompts mean slower time to first token), and quality ("lost in the middle": models use information at the start and end better than in the middle). Relevant, focused context usually beats stuffing everything in.
</details>

**33. 🟡 What is "lost in the middle", and how do you design around it?**
<details><summary>Answer</summary>

Research finding that models recall information at the beginning and end of a long context better than in the middle. Put critical instructions at the start (or repeat them at the end), keep context focused, and use retrieval to include only relevant chunks.
</details>

**34. 🔴 What happens to cost and latency as context grows, and why?**
<details><summary>Answer</summary>

Input cost grows linearly with tokens. Compute for standard attention grows roughly quadratically with sequence length (every token attends to every other), and memory for the attention cache grows with length. So long prompts raise time to first token and per-request cost. That's why providers sometimes charge more above certain context lengths, and why caching and retrieval matter.
</details>

---

## E. Training stages (35–43)

**35. 🟢 What are the three main stages of training an LLM?**
<details><summary>Answer</summary>

1. **Pretraining:** next-token prediction on trillions of tokens, which gives a base model.
2. **Supervised fine-tuning (SFT) / instruction tuning:** training on example instruction→response pairs, which gives an assistant.
3. **Preference tuning (RLHF / DPO):** learning from human comparisons, which gives a helpful, honest, safe chat model.
</details>

**36. 🟢 💬 A base model knows a lot. Why can't we use it directly as a chatbot?**
<details><summary>Answer</summary>

It only **continues text**, like autocomplete. It was never taught to answer. Ask "What is the capital of France?" and it may continue with "What is the capital of Germany?..." because it saw quiz pages like that online.
</details>

**37. 🟢 💬 Which training stage is the most expensive, and why?**
<details><summary>Answer</summary>

**Pretraining**, by far: trillions of tokens, thousands of GPUs, weeks to months, tens to hundreds of millions of dollars. Preference tuning uses thousands of comparisons and much less compute. Humans are costly per label, but the total is far smaller. *Pretraining = 15 years of school. RLHF = a few months of manager feedback.*
</details>

**38. 🟢 💬 In which stage do humans *write* answers, and in which do they *compare* answers?**
<details><summary>Answer</summary>

**SFT:** humans write example answers (the model learns *how* to answer). **RLHF/DPO:** humans compare two model answers and pick the better one (the model learns *which* answers are better).
</details>

**39. 🟢 💬 In Stage 3, what exactly does the human do, and what does the model learn from it?**
<details><summary>Answer</summary>

The human sees two answers from the model to the same prompt and picks the better one. After thousands of comparisons, the model learns what humans prefer: more helpful, honest, polite and safe, including refusing harmful requests.
</details>

**40. 🟡 Why is pretraining called "self-supervised"?**
<details><summary>Answer</summary>

No human labels are needed. The text provides its own answer key, because the "label" for each position is simply the next token, which is already in the data. That's what lets it scale to trillions of tokens.
</details>

**41. 🟡 What does RLHF stand for, and how does it work at a high level?**
<details><summary>Answer</summary>

Reinforcement Learning from Human Feedback. (1) Collect human comparisons of model outputs. (2) Train a **reward model** to predict which output humans prefer. (3) Use reinforcement learning (classically PPO) to update the LLM to produce higher-reward outputs, with a penalty that keeps it close to the SFT model so it doesn't drift or "game" the reward.
</details>

**42. 🟡 What is DPO, and why is it popular?**
<details><summary>Answer</summary>

Direct Preference Optimization. It learns directly from preference pairs (chosen vs rejected answers) with a simple classification-style loss, with **no separate reward model and no RL loop**. It's simpler, more stable and cheaper than RLHF, with similar results in many cases.
</details>

**43. 🔴 How are "reasoning" models trained differently?**
<details><summary>Answer</summary>

On top of the usual stages, they get large-scale reinforcement learning on tasks with **verifiable answers** (maths, code with tests, logic). The model is rewarded for reaching correct final answers, which teaches it to produce long chains of thought: exploring, checking and backtracking before answering.
</details>

---

## F. Sampling settings (44–54)

**44. 🟢 What does temperature do?**
<details><summary>Answer</summary>

It controls randomness. Logits are divided by the temperature before softmax. Low temperature sharpens the distribution (the top token dominates: consistent, focused). High temperature flattens it (more variety, creativity and risk). Temperature 0 is effectively greedy decoding.
</details>

**45. 🟢 💬 You're building an app that extracts the amount from bank statements. Low or high temperature? Why?**
<details><summary>Answer</summary>

**Low (0).** There's one correct answer, and you want the same result every time. There's no need for creativity.
</details>

**46. 🟢 💬 You want 10 creative names for a chai shop. Low or high temperature? Why?**
<details><summary>Answer</summary>

**High (about 0.9–1.0).** There are many good answers and you want variety. Low temperature would give safe, repetitive names.
</details>

**47. 🟡 💬 "I set temperature to 0, so my chatbot will never give wrong answers." Is this right?**
<details><summary>Answer</summary>

No. Temperature 0 always picks the model's **top guess**, and the top guess can be wrong (e.g. Sydney 55% vs Canberra 40%: it will say Sydney every time). Temperature controls **randomness, not correctness**. Also, temperature 0 isn't perfectly deterministic in practice.
</details>

**48. 🟡 Is temperature 0 fully deterministic? Why or why not?**
<details><summary>Answer</summary>

Not guaranteed. Floating-point maths on GPUs, batching with other requests, and hardware differences can change logits very slightly, which can flip a near-tie and change the rest of the output. Some APIs offer a `seed` for best-effort reproducibility.
</details>

**49. 🟢 💬 What's the difference between top-k and top-p?**
<details><summary>Answer</summary>

**Top-k** keeps a fixed number of tokens, the k most likely. **Top-p** (nucleus sampling) keeps the smallest set of top tokens whose probabilities add up to at least p. So the number kept changes with the model's confidence. Both re-normalise and then sample.
</details>

**50. 🟡 Why is top-p often considered better than top-k?**
<details><summary>Answer</summary>

It **adapts**. When the model is confident (one token at 95%), top-p keeps just that one. When it's unsure (many tokens at about 5%), it keeps many. Top-k keeps exactly k regardless, which is too many when confident and too few when unsure.
</details>

**51. 🟡 💬 Why shouldn't you change temperature and top-p together?**
<details><summary>Answer</summary>

Both control how random the sampling is, so they interact in ways that are hard to reason about and tune. Providers recommend adjusting one and leaving the other at its default.
</details>

**52. 🟢 💬 You set max_tokens = 20 and the answer stops mid-sentence. Why? How do you get short but complete answers?**
<details><summary>Answer</summary>

`max_tokens` is a **hard cut-off**, not a "be brief" instruction. The model hit the limit and was stopped. To get short answers, **ask in the prompt** ("Answer in one sentence") and set max_tokens high enough to finish. Also check the API's stop reason (e.g. `"max_tokens"` or `"length"`) so you never show a truncated answer as complete.
</details>

**53. 🟢 What is a stop sequence, and when would you use one?**
<details><summary>Answer</summary>

A string that ends generation immediately when the model produces it (e.g. `"###"` or `"\nUser:"`). Use it to stop the model running past the part you want, such as inventing the next user turn or going past an end marker.
</details>

**54. 🟡 What are frequency and presence penalties?**
<details><summary>Answer</summary>

Settings (OpenAI-style) that lower the probability of tokens that have already appeared. Frequency penalty scales with how many times a token appeared. Presence penalty applies once a token has appeared at all. Used to reduce repetition and encourage new topics.
</details>

---

## G. Hallucination (55–60)

**55. 🟢 What is hallucination?**
<details><summary>Answer</summary>

When a model produces fluent, confident output that is false or made up, such as fake citations, non-existent functions or wrong facts. It sounds just as confident as a correct answer.
</details>

**56. 🟢 💬 In your own words, why do LLMs hallucinate?**
<details><summary>Answer</summary>

1. They're trained to produce **likely** text, not **true** text. They fill the blank, they don't check facts.
2. There's **no fact database**, only compressed patterns, so rare facts are fuzzy.
3. They **always produce an answer**. Confident text was far more common in training than "I don't know".
4. They **can't backtrack**: an early wrong token gets built on.
</details>

**57. 🟡 💬 Why can a model answer "capital of France" correctly but get "the founding year of a small Pune startup" wrong?**
<details><summary>Answer</summary>

"France → Paris" appeared thousands of times in training, so the pattern is strong. A small startup's founding year appeared rarely or never, so the model has only a weak or no pattern, and it fills the gap with a plausible-looking year.
</details>

**58. 🟡 Can you fix hallucination with a prompt or with temperature 0?**
<details><summary>Answer</summary>

Not fully. "Don't hallucinate" helps only a little, because hallucination comes from how the model works, not a switchable bug. Temperature 0 just makes it consistently pick its top guess, which can still be wrong.
</details>

**59. 🟢 💬 You're building a chatbot for a college's admission rules. How do you stop it from inventing rules?**
<details><summary>Answer</summary>

Use **RAG**: retrieve the relevant sections of the official rules document, put them in the prompt, and instruct the model to answer **only** from them, an "open-book exam". Also make it quote or cite the rule it used, tell it to say "I don't know, please contact the admissions office" when the answer isn't in the documents, and test it with an eval set of real student questions.
</details>

**60. 🟡 List techniques to reduce hallucination in production.**
<details><summary>Answer</summary>

RAG/grounding · requiring citations or quotes · explicitly allowing "I don't know" · tools (search, calculator, database) · structured outputs with validation · lower temperature for factual tasks (reduces randomness only) · a second model or code to check answers · **evals** to measure the hallucination rate over time.
</details>

---

## H. Knowledge cutoff (61–64)

**61. 🟢 What is a knowledge cutoff?**
<details><summary>Answer</summary>

The date the model's training data ends. The model knows nothing about events after it.
</details>

**62. 🟢 💬 A model's cutoff is January 2025. You ask "What's the latest iPhone?" What might go wrong?**
<details><summary>Answer</summary>

It will name the latest iPhone it knows about from before January 2025, possibly presenting it confidently as "the latest". That's a hallucination caused by the cutoff. It can't know about newer releases.
</details>

**63. 🟢 💬 Why don't companies just retrain the model every week to keep it up to date?**
<details><summary>Answer</summary>

Pretraining takes weeks to months on thousands of GPUs and costs crores, and each new model also needs fine-tuning and safety testing. Much cheaper: give fresh information at question time with RAG, search tools, or by putting facts in the prompt.
</details>

**64. 🟡 Why do models know little about the last few months before their cutoff, and why don't they know today's date?**
<details><summary>Answer</summary>

When something has just happened, little has been written about it yet, so it's thin in the training data. The model has no clock, so it only knows the date if you put it in the prompt. That's why production system prompts often include "Today's date is ...".
</details>

---

## I. Model landscape (65–75)

**65. 🟢 What's the difference between closed and open-weight models? Give examples.**
<details><summary>Answer</summary>

**Closed:** only available through the provider's API, pay per token: OpenAI GPT, Anthropic Claude, Google Gemini. **Open-weight:** the weights are downloadable, so you run them yourself: Meta Llama, Mistral, Qwen, DeepSeek, Google Gemma. *Rent vs buy.*
</details>

**66. 🟡 When would you choose an open-weight model over a closed API?**
<details><summary>Answer</summary>

When data can't leave your infrastructure (banks, hospitals, government), when you need full control or fine-tuning, when you need offline or on-device use, or at very high volume where owning GPUs is cheaper than paying per token. The trade-off is hosting and ops work, plus usually slightly lower quality than the frontier.
</details>

**67. 🟡 Is "open-weight" the same as "open source"?**
<details><summary>Answer</summary>

No. Open-weight usually means you get the trained parameters, but not the training data or the full training code. Licences vary, and some restrict commercial use or large companies, so always check the licence.
</details>

**68. 🟢 What are model tiers, and how do you pick one?**
<details><summary>Answer</summary>

Providers offer sizes: large (e.g. Claude Opus) for the hardest tasks, mid (Claude Sonnet) as the everyday default, and small (Claude Haiku) for simple, high-volume, low-latency work. Bigger is smarter but slower and pricier. Pick the smallest model that meets your quality bar on your evals.
</details>

**69. 🟡 What is model routing, and why use it?**
<details><summary>Answer</summary>

Sending each request to a different model based on difficulty: easy ones to a cheap, fast small model, hard ones to a large model. Most traffic is easy, so this cuts cost and latency a lot while keeping quality where it matters.
</details>

**70. 🟡 When should you use a reasoning ("thinking") model, and when not?**
<details><summary>Answer</summary>

Use one for hard multi-step problems: maths, complex logic, difficult coding, planning. Avoid it for simple chat, extraction and classification, because it adds latency and cost (you pay for the thinking tokens) without improving quality there.
</details>

**71. 🟢 What does "multimodal" mean?**
<details><summary>Answer</summary>

Working with more than one type of data, such as text plus images, PDFs, audio or video as input, and some models generate images or speech. Example: upload a photo of a bill and ask for the total.
</details>

**72. 🟢 How is LLM API usage priced?**
<details><summary>Answer</summary>

Per million tokens, with separate prices for input and output. Output is usually several times more expensive. There are often discounts for cached input (a repeated prompt prefix) and batch processing.
</details>

**73. 🟡 Calculate: 2,000 input tokens and 500 output tokens at $3 per 1M input and $15 per 1M output. What does one request cost, and 1 lakh requests per day?**
<details><summary>Answer</summary>

Input: 2,000/1M × $3 = $0.006. Output: 500/1M × $15 = $0.0075. **Total $0.0135 per request.** × 100,000 = **$1,350 per day** (about ₹1.1 lakh per day). Small per-request savings matter a lot at scale.
</details>

**74. 🟢 What is a model card, and what do you look for in one?**
<details><summary>Answer</summary>

The model's spec sheet: context window, max output tokens, knowledge cutoff, supported input types, pricing, rate limits, benchmark scores, intended use, known limitations, and (for open-weight models) the licence.
</details>

**75. 🟡 Why shouldn't you choose a model based on public benchmarks alone?**
<details><summary>Answer</summary>

Benchmarks may not resemble your task, and models can be over-tuned to popular tests (some test questions even leak into training data). A model can score high and still do worse on your data. Build a small eval set from real examples and compare models on that (Phase 23).
</details>

---

## J. Scenario questions (76–80)

These combine several lessons. Interviewers love them.

**76. 🟡 A user says your chatbot "forgot" what they said at the start of a long conversation. What's happening and how would you fix it?**
<details><summary>Answer</summary>

The model is stateless and the conversation outgrew the context budget, so older messages were trimmed (or lost in the middle of a very long context). Fixes: summarise older turns into a running summary, store key facts (like the user's name and preferences) separately and always include them, retrieve relevant past messages (RAG over chat history), and put critical info near the start or end of the prompt.
</details>

**77. 🟡 Your monthly LLM bill doubled. What would you check?**
<details><summary>Answer</summary>

Traffic growth, longer prompts (growing chat history, bigger retrieved documents), longer outputs (max_tokens, verbose prompts), someone switching to a larger or reasoning model, retries or loops calling the API repeatedly, and missing caching. Fixes: trim history, route easy requests to a smaller model, use prompt caching and batch, and set sensible max_tokens.
</details>

**78. 🟡 You're building an app for Hindi-speaking users. What LLM-specific issues do you plan for?**
<details><summary>Answer</summary>

Higher token counts per message (higher cost, less room in context, slower), so test the tokenizer cost per message. Check model quality in Hindi with your own evals, not English benchmarks. Plan for mixed Hinglish input. Possibly choose a model or tokenizer with better Indic-language support.
</details>

**79. 🔴 Design a support bot for a bank that must not give wrong answers about interest rates. Walk through your choices.**
<details><summary>Answer</summary>

- **Data:** never rely on model memory (knowledge cutoff, hallucination). Fetch current rates from the bank's database with a **tool/function call**.
- **Grounding:** RAG over official policy documents. Answer only from retrieved text, with citations.
- **Settings:** low temperature for consistency.
- **Safety:** explicit "I don't know, here's how to contact us" behaviour. Validate numbers in the answer against the source data with code.
- **Model:** possibly open-weight or a private deployment if data can't leave the bank. A mid-tier model is usually enough.
- **Evals:** a test set of real customer questions, tracking accuracy and hallucination rate before every release.
</details>

**80. 🔴 Explain the whole journey from a user typing a question to seeing an answer stream on screen.**
<details><summary>Answer</summary>

The app builds the prompt (system prompt + trimmed history + any retrieved documents + the question) and checks it fits the context window → sends it to the API → the tokenizer converts the text to token IDs → the model processes the prompt in parallel (this sets the time to first token) → each step it outputs logits over the vocabulary → softmax → temperature/top-p sampling picks a token → the token is streamed back to the user and appended to the input → repeat until an end token, stop sequence or max tokens → the app checks the stop reason, saves the turn to history, and logs token usage for cost.
</details>

---

**Done all 80?** Re-test yourself on the ones you got wrong, then move on to Phase 2 (first API calls).
