# Getting Started with Nexus — Technical Guide

**Who this is for:** Developers or technically capable operators comfortable with the terminal, Python, and version control. You've read the non-technical guide and want the full stack: orchestration + execution layer + integrations.

**What you'll have by the end:** The full Nexus harness running locally via Claude Code CLI, a configured domain directive, and a working execution script that Nexus can call to automate real work.

---

## How Nexus Works — Technical Overview

Nexus is a 3-layer architecture that separates concerns to maximize reliability.

```
Layer 1: Directives       — Plain-language SOPs in Markdown (directives/)
Layer 2: Orchestration    — Claude Code running CLAUDE.md as Nexus
Layer 3: Execution        — Deterministic Python scripts (execution/)
```

**Why this separation matters:** LLMs are probabilistic. Business logic is deterministic. If you ask Claude to do everything — reason, decide, AND execute API calls — you compound error rates. 90% accuracy per step = 59% success over 5 steps. The fix: push deterministic work into Python scripts, keep Claude in the decision-making and routing layer.

The flow for any task:
1. You send a request in a Claude Code session
2. Nexus (CLAUDE.md) runs Skills 1–4: intake, validate, clarify, define success
3. Nexus makes a plan and assigns steps to sub-agents or execution scripts
4. Execution scripts in `execution/` do the deterministic work (API calls, data writes, file ops)
5. Nexus synthesizes results, checks quality, and delivers

---

## Part 1 — Subscription and CLI Setup

**Step 1: Get a Claude subscription with Claude Code access**

Claude Code requires **Claude Max** ($100/month) or a direct **Anthropic API key**.

