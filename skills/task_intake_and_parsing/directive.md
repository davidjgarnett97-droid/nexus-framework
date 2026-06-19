# Directive — task_intake_and_parsing

## Goal
Receive the raw request. Produce a structured TASK BRIEF. Do not answer, research, or opine. Categorize and structure.

## When to Activate
Every new request. First node. No exceptions.

## Workflow

### Step 1 — Classify Task Type
One of:
- **Research** — gather/synthesize information
- **Analysis** — examine data, options, or a situation
- **Decision support** — help choose between options
- **Planning** — produce a plan, schedule, or roadmap
- **Creative** — write, design, or generate content
- **Execution** — do something (book, send, build)
- **Review** — check, critique, or improve something
- **Unknown** — ambiguous or doesn't fit

### Step 2 — Identify Domain
Name the primary domain (e.g., sales, support, finance, operations, technology, etc.).

If it spans two, name primary + secondary.

### Step 3 — Estimate Complexity
- **Simple** — single step, clear answer
- **Moderate** — multiple steps or some ambiguity, manageable
- **Complex** — multi-phase, high ambiguity, significant research/synthesis

### Step 4 — Resolve Domain Familiarity
Call `memory_retrieval(domain=primary_domain)`:
- `is_new_domain: true` → `New`
- `past_sessions_found >= 3` → `Familiar`
- `past_sessions_found 1-2` → `Unknown — treat as new`

If memory_retrieval is unavailable: mark `Unknown`.

### Step 5 — Summarize and Flag
- One-to-two sentence summary in plain language
- List key_unknowns. If none, return `[]` (not null).

### Step 6 — Recommend Next Skill
- `key_unknowns` non-empty → `clarification`
- `key_unknowns` empty AND criteria need pressure-testing → `criteria_validation`
- Clean brief → `planning`

### Step 7 — Pass Through execution.py
```python
from skills.task_intake_and_parsing.execution import intake
result = intake(raw_request="...", task_type="Planning", primary_domain="...", ...)
```

Validates enums + logical consistency, returns formatted brief.

### Step 8 — Hand to Recommended Next Skill
Pass `task_brief` downstream.

## Rules
- Do not attempt to answer
- Do not start research
- Do not give opinions
- Read, classify, structure
- key_unknowns is always an array — never null
- recommended_next_skill must match the gap profile
