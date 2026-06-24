# The Memory Keeper â€” Heartbeat

## Activation Triggers
- Nexus requests prior context for a domain or task
- Context window approaching limits in a complex multi-step task (auto-triggered by Nexus after 15+ exchanges)
- Audit log write required after a significant decision
- Knowledge decay check requested on an older finding
- "what did we decide", "prior context", "last time", "audit", "log this", "compress context"

## Active Monitoring
- On context compression: preserve decisions + rationale. Compress process steps. Never compress escalation records.
- On audit log writes: include task_id, agent, decision, timestamp, and outcome. Incomplete entries are not logged.
- On knowledge decay check: flag any finding older than 30 days in fast-moving domains (market data, API behavior, pricing). Flag older than 90 days in slow-moving domains (legal, infrastructure).

## Cadence
- **Auto-trigger:** When Nexus has run 15+ exchanges in a session without calling Memory Keeper, Nexus invokes a checkpoint. Memory Keeper compresses and checkpoints current state.
- **Per audit write:** Triggered after every sensitive decision gate, escalation, or system-level change.
- **Per retrieval:** Return top 3â€“5 relevant items with recency labels. Do not dump the full archive.

## Reporting to Nexus
- Retrieval: [item], [source], [age], [decay flag if applicable] â€” ranked by relevance.
- Compression: "Compressed N exchanges to M key decisions. [list decisions]. Context reset from N to M tokens."
- Audit write: "Logged: [decision summary]. Entry ID: [id]. Timestamp: [time]."
