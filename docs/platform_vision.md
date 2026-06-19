# Nexus — A Tileable, Multi-Tenant Agent Platform

**Status:** Vision / Architecture Design (v1)
**Audience:** Internal build reference + portfolio artifact

---

## 1. Thesis

Most "AI assistant" deployments are bespoke — built for one company, one workflow, thrown away when the next client looks slightly different. Nexus is the opposite: **a single agent harness that any organization can deploy, then tailor by adding or removing users, agents, domains, projects, and skills without rebuilding the system.**

The core design constraint: every piece is a **tile**. Like Lego, each piece exposes a fixed interface, so pieces snap together and pull apart without breaking their neighbors. New users get their own assistant agent. New departments become domains. New capabilities become skills in a shared library. Access is gated per person. The system grows and shrinks without a rewrite.

This document defines how that works.

---

## 2. Design Principles

1. **One deployment per organization.** Each business runs its own harness on its own server, with its own data and credentials. Organizations are never co-mingled. Cross-organization isolation is *physical*, not logical — the strongest boundary there is.
2. **Enforcement lives in deterministic code, not in the agent.** LLM agents are probabilistic; access control cannot be. The execution layer hands each agent only the data and tools it is scoped to. An agent cannot "choose" to honor a boundary because it never receives what's on the other side of it.
3. **Capabilities are shared; knowledge is gated; private memory is sacred.** Skills (what the system *can do*) are reusable across every deployment. Knowledge (what the system *knows*) is scoped to who is allowed to see it. Each agent's private memory belongs to it alone.
4. **Tiles have studs.** Every tile type — skill, domain, project, user, agent — exposes a fixed, versioned interface so it can be added or removed without editing its neighbors.
5. **Honesty over comfort.** Outputs carry confidence, caveats, and source conflicts. The system tells the user when it isn't sure.

---

## 3. Deployment Model — One Harness Per Organization

```
   SOURCE REPO (single source of truth: skills, agent templates, harness code)
        |
        |  versioned release / deploy
        |---------------------|---------------------
        v                     v                     v
  +-----------+         +-----------+         +-----------+
  |  ORG A    |         |  ORG B    |         |  ORG C    |
  |  server   |         |  server   |         |  server   |
  |  own data |         |  own data |         |  own data |
  |  own creds|         |  own creds|         |  own creds|
  +-----------+         +-----------+         +-----------+
```

Each organization gets a **copy** of the harness, not a tenant slot in a shared one. Benefits: hard data isolation, independent credentials, no blast radius across clients, simpler compliance story.

**The trade-off, named honestly:** the "shared skill repository" is *one source repo, many deployed copies*. Improving a skill means publishing a new version and propagating it to each deployment. This is a versioned-release problem (manageable), not a runtime-sharing one. It is the price of physical isolation, and it is worth paying.

---

## 4. The Entity Model

Within a single organization's harness:

```
ORGANIZATION
|
+-- USERS ------------- each User has one personal ASSISTANT AGENT
|     (humans)           (the agent acts only within the user's granted scope)
|
+-- DOMAINS ------------ departments / functional areas (e.g. Sales, Ops, Eng)
|     +-- PROJECTS ------ units of work inside a domain
|
+-- SKILLS ------------- shared capability library (the "what it can do")
|
+-- KNOWLEDGE
      +-- Org-common ---- SOPs, onboarding, policy (everyone)
      +-- Domain/Project shared -- gated to users granted that domain/project
      +-- Agent-private memory -- that agent only
```

Five tile types: **User, Agent, Domain, Project, Skill.** Each adds or removes cleanly.

---

## 5. Access Model

### 5.1 Grants

Access is granted at the intersection of **user x (domain or project)**.

- A **domain grant** cascades to **all projects** under that domain.
- A **project grant** applies to **that project only** — it does *not* imply access to its parent domain or sibling projects.

> Example: User 2 is granted *Domain 3* (full) **and** *Project d2.2*. They can see everything in Domain 3 and exactly one project inside Domain 2 — nothing else in Domain 2.

### 5.2 Knowledge inherits its container's scope

Knowledge isn't gated individually. It inherits the access scope of where it lives:

| Knowledge tier | Who can read it |
|---|---|
| Org-common | Every user in the org |
| Domain knowledge | Users granted that domain |
| Project knowledge | Users granted that project (or its parent domain) |
| Agent-private memory | That agent only — never pooled, never shared |

This is the rule that prevents leaks: **a learning derived from private data lands in private memory, never in a shared tier.** Sharing flows down from common knowledge; it never bubbles up from private.

### 5.3 Gating mechanism — capability attributes ("wristbands")

Skills do **not** list which agents may call them by name. Instead:

- Each **skill declares a required capability** — e.g. `requires: domain_lead:sales` or `requires: comms`.
- Each **user/agent carries the capabilities** they've been granted (their "wristbands").
- At call time, the execution layer checks: *does this caller hold the required capability?* If yes, it runs and returns scoped data. If no, the skill is invisible to that caller.

**Why capability-based, not name-based:** adding a new user or agent means *granting capabilities*, not editing every skill. Removing one means *revoking capabilities* — no dangling references anywhere. This is what makes the system tileable. (See section 7.)

---

