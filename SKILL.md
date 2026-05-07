---
name: resume-tailor
description: Tailor Rakesh Geddam's resume to a job description and output compilable LaTeX code for Overleaf using the resume-openfont template.
---

# Resume Tailor Skill

## Overview

This skill takes a **Job Description (JD)** pasted by the user and produces a **tailored LaTeX resume file** ready to paste into Overleaf. No clarifying questions should be asked — all decisions are documented below. Execute immediately upon receiving a JD.

---

## Source Files (Read Before Every Run)

| File | Purpose |
|---|---|
| `BASE_RESUME.MD` | Master source of truth for all experience, skills, education, and projects. **Never fabricate content not grounded in this file.** |
| `latex_template.tex` | The exact LaTeX structure, commands, and styling to use. All output must compile against the `resume-openfont` document class in Overleaf. |
| `tailor_instructions.md` | Content-rewriting rules: verb usage, bullet structure, ATS rules, no-percentage policy, keyword coverage, etc. |
| `RECRUITERS_UNDERSTANDING.txt` | Context-rewriting rules: Deep understanding of the content needed to be in a resume according to a Hiring Software Recruiter |

---

## The Single Most Important Rule: The Recruiter Reads the First Bullet First

A non-technical recruiter spends 6–7 seconds scanning a resume. Their eyes land on the **first bullet of each experience**, and that bullet decides whether they keep reading. This means the first bullet of every role must answer one question before anything else:

> **"What did this person build or do, and why did it matter to real people or a real business?"**

This is not a technical summary. It is a business impact statement written in plain language that a recruiter with no engineering background can immediately understand and find impressive.

### The Two Templates for the First Bullet

**If the work was a product or app used by end users:**
> [Action verb] [what the product does in plain language] — [who uses it] and [what it does for them], reaching [concrete scale signal].

**If the work was an internal tool, system, or migration:**
> [Action verb] [what problem existed before] by building [what was built], [concrete before/after outcome for the team or business].

Every other bullet in that role can then go deeper on technical implementation, architecture, and methodology. But the first bullet must earn the recruiter's attention before any of that is visible.

---

## Validated Impact Stories (Ground Truth — Use These Exactly)

These are the real, confirmed stories behind each role. When tailoring, the first bullet of each experience must be anchored in this section. Do not fabricate, inflate, or replace these with generic claims.

### DigiBlinker — Founder / Software Engineer (10/2025–03/2026)
- **What it does:** A live iOS app on the App Store that reduces distractions by delivering calendar-aware, customized notifications — users receive smart alerts tied to their actual events rather than generic interrupts, helping them stay focused.
- **Scale:** 10,000+ monthly active users.
- **First bullet angle:** Lead with what the app solves for users (distraction reduction via calendar-driven notifications) and anchor with the user scale.
- **Technical truth to validate before writing:** SwiftUI and UIKit, EventKit and Focus Mode APIs, Xcode Cloud CI/CD. Antigravity agentic workflows were built for internal tooling (not the app itself) — do not conflate them with the iOS app features. Snowflake Cortex was used for analytics pipeline work, not core app functionality.

### Melo.co — Software Engineering Intern (09/2024–02/2025)
- **What it solved:** Before this chatbot, the CTO was personally handling all patient queries through calls and emails. The chatbot automated that entirely for 300 patients per month across appointment, billing, and FAQ workflows with no human handoff required.
- **First bullet angle:** Lead with the business problem it solved (CTO manually fielding all queries) and what the chatbot replaced, anchored to the 300-patients-per-month scale.
- **Supporting bullet angles:** Patient intake automation reduced onboarding time from 15–30 minutes per patient; WCAG 2.1 accessibility improvements.
- **Technical truth to validate:** Gemini 2.0 fine-tuning, Google Apps Script orchestration. Do not claim specific fine-tuning infrastructure details that are not confirmed.