- **Claude Max**: Go to [claude.ai](https://claude.ai) → Upgrade → Max plan. Includes Claude Code, high usage limits, and Projects.
- **API key**: Go to [console.anthropic.com](https://console.anthropic.com) → API Keys → Create. Pay-per-token. Better for high-volume automation or teams where multiple people run sessions.

For most individual operators: start with Claude Max. Switch to API key when you're running enough sessions that per-token pricing is cheaper than the flat subscription.

**Step 2: Install Claude Code**

Follow the official install guide at [docs.anthropic.com/en/docs/claude-code](https://docs.anthropic.com/en/docs/claude-code).

Verify it's working:
```bash
claude --version
```

If you're using an API key instead of a logged-in account, set it:
```bash
export ANTHROPIC_API_KEY=your_key_here
```

Or add it to a `.env` file in your project root (recommended — see Step 5).

**Step 3: Install Python 3.10+**

The execution layer is Python. Check your version:
```bash
python --version
```

If you're below 3.10, install from [python.org](https://python.org). On Mac, Homebrew works: `brew install python@3.12`.

---

## Part 2 — Set Up the Framework

**Step 4: Clone the repository**

```bash
git clone https://github.com/davidjgarnett97-droid/nexus-framework.git
cd nexus-framework
```

Repository structure:
```
nexus-framework/
├── CLAUDE.md                  # Master orchestration prompt — this IS Nexus
├── agents/
│   ├── skill_registry.yaml    # Registry of all 36 skills
│   └── *.md                   # Sub-agent system prompts
├── docs/                      # Architecture, platform vision, this guide
├── domains/                   # Domain scaffolding templates
├── skills/                    # Skill directive files (full + stub)
└── users/                     # User profile scaffolding
```

**Step 5: Create your environment file**

```bash
cp .env.example .env
```

If there's no `.env.example`, create `.env` manually:

```bash
ANTHROPIC_API_KEY=your_key_here

# Add as you enable integrations:
# NOTION_API_KEY=
# GOOGLE_OAUTH_CLIENT_ID=
# GOOGLE_OAUTH_CLIENT_SECRET=
# GMAIL_CREDENTIALS_PATH=Credentials/gmail_credentials.json
```

Never commit `.env`. Confirm it's in `.gitignore`:
```bash
grep ".env" .gitignore
```

---

## Part 3 — Configure for Your Business

**Step 6: Review and edit CLAUDE.md**

Open `CLAUDE.md`. This is the system prompt that runs every Claude Code session in this directory. Three sections you need to customize before your first session:

1. **Sub-Agent Routing Guide** — Add routing entries for your business domains. Each entry tells Nexus which requests belong to which sub-agent. Be specific with keywords — vague entries cause mis-routing.

   Example entry to add:
   ```markdown
   Route to **Sales Agent** when the task involves:
   - Qualifying a new lead
   - Following up on a proposal
   - Updating CRM records for active deals
   ```

2. **Escalation Rules** — Review the default escalation triggers. Add any that are specific to your business (e.g., "any transaction over $10,000 requires human approval").

3. **Non-Negotiables** — Leave these. They're the structural constraints that make the system reliable.

**Step 7: Create your first domain**

Domains are functional areas of your business. Create the folder structure:

```bash
mkdir -p directives/sales execution/sales
```

Write your first directive at `directives/sales/lead_qualification.md`. Use this structure:

```markdown
# Lead Qualification — SOP

## Purpose
[What this workflow accomplishes]

## Trigger
[What request or event starts this workflow]

## Inputs Required
- [Data or context Nexus needs before starting]

## Process
1. [Step one]
2. [Step two]
3. [Step three — reference execution script if applicable]

## Outputs
- [What the workflow produces]

## Execution Scripts
- `execution/sales/qualify_lead.py` — [what it does]

## Escalation Rules
- [When to surface to human]

## Edge Cases
- [Known failure modes and how to handle them]
```

---

## Part 4 — Your First Execution Script

**Step 8: Write a minimal execution script**

Execution scripts are the deterministic layer. They do exactly one thing reliably. No reasoning, no judgment — just a clean action.

Start with something simple. Create `execution/sales/qualify_lead.py`:

```python
import json
import sys
import os
from datetime import datetime

def qualify_lead(lead_data: dict) -> dict:
    """
    Scores an inbound lead based on criteria defined in the directive.
    Input: dict with name, company, revenue, use_case
    Output: dict with score, tier, recommended_action
    """
    score = 0
    reasons = []

    revenue = lead_data.get("annual_revenue_usd", 0)
    if revenue >= 1_000_000:
        score += 3
        reasons.append("Revenue qualifies (>$1M)")
    elif revenue >= 250_000:
        score += 1
        reasons.append("Revenue marginal ($250K–$1M)")

    use_case = lead_data.get("use_case", "").lower()
    target_keywords = ["automation", "operations", "efficiency", "scale"]
    if any(k in use_case for k in target_keywords):
        score += 2
        reasons.append("Use case aligns with target workflow")

    tier = "A" if score >= 4 else "B" if score >= 2 else "C"
    action = "Schedule discovery call" if tier == "A" else "Send info packet" if tier == "B" else "Add to nurture sequence"

    return {
        "score": score,
        "tier": tier,
        "recommended_action": action,
        "reasons": reasons,
        "qualified_at": datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python qualify_lead.py '<json_lead_data>'")
        sys.exit(1)

    lead = json.loads(sys.argv[1])
    result = qualify_lead(lead)
    print(json.dumps(result, indent=2))
```

Test it:
```bash
python execution/sales/qualify_lead.py '{"name": "Jane Smith", "company": "Acme Corp", "annual_revenue_usd": 2000000, "use_case": "We need to automate our onboarding operations"}'
```

Expected output:
```json
{
  "score": 5,
  "tier": "A",
  "recommended_action": "Schedule discovery call",
  "reasons": ["Revenue qualifies (>$1M)", "Use case aligns with target workflow"],
  "qualified_at": "2026-06-22T..."
}
```

---

## Part 5 — Your First Session

**Step 9: Start Claude Code**

From the repo root:
```bash
claude
```

Claude Code loads `CLAUDE.md` automatically. You are now talking to Nexus.

**Step 10: Run the 101 Project**

Send this request:

> "I have a new inbound lead — Jane Smith at Acme Corp, $2M annual revenue, looking for help automating their onboarding operations. Qualify this lead and tell me what to do next."

Watch the sequence:
1. **Skill 1 — Intake**: Nexus parses the request and classifies it as a lead qualification task
2. **Skill 2 — Validation**: Nexus checks whether all required inputs are present
3. **Skill 4 — Success Definition**: Nexus confirms what "done" means (a tier score and action recommendation)
4. **Routing**: Nexus routes to the Sales domain and references `directives/sales/lead_qualification.md`
5. **Execution**: Nexus runs `execution/sales/qualify_lead.py` with the provided data
6. **Convergence**: Nexus reviews the output against the success criteria and delivers

If you haven't added the routing entry in CLAUDE.md yet, Nexus will flag a skill gap rather than improvising — that's expected behavior, not a bug.

---

## Part 6 — Enable Integrations (Optional)

These integrations are built on MCP (Model Context Protocol) — Claude Code's native tool-calling interface. Each one extends what Nexus can act on in real time.

**Notion**
1. Create an integration at [notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Copy the Internal Integration Token
3. Add to `.env`: `NOTION_API_KEY=your_token`
4. Add MCP server config per Claude Code docs

**Gmail / Google Calendar**
1. Create OAuth credentials at [console.cloud.google.com](https://console.cloud.google.com) (OAuth 2.0 Client ID, Desktop type)
2. Download the credentials JSON → save to `Credentials/gmail_credentials.json`
3. Run the auth script to generate a token (first time only — browser auth required)
4. Add MCP server config for Gmail and Calendar

**Important:** Gmail MCP is typically read-only. Write operations (send, label, draft) need a Python script using the Gmail API directly. See `execution/lib/` for the pattern.

---

## Skill Gaps and What to Do About Them

When Nexus can't route a request because no sub-agent or directive exists for it, it flags a **skill gap**. This is intentional — the system refuses to improvise with inferior tooling.

When you hit a skill gap:
1. Decide if it's real work you'll do repeatedly (if not, handle it manually and move on)
2. If it is: write a directive for it in `directives/<domain>/`
3. Write or identify an execution script in `execution/<domain>/`
4. Add a routing entry to CLAUDE.md
5. Run the workflow once manually with Nexus to validate it

Skill gaps surface what the system can't handle yet. Treat them as a build queue, not errors.

---

## What to Build Next

In priority order:

1. **Top 5 directives** — the five workflows you run most often. Write these first.
2. **Execution scripts for each** — one script per directive action. Keep them narrow.
3. **Sub-agent system prompts** — copy from `agents/` and customize for your domain specialists
4. **MCP integrations** — connect Notion, Gmail, and Calendar once your core workflows are stable
5. **Skill registry entries** — add custom skills to `agents/skill_registry.yaml` as you build them

The architecture scales with the work. Start with one domain, one directive, one script. Get that running cleanly before adding the next layer.
