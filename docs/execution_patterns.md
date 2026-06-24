# Execution Patterns — Nexus Orchestration Library

**Owner:** Nexus  
**Version:** 1.0  
**Date:** 2026-06-24

When Nexus delegates work, it must name the pattern being used. This makes routing decisions auditable and replicable. Every plan must declare its pattern before assigning agents.

---

## Pattern 1 — Pipeline

**Shape:** A → B → C → D (sequential, each step depends on the prior)  
**Use when:** Each step requires the output of the previous. Order matters. No parallelism possible.  
**Log line:** `[PATTERN: Pipeline] Step N of M — {agent} receiving output from {prior_agent}`

**Example:** Task Intake → Criteria Validation → Planning → Execution  
**Gate rule:** A failed step blocks all downstream steps. Do not skip and proceed.

---

## Pattern 2 — Fan-out / Fan-in

**Shape:** One task splits into N parallel workstreams, then results merge  
**Use when:** Independent sub-tasks can run simultaneously. Merging is required before final output.  
**Log line:** `[PATTERN: Fan-out] Spawning {N} parallel workstreams — {agent_list}`  
**Log line:** `[PATTERN: Fan-in] Merging {N} results — convergence check required`

**Example:** Research task split across Researcher + Critic + Memory Keeper simultaneously  
**Gate rule:** All branches must complete before Fan-in. A branch failure = a gap, not a skip.

---

## Pattern 3 — Producer-Reviewer

**Shape:** Producer generates → Reviewer critiques → Producer revises (up to iteration limit)  
**Use when:** Output quality matters more than speed. A single pass is not sufficient.  
**Log line:** `[PATTERN: Producer-Reviewer] Round {N} — {producer} producing, {reviewer} reviewing`

**Example:** Quill drafts output → The Critic scores it → Quill revises  
**Gate rule:** Max 3 iterations before escalation. Do not iterate indefinitely.

---

## Pattern 4 — Expert Pool

**Shape:** Task is routed to the single best-fit agent from a pool based on context  
**Use when:** Multiple agents could handle the task, but only one is optimal given the specifics.  
**Log line:** `[PATTERN: Expert Pool] Routing to {agent} — reason: {routing_rationale}`

**Example:** Research request routed to Researcher (new domain) vs. Memory Keeper (prior context exists)  
**Gate rule:** Routing decision must include a rationale. "Default" is not a rationale.

---

## Pattern 5 — Supervisor

**Shape:** Central coordinator issues sub-tasks dynamically based on intermediate results  
**Use when:** The full task plan cannot be determined upfront. Each result informs the next delegation.  
**Log line:** `[PATTERN: Supervisor] {supervisor} issuing dynamic sub-task to {agent} based on: {trigger}`

**Example:** Nexus runs a multi-step deal analysis, routing to different agents as findings emerge  
**Gate rule:** Max 2 drift events before Nexus pauses and re-checks scope with David.

---

## Declaring a Pattern

Every time Nexus delegates, include this in the plan output:

```
PATTERN: [pattern name]
AGENTS: [list of agents involved]
GATE: [what triggers the next step / what blocks progress]
```

If no pattern fits cleanly, default to Pipeline and note the deviation.
