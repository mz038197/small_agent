---
name: skill-creator-contextual
description: Guide for creating effective skills with context-aware routing. This skill should be used when users want to create or update a skill and the agent must decide from conversation context whether to guide discovery, fill missing design gaps, produce a SKILL.md draft, or iterate on an existing skill.
license: Complete terms in LICENSE.txt
---

# Skill Creator Contextual

This skill provides guidance for creating effective skills while deciding how much guidance or production support is appropriate from context. Use it as a safer variant of `skill-creator` when the user's request may be educational, exploratory, under-specified, or ready for direct drafting.

## About Skills

Skills are modular, self-contained packages that extend Claude's capabilities by providing specialized knowledge, workflows, and tools. Treat skills as onboarding guides for specific domains or tasks: they transform Claude from a general-purpose agent into a specialized agent equipped with procedural knowledge that no model can fully possess.

### What Skills Provide

1. Specialized workflows - Multi-step procedures for specific domains
2. Tool integrations - Instructions for working with specific file formats or APIs
3. Domain expertise - Company-specific knowledge, schemas, business logic
4. Bundled resources - Scripts, references, and assets for complex and repetitive tasks

### Anatomy of a Skill

Every skill consists of a required SKILL.md file and optional bundled resources:

```text
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (required)
│   │   ├── name: (required)
│   │   └── description: (required)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
    ├── scripts/          - Executable code (Python/Bash/etc.)
    ├── references/       - Documentation intended to be loaded into context as needed
    └── assets/           - Files used in output (templates, icons, fonts, etc.)
```

#### SKILL.md (required)

Write metadata carefully. The `name` and `description` fields determine when Claude will use the skill. Make the description specific about what the skill does and when to use it. Use third-person phrasing such as "This skill should be used when..." instead of "Use this skill when..."

#### Bundled Resources (optional)

##### Scripts (`scripts/`)

Include executable code for tasks that require deterministic reliability or are repeatedly rewritten.

- Include scripts when the same code is rewritten repeatedly or deterministic reliability is needed.
- Example: `scripts/rotate_pdf.py` for PDF rotation tasks.
- Scripts are token-efficient and may be executed without loading their full contents into context.
- Scripts may still need to be read for patching or environment-specific adjustments.

##### References (`references/`)

Include documentation and reference material intended to be loaded only when needed.

- Include references for detailed domain knowledge, schemas, policies, API docs, or workflow guides.
- Keep SKILL.md lean. Move detailed information into references unless it is essential to the core workflow.
- Avoid duplication. Information should live in either SKILL.md or references files, not both.
- For large references, include search patterns or section names in SKILL.md so Claude can find relevant details quickly.

##### Assets (`assets/`)

Include files not intended to be loaded into context, but used in final outputs.

- Include assets for templates, logos, fonts, boilerplate projects, icons, sample files, or document layouts.
- Example: `assets/slides.pptx` for a presentation template or `assets/frontend-template/` for starter web app files.

### Progressive Disclosure Design Principle

Skills use a three-level loading system to manage context efficiently:

1. Metadata (`name` + `description`) - Always in context
2. SKILL.md body - Loaded when the skill triggers
3. Bundled resources - Loaded or executed only as needed

## Context-Aware Mode Routing

Before creating or drafting a skill, evaluate two signals together:

1. User intent
   - Discovery intent: the user wants to explore, learn, brainstorm, teach, or be coached.
   - Production intent: the user asks to generate, convert, package, formalize, or update a skill.

2. Material readiness
   - Ready: the user has provided enough detail to produce a usable skill.
   - Not ready: important information is missing, ambiguous, contradictory, or too generic.

Do not decide from trigger phrases alone. A request like "make this into SKILL.md" expresses production intent, but may still require gap-filling if the provided material is incomplete.

### Routing Matrix

#### Discovery Intent + Not Ready: Discovery Mode

Use Discovery Mode when the user is exploring a skill idea, designing a classroom exercise, asking how to guide learners, or has only a rough concept.

In Discovery Mode:

1. Ask one question at a time.
2. Start with concrete usage examples.
3. Clarify trigger phrases, workflow, inputs, outputs, boundaries, resources, and quality checks.
4. Avoid writing a full `SKILL.md` until enough concrete information exists or the user explicitly asks for a draft.
5. After 3 to 5 useful answers, summarize the emerging skill design and ask whether to keep refining or produce a draft.

#### Discovery Intent + Ready: Design Review Mode

Use Design Review Mode when the user is still in a learning or design conversation, but enough details exist to draft.

In Design Review Mode:

1. Summarize the inferred skill design.
2. Identify any remaining assumptions.
3. Ask whether to continue guided refinement or generate the first draft.
4. Proceed to drafting only after the user chooses production.

#### Production Intent + Ready: Production Mode

Use Production Mode when the user has provided a clear skill concept, examples, workflow, constraints, outputs, and boundaries.

In Production Mode:

1. Produce a concrete skill structure.
2. Include valid YAML frontmatter with `name` and `description`.
3. Write the SKILL.md body in imperative or infinitive instructional style.
4. Identify useful `references/`, `assets/`, or `scripts/` resources.
5. Use explicit assumptions only for minor non-blocking gaps.
6. If creating a new skill from scratch in a writable environment, run `scripts/init_skill.py` before replacing the generated placeholders.

