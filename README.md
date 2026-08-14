# JARVIS AI

> A modular personal AI assistant built with Python, combining voice interaction, computer automation, Gemini tool calling, Retrieval-Augmented Generation (RAG), and multi-step task planning.

JARVIS is designed as an evolving AI assistant rather than a single monolithic application. The architecture separates conversation, tools, knowledge retrieval, planning, verification, and computer control so that each subsystem can be developed and tested independently.

---

## Overview

JARVIS currently combines three major intelligence layers:

- **V3 — Tool Calling:** Gemini can select and execute structured computer tools.
- **V4 — RAG:** JARVIS can retrieve relevant information from a local knowledge base and generate grounded answers with source information.
- **V5 — Agent Planning:** JARVIS can convert complex requests into structured multi-step tasks, execute them, verify each step, recover from failures, and support task cancellation.

The result is a system that can distinguish between:

```text
Knowledge → RAG
Action    → Tools
Task      → Planner
Chat      → Gemini
```

---

# Architecture

```text
                           USER
                            │
                            ▼
                     Voice / Text Input
                            │
                            ▼
                         main.py
                            │
                            ▼
                         brain.py
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
         V5 Planner      V4 RAG         V3 Tools
             │              │              │
             ▼              ▼              ▼
        Task Runner     Vector Store   Tool Registry
             │              │              │
             ▼              ▼              ▼
        Verification     Retrieval      action.py
             │              │              │
             └──────────────┴──────────────┘
                            │
                            ▼
                 Browser / Computer / OS
```

JARVIS is intentionally modular so that new models, tools, retrieval systems, and integrations can be added without rewriting the entire assistant.

---

# Features

## Voice Interaction

JARVIS supports a voice-driven interaction loop with:

- Wake-word detection
- Speech recognition
- Voice command processing
- Spoken responses
- Conversational interaction

The project uses Whisper-based speech recognition and a Gemini-powered reasoning layer.

---

## Computer Automation

JARVIS can interact with the local computer through structured actions.

Examples include:

- Opening applications
- Opening Google
- Opening YouTube
- Searching YouTube
- Searching Google
- Scrolling webpages
- Clicking links
- Opening VS Code
- Opening File Explorer
- Opening PowerShell
- Opening Downloads
- Opening the JARVIS project
- Opening ChatGPT
- Opening Gemini
- Controlling system volume
- Muting and unmuting volume

---

# V3 — Gemini Tool Calling

## Overview

V3 introduces structured LLM tool calling.

Instead of relying only on manually matched intents, Gemini can select a registered tool and provide structured arguments.

The execution flow is:

```text
User Request
     │
     ▼
Gemini
     │
     ▼
Function / Tool Call
     │
     ▼
Tool Registry
     │
     ▼
action.py
     │
     ▼
Execution Result
     │
     ▼
Gemini
     │
     ▼
Final Response
```

## Tool Registry

Tools are registered through `tools.py`.

Each tool contains:

- Name
- Description
- Function
- Parameter schema

Examples:

```text
search_youtube(query)
set_volume(percent)
open_youtube()
scroll_down()
click_link(link_name)
```

## Tool Validation

Tool arguments are validated before execution.

For example:

```text
set_volume(percent=50)      ✅
set_volume(percent=500)     ❌
set_volume(percent="50")    ❌
unknown_tool(...)            ❌
missing required argument   ❌
```

This prevents invalid model-generated arguments from reaching the underlying computer actions.

## Multi-Tool Execution

JARVIS can execute multiple tools during a single request.

Example:

```text
Open YouTube and search for Python tutorials.
```

can result in:

```text
1. open_youtube()
2. search_youtube("Python tutorials")
```

The tool result is then returned to Gemini so it can generate the final response.

---

# V4 — Retrieval-Augmented Generation

## Overview

V4 gives JARVIS a local knowledge and retrieval system.

The RAG pipeline is:

```text
Document
   │
   ▼
Chunking
   │
   ▼
Embedding
   │
   ▼
Vector Store
   │
   ▼
Semantic Search
   │
   ▼
Relevant Context
   │
   ▼
Gemini
   │
   ▼
Grounded Answer
```

## Embeddings

JARVIS uses Gemini embeddings to convert text into numerical vectors.

This allows semantic retrieval rather than simple keyword matching.

---

