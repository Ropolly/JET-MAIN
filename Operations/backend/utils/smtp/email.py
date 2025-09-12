from os import getenv
import smtplib
from email.mime.text import MIMEText
from typing import List
from pathlib import Path

EMAIL_TEMPLATE_PATH = Path(__file__).resolve().parent / "email_template.html"


def send_email(subject: str, targets: List[str], body: str, is_html: bool = False):
    msg = MIMEText(body, "html") if is_html else MIMEText(body)
    msg["From"] = getenv("DEFAULT_FROM_EMAIL")
    msg["To"] = ", ".join(targets)
    msg["Subject"] = subject

    server = None
    try:
        host = getenv("EMAIL_HOST")
        port = int(getenv("EMAIL_PORT", "587"))
        user = getenv("EMAIL_HOST_USER")
        password = getenv("EMAIL_HOST_PASSWORD")

        server = smtplib.SMTP(host, port, timeout=20)
        server.ehlo()

        server.starttls()
        server.ehlo()

        server.login(user, password)
        server.sendmail(msg["From"], targets, msg.as_string())
        return True
    except Exception as e:
        print("❌ Email error:", e)
        return False
    finally:
        if server:
            server.quit()


# TODO add support for preview and text below button
def fill_template(text: str, link_address: str, link_label="Click Here!"):
    with open(EMAIL_TEMPLATE_PATH, "r") as file:
        content = file.read()
    html = content.replace("%%%PREVIEW%%%", "").replace("%%%BOTTEXT%%%", "")
    html = (
        html.replace("%%%LINK%%%", link_address)
        .replace("%%%LINKTEXT%%%", link_label)
        .replace("%%%TOPTEXT%%%", text)
    )
    return html


def send_template(subject: str, targets: List[str], title: str, link: str, link_text="Click Here!"):
    body = fill_template(title, link, link_label=link_text)
    return send_email(subject, targets, body, is_html=True)
  


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    print(
        send_template(
            "Test Email",
            ["myrmelryan@gmail.com","ck@cekitch.com"],
            "click here for fun",
            "http://www.google.com",
        )
    )
