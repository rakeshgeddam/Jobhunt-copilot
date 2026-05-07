"""
send_jpmc_emails.py
-------------------
Sends personalized outreach emails to JPMorgan Chase contacts from an Apollo
export CSV for the Data Scientist role (Job ID: 210732086).

Configuration:
  - Sender: rakeshgeddam2025@gmail.com
  - Attachment: Rakesh_Geddam_Data_Scientist_Chase.pdf
  - Personalizes the body based on the recipient's TITLE (HR, Recruiter,
    Data Scientist, Technical Recruiter, Analyst, etc.)

Setup:
  1. Enable "App Passwords" on your Google account:
     https://myaccount.google.com/apppasswords
  2. Set the GMAIL_APP_PASSWORD environment variable.
     export GMAIL_APP_PASSWORD="your_16_char_app_password"
  3. Install dependencies: pip install pandas
  4. Run: python send_jpmc_emails.py

Safety:
  - Set DRY_RUN = True to preview emails without sending.
  - Only contacts with Email Status == "Verified" are emailed by default.
"""

import csv
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
SENDER_NAME = "Rakesh Geddam"
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

# Set to False to actually send. Set to True to preview in terminal only.
DRY_RUN = False

# Paths
CSV_PATH = Path("/Users/rakeshgeddam/Downloads/apollo-contacts-export.csv")
RESUME_PDF_PATH = Path(
    "/Users/rakeshgeddam/Documents/jobsearch/custom-tool/Rakesh_Geddam_Data_Scientist_Chase.pdf"
)

# Job details
JOB_ID = "210732086"
JOB_TITLE = "Data Scientist"
BUSINESS_UNIT = "Consumer & Community Banking"

# Only email contacts whose email status matches this set (case-insensitive)
ALLOWED_STATUSES = {"verified"}

# Seconds between emails (avoids Gmail throttling)
SEND_DELAY_SECONDS = 8

# ---------------------------------------------------------------------------
# PERSONA DETECTION
# Classify each contact's Title into a messaging "persona" so the email
# body can be tailored to what that person cares about.
# ---------------------------------------------------------------------------
PERSONA_KEYWORDS = {
    "data_scientist": [
        "data scientist", "data science", "analytics", "quant", "machine learning",
        "ml engineer", "data engineer", "data analyst"
    ],
    "technical_recruiter": [
        "tech recruiter", "technical recruiter", "sr tech recruiter",
        "technology recruiter"
    ],
    "recruiter": [
        "recruiter", "talent acquisition", "recruiting", "early careers",
        "campus", "university"
    ],
    "hr_specialist": [
        "hr", "human resources", "workforce", "compensation", "performance",
        "hr specialist", "hr advisor", "hr solutions", "hr consultant",
        "hr service", "hr data"
    ],
    "product_manager": [
        "product manager", "product management"
    ],
}


def detect_persona(title: str) -> str:
    """Return the best-matching persona key for a given job title."""
    title_lower = title.lower()
    # Order matters: more specific checks first
    for persona, keywords in PERSONA_KEYWORDS.items():
        for kw in keywords:
            if kw in title_lower:
                return persona
    return "general"


# ---------------------------------------------------------------------------
# EMAIL BODY TEMPLATES  —  human, conversational, persona-specific
# ---------------------------------------------------------------------------
BASE_CLOSING = (
    "I attached my resume — happy to jump on a quick call or answer anything "
    "about my background over email, whatever works best for you.\n\n"
    "Thanks so much for taking the time to read this, {first_name}. "
    "Really appreciate it.\n\n"
    "Best,\n"
    "Rakesh Geddam\n"
    "rakeshgeddam2025@gmail.com | linkedin.com/in/rakeshge | 516-852-3579"
)

