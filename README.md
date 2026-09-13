# AI Engineering — Beginner to Pro Roadmap

> A complete, self-paced roadmap to go from **absolute beginner** to **production-grade AI Engineer**.
> Built from the AI Engineering Bootcamp syllabus ([source PDF](AI-Engineering-Bootcamp-Syllabus-Breakdown%20(1).pdf)), then **extended with everything the bootcamp leaves out** — foundations, classical ML, the interface layer, deployment/infrastructure, and the technologies its projects assume but never teach.

---

## Table of Contents

1. [How to Use This Roadmap](#how-to-use-this-roadmap)
2. [The Big Picture](#the-big-picture)
3. [Phase 0 — Absolute Beginner Foundations](#phase-0--absolute-beginner-foundations-added--not-in-the-pdf) *(added)*
4. [Phase 1 — LLM & GenAI Fundamentals](#phase-1--llm--genai-fundamentals-reconstructs-missing-modules-12) *(reconstructs missing Modules 1–2)*
5. [Phase 2 — Track A: AI Engineering (Modules 3–26)](#phase-2--track-a-ai-engineering-modules-326)
6. [Phase 3 — Track B: Deep Learning Foundations (Modules 27–33)](#phase-3--track-b-deep-learning-foundations-modules-2733)
7. [Phase 4 — The Missing Pieces](#phase-4--the-missing-pieces-added--not-in-the-pdf) *(added)*
8. [Project Catalogue — All 17 Builds + 5 Added](#project-catalogue)
9. [Technology Stack Inventory](#technology-stack-inventory)
10. [Suggested Timeline](#suggested-timeline)
11. [Known Issues in the Source Syllabus](#known-issues-in-the-source-syllabus)
12. [Guiding Principles](#guiding-principles)

---

## How to Use This Roadmap

- **Work top to bottom.** Phases are ordered by dependency, not by the PDF's page order. The bootcamp itself is applications-first (ship things early, learn internals later) — we keep that order because it works.
- **Check boxes as you go.** Every topic is a checkbox. A module is "done" when you can build its project (or a small demo) without looking at a tutorial.
- **Projects are the curriculum.** The modules exist to make the projects possible. If you must cut something, cut reading — never cut building.
- **Don't skim Modules 22–23 (Observability & Evals).** The source analysis calls these the "sleeper modules" — they are what separates someone who can *demo* an agent from someone who can be *trusted to own one in production*.
- Sections marked **🆕 (added)** are not in the bootcamp PDF. They fill real gaps identified in the syllabus's own structural analysis, plus gaps a beginner would hit.

---

## The Big Picture

```
Phase 0          Phase 1           Phase 2                Phase 3            Phase 4
Foundations  →   LLM Basics    →   AI Engineering     →   Deep Learning  →   Missing Pieces
(Python, Git,    (how LLMs         (prompting, RAG,       (math, PyTorch,    (UI layer, deploy,
 APIs, SQL)       work, APIs)       agents, production)    transformers,      infra, serving,
                                                           fine-tuning)       system design)
```

Two mindsets you will alternate between:

| Mindset | Phases | What it means |
|---|---|---|
| **AI Application Engineer** | 1, 2, 4 | You *orchestrate* models: prompting, retrieval, agents, evals, shipping. This is where jobs are today. |
| **Deep Learning Engineer** | 3 | You understand *inside* the model: tensors, attention, training, fine-tuning. Optional for shipping apps, required for reasoning about model behavior. |

---

## Phase 0 — Absolute Beginner Foundations (🆕 added — not in the PDF)

> The bootcamp assumes you already program. If you are a true beginner, this phase is non-negotiable. If you already work as a software engineer, skim it and move on.

### 0.1 Python — the language of AI

- [ ] Variables, data types, control flow, functions
- [ ] Data structures: lists, dicts, sets, tuples, comprehensions
- [ ] Object-oriented Python: classes, inheritance, dunder methods (needed for PyTorch later)
- [ ] Error handling: `try/except`, custom exceptions
- [ ] Modules, packages, virtual environments (`venv`, `pip`, and modern tooling: `uv`)
- [ ] Type hints (`typing`, `Optional`, generics) — Pydantic and FastAPI depend on these
- [ ] `async`/`await` and `asyncio` basics — every serious LLM app is async
- [ ] File I/O, JSON handling, `pathlib`
- [ ] Decorators and context managers (agent frameworks use these heavily, e.g. `@tool`)

### 0.2 Developer tooling

- [ ] Terminal fluency (bash/PowerShell): navigation, pipes, environment variables
- [ ] Git & GitHub: clone, branch, commit, push, pull requests, resolving conflicts
- [ ] VS Code (or your editor) with debugger — not just `print()` debugging
- [ ] Jupyter notebooks — and knowing when to *graduate out of them* into real scripts

### 0.3 How the web works (you cannot build AI APIs without this)

- [ ] HTTP: methods, status codes, headers, request/response lifecycle
- [ ] REST APIs: what they are, calling them with `requests`/`httpx`
- [ ] JSON as the wire format of everything
- [ ] API keys, environment variables, and `.env` files — **never commit secrets**
- [ ] What a webhook is; what long-polling vs streaming means

### 0.4 Data basics

- [ ] `numpy` fundamentals: arrays, broadcasting, matrix operations
- [ ] `pandas` fundamentals: DataFrames, filtering, groupby, joins
- [ ] SQL fundamentals: SELECT, JOIN, GROUP BY, indexes (the bootcamp only touches Cypher — plain SQL is a gap)
- [ ] Basic data visualization: `matplotlib` / `plotly`

**✅ Phase 0 exit criteria:** You can write a Python script that calls a public REST API, parses the JSON, stores results in SQLite, and lives in a Git repo with a README.

---

## Phase 1 — LLM & GenAI Fundamentals (reconstructs missing Modules 1–2)

> The source PDF explicitly notes Modules 1 and 2 were absent from the material it was built from. This is what they almost certainly cover — and what you need before Module 3 makes sense.

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

### 1.3 Your first API calls

- [ ] Set up OpenAI and Anthropic API keys; understand billing and rate limits
- [ ] Chat completions: system / user / assistant roles
- [ ] Multi-turn conversation state — *you* manage history, the API is stateless
- [ ] Counting tokens and estimating cost per request
- [ ] Streaming a response token by token
- [ ] Playgrounds (OpenAI Playground, Anthropic Console) for rapid iteration

**✅ Phase 1 exit criteria:** You can explain to a friend what a token is, and you have a CLI chatbot with conversation memory built on raw API calls — no frameworks.

---

## Phase 2 — Track A: AI Engineering (Modules 3–26)

> The core of the bootcamp: prompting → applications → retrieval → agents → production.

### Module 3 — Prompt Engineering: Foundations to Advanced

- [ ] Structured outputs and custom response formats
- [ ] Conditional prompts and reusable prompt templates
- [ ] Zero-shot, one-shot, and few-shot prompting
- [ ] Chain-of-Thought, self-consistency, Auto-CoT, persona-based prompting
- [ ] Prompt serialization formats: Alpaca, ChatML, INST
- [ ] **Context engineering** as the modern AI application design paradigm
- [ ] Context window management

### Module 4 — Real-World Text Tasks & Chatbot Development

- [ ] Summarization, translation, tone control, writing improvement
- [ ] Customer support ticket routing and analysis
- [ ] Code generation, modification, and explanation
- [ ] Role-playing chatbots, learning advisors, support assistants
- 🛠 **Project 01: Working with the OpenAI API** — production-style Python utilities for summarization, translation, tone control, ticket routing, code generation
- 🛠 **Project 02 (4A): Customer Support Agent** — classifies tickets, retrieves help docs via RAG, drafts replies, escalates to a human when out of its depth

### Module 5 — Structuring End-to-End LLM Applications

- [ ] JSON outputs and structured response handling
- [ ] Error handling and exception handling in AI applications
- [ ] Batching requests for efficiency
- [ ] Rate-limit retries and token-limit management

#### Module 5A — FastAPI Basics for AI Applications

- [ ] FastAPI project setup
- [ ] Routes, request/response models, Pydantic schemas
- [ ] Building AI API endpoints
- [ ] Error handling and environment configuration
- [ ] Connecting FastAPI with LLM workflows

### Module 6 — Function Calling & Structured Outputs

- [ ] Function calling and the `tools` parameter
- [ ] Multiple, parallel, and forced function calls
- [ ] Calling external APIs from inside the model loop
- [ ] Enforcing structured, typed outputs with Pydantic
- [ ] **6A:** OpenAI SDK & Claude SDK for production AI apps — build with both

### Module 7 — Embeddings & Semantic Search

- [ ] Creating and using embeddings
- [ ] Investigating and reasoning about vector spaces
- [ ] Semantic search and recommendation systems
- [ ] Embedding-based classification
- 🛠 **Project 03: Exploring Embeddings** — semantic search, recommendation, and classification systems; reason about the vector space behind them

### Module 8 — Vector Databases

- [ ] Vector DB theory: construction, compression, indexing (HNSW, IVF)
- [ ] ChromaDB end-to-end: CRUD, metadata filtering, cost estimation
- [ ] Pinecone end-to-end: ingestion, querying, namespaces, multitenancy
- [ ] Milvus overview
- 🛠 **Project 04: RAG Chatbot over YouTube Transcripts** — Pinecone-backed, retrieves relevant timestamps, answers grounded in what was actually said

### Module 9 — Retrieval-Augmented Generation (RAG)

- [ ] RAG fundamentals: indexing workflow and retrieval mechanism
- [ ] Building RAG with LangChain loaders, chunking, retrievers
- [ ] Hybrid search, reranking, query rewriting
- [ ] RAGAS metrics and improving the "I don't know" rate

#### Module 9A — LlamaIndex for Production RAG

- [ ] LlamaIndex fundamentals; data connectors, documents, nodes, indexes
- [ ] Query engines and retrievers
- [ ] Building RAG pipelines with LlamaIndex
- [ ] When to use LlamaIndex vs LangChain
- 🛠 **Project 05 (Flagship): Enterprise Advanced RAG** — hybrid search (BM25 + vector), cross-encoder reranking, guardrails, end-to-end RAGAS evaluation on real corporate data

### Module 10 — Scalable RAG with Async Queues

- [ ] Sync vs async RAG architectures
- [ ] Python RQ with Redis/Valkey on Docker
- [ ] FastAPI chat queue design: enqueue, poll, dequeue
- [ ] Worker orchestration and horizontal scaling

### Module 11 — Hugging Face: Pre-Trained Models in Production

- [ ] HF Hub, datasets, inference providers, CLI
- [ ] Instruction-tuned open models (e.g. Google Gemma)
- [ ] AutoModels, AutoTokenizers, AutoClasses
- [ ] Document Q&A pipelines with PyPDF

### Module 12 — Multi-Modal AI with Hugging Face

- [ ] Vision tasks: image classification, object detection, background removal
- [ ] Speech: recognition, embeddings, denoising, text-to-speech
- [ ] Zero-shot image/video classification with CLIP and CLAP
- [ ] VQA, Document VQA, diffusion, inpainting, video models

### Module 13 — AI Agents: First Agent to Multi-Agent Systems

- [ ] Agentic AI fundamentals; build your first agent
- [ ] Hugging Face smolagents; custom tools with `@tool`
- [ ] Web search and data access tools
- [ ] Agentic RAG with stateful RAG search tools
- [ ] Multi-agent systems: specialists, coordination, memory
- [ ] Workflow patterns: chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer
- [ ] **13A:** AutoGen & CrewAI for collaborative multi-agent apps
- [ ] **13B:** A2A protocol & spinning up subagents

### Module 14 — LangGraph & Stateful Agent Workflows

- [ ] LangGraph core: nodes, edges, state, StateGraph
- [ ] Complex agent graphs with LangChain and LCEL
- [ ] Debugging stateful agent workflows
- [ ] Checkpointing with MongoDB for persistence

> ⭐ **Go deep here.** The source analysis notes agent frameworks are covered broadly (smolagents, LangGraph, LangFlow, AutoGen, CrewAI in two modules) — LangGraph is the one worth real depth, because the flagship coding-agent project is built on it.

#### Module 14A — LangFlow for Visual AI Workflow Building

- [ ] Building AI workflows visually; connecting LLMs, prompts, tools, retrievers, memory
- [ ] Rapid prototyping of RAG and agent workflows
- [ ] Exporting and understanding generated workflow logic; when LangFlow is useful in real teams
- 🛠 **Project 06 (Flagship): Claude Code-like Coding Agent** — understands a codebase, inspects files, makes edits, runs commands in a sandbox, iterates on fixes for hours (LangGraph + MongoDB checkpointing + sandboxed execution)

### Module 15 — The Memory Layer in AI Agents

- [ ] Short-term, long-term, factual, episodic, and semantic memory
- [ ] Mem0 setup and configuration
- [ ] Vector-database-backed memory for agents
- [ ] Deep agents and deep research agents

### Module 16 — Graph Memory & Knowledge Graphs

- [ ] Why graph memory matters for agents
- [ ] Neo4j and Kuzu for graph storage
- [ ] Cypher query basics
- [ ] Adding and testing graph memory in an agent

### Module 17 — Multi-Modal Agents & Voice Agents

- [ ] Multi-modal agents and image-based reasoning
- [ ] Speech-to-Speech voice agents
- [ ] Chained voice agents: STT → LLM → TTS
- 🛠 **Project 08 (Flagship): Voice-Based AI Agent** — chained STT→LLM→TTS agent that holds natural conversations, calls tools, and runs as a Cursor-style voice coding assistant

### Module 18 — Model Context Protocol (MCP) & Agent SDK

- [ ] What MCP is and why it matters; MCP architecture
- [ ] Building a tiny MCP server
- [ ] Agent SDK concepts: Hosted Tools, Function Tools, Agent-as-a-Tool
- 🛠 **Project 07 (Flagship, 18A): AI Code Reviewer like CodeRabbit** — reads PRs, flags bugs and security issues with RAG over your style guide, posts structured inline comments via the GitHub API

### Module 19 — Streaming, Retries, Fallbacks & Rate Limits

- [ ] Streaming responses with Server-Sent Events (SSE)
- [ ] Exponential backoff and retry strategies
- [ ] Idempotency keys
- [ ] Token budgets
- [ ] Building a multi-provider LLM Gateway with automatic fallback

### Module 20 — Local LLM Deployment

- [ ] Ollama as a local LLM runtime
- [ ] Dockerized LLM environments
- [ ] OpenWebUI
- [ ] FastAPI services on top of Ollama

### Module 21 — Prompt Caching & Cost/Latency Optimization

- [ ] Anthropic and OpenAI prompt-caching mechanics
- [ ] Prefix-based caching and cache-friendly prompt design
- [ ] KV cache fundamentals
- [ ] Batching, prefill, and decode phases

### Module 22 — Observability & Tracing ⭐ *sleeper module — do not skim*

- [ ] Why traditional logs are not enough for agentic apps
- [ ] Langfuse, LangSmith, Braintrust, OpenLLMetry
- [ ] OpenTelemetry GenAI semantic conventions
- [ ] Tracing model calls, tools, retrieval, agent workflows

### Module 23 — Evaluations: The Underrated AI Engineering Skill ⭐ *sleeper module — do not skim*

- [ ] Trace-by-hand workflow on production traces
- [ ] Failure bucketing
- [ ] Binary pass/fail evaluations
- [ ] LLM-as-judge prompts and achieving strong judge alignment
- [ ] The three gulfs model: comprehension, specification, generalization
- [ ] RAGAS metrics in practice

### Module 24 — Security, Guardrails & Responsible Deployment

- [ ] OWASP Top 10 for LLM Applications
- [ ] Defense-in-depth for AI systems
- [ ] Least-privilege tool design
- [ ] Schema validation
- [ ] Human-in-the-loop workflows
- [ ] NeMo Guardrails, Llama Guard, ShieldGemma
- [ ] Prompt injection testing — hands-on: prompt-inject your own agent

### Module 25 — MLOps & LLMOps in Production

- [ ] MLOps lifecycle: roles, deployment, monitoring, drift
- [ ] LLMOps lifecycle: ideation, development, operations
- [ ] Cost management and prompt compression
- [ ] Governance and production readiness
- [ ] Choosing between RAG and fine-tuning

### Module 26 — Production Best Practices

- [ ] Moderation APIs
- [ ] Prompt-injection mitigation
- [ ] Guardrails and output validation
- [ ] Adversarial testing
- [ ] Minimizing model risks in production
- 🛠 **Project 09 (Bonus): AI Trading Agent** — ingests market data and financial news, reasons over signals via agentic RAG, proposes structured trade ideas with risk controls for humans to act on

**✅ Phase 2 exit criteria:** You have shipped at least one flagship project end-to-end with tracing, evals, and guardrails — not just a happy-path demo.

---

## Phase 3 — Track B: Deep Learning Foundations (Modules 27–33)

> A separate track that starts from math. Optional for an application engineer; required if you want to *reason about* model behavior, fine-tune models, or interview for ML roles.

### Module 27 — Math & PyTorch Foundations

- [ ] Linear algebra, probability, statistics, calculus (as used in DL)
- [ ] Gradient descent
- [ ] PyTorch tensors, layers, weights, parameters
- [ ] Training loops, optimizers, learning rate, momentum
- [ ] Overfitting, dropout, evaluation with torchmetrics
- 🛠 **Project 10 (Mini): Simple Neural Network in TensorFlow** — first end-to-end model: forward pass, training loop, evaluation
- 🛠 **Project 11 (Mini): MNIST Autoencoder** — unsupervised representation learning; your first generative model

### Module 28 — Robust Deep Learning & Computer Vision

- [ ] PyTorch with OOP: clean Dataset, DataLoader, Model, Trainer classes
- [ ] Vanishing/exploding gradients; ReLU vs ELU; Batch Normalization
- [ ] CNNs end-to-end: convolutional layers, augmentation, training, evaluation

### Module 29 — Sequence Modelling & Multi-IO Architectures

- [ ] RNNs, LSTMs, GRUs; forecasting with RNNs
- [ ] Multi-input and multi-output architectures
- [ ] Loss weighting for complex models
- 🛠 **Project 12: Multi-Input Models for OCR** — fuses image and metadata streams for end-to-end OCR with multi-loss training

### Module 30 — Transformers from Scratch

- [ ] Self-attention, positional encoding, multi-head attention, masked attention
- [ ] Full Transformer architecture
- [ ] Encoder-only vs decoder-only vs encoder-decoder
- [ ] Pretraining objectives: MLM and CLM; GPT vs BERT
- [ ] Building a custom BPE tokenizer

### Module 31 — Deep Generative Models

- [ ] GAN fundamentals; implement a GAN for handwritten digit generation
- [ ] Variational Autoencoders (VAEs); train a face-generation VAE on CelebA
- [ ] TensorBoard for generative-model metrics

### Module 32 — LLM Internals: Theory to Match the Practice

- [ ] KV Cache · Paged Attention · Flash Attention · Sparse Attention
- [ ] Quantization · Mixture of Experts · Distillation · Speculative Decoding
- [ ] RLHF
- [ ] Chain of Thought and Tree of Thought
- [ ] DeepSeek architecture case study

### Module 33 — Fine-Tuning, LoRA/QLoRA & Trending Topics

- [ ] Pretraining vs fine-tuning; when to fine-tune and when *not* to
- [ ] LoRA and QLoRA; parameter-efficient fine-tuning
- [ ] Hands-on fine-tuning with Unsloth
- [ ] Diffusion models · Vision Transformers · CLIP recap

**✅ Phase 3 exit criteria:** You can explain attention on a whiteboard, and you have fine-tuned an open model on your own dataset with LoRA and measured whether it actually beat the base model.

---

## Phase 4 — The Missing Pieces (🆕 added — not in the PDF)

> The bootcamp's own structural analysis admits these gaps. This phase closes them. **This is what turns "completed a bootcamp" into "hireable AI engineer."**

### 4.1 🆕 Classical Machine Learning (the jump the syllabus skips)

The syllabus goes straight from Python to deep learning. Real-world data work (and most interviews) still lean on classical ML.

- [ ] Supervised vs unsupervised learning; train/validation/test splits
- [ ] scikit-learn: linear/logistic regression, decision trees, random forests, gradient boosting (XGBoost/LightGBM)
- [ ] Clustering (k-means) and dimensionality reduction (PCA, t-SNE/UMAP — you'll want these for visualizing embeddings anyway)
- [ ] Metrics: accuracy, precision/recall, F1, ROC-AUC, RMSE — and when each is the *wrong* metric
- [ ] Feature engineering, leakage, cross-validation
- [ ] When a 50-line sklearn model beats an LLM (spoiler: often, on tabular data)

### 4.2 🆕 The Interface Layer (the single biggest gap in the syllabus)

> The source analysis is blunt: *"Across 31 modules and 17 projects, the only interface layer mentioned is Streamlit, in one project. Everything else stops at the FastAPI boundary."* No modern AI product ships without a real UI.

- [ ] JavaScript/TypeScript fundamentals (enough to be dangerous)
- [ ] React basics: components, state, effects
- [ ] Next.js: routing, server components, API routes
- [ ] **Vercel AI SDK** — the de-facto standard for streaming chat UIs
- [ ] Token-by-token streaming rendering (consume the SSE endpoints you built in Module 19)
- [ ] Rendering tool calls and agent state legibly: "thinking" indicators, tool-call cards, citations, expandable traces
- [ ] Markdown + code-block rendering in chat (syntax highlighting, copy buttons)
- [ ] Optimistic UI, error/retry states, stop-generation buttons
- [ ] Chat UX patterns: message editing, regeneration, conversation history sidebar

### 4.3 🆕 Deployment & Infrastructure (the syllabus stops at "robust code")

> The source analysis: *"There is no cloud provider, no CI/CD, no Kubernetes, no infrastructure-as-code... do not expect to come out able to deploy and operate a service end to end."*

- [ ] Docker beyond basics: multi-stage builds, docker-compose for full stacks (API + worker + Redis + vector DB)
- [ ] One cloud provider properly (pick AWS): EC2, S3, IAM basics, a managed database
- [ ] Simple deploys first: Vercel (frontend), Railway/Render/Fly.io (backend)
- [ ] CI/CD with GitHub Actions: run tests, build image, deploy on merge
- [ ] Reverse proxy + HTTPS (nginx/Caddy), domains, environment secrets management
- [ ] Kubernetes *concepts* (pods, deployments, services) — enough to converse, not to administer
- [ ] Infrastructure-as-code taste: Terraform hello-world
- [ ] Monitoring beyond LLM tracing: uptime, error rates, alerts (e.g. Grafana/Prometheus or a hosted equivalent)

### 4.4 🆕 Production Model Serving (beyond Ollama)

Ollama is for your laptop. Serving open models at scale is its own skill:

- [ ] **vLLM**: PagedAttention in practice, continuous batching, OpenAI-compatible server
- [ ] Quantization formats for deployment: GGUF, AWQ, GPTQ — what runs where
- [ ] GPU basics: VRAM math (what fits on what card), renting GPUs (RunPod, Modal, Lambda)
- [ ] Serverless inference: Modal / Replicate / HF Inference Endpoints
- [ ] Latency anatomy: time-to-first-token vs tokens-per-second, and what moves each

### 4.5 🆕 Technologies the projects assume but no module teaches

> The source analysis: *"The projects assume BM25, cross-encoder reranking, sandboxed command execution, the GitHub API, Streamlit, and market data ingestion. None of these appear as a module topic."* Budget explicit self-study time:

- [ ] **BM25 / lexical search**: `rank_bm25`, or better, how Elasticsearch/OpenSearch do it (needed for Project 05)
- [ ] **Cross-encoder rerankers**: `sentence-transformers` cross-encoders, Cohere Rerank (Project 05)
- [ ] **Sandboxed code execution**: Docker-based sandboxes, subprocess isolation, timeouts, resource limits (Projects 06, 16)
- [ ] **GitHub API**: REST + webhooks, reading diffs, posting review comments, GitHub Apps vs PATs (Project 07)
- [ ] **Streamlit**: fast UI for internal tools and demos (Project 13)
- [ ] **Market data ingestion**: free APIs (yfinance, Alpha Vantage), rate limits, news feeds (Project 09)
- [ ] **PDF parsing done right**: PyPDF vs pymupdf vs unstructured vs LLM-native document parsing (Project 14)

### 4.6 🆕 Modern & Frontier Topics (keep current — this field moves monthly)

- [ ] Reasoning models & test-time compute: when "thinking" tokens are worth it
- [ ] Computer-use / browser-use agents
- [ ] Structured agent harnesses: OpenAI Agents SDK, Claude Agent SDK, Google ADK — compare with what you built by hand
- [ ] DPO and modern post-training (the successor conversation to RLHF from Module 32)
- [ ] Synthetic data generation for fine-tuning and evals
- [ ] Small language models on-device; edge inference
- [ ] Context engineering at scale: compaction, memory files, subagent context isolation
- [ ] Follow the field: model release notes, provider changelogs, one good newsletter — 30 min/week, permanently

### 4.7 🆕 AI System Design & Career

- [ ] System design for AI apps: draw the architecture of a RAG product, an agent platform, a Perplexity clone — with queues, caches, DBs, failure modes, and cost model
- [ ] Cost modelling: tokens × price × traffic; caching strategy; model-tier routing
- [ ] Estimating and defending latency budgets
- [ ] Write about what you build: one README + one blog post per flagship project
- [ ] Portfolio: 3 polished projects > 17 half-finished ones (the source analysis warns *"a half-finished Perplexity clone reads worse than a polished smaller build"*)
- [ ] Interview prep: LLM system design questions, agent design questions, eval design questions

**✅ Phase 4 exit criteria:** One flagship project deployed on a real domain with a streaming chat UI, CI/CD, tracing, and an eval suite — a URL you can put on a resume.

---

## Project Catalogue

### The 17 builds from the bootcamp

| # | Project | Type | Module | Stack |
|---|---------|------|--------|-------|
| 01 | Working with the OpenAI API | Core | 4 | OpenAI API, Python |
| 02 | Customer Support Agent | Core | 4A | OpenAI API, RAG, vector store, routing logic |
| 03 | Exploring Embeddings | Core | 7 | Embedding models, numpy, visualization |
| 04 | RAG Chatbot over YouTube Transcripts | Core | 8 | Pinecone, OpenAI, transcript ingestion, chunking |
| 05 | Enterprise Advanced RAG | **Flagship** | 9A | LangChain, BM25, cross-encoder reranker, RAGAS, guardrails |
| 06 | Claude Code-like Coding Agent | **Flagship** | 14A | LangGraph, MongoDB checkpointing, sandboxed execution, tool calling |
| 07 | AI Code Reviewer like CodeRabbit | **Flagship** | 18A | MCP / Agent SDK, GitHub API, RAG, structured outputs |
| 08 | Voice-Based AI Agent | **Flagship** | 17 | STT, TTS, tool calling, streaming |
| 09 | AI Trading Agent | Bonus | 26 | Agentic RAG, market data APIs, structured outputs, risk rules |
| 10 | Simple Neural Network in TensorFlow | Mini | 27 | TensorFlow |
| 11 | MNIST Autoencoder | Mini | 27 | PyTorch/TensorFlow, MNIST |
| 12 | Multi-Input Models for OCR | Core | 29 | PyTorch, CNN + sequence heads, multi-loss training |
| 13 | ChatGPT-Style Chatbot Platform | **Flagship** | capstone* | Streamlit, ChromaDB, memory layer, web search tools |
| 14 | Chat With Any Document | Core | capstone* | PDF parsing, chunking, vector store, RAG |
| 15 | AI Search Engine like Perplexity | **Flagship** | capstone* | Agentic retrieval, hybrid search, SSE streaming, eval harness |
| 16 | AI Web App Builder like Lovable/v0 | **Flagship** | capstone* | Multi-agent orchestration, code generation, sandboxed preview |
| 17 | AI Interview Taker like Mercor | **Flagship** | capstone* | Voice pipeline, Pydantic rubric scoring, report generation |

\* *Capstones: the PDF notes these five don't map to any module — they're assembled from techniques across many modules. Treat them as end-of-Phase-2 (or Phase 4) capstone builds.*

### 🆕 5 added projects (to close the Phase 4 gaps)

| # | Project | Closes gap | Stack |
|---|---------|-----------|-------|
| A1 | Streaming Chat UI for your RAG backend | 4.2 Interface layer | Next.js, Vercel AI SDK, SSE, tool-call rendering |
| A2 | Deploy Project 05 end-to-end | 4.3 Deployment | Docker Compose, GitHub Actions, Railway/AWS, domain + HTTPS |
| A3 | Serve an open model with vLLM + load test it | 4.4 Serving | vLLM, quantized Llama/Qwen, locust/k6, latency dashboard |
| A4 | Tabular ML baseline vs LLM shootout | 4.1 Classical ML | scikit-learn, XGBoost, honest eval writeup |
| A5 | Eval harness as a reusable library | Module 23 depth | pytest-style LLM evals, LLM-as-judge, CI integration |

**Portfolio strategy:** clone-projects (Claude Code, CodeRabbit, Perplexity, Lovable, Mercor, ChatPDF) are deliberately named after real products — a reviewer instantly understands scope. The bar is therefore high: **pick 2–3 and polish them fully** (deployed, UI, evals, README, demo video) instead of shipping all 17 at demo quality.

---

## Technology Stack Inventory

Everything the roadmap touches. Bootcamp items are from the PDF; 🆕 items are added by this roadmap.

| Category | Tools & techniques |
|---|---|
| Languages & core | Python, Cypher · 🆕 SQL, TypeScript |
| Backend & serving | FastAPI, Pydantic, SSE, Docker, Python RQ, Redis/Valkey · 🆕 vLLM, nginx/Caddy |
| Model providers & SDKs | OpenAI API/SDK, Anthropic Claude SDK, Hugging Face Hub, Google Gemma, Ollama |
| Agent frameworks | LangChain, LCEL, LangGraph, LangFlow, LlamaIndex, smolagents, AutoGen, CrewAI, Agent SDK · 🆕 OpenAI Agents SDK, Claude Agent SDK |
| Protocols | MCP, A2A |
| Vector & graph stores | ChromaDB, Pinecone, Milvus, Neo4j, Kuzu, MongoDB (checkpointing) · 🆕 pgvector |
| Memory | Mem0, vector-DB-backed memory, graph memory |
| Retrieval | Chunking, hybrid search (BM25 + vector), cross-encoder reranking, query rewriting |
| Observability | Langfuse, LangSmith, Braintrust, OpenLLMetry, OpenTelemetry GenAI conventions |
| Evaluation | RAGAS, LLM-as-judge, binary pass/fail, failure bucketing, three gulfs model |
| Safety & guardrails | OWASP Top 10 for LLMs, NeMo Guardrails, Llama Guard, ShieldGemma, moderation APIs |
| Deep learning | PyTorch, TensorFlow, torchmetrics, TensorBoard, Unsloth, CLIP, CLAP · 🆕 scikit-learn, XGBoost |
| UI | Streamlit · 🆕 React, Next.js, Vercel AI SDK |
| Infra & deploy 🆕 | GitHub Actions, Vercel, Railway/Render/Fly.io, AWS basics, Terraform (taste), Kubernetes (concepts) |
| External APIs | GitHub API, web search tools, market data & news feeds |

---

## Suggested Timeline

Assumes ~10–15 hrs/week alongside work. Compress if full-time; the order matters more than the pace.

| Phase | Duration | Milestone |
|---|---|---|
| Phase 0 — Foundations | 4–8 weeks (skip if you already code) | API-calling Python script in a Git repo |
| Phase 1 — LLM Fundamentals | 2–3 weeks | CLI chatbot on raw API calls |
| Phase 2a — Modules 3–9A (prompting → RAG) | 6–8 weeks | Projects 01–05 done; Enterprise RAG is your first flagship |
| Phase 2b — Modules 10–18 (agents) | 6–8 weeks | Coding agent or code reviewer flagship done |
| Phase 2c — Modules 19–26 (production) | 4–6 weeks | Tracing + evals + guardrails retrofitted onto your flagship |
| Phase 4 (part 1) — UI + deployment (4.2–4.3) | 4–6 weeks | Flagship live on a real URL with streaming UI |
| Phase 3 — Deep learning track | 8–12 weeks (parallelizable / optional) | Transformer from scratch + LoRA fine-tune |
| Phase 4 (part 2) — Serving, capstone, career | 4–6 weeks | One capstone (Perplexity/Lovable/Mercor class) polished |

> Phase 3 can run in parallel with Phase 4, or be deferred entirely if your goal is application engineering. Do Phase 4.2–4.3 **before** Phase 3 — a deployed project with a real UI is worth more on a resume than knowing what a GRU is.

---

## Known Issues in the Source Syllabus

Carried over from the PDF's own structural analysis, so you don't get confused mid-course:

1. **Modules 1–2 are absent** from the source material — reconstructed here as [Phase 1](#phase-1--llm--genai-fundamentals-reconstructs-missing-modules-12).
2. **Numbering collisions:** "9A" labels both the LlamaIndex section *and* the Enterprise RAG project; "14A" labels both the LangFlow section *and* the coding-agent project.
3. **Framework inconsistency:** Module 27 is titled "Math & *PyTorch* Foundations" but its first mini project is in *TensorFlow* (likely carried over from an older course version). Don't sweat it — do one in each, the concepts transfer.
4. **Five capstone projects map to no module** — they're integration builds, not module deliverables.
5. **Two stacked courses, not one:** Modules 3–26 and 27–33 are separate tracks. The seam is intentional — applications first, internals second.

---

## Guiding Principles

1. **Build > watch.** One deployed project beats ten completed tutorials.
2. **Raw APIs before frameworks.** Write your first agent loop with bare `while` + function calling before touching LangGraph — you'll actually understand what the framework abstracts.
3. **Evals are the moat.** Anyone can demo an agent. Measuring and improving one systematically (Modules 22–23) is the rare, hireable skill.
4. **Treat AI apps as software first.** Retries, schemas, tracing, tests, and security are not optional garnish — they *are* the job. "AI Engineer" = software engineer who happens to orchestrate models.
5. **Every project stops at an API boundary — yours shouldn't.** Add the UI, deploy it, put it on a URL. That's the arbitrage the source analysis identified.
6. **Stay current on a schedule, not a doomscroll.** 30 minutes a week reading release notes beats 5 hours of Twitter panic.
7. **Depth over breadth in frameworks.** Overview all of them; master LangGraph + one SDK.
8. **Write it up.** A README with architecture diagram, trade-offs, and eval results turns a repo into a portfolio piece.

---

*Roadmap sources: [AI-Engineering-Bootcamp-Syllabus-Breakdown (1).pdf](AI-Engineering-Bootcamp-Syllabus-Breakdown%20(1).pdf) (31 modules, 17 projects, structural analysis) + added phases 0, 1, and 4 closing the gaps that analysis identifies.*
