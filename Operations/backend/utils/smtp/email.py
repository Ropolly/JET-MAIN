from os import getenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from typing import List, Optional
from pathlib import Path

EMAIL_TEMPLATE_PATH = Path(__file__).resolve().parent / "email_template.html"


def send_email(subject: str, targets: List[str], body: str, is_html: bool = False, attachments: Optional[List[str]] = None):
    # Create multipart message if we have attachments
    if attachments:
        msg = MIMEMultipart()
        msg.attach(MIMEText(body, "html" if is_html else "plain"))

        # Add attachments
        for attachment_path in attachments:
            if Path(attachment_path).exists():
                with open(attachment_path, 'rb') as f:
                    attachment = MIMEApplication(f.read(), _subtype='pdf')
                    attachment.add_header('Content-Disposition', 'attachment', filename=Path(attachment_path).name)
                    msg.attach(attachment)
    else:
        msg = MIMEText(body, "html") if is_html else MIMEText(body)

    msg["From"] = getenv("DEFAULT_FROM_EMAIL")
    msg["To"] = ", ".join(targets)
    msg["Subject"] = subject

    server = None
    connection_established = False
    try:
        host = getenv("EMAIL_HOST")
        port = int(getenv("EMAIL_PORT", "587"))
        user = getenv("EMAIL_HOST_USER")
        password = getenv("EMAIL_HOST_PASSWORD")

        server = smtplib.SMTP(host, port, timeout=20)
        server.ehlo()
        connection_established = True

        server.starttls()
        server.ehlo()

        server.login(user, password)
        server.sendmail(msg["From"], targets, msg.as_string())
        return True
    except Exception as e:
        print("❌ Email error:", e)
        return False
    finally:
        if server and connection_established:
            try:
                server.quit()
            except:
                pass


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


def send_template(subject: str, targets: List[str], title: str, link: str, link_text="Click Here!", attachments: Optional[List[str]] = None):
    body = fill_template(title, link, link_label=link_text)
    return send_email(subject, targets, body, is_html=True, attachments=attachments)


def send_user_activation_email(email: str, first_name: str, last_name: str, token: str, frontend_url: str = "http://localhost:3000"):
    """Send user activation email with token link"""
    activation_link = f"{frontend_url}/setup-password?token={token}"

    subject = "Welcome to JET ICU - Activate Your Account"

    message = f"""Hello {first_name} {last_name},

Welcome to JET ICU Medical Transport! Your account has been created and you're almost ready to get started.

To complete your account setup, please click the button below to set your password and complete your profile:

This link will expire in 24 hours for security purposes. If you need assistance or have any questions, please contact our team at ops@jeticu.com.

Thank you for joining JET ICU!"""

    return send_template(
        subject=subject,
        targets=[email],
        title=message,
        link=activation_link,
        link_text="Activate My Account"
    )


def send_password_reset_email(email: str, token: str, frontend_url: str = "http://localhost:3000"):
    """Send password reset email with token link"""
    reset_link = f"{frontend_url}/reset-password?token={token}"

    subject = "JET ICU - Password Reset Request"

    message = f"""Hello,

We received a request to reset the password for your JET ICU account associated with this email address.

If you requested this password reset, please click the button below to set a new password:

This link will expire in 2 hours for security purposes. If you did not request this password reset, please ignore this email and your password will remain unchanged.

If you continue to have trouble accessing your account, please contact our team at ops@jeticu.com.

Best regards,
JET ICU Team"""

    return send_template(
        subject=subject,
        targets=[email],
        title=message,
        link=reset_link,
        link_text="Reset My Password"
    )
  


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