## Smart Document Chunking

Documents are divided into manageable chunks before embedding.

The chunking system is designed to prefer:

```text
Paragraph boundary
        ↓
Sentence boundary
        ↓
Word boundary
```

instead of splitting words in the middle.

This improves the quality of retrieved context.

---

## Vector Store

JARVIS includes a local vector store that supports:

- Embedding storage
- Metadata
- Cosine similarity
- Top-k retrieval
- Persistent local storage

Each stored item can contain:

```text
text
embedding
metadata
content_hash
```

---

## Document Ingestion

The knowledge system can ingest supported text-based files and convert them into searchable knowledge.

Supported formats currently include:

```text
.txt
.md
.py
.json
```

The ingestion pipeline is:

```text
File
 ↓
Read
 ↓
Chunk
 ↓
Embed
 ↓
Store
```

---

## Duplicate Protection

V4 includes duplicate-ingestion protection using content hashing.

When the same content is ingested again:

```text
First ingestion
→ Store chunks

Second ingestion
→ Detect duplicate
→ Skip existing chunks
```

This prevents unnecessary duplicate vectors from accumulating.

---

## Multi-Document Knowledge Base

JARVIS can ingest multiple documents while preserving the source associated with each document.

Example:

```text
Document A
    ↓
Vector Store

Document B
    ↓
Vector Store

Document C
    ↓
Vector Store
```

Semantic search then retrieves the most relevant chunks across the knowledge base.

---

## Source-Aware Answers

RAG responses can include their source information.

Example:

```text
JARVIS V5 supports task cancellation between steps.

Sources:
- knowledge_tests/test_knowledge_a.txt
```

This makes retrieved answers easier to trace back to the underlying knowledge.

---

# V5 — Agent Planning and Multi-Step Execution

## Overview

V5 introduces structured task planning.

A complex user request is converted into a `TaskPlan` containing multiple `TaskStep` objects.

Example:

```text
User:
Open YouTube and search YouTube for Python tutorials
and scroll down.
```

becomes:

```text
1. Open YouTube
2. Search YouTube for "python tutorials"
3. Scroll down
```

A more complex request can become:

```text
1. Open YouTube
2. Search YouTube for "python beginner course"
3. Scroll down
4. Click "python full course"
```

---

## Task Runner

The task runner executes each planned step in order.

For every step, JARVIS can:

- Start the step
- Execute the action
- Verify the result
- Report progress
- Retry when necessary
- Attempt recovery
- Continue to the next step

---

## Verification

V5 includes step-level verification and overall goal verification.

Example:

```text
V5 VERIFY: open_youtube -> True
V5 VERIFY: search_youtube -> True
V5 VERIFY: scroll_down -> True

V5 GOAL VERIFY: True
```

This prevents JARVIS from simply assuming a task succeeded.

---

## Retry and Recovery

When an action fails, V5 can attempt recovery.

For example, a link click may trigger:

```text
Click failed
    ↓
Scroll
    ↓
Retry click
    ↓
Verify result
```

This allows the task runner to recover from common browser interaction failures.

---

## Task Cancellation

V5 supports live task cancellation.

A running task can be stopped between steps so that execution does not continue unnecessarily.

The task state is updated to indicate cancellation.

---

## Task Progress

The task system can report progress such as:

```text
Step 1/4: Open YouTube
Completed 1/4

Step 2/4: Search YouTube
Completed 2/4

Step 3/4: Scroll down
Completed 3/4

Step 4/4: Click course
Completed 4/4

Task completed.
```

---

# Routing Strategy

JARVIS uses different subsystems depending on the type of request.

```text
User Request
     │
     ▼
   brain.py
     │
     ├── Known direct action
     │       └── Existing action handler
     │
     ├── Multi-step task
     │       └── V5 Planner
     │
     ├── Knowledge question
     │       └── V4 RAG
     │
     ├── Action not handled directly
     │       └── V3 Tool Calling
     │
     └── General conversation
             └── Gemini
```

This separation allows the assistant to use the most appropriate subsystem instead of treating every request as a simple chat question.

---

# Project Structure

The project includes the following major modules:

