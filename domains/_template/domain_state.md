<!--
  domain_state.md — [YOUR_DOMAIN] Domain
  =========================================
  Purpose: Persistent knowledge base for the [YOUR_DOMAIN] domain. Captures
  architecture decisions, active projects, lessons learned, and open questions
  so that any agent or operator picking up this domain has full context without
  re-deriving it from scratch.

  When to update:
  - After any architecture decision is validated or invalidated
  - When a project changes status (starts, pauses, completes, is cancelled)
  - After a lesson is learned from a failure or unexpected behavior
  - When a new cross-domain dependency is established or removed
  - At the end of each sprint as part of the weekly review cycle

  Owner: [DOMAIN_OWNER_AGENT or OPERATOR]
  Last updated: [YYYY-MM-DD]
-->

# [YOUR_DOMAIN] Domain State

---

## Active Architecture Knowledge

<!--
  What belongs here: Validated facts about tools, APIs, schemas, integrations,
  and behavioral quirks that affect how this domain operates. Each entry should
  have a last_validated date so stale knowledge can be identified and challenged.
  Add a new entry any time you discover something non-obvious that cost time to learn.
  Do NOT add things that are obvious from reading the code or documentation.
-->

| # | Finding | Impact | Last Validated |
|---|---------|--------|----------------|
| 1 | [Brief description of a validated behavior, e.g. "API endpoint X returns 429 after N req/min"] | [How this changes what you do, e.g. "Add 2s sleep between batch calls"] | [YYYY-MM-DD] |
| 2 | [Brief description of a schema constraint, e.g. "Notion DB field Y does not accept empty strings"] | [e.g. "Always pass a fallback value of 'N/A' when field may be blank"] | [YYYY-MM-DD] |
| 3 | [Brief description of an integration quirk, e.g. "OAuth token for service Z expires after 7 days with no refresh"] | [e.g. "Re-auth script must run weekly; add to cron"] | [YYYY-MM-DD] |

---

## Project Management Convention

<!--
  This domain follows a two-layer project management model. Both layers must
  stay in sync — the portfolio tracker is the source of truth for STATUS and
  PRIORITY; the local execution folder is the source of truth for HOW.
-->

### Layer 1 — Portfolio Tracker (Notion)
- **What it is:** The central project registry in Notion. Every project in this domain has a record here with status, owner, priority, and sprint assignment.
- **When to use it:** When deciding what to work on next, assigning work, reporting progress, or doing the weekly review. This is the planning surface.
- **Database:** [NOTION_DB_NAME] — [NOTION_DB_ID or URL]
- **Status values in use:** `Backlog | In Progress | Blocked | Done | Archived`

### Layer 2 — Local Execution Folder
- **What it is:** `domains/[YOUR_DOMAIN]/projects/[YOUR_PROJECT]/` — contains directives, scripts, temp files, and outputs specific to each project.
- **When to use it:** When running, debugging, or extending a project. This is the execution surface.
- **Convention:** Each project subfolder contains at minimum: a `README.md` or directive, any domain-specific scripts, and a `.tmp/` folder for intermediate files (never committed).
- **Rule:** Never create a local project folder without a corresponding Notion record. Never close a Notion record without archiving or deleting the local folder.

---

## Active Projects

<!--
  One row per active project. "Status" should mirror the Notion portfolio tracker.
  "Next Action" is the single most important thing that must happen next —
  keep it specific enough that any agent can pick it up without asking.
  Archive or remove rows when a project reaches Done or Cancelled.
-->

| Project | Status | Owner | Notion Record | Next Action |
|---------|--------|-------|---------------|-------------|
| [YOUR_PROJECT] | [In Progress / Blocked / Backlog] | [AGENT or OPERATOR] | [Notion page ID or URL] | [Specific next step, e.g. "Run import script with dry_run=True and verify output before committing"] |
| [YOUR_PROJECT_2] | [Status] | [Owner] | [Notion page ID or URL] | [Next action] |

---

## Lessons Learned

<!--
  What belongs here: Hard-won knowledge from failures, surprises, and
  near-misses. Each entry should explain what happened, why it happened,
  and what was changed as a result. This section is the institutional memory
  that prevents repeat failures. Write entries in past tense.
  Format: [YYYY-MM-DD] — [What went wrong or surprised us] → [What changed]
-->

<!-- No lessons logged yet. Add the first entry after the first failure or surprise. -->

---

## Open Questions

<!--
  What belongs here: Unresolved questions that are blocking, nearly blocking,
  or likely to matter soon. Each entry should have an owner and a target
  resolution date. Remove entries when resolved — don't leave them here as
  a graveyard. If the answer becomes a lesson or an architecture finding,
  move it to the appropriate section above.
-->

| # | Question | Why It Matters | Owner | Target Date |
|---|----------|----------------|-------|-------------|
| 1 | [e.g. "Does API X support bulk writes, or must each record be posted individually?"] | [e.g. "Bulk support would cut import time from ~20min to <1min for large datasets"] | [AGENT or OPERATOR] | [YYYY-MM-DD] |
| 2 | [Open question] | [Why it matters] | [Owner] | [YYYY-MM-DD] |

---

## Cross-Domain Touchpoints

<!--
  What belongs here: Any dependency between this domain and another domain
  in the harness. This includes shared scripts, shared Notion databases,
  shared credentials, shared agents, or any output from this domain that
  another domain consumes (and vice versa). If a touchpoint breaks, both
  domain owners need to know — list them both.
-->

| Touchpoint | This Domain's Role | Other Domain | Other Domain's Role | Notes |
|------------|--------------------|--------------|---------------------|-------|
| [e.g. `execution/lib/crm.py`] | [e.g. "Consumer — calls create_contact() to write leads"] | [e.g. RE Wholesaling] | [e.g. "Owner — maintains schema and API wrapper"] | [e.g. "Coordinate before changing contact schema"] |
| [Shared resource or dependency] | [Producer / Consumer / Shared owner] | [Other domain name] | [Their role] | [Coordination note] |
