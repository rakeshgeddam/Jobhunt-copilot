"""
send_rhp_ai_engineer_emails.py
------------------------------
Personalized outreach for the RHP Properties AI Engineer role.

Uses a verified Apollo CSV, attaches both the tailored resume and cover letter,
and personalizes the message by contact persona.

Setup:
  1. Enable Gmail App Passwords
  2. export GMAIL_APP_PASSWORD="xxxx xxxx xxxx xxxx"
  3. python3 send_rhp_ai_engineer_emails.py
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

SENDER_EMAIL = "rakeshgeddam2025@gmail.com"
SENDER_NAME = "Rakesh Geddam"
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
DRY_RUN = False

CSV_PATH = Path("/Users/rakeshgeddam/Documents/jobsearch/custom-tool/apollo-contacts-export (1).csv")
RESUME_PDF_PATH = Path("/Users/rakeshgeddam/Documents/jobsearch/custom-tool/Rakesh_Geddam_RHP_AI_Engineer.pdf")
COVER_LETTER_PDF_PATH = Path("/Users/rakeshgeddam/Documents/jobsearch/custom-tool/cover_letter_rhp_ai_engineer.pdf")

JOB_TITLE = "AI Engineer"
COMPANY = "RHP Properties"
LOCATION = "Farmington Hills, Michigan"
ALLOWED_STATUSES = {"verified"}
SEND_DELAY_SECONDS = 8

PERSONA_KEYWORDS = {
    "hr_talent": [
        "human resources", "talent", "culture", "recruit", "engagement"
    ],
    "it_project": [
        "it project manager", "project manager", "engineering", "information technology", "it operations"
    ],
    "finance_risk": [
        "finance", "accounting", "asset", "funds", "risk", "titling", "procurement"
    ],
    "community_ops": [
        "community manager", "assistant community manager", "regional manager", "home titling", "operations manager"
    ],
}

SUBJECTS = {
    "hr_talent": "Application follow-up for AI Engineer at RHP Properties",
    "it_project": "AI Engineer application for RHP Properties | Quick introduction",
    "finance_risk": "AI Engineer application | Workflow automation and decision support",
    "community_ops": "Interest in RHP AI Engineer role | Quick intro from Novi",
    "general": "AI Engineer application at RHP Properties | Rakesh Geddam",
}

BASE_CLOSING = (
    "If you are open to a quick 15-minute conversation this week or next, I would really appreciate the chance to learn more about the role and your team. "
    "If someone else would be better to speak with, I would be grateful if you could point me in the right direction.\n\n"
    "I attached both my resume and cover letter for context.\n\n"
    "Thank you for your time, {first_name}.\n\n"
    "Best,\n"
    "Rakesh Geddam\n"
    "Novi, MI\n"
    "rakeshgeddam2025@gmail.com | 516-852-3579 | linkedin.com/in/rakeshge"
)

TEMPLATES = {
    "hr_talent": (
        "Hi {first_name},\n\n"
        "I recently applied for the {job_title} role at {company} and wanted to introduce myself directly. I am based in Novi, so the {location} opportunity is a very natural fit, and I am especially interested in the role because it sits at the intersection of applied AI, workflow transformation, and enterprise adoption.\n\n"
        "Over the last several years, I have been building the kind of AI systems your posting describes. I launched DigiBlinker, a production product serving more than 10,000 monthly active users, where I built agentic AI workflows and Python-based analytics pipelines to support faster product decisions. I also built a retrieval workflow using vector search to surface contextual debugging support, and designed a knowledge-graph-driven AI mentoring platform that personalized recommendations through structured relationships and LLM feedback.\n\n"
        "What stands out to me about RHP is the opportunity to turn manual enterprise processes into practical AI-assisted workflows across teams. That is the type of work I want to keep doing, not just building models, but helping an organization adopt AI in a way that is useful, reliable, and easy for teams to embrace.\n\n"
        + BASE_CLOSING
    ),
    "it_project": (
        "Hi {first_name},\n\n"
        "I applied for the {job_title} role at {company} and wanted to reach out directly because the mix of AI delivery, enterprise integration, and workflow modernization in the posting matches the work I have been doing recently. I am nearby in Novi, and I would be glad to contribute in a role centered in {location}.\n\n"
        "My recent work has focused on production AI systems rather than isolated demos. At DigiBlinker, I built agentic workflows, Python pipelines, and API-driven analytics around a live product used by more than 10,000 monthly active users. In project work, I built a RAG-style developer tool using vector search with Qdrant, and I designed a knowledge-graph-based AI platform that combined LLMs, structured relationships, and full-stack delivery. I also have experience integrating AI solutions with APIs, SQL-driven data systems, and business-facing applications.\n\n"
        "Your role stood out because it is not just about experimentation. It is about deploying AI systems that teams can actually use to improve operations, decision-making, and day-to-day execution. That is exactly the kind of ownership I am looking for.\n\n"
        + BASE_CLOSING
    ),
    "finance_risk": (
        "Hi {first_name},\n\n"
        "I recently applied for the {job_title} role at {company} and wanted to introduce myself. I am based in Novi, so the Farmington Hills location is a strong fit, and I was drawn to the role because of its focus on using AI to improve business operations in a practical way.\n\n"
        "My background combines AI engineering with data systems and decision support. I built DigiBlinker into a live product with more than 10,000 monthly active users and used Python-based AI workflows and analytics agents to turn usage data into actionable product decisions. I also built a retrieval system using vector search to surface relevant context from historical issues, and designed a knowledge-graph-driven AI platform that personalized recommendations through structured data relationships. Earlier in my career, I automated 6 workflows in a 100+ TB migration at Bank of America, which gave me a strong foundation in data quality, operational reliability, and business-critical systems.\n\n"
        "What excites me about RHP is the opportunity to apply AI to forecasting, workflow automation, anomaly identification, and enterprise decision support in ways that create real operational value across the business.\n\n"
        + BASE_CLOSING
    ),
    "community_ops": (
        "Hi {first_name},\n\n"
        "I applied for the {job_title} role at {company} and wanted to send a direct note. I live in Novi, so the Farmington Hills opportunity is a very practical fit, and I am especially interested because the role is focused on using AI to make internal workflows more effective for teams across the organization.\n\n"
        "In my recent work, I have been building AI systems that are meant to be used, not just demonstrated. At DigiBlinker, I launched a live product used by more than 10,000 monthly active users and built agentic workflows and analytics pipelines around it. I also built a retrieval workflow using vector search to deliver context-aware support, and designed a knowledge-graph-driven AI platform that used structured relationships and LLM reasoning to guide recommendations. At Melo.co, I deployed a Gemini-powered chatbot that automated support workflows for 300 patients each month and reduced manual onboarding work by 15 to 30 minutes per patient.\n\n"
        "That is why the RHP role caught my attention. I would love to help teams move from manual processes to AI-augmented workflows that improve service quality, speed, and consistency.\n\n"
        + BASE_CLOSING
    ),
    "general": (
        "Hi {first_name},\n\n"
        "I recently applied for the {job_title} role at {company} and wanted to introduce myself directly. I am based in Novi, which makes the Farmington Hills opportunity a strong fit, and I am very interested in the role because it combines applied AI, enterprise systems, and workflow transformation.\n\n"
        "My recent experience includes building DigiBlinker, a live product used by more than 10,000 monthly active users, where I developed agentic AI workflows and Python-based analytics pipelines. I also built a RAG-style retrieval tool using vector search to surface relevant debugging context, and designed a knowledge-graph-driven AI platform that used LLMs and structured data relationships to personalize recommendations. In addition, I have delivered AI workflow automation in healthcare through a Gemini-powered chatbot that supported 300 patients each month.\n\n"
        "I am reaching out because I would value the chance to learn more about how RHP is thinking about AI adoption across the business and where this role can have the biggest impact.\n\n"
        + BASE_CLOSING
    ),
}


def detect_persona(title: str) -> str:
    title_lower = (title or "").lower()
    for persona, keywords in PERSONA_KEYWORDS.items():
        for keyword in keywords:
            if keyword in title_lower:
                return persona
    return "general"



def attach_file(msg: MIMEMultipart, path: Path) -> None:
    if not path.exists():
        print(f"  ⚠️  Attachment not found: {path}")
        return
    with open(path, "rb") as f:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f'attachment; filename="{path.name}"')
    msg.attach(part)



def build_email(contact: dict) -> MIMEMultipart:
    first_name = contact.get("First Name", "").strip() or "there"
    email = contact.get("Email", "").strip()
    title = contact.get("Title", "").strip()
    persona = detect_persona(title)

    msg = MIMEMultipart()
    msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
    msg["To"] = email
    msg["Subject"] = SUBJECTS[persona]

    body = TEMPLATES[persona].format(
        first_name=first_name,
        job_title=JOB_TITLE,
        company=COMPANY,
        location=LOCATION,
    )
    msg.attach(MIMEText(body, "plain"))

    attach_file(msg, RESUME_PDF_PATH)
    attach_file(msg, COVER_LETTER_PDF_PATH)
    return msg



def send_emails(app_password: str, contacts: list[dict]) -> None:
    mode = "DRY RUN" if DRY_RUN else "LIVE MODE"
    print(f"\n{'=' * 72}\n{mode}\n{'=' * 72}")

    smtp_conn = None
    if not DRY_RUN:
        smtp_conn = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        smtp_conn.ehlo()
        smtp_conn.starttls()
        smtp_conn.login(SENDER_EMAIL, app_password)

    sent_count = 0
    skipped_count = 0

    try:
        for index, contact in enumerate(contacts, start=1):
            email = contact.get("Email", "").strip()
            status = contact.get("Email Status", "").strip().lower()
            if not email or status not in ALLOWED_STATUSES:
                skipped_count += 1
                print(f"[{index:02d}] SKIP | {contact.get('First Name', '')} {contact.get('Last Name', '')} | status={status or 'missing'}")
                continue

            msg = build_email(contact)
            persona = detect_persona(contact.get("Title", ""))
            action = "WOULD SEND" if DRY_RUN else "SENDING"
            print(f"\n[{index:02d}] {action}")
            print(f"     To      : {contact.get('First Name', '')} {contact.get('Last Name', '')} <{email}>")
            print(f"     Title   : {contact.get('Title', '')}")
            print(f"     Persona : {persona}")
            print(f"     Subject : {msg['Subject']}")

            if not DRY_RUN:
                smtp_conn.send_message(msg)
                print("     ✅ Sent")
                time.sleep(SEND_DELAY_SECONDS)

            sent_count += 1
    finally:
        if smtp_conn:
            smtp_conn.quit()

    print(f"\n{'=' * 72}")
    if DRY_RUN:
        print(f"DRY RUN complete. Would have sent {sent_count} emails. Skipped {skipped_count}.")
    else:
        print(f"Done. Sent {sent_count} emails. Skipped {skipped_count}.")
    print(f"{'=' * 72}")



def main() -> None:
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"CSV not found: {CSV_PATH}")

    with open(CSV_PATH, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        contacts = list(reader)

    app_password = os.environ.get("GMAIL_APP_PASSWORD", "mqwz vkrc jlrj nymx")
    if not app_password and not DRY_RUN:
        raise EnvironmentError("Set GMAIL_APP_PASSWORD before running in LIVE mode.")

    send_emails(app_password, contacts)


if __name__ == "__main__":
    main()
