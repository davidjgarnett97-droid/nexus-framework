# Nexus Framework Architecture

## Overview

Nexus is a 3-layer system that separates intent from decision-making from execution. LLMs are probabilistic; most business logic is deterministic. This separation fixes that mismatch.

---

## Layer 1 — Directive (What to Do)

SOPs written in Markdown. No code, no logic — just clear instructions in plain language, like giving a task to a mid-level employee.

**File locations:**
- `skills/<name>/directive.md` — per-skill instructions
- `domains/<domain>/domain_state.md` — domain-level context and running state

Each directive defines: goal, inputs, tools to call, expected outputs, and edge cases. Directives are living documents — agents update them when they learn something new.

---

## Layer 2 — Orchestration (Decision Making)

The AI agents. They read directives, call execution tools in the right order, handle errors, and route work to the right specialist.

**Agent roster:**

| Agent | Role |
|---|---|
| Nexus | Master orchestrator — routes all tasks |
| Vertex | Calendar, email, communications |
| The Researcher | Domain research, source validation |
| The Critic | Challenges conclusions, scores confidence |
| The Memory Keeper | Audit trails, context management |
| The Escalation Handler | Routes blocked or sensitive decisions to the human |
| Quill | Formats and delivers final output |
| The Meta Agent | Proposes new agents and tool integrations |

Agents do not scrape websites or write SQL themselves. They read the directive for a task and call the execution script for it. The orchestration layer is the glue — not the worker.

---

## Layer 3 — Execution (Doing the Work)

Deterministic Python scripts in `execution/`. Fast, testable, and reliable. Credentials live in `.env`. Scripts are called by agents, never by users directly.

**Why this matters:** If an agent does everything itself, errors compound. 90% accuracy per step = 59% success over 5 sequential steps. Pushing complexity into deterministic code breaks that failure chain.

---

## Self-Annealing Loop

When something breaks:

1. Fix the script
2. Update the tool
3. Test — confirm it works
4. Update the directive with the new behavior or edge case

The system gets stronger from every failure. Bugs become institutional knowledge.

---

## Skill Contract Model

Each skill is a unit of deployable capability with four required components:

| File | Purpose |
|---|---|
| `directive.md` | SOP — what this skill does and how |
| `skill_contract.md` | I/O spec — inputs, outputs, success criteria |
| `execution.py` | Validation script — confirms the skill produces correct output |
| `version.yaml` | Version tracking — status (draft/production), changelog |

A skill cannot be deployed to production without all four components passing review.

---

## Domain and Project Hierarchy

```
org
└── domain (e.g., sales, support, finance)
    ├── domain_state.md
    └── project (e.g., lead_pipeline, customer_onboarding)
        ├── directive.md
        └── execution scripts
```

Domains group related capabilities. Projects are discrete units of work within a domain. Agents operate at the project level; Nexus operates at the domain and org level.
