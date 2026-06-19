# Directive — success_definition

## Goal
Lock the finish line before any execution begins. Two-phase: identify ambiguities, then finalize with user input.

## When to Activate
After `criteria_validation` returns `gate_status: approved_proceed`. Always runs — do not skip.

## Workflow

### Phase A — Identify Ambiguities

#### Step 1 — Scan the Brief
Read the completed brief. Identify points where success is unclear:
- Desired output format unspecified?
- Quantity/scope undefined?
- Quality bar missing?
- End use case unclear?
- Competing interpretations of "good result"?

Compile into a numbered ambiguity list.

#### Step 2 — Call execution.py (Mode A)
```python
from skills.success_definition.execution import identify_ambiguities
result = identify_ambiguities(completed_brief={...}, ambiguities=[
    {"number": 1, "label": "deliverable_format", "description": "..."},
    ...
])
```

Returns a `user_prompt` ready to deliver.

#### Step 3 — Deliver the User Prompt
The orchestrating agent presents the pre-formatted prompt:
> Quick check before I start — I want to make sure I'm aiming at the right target.
> Here's where I'm not 100% sure what success looks like:
> 1. [item]
> 2. [item]
>
> **Option 1 — Let's talk:** I'll go through each one with you.
> **Option 2 — Just go:** I'll make reasonable assumptions, document them, and proceed.

### Phase B — Finalize

#### Step 4 — Branch on User Response
**If user chose `collaborative`:**
- Work through each ambiguity sequentially
- After each response, assign clarity_score (0–100)
- If ≥ 97: accept, next item
- If < 97: one focused pushback. Max 5 pushbacks per item.

**If user chose `autonomous`:**
- Make a reasonable assumption per ambiguity
- Document each assumption explicitly in `assumptions_made`

#### Step 5 — Set Convergence Threshold
- Simple → 70
- Moderate → 80
- Complex → 85
- High-stakes (financial, legal, irreversible) → 90–95
- Default if uncertain → 80

#### Step 6 — Call execution.py (Mode B)
```python
from skills.success_definition.execution import finalize
result = finalize(
    user_choice="collaborative",
    agreed_outcome="...",
    output_format="...",
    measurable_criteria=["...", "..."],
    convergence_threshold=80,
    ...
)
```

#### Step 7 — Hand to planning
Pass `success_definition` to `planning`.

## Rules
- Never skip Phase A — always present the user prompt
- One question at a time in collaborative mode
- 97% clarity threshold
- Max 5 pushbacks per item — beyond that, escalate
- convergence_threshold must be concrete enough for `convergence` to evaluate against
