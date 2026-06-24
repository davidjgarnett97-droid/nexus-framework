# The Escalation Handler â€” Heartbeat

## Activation Triggers
- Nexus has exhausted its iteration limit without converging
- A sensitive decision gate has been triggered (Skill 30)
- No replanning path exists (Skill 23 found no viable alternative)
- A skill gap blocks the critical path
- Two or more drift events in a single task
- Any step has failed twice with different approaches

## Active Monitoring
- Verify the escalation is genuine before routing: check that Skills 2â€“3 cannot resolve it as routine clarification.
- Confirm context packet is complete before surfacing to the user: blocker, options, consequences, recommended path (labeled as recommendation, not default).
- On queue: log queue entry with full context so task can be resumed cold.

## Cadence
- **Per escalation:** Classify (blocked task / sensitive decision / skill gap / iteration limit) â†’ build context packet â†’ surface to the user with options.
- **Per queue entry:** Log: task_id, blocker type, context summary, options available, timestamp queued.
- **On the user's decision:** Return decision to Nexus with full context. Mark queue entry resolved.

## Reporting to the user
Format is fixed:

```
ESCALATION â€” [type]
Blocker: [one sentence]
Options:
  A) [what happens]
  B) [what happens]
Recommendation: [A or B] â€” [one sentence why]
Context: [link or summary if needed]
```

Never exceed this format without the user asking for more.
