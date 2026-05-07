# 🚀 Agentic Job Application Automation: Customization & Usage Guide

This guide explains how to adapt this system for your own background and use it to automate your job application and outreach pipeline.

## 🏗️ 1. Customizing Your Source of Truth

The agent relies on "Ground Truth" files. You must update these with your own information:

### `BASE_RESUME.MD`
*   **Purpose:** The master source for all your experience.
*   **Action:** Replace Rakesh's details with your own. Use the most verbose descriptions here; the agent will selectively prune and summarize based on the JD.

### `technical_projects.md`
*   **Purpose:** A "bank" of your projects.
*   **Action:** Add your top 5-10 projects. Use the **XYZ format** (Accomplished X, as measured by Y, by doing Z). The agent will pick the 3 most relevant projects for every specific job.

### `SKILL.md` (The "Brain")
*   **Purpose:** Defines the rules for tailoring.
*   **Action:** Update the **"Validated Impact Stories"** section. These are the core narrative anchors for your career. When you update these, the agent will never deviate from your "True North" stories.

---

## 🛠️ 2. Setting Up the Automation Environment

### Prerequisites
*   **LaTeX:** Install `BasicTeX` or `MacTeX`.
*   **Python:** `pip install pandas` (for email automation).

### LaTeX Template
Ensure you have a `latex_template.tex` file in the root. 
*   **Note:** This system is optimized for the **`resume-openfont`** class. If you use a different template, update the LaTeX commands in `SKILL.md` under the "LaTeX Template Command Reference" section.

---

## 🚀 3. Daily Workflow

### Step 1: Tailor the Resume
Paste a Job Description into the Gemini CLI and run the command:
```bash
tailor resume [Paste JD Here]
```
*   **What happens:** The agent analyzes the JD, selects your best projects, rewrites bullets for impact, and generates a file named `resume_<company>_<role>.tex`.

### Step 2: Convert to PDF
Run the provided compiler script:
```bash
python tex_to_pdf.py resume_<company>_<role>.tex
```
*   **What happens:** This generates a professional, ATS-ready PDF and cleans up the temporary LaTeX logs.

### Step 3: Targeted Outreach
1.  Export a CSV of contacts from **Apollo.io** for your target company.
2.  Set your Gmail App Password as an environment variable:
    ```bash
    export GMAIL_APP_PASSWORD="your-16-char-password"
    ```
3.  Update the configuration in `send_emails.py` (PDF path, CSV path) and run:
    ```bash
    python send_emails.py
    ```
*   **What happens:** The script detects if the contact is a Recruiter or an Engineer and sends a personalized email with your tailored resume attached.

---

## ⚙️ 4. Advanced Customization

### Changing the "Tone"
You can modify the `TEMPLATES` dictionary in `send_emails.py` to match your personal voice. The system currently supports:
*   `data_scientist` (Peer-to-peer technical tone)
*   `technical_recruiter` (Brief, high-signal tone)
*   `hr_specialist` (Professional, company-alignment tone)

### Adjusting the Agent's "Scoring"
In `SKILL.md`, you can adjust the "Phase 3: Output" rules to change how the agent evaluates your resume (e.g., if you want it to be more aggressive about ATS keyword density vs. human readability).

---

### 💡 Pro-Tip for GitHub
When showcasing this, highlight the **`SKILL.md`** file. It demonstrates your ability to "program" an LLM with complex business logic, which is a highly sought-after skill in the era of AI Engineering.