TEMPLATES = {

    # ---- Peer data scientist / analyst ----
    "data_scientist": (
        "Hi {first_name},\n\n"
        "I came across your profile while poking around the JPMC data science team "
        "and figured I should just reach out directly. I recently applied for the "
        "{job_title} role (Job ID: {job_id}) in {business_unit} and wanted to put "
        "a real name behind the application.\n\n"
        "The Quant Analytics work your team does in Consumer Banking is genuinely "
        "what drew me here — not just a company name on a resume. I spent the "
        "last few years doing similar work: writing Python and SQL pipelines that "
        "turned a week-long reporting cycle into a 24-hour job, and training "
        "predictive models that hit 91% accuracy on live production data. "
        "More recently I have been building LLM-based inference systems and "
        "Snowflake dashboards, which honestly felt like a natural extension of "
        "the same instinct — make the data actually useful for the people who "
        "need it.\n\n"
        "Would love your honest take on the team if you ever have 5 minutes. "
        "And of course, if there is any way you could pass along a kind word "
        "on my application, that would mean a lot.\n\n"
        + BASE_CLOSING
    ),

    # ---- Tech-focused recruiter ----
    "technical_recruiter": (
        "Hi {first_name},\n\n"
        "I know as a technical recruiter you read a hundred of these. I will "
        "skip the corporate speak and just be real with you — I applied for "
        "the {job_title} role (Job ID: {job_id}) at JPMC last week and wanted "
        "to reach out in case it helps move my application along.\n\n"
        "Here is the short version of why I think I am a strong fit: four-plus "
        "years of Python and SQL as my daily tools, not just resume keywords. "
        "I led a 100+ TB data migration at Bank of America without a single "
        "data integrity issue, and I built a prediction model from scratch that "
        "ended up at 91% accuracy on real production data. I have also been "
        "deep in LLM engineering recently, which maps to where a lot of "
        "financial data science is heading.\n\n"
        "Happy to send over anything that would make your review easier. "
        "Appreciate you taking the time.\n\n"
        + BASE_CLOSING
    ),

    # ---- General / campus recruiter ----
    "recruiter": (
        "Hi {first_name},\n\n"
        "Hope your week is treating you well! I applied for the {job_title} "
        "opening (Job ID: {job_id}) in {business_unit} a few days ago and "
        "wanted to send a personal note — ATS systems are great at filtering, "
        "but they do not always surface the full picture of a candidate.\n\n"
        "Here is mine in a nutshell: MS in Computer Science from University of "
        "Michigan, 4+ years building data pipelines and prediction models across "
        "healthcare tech and enterprise banking. At Bank of America I owned a "
        "100+ TB migration end-to-end — no data issues on delivery. I also "
        "built automation scripts that my team still uses today. More recently "
        "I shipped an LLM-powered onboarding tool that cut a 15-minute manual "
        "process down to under 5 minutes for clinical staff.\n\n"
        "I have been intentional about which roles I apply to, and this one "
        "genuinely excited me. Is there anything else I can send over that "
        "would be helpful for your review?\n\n"
        + BASE_CLOSING
    ),

    # ---- HR specialist / generalist / comp / workforce ----
    "hr_specialist": (
        "Hi {first_name},\n\n"
        "My name is Rakesh Geddam. I applied for the {job_title} position "
        "(Job ID: {job_id}) in {business_unit} at Chase and wanted to send "
        "a quick note — I realize HR gets a flood of these, so I will keep "
        "it genuine and brief.\n\n"
        "I am a data scientist with 4+ years of experience who has been "
        "specifically eyeing Chase for a while — not just adding you to a "
        "spray-and-pray list. The way Chase talks about putting data at the "
        "center of customer experience actually matches how I think about the "
        "work. I built reporting pipelines that saved teams days of manual "
        "effort every week, trained models that hit 91% accuracy in "
        "production, and led a 100+ TB migration that landed cleanly with "
        "no data issues.\n\n"
        "I know you may not be directly involved in hiring decisions for this "
        "role, but even a nudge in the right direction would genuinely mean "
        "a lot. Thank you so much for reading this far.\n\n"
        + BASE_CLOSING
    ),

    # ---- Product manager ----
    "product_manager": (
        "Hi {first_name},\n\n"
        "I saw your role in product at JPMC and figured you might have a "
        "perspective I do not get from the job posting alone. I applied for "
        "the {job_title} opening (Job ID: {job_id}) in {business_unit} and "
        "wanted to reach out.\n\n"
        "My background sits at the intersection of data engineering and "
        "product thinking — I have built end-to-end pipelines, trained models "
        "that reached 91% accuracy, and probably most relevant for a PM "
        "context, I have spent a lot of time partnering with non-technical "
        "leadership to turn a complex model output into a decision someone "
        "can actually act on. I love that translation layer. It is where "
        "I feel most useful.\n\n"
        "Would genuinely love to hear what the team culture is like if you "
        "have a few minutes. No pressure at all — just curious and clearly "
        "a little eager.\n\n"
        + BASE_CLOSING
    ),

    # ---- Anyone else in the CSV ----
    "general": (
        "Hi {first_name},\n\n"
        "My name is Rakesh Geddam. I applied for the {job_title} role "
        "(Job ID: {job_id}) in {business_unit} at JPMorgan Chase and wanted "
        "to send a direct note rather than just disappear into the inbox of "
        "an ATS.\n\n"
        "A bit about me: Master's in Computer Science from University of "
        "Michigan, 4+ years in data science and engineering. My work spans "
        "from leading a 100+ TB migration at Bank of America to building "
        "LLM-powered tools that saved clinical teams 10 minutes per patient "
        "session. Python and SQL are genuinely how I think, not lines I added "
        "to pass a keyword filter.\n\n"
        "Chase has been at the top of my list for a while — the combination "
        "of data scale and real customer impact is rare, and I would love to "
        "be part of it. If you have any context on the team or the role, "
        "I would really appreciate it.\n\n"
        + BASE_CLOSING
    ),
}

