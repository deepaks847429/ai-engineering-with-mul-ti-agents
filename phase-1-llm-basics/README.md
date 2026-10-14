# Phase 1 — LLM Basics (Module 1)

> Topics copied from the main [roadmap](../README.md). Notes, exercises and solutions get added here when you reach this phase.

### 1.1 What an LLM actually is (conceptual, no math yet)

- [ ] Tokens and tokenization — why "strawberry" trips up models, why token count = cost
- [ ] Next-token prediction: what the model is *really* doing
- [ ] Context window: what it is, what happens when you exceed it
- [ ] Pretraining vs instruction tuning vs RLHF (conceptual overview — deep dive comes in Phase 3)
- [ ] Temperature, top-p, max tokens, stop sequences — every sampling parameter and when to change it
- [ ] Hallucination: why it happens, why it is *not* a bug you can prompt away
- [ ] Knowledge cutoff and why models don't "know" current events

### 1.2 The model landscape (as of 2025–2026)

- [ ] Closed providers: OpenAI (GPT), Anthropic (Claude), Google (Gemini)
- [ ] Open-weight models: Llama, Mistral, Qwen, DeepSeek, Gemma
- [ ] Reasoning/"thinking" models vs standard chat models — when each is worth the latency and cost
- [ ] Model tiers: frontier vs mid vs small — cost/latency/quality trade-offs
- [ ] Multimodal capabilities: vision input, audio, image generation
- [ ] How to read a model card and a pricing page