## 6. Admin / Identity Layer

The system supports a **hybrid** model so each business can tailor it. The demo configuration below uses the hierarchical path, because inheritance is the clearest mental model for an organization.

### 6.1 Hierarchical RBAC (demo configuration)

```
ORG  --grants-->  default capabilities for everyone
 |
 +-- TEAM  --grants-->  capabilities for team members (inherits Org)
       |
       +-- USER  --grants-->  capabilities for the individual (inherits Team)
```

Permissions inherit **downward**. Grant "read Sales domain" at the Team level and every member of that team gets it automatically. An **admin role** grants and revokes, and every access change is itself logged to the audit trail.

### 6.2 Capability-token overrides (the flex layer)

On top of inheritance, individual **capability tokens** handle exceptions: give one user access to a single project outside their team, or temporarily revoke a capability, without restructuring the hierarchy. Tokens are the same primitive the skill gates check in section 5.3 — so the admin model and the access model run on **one mechanism, not two.**

> **The unifying insight:** a capability token a user holds *is* exactly what a skill's gate checks for. Identity, access, and skill-gating are three views of the same primitive.

---

## 7. Tileability — The Lego Claim, and Why It Holds

A piece is tileable when adding or removing it requires **zero edits to its neighbors.** Here is what makes each tile type true:

| Tile | Add | Remove | What keeps neighbors untouched |
|---|---|---|---|
| **Skill** | Register it with a `requires:` capability | Deregister it | Callers are matched by capability, never by name |
| **User** | Create user, grant capabilities, attach assistant agent | Revoke capabilities, archive | No skill or domain references the user directly |
| **Agent** | Instantiate from template, assign to user | Detach | Agents carry capabilities; skills check capabilities |
| **Domain** | Create domain + capability (e.g. `domain_lead:ops`) | Remove domain + capability | Skills require *roles*, not specific domains |
| **Project** | Create under a domain; inherits domain grants | Archive | Grants and knowledge are scoped by container |

**The single rule that buys all of this:** authority lives *with the caller* (capabilities they hold), not *on the resource* (a list of names the resource maintains). Change the population of users/agents/domains all you like — no skill's definition ever has to change.

---

## 8. How a Request Flows

1. **User makes a request** to their personal assistant agent.
2. **The harness resolves the caller's capabilities** (Org -> Team -> User inheritance + any tokens).
3. **Orchestration plans the work** — which skills, in what order (Nexus master agent).
4. **For each skill call, the execution layer enforces scope:** it checks the required capability, then returns *only* data within the caller's grants. Out-of-scope data is never loaded.
5. **Private learnings write to the agent's private memory;** shared outputs write to the appropriate gated knowledge tier.
6. **Every access decision and access change is audited.**

The agent never sees what it isn't allowed to see — not because it was told not to look, but because the execution layer never handed it over.

---

## 9. Current State vs. Target

| Capability | Today | Target |
|---|---|---|
| Domain/skill structure | Exists (4 domains, skill registry) | Keep |
| Skill gating | Named caller lists | Capability/role attributes |
| Enforcement | Instruction-based (soft) | Execution-layer enforced (hard) |
| Multi-user | Single-user deployment | Org -> Team -> User + assistant agents |
| Admin/identity layer | None | Hybrid RBAC + capability tokens |
| Per-org deployment | Single instance | Source repo -> versioned per-org deploys |

**Path:** (1) convert skill gates from named callers to capability attributes; (2) move enforcement into the execution layer; (3) introduce the user/identity layer with per-user assistant agents; (4) build the admin layer; (5) define the per-org release/deploy pipeline.

---

## 10. Why This Matters

Bespoke AI deployments don't scale — every client is a rebuild. Nexus turns the agent harness into a **product**: one architecture, deployed per organization, tailored by configuration rather than code. Add a department, onboard a person, grant access to a project — all without touching the system's core. A common capability library improves once and propagates everywhere. Access is gated to the person, enforced by code, and audited end to end.

It is, in short, an operating system for an organization's AI workforce — tileable by design.

---

## 11. Future Note — The Orchestration Tier (Coordination != Authorization)

At scale (e.g. 50 personal assistant agents), a tier of **supervisor / orchestrator agents** can coordinate pods of assistant agents — workload routing, request fan-out, cross-agent coordination — at roughly a 10:1 ratio. This is a sound, probabilistic-friendly pattern, and worth designing when an org grows past a handful of users.

**The hard boundary:** this tier *coordinates*; it never *authorizes*. Authorization stays in the deterministic guard library that every agent **calls** — never in an agent that **decides**. Putting the gate inside agents would revert the hard wall back into a soft curtain, because agents can be persuaded, jailbroken, or confused. Coordination tolerates probabilistic agents; authorization does not.

- **Authorization = a lock** (a library every agent calls). Deterministic, in-process, runs inside each request, never bottlenecks no matter how many users, cannot be talked around.
- **Orchestration = where the 10:1 agent tier earns its keep.** Probabilistic agents coordinating other agents — fan-out is exactly the right tool *here*.

Scaling note: if authorization ever becomes a separate network *service*, you scale it by running multiple copies of the *same deterministic code* behind a load balancer — replicated locks, not coordinating guards. Single-server-per-org deployments don't need this for years.
