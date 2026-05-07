"""
send_microsoft_emails.py
------------------------
Personalized outreach to Microsoft contacts for the AI Software Engineer II
role (Job ID: 200020076).

Outreach psychology by persona:
  - recruiter    → Efficient, specific, low-friction ask. Lead with Job ID +
                   2-3 proof points. End with a single clear CTA.
  - exec_vp      → Ultra-brief. Lead with value, not story. No fluff.
  - eng_manager  → Technical synergy first, referral ask second. Show you
                   understand their domain, not just your own resume.
  - senior_ic    → Peer-to-peer. Curious, not salesy. Ask about their stack
                   as much as you pitch yourself.

Setup:
  1. Enable Gmail App Passwords: https://myaccount.google.com/apppasswords
  2. export GMAIL_APP_PASSWORD="xxxx xxxx xxxx xxxx"
  3. Set DRY_RUN = False to send for real.
  4. python3 send_microsoft_emails.py
"""

import os
import smtplib
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------
SENDER_EMAIL = "rakeshgeddam2025@gmail.com"
SENDER_NAME  = "Rakesh Geddam"
SMTP_HOST    = "smtp.gmail.com"
SMTP_PORT    = 587

# ← Flip to False when you're ready to send for real
DRY_RUN = False

RESUME_PDF_PATH = Path(
    "/Users/rakeshgeddam/Documents/jobsearch/custom-tool/Rakesh_Geddam_SDE_Devices_Software_Services.pdf"
)

# Role being applied to
JOB_ID    = "200020076"
JOB_TITLE = "AI Software Engineer II"
COMPANY   = "Microsoft"
TEAM      = "CoreAI / Consumer & Devices"

# Seconds between sends (avoids Gmail throttling)
SEND_DELAY_SECONDS = 8

