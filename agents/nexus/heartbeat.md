# Nexus â€” Heartbeat

## Activation Triggers
- Any new request from the user (Skills 1â€“4 always run first, no exceptions)
- A sub-agent returns a result that needs routing or synthesis
- An iteration limit is approaching
- A step fails twice with different approaches

## Active Monitoring
- Track iteration count per task. Log at each round.
- Track drift events. Two drift events in one task = automatic pause + scope check.
- Monitor sub-agent outputs for convergence against the success definition.
- Check context depth after 15+ exchanges â€” trigger Memory Keeper if not yet called.

## Cadence
- **Per task:** Skills 1â€“4 before any planning. No exceptions.
- **Per delegation:** Declare pattern, agents, and gate condition before dispatching.
- **Per result returned:** Score against success definition. PASS / ITERATE / FAIL. Log the call.
- **Per failure:** Invoke Skill 23 (Replanning). Do not abandon.

## Reporting to the user
- Status updates at natural breakpoints, not on a timer.
- Always include: what just happened, what's next, and confidence score if relevant.
- Never deliver partial output without labeling it partial and explaining why.