```text
JARVIS/
│
├── main.py
├── brain.py
├── ai.py
├── action.py
├── intent.py
├── config.py
├── memory.py
│
├── browser_controller.py
│
├── voice.py
├── whisper_ai.py
├── interrupt.py
├── stop_listening.py
│
├── tools.py
├── gemini_tools.py
│
├── planner.py
├── task_engine.py
├── task_manager.py
├── task_runner.py
├── task_state.py
├── verifier.py
├── goal_verifier.py
│
├── document_chunker.py
├── document_ingest.py
├── embeddings.py
├── vector_store.py
├── rag_store.py
├── rag_answer.py
├── knowledge_base.py
│
└── knowledge_tests/
```

---

# Installation

## Requirements

JARVIS requires Python and the project's Python dependencies.

Install the dependencies used by the project environment.

Example:

```powershell
pip install google-genai
pip install python-dotenv
pip install playwright
```

Additional packages may be required for the voice, Whisper, audio, computer-automation, and Windows-specific components.

Install the Playwright browser if required:

```powershell
playwright install
```

---

# Configuration

Create a local `.env` file in the project directory.

Example:

```env
GEMINI_API_KEY=your_api_key_here
```

Never commit API keys or other secrets to GitHub.

The project should keep `.env` excluded through `.gitignore`.

---

# Running JARVIS

From the project directory:

```powershell
python main.py
```

JARVIS will start the voice interaction loop and wait for the wake word.

Example:

```text
Hey Jarvis
```

Then try:

```text
Open Google.
```

or:

```text
Could you bring up the YouTube homepage for me?
```

or:

```text
How does V5 handle task cancellation?
```

or:

```text
Open YouTube and search for Python tutorials.
```

---

# Testing

The project contains subsystem tests for the major components.

## Tool Calling

```powershell
python test_tools.py
python test_tool_schemas.py
python test_gemini_tools.py
python test_tools_execution.py
python test_tool_safety.py
```

## RAG

```powershell
python test_embeddings.py
python test_chunker.py
python test_vector_store.py
python test_rag_store.py
python test_rag_answer.py
python test_document_ingest.py
python test_knowledge_base.py
python test_rag_sources.py
python test_v4_12.py
```

## V5 Planning and Execution

```powershell
python test_planner.py
python test_live_task.py
python test_v5_final.py
```

These tests cover:

- Tool registration
- Tool schemas
- Gemini function calling
- Tool execution
- Argument validation
- Embeddings
- Chunking
- Semantic retrieval
- RAG generation
- Document ingestion
- Duplicate protection
- Multi-document retrieval
- Source-aware answers
- Task planning
- Step verification
- Goal verification
- Retry and recovery
- Task cancellation

---

# Development Philosophy

JARVIS is developed incrementally.

Each major subsystem is built and tested independently before being connected to the main assistant.

The project emphasizes:

- Modularity
- Testability
- Clear separation of responsibilities
- Structured tool execution
- Retrieval-grounded responses
- Verified task execution
- Safe handling of tool arguments
- Incremental architecture improvements

The goal is to allow future components such as local language models, MCP integrations, advanced memory, evaluation systems, and deployment infrastructure to be added without replacing the existing architecture.

---

# Roadmap

```text
V1  ✅ Voice pipeline
V2  ✅ Modular architecture + computer actions + interrupts + memory
V3  ✅ LLM tool/function calling
V4  ✅ RAG + embeddings + vector database
V5  ✅ Agent planning + multi-step execution
V6  ⏳ Ollama / local LLM support
V7  ⏳ MCP integration
V8  ⏳ Advanced memory + evaluation + observability
V9  ⏳ Docker / deployment + polished UI
```

---

# Current Status

JARVIS currently has working implementations for:

```text
V3  Tool Calling
V4  Retrieval-Augmented Generation
V5  Agent Planning
```

The next major development milestone is:

```text
V6 — Local LLM Support
```

---

# Security Notes

Never commit the following to the repository:

```text
.env
API keys
credentials
browser profiles
local vector-store data
temporary audio files
generated caches
Python __pycache__ files
local test artifacts
```

Use `.gitignore` to keep local runtime data and secrets out of version control.

---

# License

Add your preferred license here.

For example:

```text
MIT License
```

or replace this section with the license you choose for the project.

---

# Acknowledgements

JARVIS builds on a number of open-source and commercial technologies, including:

- Python
- Google Gemini
- Google GenAI SDK
- Whisper-based speech recognition
- Playwright
- Python audio and automation libraries
