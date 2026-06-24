# Directive — build_pipeline

## Role
Orchestrates the four-stage build pipeline: Architect → Builder → Code Reviewer → QA Agent.

## Goal
Take a task brief with a confirmed success definition and produce production-ready code — with required quality gates between every stage. Nothing reaches production without passing all four stages.

## When to Activate
- Any code build task routed through Nexus
- Success definition (Skill 4) must be confirmed before invoking
- Nexus declares `PATTERN: Pipeline` when invoking this skill

## Inputs
- `task_brief` — from Skill 1
- `success_definition` — from Skill 4, confirmed by David
- `domain` — build domain (re_wholesaling, assistant, development, etc.)

## Pipeline

```
[Nexus: Task Brief + Success Definition confirmed]
         │
         ▼
   ┌─────────────┐
   │  ARCHITECT  │  Stage 1: Design document
   └──────┬──────┘
          │ Gate: design complete + gate check passes
          ▼
   ┌─────────────┐
   │   BUILDER   │  Stage 2: Implementation in tmp/builds/{build_id}/output/
   └──────┬──────┘
          │ Gate: build manifest complete, no placeholder TODOs
          ▼
   ┌──────────────────┐
   │  CODE REVIEWER   │  Stage 3: Security + correctness + design conformance
   └──────┬───────────┘
          │ Gate: PASS or PASS WITH NOTES (zero blocks)
          ▼
   ┌──────────────┐
   │   QA AGENT  │  Stage 4: Runtime verification
   └──────┬───────┘
          │ Gate: QA PASS
          ▼
   [Files promoted to execution/{domain}/]
   [Promotion record written]
   [Nexus notified — task complete]
```

## Build ID
Generate at pipeline start: `build_{domain}_{YYYYMMDD}_{short_task_slug}`
Example: `build_re_wholesaling_20260624_import_fix`

All intermediate files for this build live under `tmp/builds/{build_id}/`.

## Gate Behavior
Each stage has a required gate. A failed gate **stops the pipeline** and returns to the prior stage — not to Stage 1.

| Stage fails | Returns to | Max cycles |
|---|---|---|
| Architect gate fails | Nexus (scope problem) | 1 |
| Builder self-review fails | Architect (design gap) | 1 |
| Code Review: FAIL | Builder (implement fixes) | 2 |
| QA: FAIL | Builder (implement fixes) | 2 |

After max cycles: escalate to Nexus. Do not loop indefinitely.

## Iteration Tracking
Log iteration count per stage. If any stage exceeds its max cycle count, escalate immediately — do not attempt another pass.

## Pattern Declaration
```
PATTERN: Pipeline
AGENTS: Architect → Builder → Code Reviewer → QA Agent
GATE: Each stage passes gate check before next stage starts
```

## Permissions
**Authorized callers:** nexus  
**Orchestrates:** architect, builder, code_reviewer, qa_agent  
**Allowed paths (write):** `tmp/builds/{build_id}/` (intermediate), `execution/{domain}/` (promotion after QA PASS only)  
**Disallowed:** Skipping stages, promoting code that has not passed Code Review and QA, running stages in parallel.
