# Directive — planning

## Goal
Produce the ordered execution plan. Decompose the goal into discrete steps, each assigned to one skill.

## When to Activate
After `success_definition.finalize` returns the locked definition. Always runs.

## Workflow

### Step 1 — Decompose the Goal
For each step ask:
- What specifically needs to happen?
- What does completion look like?
- Does this depend on a previous step's output?
- Which skill best handles this?
- How much effort is this?

Aim for narrow, single-skill steps.

### Step 2 — Classify Execution Type
- **SEQUENTIAL** — waits for previous step
- **PARALLEL with Step X** — runs alongside another step
- **CONDITIONAL on (condition)** — only runs if condition met

### Step 3 — Inherit Convergence Threshold
Pull from `success_definition.convergence_threshold`. Do not override here.

### Step 4 — Assign Skills
For each step, name the skill from `agents/skill_registry.yaml` that handles it.

If no suitable skill exists → mark `UNASSIGNED`, log the missing capability. Plan returns `BLOCKED_SKILL_GAP`.

### Step 5 — Pass Through execution.py
```python
from skills.planning.execution import build_plan
result = build_plan(task="...", success_definition={...}, steps=[...])
```

Validator catches:
- Missing fields
- Invalid execution_type
- CONDITIONAL without condition
- Circular dependencies
- depends_on referencing unknown step names
- No entry point
- Unknown assigned_skill (treated as skill gap)

### Step 6 — Inspect Result
- `plan_status = READY_TO_EXECUTE` → hand to `dependency_mapping` then `priority_and_sequencing`
- `plan_status = BLOCKED_SKILL_GAP` → escalate via `human_escalation` (skills must be built first)

## Rules
- Do not execute any step — this skill produces a plan only
- Every step has an assigned skill (gaps OK as `UNASSIGNED`, flagged for escalation)
- Constraints must be explicit
- Log the completed plan to audit trail (TASK_START or SKILL_OUTPUT) before passing on