#### Production Intent + Not Ready: Gap-Filling Mode

Use Gap-Filling Mode when the user asks for a finished skill, but the current material is not mature enough for a useful skill.

In Gap-Filling Mode:

1. Do not blindly generate a complete skill.
2. Name the most important missing design information briefly.
3. Ask the smallest number of focused questions needed to make the skill usable.
4. Prefer one question at a time when the task is educational or the user is a student.
5. If only minor information is missing, draft with clearly labeled assumptions instead of stalling.

#### Existing Skill + Change Request: Iteration Mode

Use Iteration Mode when the user has an existing skill and wants to improve, debug, rename, re-scope, package, or validate it.

In Iteration Mode:

1. Inspect the current skill structure when files are available.
2. Identify whether the requested change affects metadata, workflow, resources, scripts, or packaging.
3. Preserve unrelated behavior.
4. Update the smallest necessary surface area.
5. Validate or package after edits when appropriate.

### Material Readiness Checklist

Consider a skill ready for production only if most of the following are clear:

- Purpose: What problem does the skill solve?
- User: Who will use it?
- Trigger: What user requests should activate it?
- Workflow: What steps should Claude follow?
- Inputs: What information must be collected from the user?
- Outputs: What should the skill produce?
- Boundaries: What should the skill avoid doing?
- Resources: Are references, assets, or scripts needed?
- Quality checks: How should the output be evaluated?

Treat missing purpose, trigger, workflow, outputs, or boundaries as blocking gaps. Treat missing packaged resources as non-blocking when the first version can work with SKILL.md alone.

### Ambiguity Handling

When intent is ambiguous, ask exactly one routing question:

```text
想先用引導模式一步步設計，還是直接把目前內容整理成正式 SKILL.md？如果目前資訊還不夠，我會先幫你補最關鍵的缺口。
```

Do not proceed until the user chooses or provides enough context to infer a mode.

## Skill Creation Process

Follow this process in order, skipping steps only when the selected mode makes a step unnecessary or the skill already exists.

### Step 1: Understand the Skill with Concrete Examples

Skip this step only when usage patterns are already clear from prior context or supplied material.

Clarify concrete examples of how the skill will be used. Use direct user examples when available; otherwise generate plausible examples and ask the user to validate them.

Relevant questions include:

- What functionality should the skill support?
- What would a user say that should trigger this skill?
- What are 2 to 4 realistic requests this skill should handle?
- What should the skill refuse, avoid, or ask follow-up questions about?

Avoid overwhelming users. Ask one question at a time in Discovery Mode and Gap-Filling Mode.

### Step 2: Plan Reusable Skill Contents

Analyze each concrete example by:

1. Considering how to execute on the example from scratch.
2. Identifying what scripts, references, and assets would help when repeating the workflow.

Examples:

- A PDF editing skill may need `scripts/rotate_pdf.py` because rotation code should not be rewritten each time.
- A frontend web app builder may need an `assets/hello-world/` boilerplate project.
- A database query skill may need `references/schema.md` so schemas are not rediscovered repeatedly.

Establish the reusable resources to include before editing SKILL.md. Omit resource directories that are not useful.

### Step 3: Initialize the Skill

When creating a new skill from scratch, run the `init_skill.py` script before editing files:

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

The script creates:

- The skill directory
- A SKILL.md template with required frontmatter
- Example `scripts/`, `references/`, and `assets/` files

Customize or delete generated example files after initialization.

Skip initialization only when the skill already exists or when the environment is read-only and the response is only a proposed draft.

### Step 4: Edit the Skill

When editing the newly generated or existing skill, write for another Claude instance that will use the skill later. Include procedural knowledge, domain-specific details, quality gates, and reusable resources that are not obvious from general model knowledge.

Start with reusable resources:

1. Create or update needed `scripts/`, `references/`, and `assets/` files.
2. Delete generated example resources that are not part of the real skill.
3. Keep detailed reference material out of SKILL.md unless it is essential to the core workflow.

Then update SKILL.md:

- Write in imperative or infinitive instructional style.
- Keep the workflow specific and executable.
- Include when to use the skill, how to proceed, what to ask, what to produce, and what to avoid.
- Prefer concrete examples over abstract advice.

### Step 5: Package the Skill

Once the skill is ready, package it into a distributable zip file:

```bash
scripts/package_skill.py <path/to/skill-folder>
```

Optional output directory:

```bash
scripts/package_skill.py <path/to/skill-folder> ./dist
```

The packaging script validates the skill before creating a zip. If validation fails, fix errors and run packaging again.

### Step 6: Iterate

After testing the skill on real tasks:

1. Notice struggles, over-asking, premature drafting, weak triggers, or missing resources.
2. Identify whether the fix belongs in metadata, SKILL.md workflow, references, assets, or scripts.
3. Make the smallest effective update.
4. Test again with realistic examples.

## Classroom-Friendly Behavior

When the context involves students, teaching, workshops, or learning how to create skills, prefer Discovery Mode or Gap-Filling Mode. The goal is often for learners to understand how skill design works, not merely to receive a finished file.

For student-facing skill creation:

- Ask one question at a time.
- Make design decisions visible.
- Distinguish between "I want a tool to do this" and "I have specified enough for a tool to do this well."
- Let students attempt examples before revealing the final application.
- Move to Production Mode only after students have articulated concrete use cases and boundaries.
