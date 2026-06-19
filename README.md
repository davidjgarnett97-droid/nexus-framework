# nexus-framework

A multi-agent AI orchestration harness. Deploy it, add your domains and agents, and run structured work through a deterministic execution layer — without rebuilding anything.

---

## What It Is

Nexus is an open-source harness for orchestrating multiple AI agents on structured tasks. It is designed to be tileable: any organization can deploy it and extend it with their own domains, skills, and agents without touching the core. Every piece — skill, domain, project, user, agent — exposes a fixed, versioned interface so it can be added or removed without breaking its neighbors.

The core problem it solves: LLMs are probabilistic. Most business logic is deterministic. Running one through the other unmediated produces inconsistent results. Nexus separates these concerns into three layers.

---

## How It Works

**Layer 1 — Directive (what to do)**
SOPs written in Markdown. Each directive defines the goal, inputs, tools to call, outputs, and edge cases. Plain language, like you would give a capable employee.

**Layer 2 — Orchestration (decision-making)**
The master agent (Nexus) reads directives, sequences execution, delegates to specialist agents, and handles errors. It does not scrape websites or write SQL — it calls the right tool and routes the result.

**Layer 3 — Execution (doing the work)**
Deterministic Python scripts. Reliable, testable, environment-variable-driven. Complexity lives here, not in the agent.

---

## The Agent Roster

| Agent | Role |
|---|---|
| Nexus | Master orchestrator — receives all tasks, plans execution, delegates |
| Vertex | Communications — calendar, email, scheduling |
| The Researcher | Domain research with source validation and triangulation |
| The Critic | Challenges conclusions, scores confidence, flags contradictions |
| The Memory Keeper | Audit trails, prior context retrieval, knowledge decay |
| The Escalation Handler | Routes blocked or sensitive tasks back to the human |
| Quill | Formats final output for delivery channels |
| The Meta Agent | Proposes new agents, tools, and domain knowledge updates |

---

## The Skill System

39 skills distributed across agents. Each skill is a reusable, versioned capability with a machine-readable contract: inputs, outputs, dependencies, confidence thresholds, and iteration limits defined up front.

Five skills are fully built and production-ready: task intake, success definition, planning, convergence, and replanning. These form the core decision loop that every task runs through.

---

## Getting Started

See [docs/getting_started.md](docs/getting_started.md).

---

## Structure

```
directives/        SOPs by domain — define what each skill does
execution/         Python scripts by domain — do the actual work
Nexus/
  Skills/          39 skill contracts
  SystemPrompts/   Agent system prompts
  Nexus_Platform_Vision.md
```

---

## Design Principles

- Enforcement lives in deterministic code, not in the agent
- Capabilities are shared; knowledge is gated; private memory is sacred
- Honesty over comfort — outputs carry confidence scores and caveats
- Physical isolation per deployment — no shared tenancy, no blast radius across clients

---

## License

MIT
