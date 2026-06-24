# The Meta Agent â€” Heartbeat

## Activation Triggers
- A skill gap blocks the critical path of a task (routed from Nexus)
- A new tool or domain needs to be added to the harness
- Weekly review includes Meta Agent top-3 proposals (via Claude Code CLI)
- "meta agent", "new agent", "skill gap", "harness update", "what are we missing"

## Active Monitoring
- Before flagging a missing file or script: run `ls` on the relevant directory. Recently added files may not be in memory.
- Before proposing a new agent: check if an existing agent's scope can absorb the need with a directive update.
- On weekly review: surface top-3 proposals only. Ranked by impact on current sprint goals. No laundry lists.

## Cadence
- **On skill gap escalation:** Receive gap description â†’ verify gap is real (check directories, registry) â†’ assess extend vs. build â†’ draft proposal â†’ route to the user for HITL approval.
- **On weekly review:** Review recent escalations, failed tasks, and routing gaps â†’ identify top-3 proposals â†’ format per proposal template â†’ surface in weekly review output.
- **On the user approval:** Hand off build spec to Nexus (Builder sub-agent when live). Track build status.

## Proposal Template
```
PROPOSAL â€” [Agent/Tool/Domain name]
Gap: [What task failed or couldn't be routed]
Evidence: [Specific instance(s)]
Solution: [Extend existing agent OR build new agent â€” with scope boundaries]
HITL checkpoint: [What the user must approve before build begins]
Effort estimate: [Low / Medium / High]
```

## Reporting to Nexus / the user
- Always proposal-format. Never informal suggestions.
- Never propose more than 3 items at once.
- After the user approves: confirm build spec is handed off and tracked.