# ---------------------------------------------------------------------------
# CONTACTS
# Hard-coded because there is no CSV — sourced from the user's provided list.
# Each dict has:  first, full_name, email, role, persona, team_context
# ---------------------------------------------------------------------------
CONTACTS = [

    # ── RECRUITERS & TALENT ─────────────────────────────────────────────────
    {
        "first": "Mike",
        "full_name": "Mike Maglio",
        "email": "mike.maglio@microsoft.com",
        "role": "Senior Technical Recruiter",
        "persona": "recruiter",
        "team_context": "Cloud, Azure & AI"
    },
    {
        "first": "Ela",
        "full_name": "Ela Mościcka",
        "email": "ela.moscicka@microsoft.com",
        "role": "Talent Sourcer / Referral Lead",
        "persona": "recruiter",
        "team_context": "Engineering Referrals"
    },
    {
        "first": "Priya",
        "full_name": "Priya Sharma",
        "email": "priya.sharma@microsoft.com",
        "role": "Technical Recruiter",
        "persona": "recruiter",
        "team_context": "Microsoft AI (MAI)"
    },
    {
        "first": "David",
        "full_name": "David Chen",
        "email": "david.chen@microsoft.com",
        "role": "Technical Recruiter",
        "persona": "recruiter",
        "team_context": "Microsoft Security"
    },
    {
        "first": "Sarah",
        "full_name": "Sarah Jenkins",
        "email": "sarah.jenkins@microsoft.com",
        "role": "University / New Grad Recruiter",
        "persona": "recruiter",
        "team_context": "Software Engineering"
    },
    {
        "first": "Courtney",
        "full_name": "Courtney",
        "email": "courtney@microsoft.com",
        "role": "Talent Community Manager",
        "persona": "recruiter",
        "team_context": "LinkedIn Hiring Initiatives"
    },

    # ── EXECUTIVE / VP ───────────────────────────────────────────────────────
    {
        "first": "Tina",
        "full_name": "Tina Schuchman",
        "email": "tina.schuchman@microsoft.com",
        "role": "VP, Engineering (CoreAI)",
        "persona": "exec_vp",
        "team_context": "AI Agent Platforms"
    },
    {
        "first": "Ashish",
        "full_name": "Ashish Kelkar",
        "email": "ashish.kelkar@microsoft.com",
        "role": "Corporate VP (CoreAI)",
        "persona": "exec_vp",
        "team_context": "Data Science & Infrastructure"
    },

    # ── ENGINEERING MANAGERS ─────────────────────────────────────────────────
    {
        "first": "Robert",
        "full_name": "Robert Gruen",
        "email": "robert.gruen@microsoft.com",
        "role": "Principal Dev Leader",
        "persona": "eng_manager",
        "team_context": "Research & Talent"
    },
    {
        "first": "Mukul",
        "full_name": "Mukul Singhal",
        "email": "mukul.singhal@microsoft.com",
        "role": "Partner Group Engineering Manager",
        "persona": "eng_manager",
        "team_context": "Microsoft Digital / AI"
    },
    {
        "first": "Ragini",
        "full_name": "Ragini Singh",
        "email": "ragini.singh@microsoft.com",
        "role": "Partner Group Engineering Manager",
        "persona": "eng_manager",
        "team_context": "Microsoft Digital / Copilot"
    },
    {
        "first": "Chris",
        "full_name": "Chris Lovett",
        "email": "chris.lovett@microsoft.com",
        "role": "Principal Research SDE Manager",
        "persona": "eng_manager",
        "team_context": "Central Engineering"
    },
    {
        "first": "Jason",
        "full_name": "Jason Kellington",
        "email": "jason.kellington@microsoft.com",
        "role": "Engineering Lead",
        "persona": "eng_manager",
        "team_context": "Cloud-First / Security"
    },
    {
        "first": "Stephanie",
        "full_name": "Stephanie Parry",
        "email": "stephanie.parry@microsoft.com",
        "role": "AI Engineering Lead",
        "persona": "eng_manager",
        "team_context": "Frontier AI Tools"
    },
    {
        "first": "Matthew",
        "full_name": "Matthew Cooke",
        "email": "matthew.cooke@microsoft.com",
        "role": "Engineering Manager",
        "persona": "eng_manager",
        "team_context": "IT & Security"
    },

    # ── SENIOR ICs / PRINCIPAL ENGINEERS ────────────────────────────────────
    {
        "first": "Kiran",
        "full_name": "Kiran Muthabatulla",
        "email": "kiran.muthabatulla@microsoft.com",
        "role": "Principal Architect",
        "persona": "senior_ic",
        "team_context": "Engineering Strategy"
    },
    {
        "first": "Andres",
        "full_name": "Andres Codas",
        "email": "andres.codas@microsoft.com",
        "role": "Senior Research SDE",
        "persona": "senior_ic",
        "team_context": "AI Systems"
    },
    {
        "first": "Dany",
        "full_name": "Dany Rouhana",
        "email": "dany.rouhana@microsoft.com",
        "role": "Principal ML Data Scientist",
        "persona": "senior_ic",
        "team_context": "Research & Data"
    },
    {
        "first": "Shweti",
        "full_name": "Shweti Mahajan",
        "email": "shweti.mahajan@microsoft.com",
        "role": "Senior Research SDE",
        "persona": "senior_ic",
        "team_context": "Software Engineering"
    },
    {
        "first": "ThuVan",
        "full_name": "ThuVan Pham",
        "email": "thuvan.pham@microsoft.com",
        "role": "Senior Software Engineer",
        "persona": "senior_ic",
        "team_context": "Cloud Platforms"
    },
]

# ---------------------------------------------------------------------------
# SUBJECT LINES  (one per persona — keeps inbox variety, avoids spam triggers)
# ---------------------------------------------------------------------------
SUBJECTS = {
    "recruiter":    f"Applied: {JOB_TITLE} (Job ID {JOB_ID}) — Rakesh Geddam",
    "exec_vp":      f"AI Engineer with LLM + Data Pipeline background — Job ID {JOB_ID}",
    "eng_manager":  f"Connecting on {{team_context}} work at Microsoft — Rakesh Geddam",
    "senior_ic":    f"Fellow engineer interested in your work on {{team_context}}",
}

# ---------------------------------------------------------------------------
# TEMPLATES — Each one is written to match the reader's role and priorities.
# ---------------------------------------------------------------------------
BASE_CLOSING = (
    "I have attached my resume if it helps — and happy to answer anything "
    "over email or jump on a short call, whatever's easiest.\n\n"
    "Thanks for reading, {first}. Genuinely appreciate the time.\n\n"
    "— Rakesh Geddam\n"
    "rakeshgeddam2025@gmail.com | linkedin.com/in/rakeshge | 516-852-3579"
)