### University of Michigan – Flint — Software Engineer Intern (08/2023–05/2024)
- **What it solved:** The underlying physical experiments (multi-dimensional materials science tests) were expensive. By building an LSTM prediction model on existing MD simulation data, the research generated synthetic data that replaced the need for additional physical runs, cutting experimental costs by approximately 30% and compressing the research timeline from 12 months to 6 months.
- **First bullet angle:** Lead with the cost and timeline impact on the research program, not the model architecture. A recruiter understands "cut research costs by 30% and halved the timeline" far better than "built an LSTM model."
- **Technical truth to validate:** TensorFlow LSTM trained on MD simulation data, benchmarked against Linear Regression and SVM, achieving 91% accuracy (MSE reduced from 576 to 52). Preprocessing via Pandas/NumPy. These numbers are confirmed — use them.

### Bank of America — Assistant System Engineer (04/2021–01/2023)
- **What it solved:** A 100+ TB Teradata-to-Hive migration required workflows that teams of 5 were running manually, each taking a full week per cycle. By automating 6 workflows with Python and Spark orchestration (with human-in-the-loop validation requiring only 1 person), the same work was completed in 24–48 hours.
- **First bullet angle:** Lead with the scale of the migration (100+ TB) and the operational transformation: from a 5-person, week-long process to a 1-person, 24–48 hour process.
- **Do not use percentages.** The confirmed real numbers are: 6 workflows automated, 5 people reduced to 1 for validation, 1 week reduced to 24–48 hours, 100+ TB of data. Use these absolute figures exclusively.
- **Technical truth to validate:** Python and Spark for orchestration and automation, Teradata to Hive migration, cross-functional coordination across 5+ teams. Custom Spark partitioning and caching for pipeline optimization. Do not add infrastructure details not grounded in BASE_RESUME.MD.

---

## Design Decisions (Locked — Do Not Re-Ask)

### 1. LaTeX Compilation
- The user pastes output directly into **Overleaf**, which already has the `resume-openfont.cls` and supporting files.
- Do NOT include or generate any `.cls`, `.sty`, or font files.
- Output must be a single self-contained `.tex` file that compiles when dropped into the user's existing Overleaf project.

### 2. Section Order — Follow the LaTeX Template

```
1. Profile / Header (name, contact — as \newcommand variables)
2. Professional Summary
3. Education
4. Work Experience
5. Projects
6. Publications
7. Skills
8. Certifications (include only when JD-relevant certs exist)
```

### 3. Styling — Use the LaTeX Template As-Is
Keep the template's fonts and formatting commands exactly. Do NOT override with plain-text formatting. Use the template's existing commands: `\resumeHeading`, `\educationHeading`, `\projectHeading`, `\singleItem`, `\begin{bullets}`, `\sectionsep`, etc.

### 4. Contact Info — Parameterized via `\newcommand`

```latex
\newcommand{\yourName}{Rakesh Geddam}
\newcommand{\yourWebsite}{}
\newcommand{\yourWebsiteLink}{}
\newcommand{\yourEmail}{rakeshgeddam2025@gmail.com}
\newcommand{\yourPhone}{516-852-3579}
\newcommand{\githubUserName}{rakeshgeddam}
\newcommand{\linkedInUserName}{rakeshge}
```

### 5. Publications & Projects — Always Include
Always include both sections. Tailor descriptions and emphasis to match JD keywords. Reorder by relevance to the JD.

### 6. Output Files — Uniquely Named

```
resume_<company>_<role>.tex
```

Examples: `resume_google_sde.tex`, `resume_stripe_data_engineer.tex`

---

## Phase 1: JD Analysis (Internal — Do Not Print)

### 1.1 Decode Hidden Requirements

