---
description: Generate a tailored LaTeX resume from a pasted job description
---

# /tailor-resume

Triggered when the user pastes a Job Description (JD) or says "tailor resume".

## Steps

1. **Read the skill file** at `/Users/rakeshgeddam/Documents/jobsearch/custom-tool/SKILL.md` for all rules and decisions.

2. **Read source files** (every time — do not rely on cached content):
   - `/Users/rakeshgeddam/Documents/jobsearch/custom-tool/BASE_RESUME.MD`
   - `/Users/rakeshgeddam/Documents/jobsearch/custom-tool/latex_template.tex`
   - `/Users/rakeshgeddam/Documents/jobsearch/custom-tool/tailor_instructions.md`

3. **Analyze the JD:**
   - Extract company name and role title
   - List all required and preferred skills, tools, and technologies
   - Identify domain-specific keywords, collaboration patterns, and ownership expectations
   - Derive a short filename slug (e.g., `google_sde`, `meta_ios_engineer`)

4. **Tailor the resume content:**
   - Rewrite the Professional Summary to align with the JD
   - Adjust job titles across all roles to best match the target role
   - Rewrite every bullet point following Action → Method → Outcome
   - Ensure every JD keyword is covered across the resume
   - Reorder and adjust Skills categories to reflect JD priorities
   - Adjust Projects and Publications emphasis for JD relevance
   - Remove irrelevant content; do NOT fabricate new experience
   - No percentages, no buzzwords, no repeated verbs

5. **Generate the LaTeX file:**
   - Use the `resume-openfont` document class and all template commands exactly as defined in `latex_template.tex`
   - Follow the section order: Header → Summary → Education → Experience → Projects → Publications → Skills → Certifications (if relevant)
   - Keep contact info as `\newcommand` variables with Rakesh's real details
   - Save to `/Users/rakeshgeddam/Documents/jobsearch/custom-tool/resume_<company>_<role>.tex`

6. **Print evaluation in chat** (not in the .tex file):
   - ATS Score: X/100
   - Recruiter Score: X/100
   - JD Coverage: X%
   - Immediate Improvement Notes
   - Improvement Notes After One Week of Iteration

## Rules
- Do NOT ask clarifying questions — all decisions are in SKILL.md
- Do NOT generate .cls or .sty files
- Do NOT use Arial/Calibri — stick with the LaTeX template's fonts
- Do NOT include evaluation inside the .tex file
- Always read all 3 source files fresh before generating