TEMPLATES = {

    # ── RECRUITER ────────────────────────────────────────────────────────────
    # Psychology: get to the point immediately. Prove fit in 3 lines.
    # One clear ask at the end. No corporate filler.
    "recruiter": (
        "Hi {first},\n\n"
        "I applied for the {job_title} role (Job ID: {job_id}) at Microsoft "
        "last week and wanted to drop a direct note alongside the application — "
        "sometimes it helps to put a real person behind the submission.\n\n"
        "Quick picture of why I think I am a fit for the {team_context} team:\n"
        "  • Built and deployed end-to-end LLM inference pipelines in Python, "
        "including agentic reasoning workflows that reduced manual processing "
        "from hours to minutes.\n"
        "  • Led a 100+ TB cloud data migration at Bank of America — scoped it, "
        "executed it, and delivered without a single data integrity incident.\n"
        "  • MS in Computer Science from University of Michigan, with recent "
        "hands-on work in TensorFlow, HuggingFace, and Azure ML.\n\n"
        "I am not applying everywhere — Microsoft's AI engineering platform "
        "is specifically where I want to be building. If you have a moment, "
        "I would love for my application to get a look from the right hiring "
        "manager. Even a nudge in the right direction would be hugely helpful.\n\n"
        + BASE_CLOSING
    ),

    # ── EXEC / VP ────────────────────────────────────────────────────────────
    # Psychology: they have 30 seconds. Lead with value. Be specific and short.
    # The ask is implicit, not explicit — respect their time.
    "exec_vp": (
        "Hi {first},\n\n"
        "I recently applied for the {job_title} role (Job ID: {job_id}) on "
        "your {team_context} org and wanted to send a short note directly.\n\n"
        "My background is in building the data and inference infrastructure "
        "that makes AI products actually work at scale — not just demo well. "
        "I led a 100+ TB cloud migration at Bank of America end-to-end, "
        "shipped LLM pipelines that cut multi-hour workflows to under 5 "
        "minutes, and hold an MS in Computer Science from University of "
        "Michigan. I think there is a real overlap between what your team "
        "is building and what I have been doing.\n\n"
        "I know your time is limited, so I will keep this one short. "
        "I attached my resume in case it is useful to pass along.\n\n"
        + BASE_CLOSING
    ),

    # ── ENGINEERING MANAGER ──────────────────────────────────────────────────
    # Psychology: show genuine technical curiosity about their domain first.
    # Referral ask comes second, softly. They respond to builders, not pitches.
    "eng_manager": (
        "Hi {first},\n\n"
        "I have been following the work coming out of your {team_context} "
        "team with a lot of interest — the way Microsoft is threading AI "
        "into the engineering fabric (not just as a feature, but as actual "
        "infrastructure) is exactly the kind of problem space I want to work in.\n\n"
        "I applied for the {job_title} role (Job ID: {job_id}) at Microsoft "
        "and figured a direct note to someone doing the work would be more "
        "meaningful than waiting on an ATS.\n\n"
        "A bit about me: I have spent the last few years building AI systems "
        "that actually ship — LLM inference pipelines, ML models at 91% "
        "production accuracy, and data infrastructure at Bank of America "
        "scale (100+ TB moved without a data issue). I am comfortable "
        "operating at the boundary where research meets production, which "
        "I think is where your team lives.\n\n"
        "If you have 15 minutes to talk about what the team is working on, "
        "I would genuinely love that conversation. And if it makes sense, "
        "a referral for the open role would mean a lot.\n\n"
        + BASE_CLOSING
    ),

    # ── SENIOR IC / PRINCIPAL ────────────────────────────────────────────────
    # Psychology: peer-to-peer, not transactional. Lead with genuine curiosity.
    # Be specific about their domain. The referral ask is soft and optional.
    "senior_ic": (
        "Hi {first},\n\n"
        "I came across your work in {team_context} at Microsoft and wanted to "
        "reach out — I am a software engineer with a heavy focus on AI systems "
        "and I have been following what your team is building pretty closely.\n\n"
        "I recently applied for the {job_title} role (Job ID: {job_id}) and "
        "am genuinely curious about the technical challenges your team is "
        "tackling day-to-day: how you are thinking about LLM latency at "
        "scale, where the complexity actually lives in the system vs. what "
        "looks complex from the outside.\n\n"
        "For context on me: I build and ship AI infrastructure — LLM "
        "inference pipelines, real-time data systems, model training loops. "
        "MS in Computer Science from University of Michigan. Most recently "
        "deep in agentic reasoning systems and Snowflake-backed ML pipelines.\n\n"
        "If you ever have 20 minutes and are open to it, I would love to "
        "hear your perspective on the space. No pressure at all — and if "
        "a referral ever made sense, that would obviously be incredible.\n\n"
        + BASE_CLOSING
    ),
}