| Written Requirement | Actual Meaning |
|---|---|
| "Cross-functional collaboration" | Influences without authority across departments |
| "Leadership" | Drives outcomes without being told |
| "Fast-paced environment" | Handles multiple priorities with minimal hand-holding |
| "Strategic thinker" | Sees the big picture, connects dots, plans ahead |
| "Self-starter" | Takes initiative proactively with minimal supervision |
| "Stakeholder management" | Manages competing expectations across multiple parties |
| "Data-driven" | Uses metrics to make decisions, proves impact with numbers |
| "Agile" | Comfortable with changing priorities and iterative delivery |
| "Ownership" | End-to-end accountability, not just task completion |
| "Scale" | Experience with high volume, high throughput, or large user bases |

### 1.2 Extract ATS Keywords

Internally build a prioritized list:
- **Hard skills** — technologies, tools, languages (must match exactly)
- **Soft skills** — culture/fit indicators (demonstrate through bullet outcomes)
- **Industry terms** — domain language (weave naturally)
- **Qualifications** — degrees, certs, years of experience

### 1.3 Map Experience to Requirements

For each JD requirement:
- **Direct match** — reuse or reframe existing bullet from `BASE_RESUME.MD`
- **Reframeable** — existing experience that can be reworded to match
- **Gap** — no matching experience (flag in Gap Analysis output)

---

## Phase 2: Content Tailoring Rules

### The "So What?" Quality Gate

Before finalizing any bullet, ask: does this show **impact**, not just activity? Would a recruiter care about this in 6–7 seconds? Is the outcome concrete?

If a bullet only describes what was done without showing why it mattered, rewrite it.

### Bullet Point Format
- Format: **Action → Method → Outcome**
- Start every bullet with a **strong, unique action verb**
- **No repeated verbs** across the entire resume
- Bullets should be **one line** (two lines only if truly unavoidable)
- Bold technologies and metrics using `\textbf{}`

### Banned Words (Never Use)

```
cutting-edge, leveraged, synergy, spearheaded, utilized, state-of-the-art,
passionate, innovative, dynamic, revolutionized, best-in-class, world-class,
game-changer, paradigm, disruptive, next-generation, robust, seamless,
end-to-end (as filler), helped with, worked on, was responsible for,
assisted in, participated in, contributed to
```

### Approved Strong Action Verbs

| Category | Verbs |
|---|---|
| **Building** | Architected, Constructed, Developed, Engineered, Implemented, Assembled, Formulated |
| **Leading** | Directed, Governed, Coordinated, Managed, Supervised, Guided, Mentored |
| **Delivering** | Shipped, Deployed, Delivered, Released, Launched, Executed, Produced |
| **Improving** | Optimized, Accelerated, Streamlined, Reduced, Eliminated, Consolidated, Refined |
| **Analyzing** | Diagnosed, Investigated, Evaluated, Benchmarked, Profiled, Assessed, Audited |
| **Creating** | Designed, Prototyped, Invented, Originated, Established, Introduced, Initiated |
| **Automating** | Automated, Programmed, Scripted, Instrumented, Configured, Integrated, Migrated |
| **Communicating** | Presented, Documented, Trained, Advised, Reported, Demonstrated, Published |
| **Scaling** | Scaled, Distributed, Parallelized, Partitioned, Replicated, Load-balanced |
| **Securing** | Hardened, Encrypted, Authenticated, Validated, Audited, Enforced, Restricted |

### Absolute Numbers Only — No Percentages

Never use percentages anywhere on the resume. Use real, concrete figures.

| ❌ Wrong | ✅ Right |
|---|---|
| "Reduced migration time by 60%" | "Cut migration cycle from 1 week to 24–48 hours" |
| "Reduced team effort by 80%" | "Reduced validation from a 5-person to a 1-person operation" |
| "Improved throughput by 50%" | "Increased pipeline throughput from 2M to 3M records daily" |
| "Cut costs by 40%" | "Reduced cloud spend from $50K to $30K monthly" |

The confirmed absolute numbers for each role are documented in the **Validated Impact Stories** section above. Use those as the primary source.

### Technical Precision Rule

