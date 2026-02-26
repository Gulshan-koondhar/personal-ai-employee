"""
Email Agent Skill for AI Employee

This skill handles email operations for the AI Employee.
"""
import json
from typing import Dict, Any, List
from pathlib import Path

def send_email(to: str, subject: str, body: str, cc: str = "", bcc: str = "") -> Dict[str, Any]:
    """
    Send an email to a recipient using either Gmail API or SMTP.

    Args:
        to: Recipient email address
        subject: Email subject
        body: Email body content
        cc: CC recipients (optional)
        bcc: BCC recipients (optional)

    Returns:
        Dictionary with success status and email ID
    """
    import base64
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    import smtplib
    from email.utils import formataddr

    # First, try using Gmail API
    try:
        # Import required modules for Gmail API
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        import os
        from pathlib import Path

        # Load environment variables
        env_path = Path('../../gold/.env')
        if env_path.exists():
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"\'')
                        if key not in os.environ:
                            os.environ[key] = value

        # Get Gmail credentials from environment
        client_id = os.environ.get('GMAIL_CLIENT_ID')
        client_secret = os.environ.get('GMAIL_CLIENT_SECRET')
        refresh_token = os.environ.get('GMAIL_REFRESH_TOKEN')
        from_email = os.environ.get('EMAIL_FROM_ADDRESS')

        if all([client_id, client_secret, refresh_token]):
            # Try Gmail API approach
            creds = Credentials(
                token=None,
                refresh_token=refresh_token,
                token_uri='https://oauth2.googleapis.com/token',
                client_id=client_id,
                client_secret=client_secret,
                scopes=['https://www.googleapis.com/auth/gmail.send']
            )

            # Build the Gmail service
            service = build('gmail', 'v1', credentials=creds)

            # Create email message
            message = MIMEMultipart()
            message['to'] = to
            message['subject'] = subject

            if cc:
                message['cc'] = cc

            # Add body to email
            message.attach(MIMEText(body, 'plain'))

            # Encode the message
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

            # Send email using Gmail API
            sent_message = service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()

            email_id = sent_message.get('id', f"email_{hash(to + subject + str(hash(body))) % 10000}")
            return {
                "success": True,
                "email_id": email_id,
                "message": f"Email sent successfully via Gmail API to {to}"
            }

    except Exception as api_error:
        # If Gmail API fails, fall back to SMTP
        try:
            import os
            from pathlib import Path

            # Load environment variables
            env_path = Path('../../gold/.env')
            if env_path.exists():
                with open(env_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip().strip('"\'')
                            if key not in os.environ:
                                os.environ[key] = value

            # Get SMTP credentials from environment
            smtp_username = os.environ.get('EMAIL_SMTP_USERNAME')
            smtp_password = os.environ.get('EMAIL_SMTP_PASSWORD')
            smtp_host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
            smtp_port = int(os.environ.get('SMTP_PORT', '587'))
            from_email = os.environ.get('EMAIL_FROM_ADDRESS')

            # For Gmail, use the from email address as username if SMTP username looks incorrect
            if not smtp_username or '@' not in smtp_username:
                smtp_username = from_email

            if not all([smtp_username, smtp_password, from_email]):
                return {
                    "success": False,
                    "email_id": None,
                    "message": "SMTP credentials not properly configured"
                }

            # Create email message
            message = MIMEMultipart()
            message['From'] = formataddr(('', from_email))
            message['To'] = to
            message['Subject'] = subject

            if cc:
                message['Cc'] = cc

            # Add body to email
            message.attach(MIMEText(body, 'plain'))

            # Connect to SMTP server and send email
            server = smtplib.SMTP(smtp_host, smtp_port)
            server.starttls()
            server.login(smtp_username, smtp_password)

            # Get all recipients including CC
            all_recipients = [to]
            if cc:
                all_recipients.append(cc)
            if bcc:
                all_recipients.append(bcc)

            text = message.as_string()
            server.sendmail(from_email, all_recipients, text)
            server.quit()

            email_id = f"email_{hash(to + subject + str(hash(body))) % 10000}"
            return {
                "success": True,
                "email_id": email_id,
                "message": f"Email sent successfully via SMTP to {to}"
            }

        except Exception as smtp_error:
            return {
                "success": False,
                "email_id": None,
                "message": f"Both Gmail API and SMTP failed. Gmail API error: {str(api_error)}, SMTP error: {str(smtp_error)}"
            }

def queue_email_for_approval(to: str, subject: str, body: str, priority: str = "medium") -> Dict[str, Any]:
    """
    Queue an email for approval before sending.

    Args:
        to: Recipient email address
        subject: Email subject
        body: Email body content
        priority: Priority level (low, medium, high)

    Returns:
        Dictionary with success status and email ID
    """
    # Create an approval request in the Pending_Approval folder
    from datetime import datetime

    approval_content = f"""---
type: approval_request
action_type: email
priority: {priority}
created: {datetime.now().isoformat()}
status: pending_approval
---

# Email Approval Request

## Email Details
- **To:** {to}
- **Subject:** {subject}
- **Priority:** {priority}

## Email Content
{body}

## Actions Required
- [ ] Approve this email to send
- [ ] Move to /Approved folder to send
- [ ] Move to /Rejected folder to discard

## Notes
This email was generated by AI Employee and requires human approval before sending.
"""

    # Write to approval queue
    vault_path = Path("../AI_Employee_Vault")
    pending_approval_path = vault_path / "Plans" / "Pending_Approval"
    pending_approval_path.mkdir(parents=True, exist_ok=True)

    approval_filename = f"EMAIL_APPROVAL_{int(datetime.now().timestamp())}.md"
    approval_file_path = pending_approval_path / approval_filename
    approval_file_path.write_text(approval_content)

    return {
        "success": True,
        "approval_id": approval_filename,
        "message": f"Email queued for approval: {approval_filename}"
    }

def read_emails(count: int = 10) -> List[Dict[str, Any]]:
    """
    Read recent emails (simulated for this demo).

    Args:
        count: Number of emails to read

    Returns:
        List of email dictionaries
    """
    # This is a simulated function
    return [
        {
            "id": "sim1",
            "from": "client@example.com",
            "subject": "Project Update Request",
            "body": "Could you please provide an update on the project?",
            "received": "2026-02-19T10:00:00Z",
            "priority": "high"
        },
        {
            "id": "sim2",
            "from": "team@company.com",
            "subject": "Weekly Team Meeting",
            "body": "Reminder about the weekly team meeting.",
            "received": "2026-02-19T09:30:00Z",
            "priority": "medium"
        }
    ]

# Define the skill specification
SKILL_SPEC = {
    "name": "email_skill",
    "description": "Handles email operations for the AI Employee",
    "functions": [
        {
            "name": "send_email",
            "description": "Send an email to a recipient",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {"type": "string", "description": "Recipient email address"},
                    "subject": {"type": "string", "description": "Email subject"},
                    "body": {"type": "string", "description": "Email body content"},
                    "cc": {"type": "string", "description": "CC recipients (optional)"},
                    "bcc": {"type": "string", "description": "BCC recipients (optional)"}
                },
                "required": ["to", "subject", "body"]
            }
        },
        {
            "name": "queue_email_for_approval",
            "description": "Queue an email for approval before sending",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {"type": "string", "description": "Recipient email address"},
                    "subject": {"type": "string", "description": "Email subject"},
                    "body": {"type": "string", "description": "Email body content"},
                    "priority": {"type": "string", "description": "Priority level: low, medium, high"}
                },
                "required": ["to", "subject", "body"]
            }
        },
        {
            "name": "read_emails",
            "description": "Read recent emails",
            "parameters": {
                "type": "object",
                "properties": {
                    "count": {"type": "integer", "description": "Number of emails to read (default: 10)"}
                }
            }
        }
    ]
}