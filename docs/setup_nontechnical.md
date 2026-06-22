# Getting Started with Nexus — Non-Technical Guide

**Who this is for:** Business owners or operators who are comfortable using ChatGPT or Claude in a browser but have never touched a terminal, written code, or worked with developer tools. No technical background required.

**What you'll have by the end:** A working version of the Nexus AI system running inside Claude's web app, configured for your business, and a completed planning exercise you can use immediately.

---

## How Nexus Works — Plain Language

Before you set anything up, understand what you're building.

Most people use AI the same way they use Google: they type a question, get an answer, and move on. Nexus is different. It's a structured system that turns Claude into a disciplined business operator — not just a smart search engine.

Three things make it work:

**1. Directives (What to do)**
Written instructions that define how each part of your business operates. Think of these like job descriptions for your AI agents. They live as documents in your project and tell the AI what it's responsible for, what inputs it needs, and what outputs it should produce.

**2. Nexus (The Decision-Maker)**
The master orchestrator. When you send a request, Nexus doesn't just answer — it structures your request, validates that it's clear, asks for what's missing, defines what "done" looks like, makes a plan, and then delegates the right parts to the right specialist agents. It's the manager, not the worker.

**3. Specialist Agents**
Sub-agents that handle specific types of work: The Researcher for deep information gathering, The Critic for stress-testing plans, Quill for formatting final outputs, and others. Nexus assigns work to them and synthesizes the results.

The system runs inside Claude's Projects feature — no software to install, no code to write.

---

## Part 1 — Set Up Your Claude Subscription

**Step 1: Create an account**

Go to [claude.ai](https://claude.ai) and sign up with your email. The free tier is limited — it won't give you access to Projects or the usage you need to run a real business workflow.

**Step 2: Subscribe to Claude Pro**

- Click your profile icon (bottom left) → Upgrade
- Select **Claude Pro** ($20/month)
- This unlocks Projects, higher usage limits, and the ability to upload documents as persistent context

Claude Pro is the minimum for non-technical setup. If you find yourself hitting usage limits as your workflows grow, you can upgrade to Max later.

---

## Part 2 — Get the Nexus Framework

You don't need to understand GitHub to do this. You're just downloading a folder of text files.

**Step 3: Download the framework**

1. Go to: [github.com/davidjgarnett97-droid/nexus-framework](https://github.com/davidjgarnett97-droid/nexus-framework)
2. Click the green **Code** button
3. Click **Download ZIP**
4. Unzip the folder somewhere easy to find — your Desktop works fine

Inside you'll see folders: `agents`, `docs`, `domains`, `skills`, `users`, and two files: `CLAUDE.md` and `README.md`.

The most important file is `CLAUDE.md`. This is the brain of the system — it tells Claude how to behave as Nexus.

---

## Part 3 — Build Your Claude Project

Claude Projects let you give Claude a persistent identity and memory for a specific purpose. You're going to create a Project where Claude always acts as Nexus.

**Step 4: Create a new Project**

1. In Claude, click **Projects** in the left sidebar
2. Click **New Project**
3. Name it: `Nexus — [Your Business Name]`

**Step 5: Set the Project Instructions**

Project Instructions are the system prompt — what Claude reads before every conversation in this project. This is where Nexus lives.

1. Inside your new project, click **Project Instructions** (or the gear/settings icon)
2. Open the `CLAUDE.md` file from the downloaded framework (open it in Notepad or any text editor)
3. Copy the entire contents
4. Paste it into the Project Instructions field
5. Save

Claude will now behave as Nexus in every conversation inside this project.

**Step 6: Upload your domain directives as knowledge**

Project Knowledge is where you store reference documents that Claude can access during conversations. This is where your business-specific instructions live.

1. In your project, click **Add Content** or **Project Knowledge**
2. Upload these files from the downloaded framework:
   - `docs/architecture.md` — system reference
   - Any files from `domains/` or `skills/` that apply to your business
3. You can also create your own directive documents and upload them here (see the 101 Project below for how to write your first one)

You don't need to upload everything at once. Start with `architecture.md` and add more as you build out your workflows.

---

## Part 4 — Your First Conversation with Nexus

**Step 7: Test the system**

Open a new conversation inside your project (not in the main Claude interface — inside the project).

Type this exactly:

> "I want to map out a plan to get 10 new customers this quarter. My business is [describe your business in one sentence]."

Watch what happens. Nexus will not immediately give you a plan. Instead it will:

1. **Intake your request** — classify what you're asking for
2. **Validate your criteria** — check if the goal is specific enough to work with
3. **Ask clarifying questions** — what's your current customer base? What does "getting a customer" mean in your context? What resources do you have?
4. **Define success** — before planning, it will confirm what "done" looks like so you're aligned
5. **Produce a structured plan** — only after steps 1–4 are complete

This is the behavior that makes Nexus different from a standard chat session. It refuses to skip the structure.

---

## Part 5 — The 101 Project

Now that Nexus is running, complete this exercise. It demonstrates every layer of the system and produces something you can actually use.

**The Project: Write Your First Business Directive**

A directive is a plain-language document that tells Nexus how to handle one type of work in your business. Once it exists, you can run that workflow anytime by referencing it in a conversation.

**Step 8: Choose one recurring task your business does**

Pick something you do regularly that takes real time. Examples:
- Following up with leads
- Researching a new vendor or market
- Writing a weekly status update
- Qualifying a sales prospect
- Onboarding a new client

**Step 9: Ask Nexus to help you write the directive**

In your project, type:

> "I want to create a directive for [your task]. Help me write a structured SOP that Nexus can follow every time I need to run this workflow. Ask me whatever you need to build it properly."

Nexus will interview you — asking about inputs, outputs, decisions that need human judgment, common failure points, and what a good result looks like. Answer honestly. The more specific you are, the more reliable the directive will be.

**Step 10: Save the directive**

When Nexus produces the directive document, copy it and save it as a `.md` file (e.g., `lead_followup.md`). Then upload it to your Project Knowledge. Now Nexus can reference it in future conversations.

**What you've built:** A working AI business operator that has a structured identity (Nexus), a reference document describing how your business works (the directive), and a repeatable workflow it can execute on command.

---

## What to Build Next

In priority order:

1. **Write directives for your top 3 workflows** — the three things you do most often that consume the most time
2. **Add a routing rule to your CLAUDE.md** — for each new domain you add, update the Sub-Agent Routing Guide section so Nexus knows what belongs where
3. **Create a domain folder** — as you add more directives, organize them under a domain name (Sales, Ops, Finance) to keep the system navigable
4. **Upgrade to technical setup** — once you've validated the workflows and know what you need to automate, the technical path adds Python execution scripts that eliminate manual steps entirely

---

## Limitations of the Non-Technical Setup

Be clear about what this setup cannot do:

- **No automation** — Nexus can plan and structure work, but it can't automatically send emails, update your CRM, or pull data from external sources without the execution layer (Python scripts). Everything is still manual action based on Nexus's output.
- **No persistent memory across sessions** — each conversation starts fresh unless you explicitly tell Nexus what happened before. The technical setup has a Memory Keeper agent that handles this systematically.
- **No integrations** — connecting to Gmail, Notion, Google Calendar, or other tools requires the technical setup with MCP configurations.

If you need those capabilities, see the Technical Setup Guide.