Before writing any technical detail, ask: is this grounded in `BASE_RESUME.MD` or the **Validated Impact Stories** section? If not, omit it. Do not infer or embellish technical architecture. For example:
- Do not claim Antigravity workflows power the DigiBlinker iOS app — they were used for internal tooling.
- Do not add infrastructure or system design details to the BofA migration that are not confirmed.

### JD Keyword Coverage
- Align content with JD keywords and tools while keeping wording authentic
- Cover all JD requirements — minimum and preferred qualifications
- Adjust job titles across roles to best match the target role where reasonable
- Remove bullets not relevant to the JD to stay within one page

### 6–7 Second Scannability Check

- The **Summary** immediately signals role fit
- The **most relevant keywords** appear in the first 2 bullets of each role
- **Job titles** match what the recruiter is searching for
- **Skills section** lists the most critical JD-matching skills first
- `\textbf{}` is used strategically on technologies and metrics as visual anchors

### Skills Section
Use `\begin{skillList}` / `\singleItem{}{}` format. Tailor categories to JD. Most critical skills listed first within each category.

### Education
- No GPA
- No graduation year for the Bachelor's degree
- Include graduation info for the Master's degree only

### Certifications
Add only if directly relevant to the JD. If none are relevant, omit the section entirely.

---

## Phase 3: Output

### A. LaTeX File

Generate a complete `.tex` file using the `resume-openfont` document class. Save as `resume_<company>_<role>.tex`.

### B. Chat Output — Evaluation + Gap Analysis

```
## Resume Evaluation
- **ATS Score:** X/100
- **Recruiter Score:** X/100
- **JD Coverage:** X%
- **Scannability:** Pass/Fail

## Gap Analysis
| JD Requirement | Status | Notes |
|---|---|---|
| [requirement] | ✅ Matched | [which bullet] |
| [requirement] | 🔄 Reframed | [how adapted] |
| [requirement] | ❌ Gap | [suggestion] |

## Improvement Notes
- **Immediate:** 2–3 lines
- **After One Week of Iteration:** 2–3 lines
```

---

## LaTeX Template Command Reference

| Command | Parameters | Purpose |
|---|---|---|
| `\resumeHeading{company}{title}{location}{dates}` | 4 | Job entry header |
| `\educationHeading{school}{degree}{location}{date}` | 4 | Education entry |
| `\projectHeading{name}{url}{techstack}` | 3 | Project entry |
| `\projectHeadingWithDate{name}{url}{stack}{date}` | 4 | Project with date |
| `\singleItem{category:}{items}` | 2 | Skill line |
| `\courseWork{courses}` | 1 | Coursework line |
| `\begin{bullets} ... \end{bullets}` | — | Bullet list |
| `\sectionsep` | — | Section separator |
| `\section{Name}` | 1 | Section heading |
| `\textbf{text}` | 1 | Bold inline text |
| `\href{url}{text}` | 2 | Hyperlink |
| `\underlinedLink{url}{text}` | 2 | Underlined link |

---

## Workflow Trigger

When the user pastes a Job Description:

1. **Read** `BASE_RESUME.MD`, `latex_template.tex`, and this `SKILL.md` (every time, fresh)
2. **Review** the Validated Impact Stories section — these are the confirmed ground truths for each role
3. **Analyze** the JD silently — decode requirements, extract keywords, map experience (Phase 1)
4. **Draft the first bullet of each experience first** — apply the First Bullet Rule before writing any other bullets
5. **Tailor** all remaining bullets per Phase 2 rules — apply the "So What?" gate to every bullet
6. **Validate** that no percentages appear, no banned words appear, and no technical details are fabricated
7. **Generate** the complete `.tex` file using the template's LaTeX commands (Phase 3A)
8. **Save** to `resume_<company>_<role>.tex` in the workspace
9. **Print** the Evaluation + Gap Analysis in chat (Phase 3B)

**Do not ask any questions. Execute immediately.**