SUBJECT = (
    "Application Follow-Up: {job_title} | Job ID {job_id} — Rakesh Geddam"
)


# ---------------------------------------------------------------------------
# EMAIL BUILDER
# ---------------------------------------------------------------------------
def build_email(
    first_name: str,
    recipient_email: str,
    persona: str,
) -> MIMEMultipart:
    """Build a MIMEMultipart email with text body and PDF attachment."""
    msg = MIMEMultipart()
    msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
    msg["To"] = recipient_email
    msg["Subject"] = SUBJECT.format(job_title=JOB_TITLE, job_id=JOB_ID)

    body = TEMPLATES[persona].format(
        first_name=first_name,
        job_title=JOB_TITLE,
        job_id=JOB_ID,
        business_unit=BUSINESS_UNIT,
    )
    msg.attach(MIMEText(body, "plain"))

    # Attach the resume PDF
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
        print(f"  ⚠️  Resume PDF not found at: {RESUME_PDF_PATH}")

    return msg


# ---------------------------------------------------------------------------
# SEND / DRY-RUN LOGIC
# ---------------------------------------------------------------------------
def send_emails(app_password: str, contacts: list[dict]) -> None:
    if DRY_RUN:
        print("\n" + "=" * 70)
        print("DRY RUN MODE — No emails will actually be sent.")
        print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print("LIVE MODE — Emails WILL be sent!")
        print("=" * 70)

    sent_count = 0
    skipped_count = 0

    smtp_conn = None
    if not DRY_RUN:
        smtp_conn = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        smtp_conn.ehlo()
        smtp_conn.starttls()
        smtp_conn.login(SENDER_EMAIL, app_password)

    try:
        for i, contact in enumerate(contacts, start=1):
            first_name = contact.get("First Name", "").strip()
            last_name = contact.get("Last Name", "").strip()
            email = contact.get("Email", "").strip()
            title = contact.get("Title", "").strip()
            status = contact.get("Email Status", "").strip().lower()

            if not email or status not in ALLOWED_STATUSES:
                print(f"[{i:02d}] SKIP — {first_name} {last_name} | Status: {status or 'missing'}")
                skipped_count += 1
                continue

            persona = detect_persona(title)
            msg = build_email(first_name, email, persona)

            print(f"\n[{i:02d}] {'→ WOULD SEND' if DRY_RUN else '→ SENDING'}")
            print(f"     To      : {first_name} {last_name} <{email}>")
            print(f"     Title   : {title}")
            print(f"     Persona : {persona}")
            print(f"     Subject : {msg['Subject']}")
            if DRY_RUN:
                body_lines = TEMPLATES[persona].format(
                    first_name=first_name,
                    job_title=JOB_TITLE,
                    job_id=JOB_ID,
                    business_unit=BUSINESS_UNIT,
                ).splitlines()
                preview = "\n".join(f"     {ln}" for ln in body_lines[:6])
                print(f"     Body preview:\n{preview}\n     ...")

            if not DRY_RUN:
                smtp_conn.send_message(msg)
                print(f"     ✅ Sent successfully")
                time.sleep(SEND_DELAY_SECONDS)

            sent_count += 1

    finally:
        if smtp_conn:
            smtp_conn.quit()

    print("\n" + "=" * 70)
    if DRY_RUN:
        print(f"DRY RUN complete. Would have sent {sent_count} emails.")
        print("Set DRY_RUN = False and run again to send for real.")
    else:
        print(f"Done. Sent {sent_count} emails. Skipped {skipped_count}.")
    print("=" * 70)


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main() -> None:
    # Read contacts from CSV
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"CSV not found: {CSV_PATH}")

    with open(CSV_PATH, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        contacts = list(reader)

    print(f"Loaded {len(contacts)} contacts from CSV.")

    # Get Gmail App Password
    app_password = os.environ.get("GMAIL_APP_PASSWORD", "mqwz vkrc jlrj nymx")
    if not app_password and not DRY_RUN:
        raise EnvironmentError(
            "Set GMAIL_APP_PASSWORD env var before running in LIVE mode.\n"
            "e.g.: export GMAIL_APP_PASSWORD='xxxx xxxx xxxx xxxx'"
        )

    send_emails(app_password, contacts)


if __name__ == "__main__":
    main()
