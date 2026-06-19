# Getting Started — Nexus Agent Harness

A practical guide for deploying Nexus inside your organization. Read time: ~10 minutes.

---

## 1. Prerequisites

- **Claude Code CLI** — [Install guide](https://docs.anthropic.com/en/docs/claude-code). You need this to run the harness. Claude Code is the execution environment.
- **Python 3.10+** — The execution layer is Python. Run `python --version` to confirm.
- **An Anthropic account** — Claude Pro (for interactive use) or an API key (for programmatic agents). Set it as `ANTHROPIC_API_KEY` in your environment or `.env` file.
- Optional: MCP integrations (Gmail, Google Calendar, Notion) if you want those tools available to agents. Each requires its own credentials.

---

## 2. Clone and Explore

```bash
git clone <your-fork-url>
cd nexus
```

Key directories:

```
CLAUDE.md                  # Master orchestration prompt — this is Nexus
Nexus/
  SystemPrompts/           # One .md file per sub-agent (Nexus, Vertex, Researcher, etc.)
  Skills/                  # 36 skill docs — each is a deployable agent behavior
directives/                # SOPs written in plain language (what to do and when)
execution/                 # Python scripts — deterministic execution layer
execution/lib/             # Shared utilities (auth, CRM, Notion, Google APIs)
execution/nexus/           # Orchestration runner and test suite
```

The three-layer model: **directives** define intent, **Nexus** (CLAUDE.md) routes and reasons, **execution scripts** do the deterministic work. Don't skip any layer.

---

## 3. Set Up Your First Domain

A domain is a functional area — Sales, Ops, Finance, etc. Each domain gets:
- A folder under `directives/<domain>/`
- An SOP file describing the work the domain handles
- Optionally, a sub-agent system prompt under `Nexus/SystemPrompts/`

To add a domain:

```bash
mkdir directives/sales
```

Create `directives/sales/sales.md` with:
- **Purpose** — what this domain handles
- **Key inputs** — what data or requests come in
- **Key outputs** — what the agent produces
- **Execution scripts** — which `execution/` scripts this domain uses
- **Escalation rules** — when to surface to a human

Then add a routing entry in `CLAUDE.md` under the Sub-Agent Routing Guide section so Nexus knows when to delegate to this domain.

---

## 4. Register Your First Skill

Skills live in `Nexus/Skills/`. Each file is a deployable behavior that gets embedded in a sub-agent's system prompt.

A skill doc has this structure:

```yaml
# Skill N — Name

Sub-Agent: <which agent runs this>
Status: Draft | Source | AI Generated
Trigger: <when this skill activates>

## Skill Contract
| Field      | Value                         |
|------------|-------------------------------|
| Input      | <what comes in>               |
| Process    | <what the agent does>         |
| Output     | <what comes out>              |
| Downstream | <next skill or terminal>      |

## Skill File
<the actual system prompt text to paste into the agent>
```

Copy an existing skill (e.g., `Nexus/Skills/Skill_01_Task_Intake_and_Parsing.md`) as a template. Name it `Skill_37_Your_Skill_Name.md`. Write the skill contract first — input, output, downstream — before writing the prompt text. Vague contracts produce unreliable agents.

---

## 5. Create a User

Users are defined in `CLAUDE.md` or in a separate profile file if you build a multi-user layer. At minimum, document:

```yaml
# users/alice/profile.yaml
name: Alice
role: builder          # operational | builder | admin
domain_grants:
  - sales
  - ops
project_grants: []
compute: own           # own (Claude Pro) | host (API key)
```

`operational` users get a fixed action menu — no open-ended agent. `builder` users get open-ended Claude scoped to their granted domains. `admin` is you. See `Nexus/Nexus_User_Tiers_and_Skill_Promotion.md` for the full tier design.

---

## 6. Configure CLAUDE.md

`CLAUDE.md` is the master orchestration prompt. It tells Nexus:
- Its responsibilities and skill sequence (Skills 1–7, 20–23)
- Which requests to handle directly vs. delegate
- The routing table (which domain or sub-agent handles what)
- Escalation rules

Edit the **Sub-Agent Routing Guide** section to add your domains. Keep the routing entries specific — Nexus pattern-matches on keywords, so vague entries cause mis-routing.

Copy the sub-agent system prompts from `Nexus/SystemPrompts/` into your agents. At minimum you need Nexus (master) and whichever domain agents you build. The specialist agents (Researcher, Critic, Memory Keeper) are optional until you need them.

---

## 7. Your First Session

Open a terminal in the repo root and start Claude Code:

```bash
claude
```

Claude Code loads `CLAUDE.md` automatically. You are now talking to Nexus.

Test with a simple intake:

> "Pull together a summary of what Sales worked on last week."

Nexus will run Skills 1–4 (intake, validation, clarification if needed, success definition) before doing any work. If a routing target doesn't exist yet, it will tell you — that's a skill gap, not a bug.

---

## 8. What to Build Next

In priority order:

1. **Domain lead agents** — write a system prompt for each domain's primary agent. Start with your highest-volume workflow.
2. **Top 5 skill directives** — pick the 5 tasks your team does most. Write a skill doc for each. These become the core of your shared skill library.
3. **Execution scripts** — for each skill, write or identify a Python script in `execution/` that does the deterministic part (API calls, data writes, file operations). Keep logic out of the agent prompts.
4. **More users** — add user profiles, grant domains, test the access boundaries before you onboard real people.
5. **Skill promotion workflow** — once multiple people are building, set up the Draft -> Proposed -> Review -> Published pipeline from `Nexus/Nexus_User_Tiers_and_Skill_Promotion.md` so individual skills can enter the shared library without a manual registry edit.