# ---------------------------------------------------------------------------
# EMAIL BUILDER
# ---------------------------------------------------------------------------
def build_email(contact: dict) -> MIMEMultipart:
    persona      = contact["persona"]
    first        = contact["first"]
    team_context = contact["team_context"]

    subject_tpl = SUBJECTS[persona]
    subject     = subject_tpl.format(team_context=team_context)

    body_tpl = TEMPLATES[persona]
    body = body_tpl.format(
        first        = first,
        job_title    = JOB_TITLE,
        job_id       = JOB_ID,
        team_context = team_context,
    )

    msg = MIMEMultipart()
    msg["From"]    = f"{SENDER_NAME} <{SENDER_EMAIL}>"
    msg["To"]      = contact["email"]
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Attach resume if it exists
    if RESUME_PDF_PATH.exists():
        with open(RESUME_PDF_PATH, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f'attachment; filename="{RESUME_PDF_PATH.name}"',
        )
        msg.attach(part)
    else:
        print(f"  ⚠️  Resume PDF not found: {RESUME_PDF_PATH}")
        print(f"     Sending without attachment.")

    return msg

# ---------------------------------------------------------------------------
# SEND / DRY-RUN
# ---------------------------------------------------------------------------
def run(app_password: str) -> None:
    mode = "DRY RUN — no emails sent" if DRY_RUN else "LIVE MODE — sending now"
    print(f"\n{'='*70}\n{mode}\n{'='*70}")

    smtp_conn = None
    if not DRY_RUN:
        smtp_conn = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        smtp_conn.ehlo()
        smtp_conn.starttls()
        smtp_conn.login(SENDER_EMAIL, app_password)

    sent = skipped = 0

    try:
        for i, contact in enumerate(CONTACTS, start=1):
            msg = build_email(contact)
            action = "→ WOULD SEND" if DRY_RUN else "→ SENDING"

            print(f"\n[{i:02d}] {action}")
            print(f"     To      : {contact['full_name']} <{contact['email']}>")
            print(f"     Role    : {contact['role']}")
            print(f"     Persona : {contact['persona']}")
            print(f"     Team    : {contact['team_context']}")
            print(f"     Subject : {msg['Subject']}")

            if DRY_RUN:
                body_preview = TEMPLATES[contact["persona"]].format(
                    first        = contact["first"],
                    job_title    = JOB_TITLE,
                    job_id       = JOB_ID,
                    team_context = contact["team_context"],
                ).splitlines()
                preview = "\n".join(f"     {ln}" for ln in body_preview[:6])
                print(f"     Body preview:\n{preview}\n     ...")
            else:
                smtp_conn.send_message(msg)
                print(f"     ✅ Sent")
                time.sleep(SEND_DELAY_SECONDS)

            sent += 1

    finally:
        if smtp_conn:
            smtp_conn.quit()

    print(f"\n{'='*70}")
    if DRY_RUN:
        print(f"DRY RUN complete. Would have sent {sent} emails.")
        print("Set DRY_RUN = False and re-run to send for real.")
    else:
        print(f"Done. Sent {sent} | Skipped {skipped}")
    print("="*70)


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main() -> None:
    app_password = os.environ.get("GMAIL_APP_PASSWORD", "mqwz vkrc jlrj nymx")
    if not app_password and not DRY_RUN:
        raise EnvironmentError(
            "Set GMAIL_APP_PASSWORD before running in LIVE mode.\n"
            "  export GMAIL_APP_PASSWORD='xxxx xxxx xxxx xxxx'"
        )
    run(app_password)


if __name__ == "__main__":
    main()
