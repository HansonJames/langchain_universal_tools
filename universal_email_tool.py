import os
from typing import Optional, Type
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from langchain.tools import BaseTool
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import imaplib
import email
from email.header import decode_header
import html2text

load_dotenv()

import json

# Load email configurations from environment
EMAIL_CONFIGS = json.loads(os.getenv("EMAIL_CONFIGS"))


class EmailInput(BaseModel):
    """Input for Universal Email Tool."""
    to: str = Field(..., description="The recipient's email address")
    subject: str = Field(..., description="The subject of the email")
    body: str = Field(..., description="The content of the email")
    cc: Optional[str] = Field(None, description="Optional CC recipient's email address")
    is_html: Optional[bool] = Field(False, description="Whether the email content is HTML format")
    attachment_path: Optional[str] = Field(None, description="Optional path to an attachment file")


class UniversalEmailTool(BaseTool):
    """Tool for sending emails via multiple email services."""
    name: str = "universal_email_sender"
    description: str = """Send emails via multiple email services (QQ, 163, Aliyun) with support for HTML content, CC recipients, and attachments.
    Input should be a natural language request describing the email details.

    Examples:
    1. "Send an email to user@example.com with subject 'Hello' and body 'Test email'"
    2. "Send HTML email to user@example.com, CC to cc@example.com, subject 'Test', content '<h1>Hello</h1>'"
    3. "Send email to user@example.com, subject 'Files', body 'See attachment', attach file.txt"

    The tool will format your request into proper email parameters."""
    args_schema: Type[BaseModel] = EmailInput

    def __init__(self, **data):
        super().__init__(**data)
        self._email_service = os.getenv("EMAIL_USE", "QQ").upper()
        if self._email_service not in EMAIL_CONFIGS:
            raise ValueError(f"Unsupported email service: {self._email_service}")

        config = EMAIL_CONFIGS[self._email_service]
        self._sender_email = config["username"]
        self._auth_code = config["password"]
        self._smtp_host = config["smtp_host"]
        self._smtp_port = config["smtp_port"]

        if not self._sender_email or not self._auth_code:
            raise ValueError(f"Email credentials for {self._email_service} are missing in EMAIL_CONFIGS")

    def _prepare_message(
            self,
            to_email: str,
            subject: str,
            body: str,
            cc_email: Optional[str] = None,
            is_html: bool = False,
            attachment_path: Optional[str] = None
    ) -> MIMEMultipart:
        """Prepare the email message with all components."""
        message = MIMEMultipart()
        message["From"] = self._sender_email
        message["To"] = to_email
        if cc_email:
            message["Cc"] = cc_email
        message["Subject"] = subject

        # Add body
        body_part = MIMEText(body, 'html' if is_html else 'plain', 'utf-8')
        message.attach(body_part)

        # Add attachment if provided
        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, 'rb') as f:
                attachment = MIMEApplication(f.read())
                attachment.add_header(
                    'Content-Disposition',
                    'attachment',
                    filename=os.path.basename(attachment_path)
                )
                message.attach(attachment)

        return message

    def _run(
            self,
            to: str,
            subject: str,
            body: str,
            cc: Optional[str] = None,
            is_html: bool = False,
            attachment_path: Optional[str] = None
    ) -> str:
        """Run the tool to send an email."""
        try:
            # Create message
            msg = self._prepare_message(
                to_email=to,
                subject=subject,
                body=body,
                cc_email=cc,
                is_html=is_html,
                attachment_path=attachment_path
            )

            # Create list of recipients
            recipients = [to]
            if cc:
                recipients.append(cc)

            try:
                # Connect to SMTP server
                server = smtplib.SMTP_SSL(self._smtp_host, self._smtp_port)
                server.login(self._sender_email, self._auth_code)

                # Send the email
                server.sendmail(self._sender_email, recipients, msg.as_string())
                server.quit()

                return f"Email sent successfully via {self._email_service} to {to}" + (
                    f" with CC to {cc}" if cc else "")

            except smtplib.SMTPException as e:
                return f"SMTP error occurred: {str(e)}"

        except Exception as e:
            return f"Failed to send email: {str(e)}"


class EmailReadInput(BaseModel):
    """Input for reading emails."""
    num_emails: int = Field(..., description="Number of recent emails to read (max 50)")


class UniversalEmailToolReading(BaseTool):
    """Tool for reading and summarizing emails."""
    name: str = "universal_email_reader"
    description: str = """Read and summarize recent emails from your email inbox.
    Input should be a number between 1 and 50 indicating how many recent emails to read.

    Examples:
    1. "Read my last 20 emails"
    2. "Show me my 30 most recent emails"
    3. "Summarize my latest 50 emails"
    4. "Get a summary of my last 15 emails"
    """
    args_schema: Type[BaseModel] = EmailReadInput

    def __init__(self, **data):
        super().__init__(**data)
        self._email_service = os.getenv("EMAIL_USE", "QQ").upper()
        if self._email_service not in EMAIL_CONFIGS:
            raise ValueError(f"Unsupported email service: {self._email_service}")

        config = EMAIL_CONFIGS[self._email_service]
        self._email = config["username"]
        self._auth_code = config["password"]
        self._imap_host = config["imap_host"]

        if not self._email or not self._auth_code:
            raise ValueError(f"Email credentials for {self._email_service} are missing in EMAIL_CONFIGS")
        self._h2t = html2text.HTML2Text()
        self._h2t.ignore_links = True

    def _decode_email_subject(self, subject):
        """Decode email subject."""
        if not subject:
            return "No Subject"
        decoded_list = decode_header(subject)
        subject = ""
        for decoded_str, charset in decoded_list:
            if isinstance(decoded_str, bytes):
                if charset:
                    try:
                        subject += decoded_str.decode(charset)
                    except:
                        subject += decoded_str.decode('utf-8', errors='ignore')
                else:
                    subject += decoded_str.decode('utf-8', errors='ignore')
            else:
                subject += str(decoded_str)
        return subject

    def _get_email_content(self, msg):
        """Extract email content from message."""
        try:
            content = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        try:
                            content = part.get_payload(decode=True).decode()
                            break
                        except:
                            content = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                            break
                    elif part.get_content_type() == "text/html":
                        try:
                            html_content = part.get_payload(decode=True).decode()
                            content = self._h2t.handle(html_content)
                            break
                        except:
                            html_content = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                            content = self._h2t.handle(html_content)
                            break
            else:
                try:
                    content = msg.get_payload(decode=True).decode()
                except:
                    content = msg.get_payload(decode=True).decode('utf-8', errors='ignore')

            # Clean up the content
            content = content.strip()
            content = ' '.join(content.split())  # Remove extra whitespace
            return content
        except Exception as e:
            return f"[Error extracting content: {str(e)}]"

    def _run(
            self,
            num_emails: int
    ) -> str:
        """Run the tool to read recent emails."""
        try:
            # Limit number of emails to 50
            num_emails = min(max(1, num_emails), 50)

            # Connect to IMAP server
            mail = imaplib.IMAP4_SSL(self._imap_host)
            mail.login(self._email, self._auth_code)

            # Select inbox
            mail.select("INBOX")

            # Search for all emails and get the latest ones
            _, messages = mail.search(None, "ALL")
            email_ids = messages[0].split()
            latest_emails = email_ids[-num_emails:]

            # Process each email
            summaries = []
            separator = "-" * 50

            for email_id in reversed(latest_emails):
                try:
                    _, msg_data = mail.fetch(email_id, "(RFC822)")
                    email_body = msg_data[0][1]
                    msg = email.message_from_bytes(email_body)

                    # Get subject
                    subject = self._decode_email_subject(msg["subject"])

                    # Get sender
                    sender = msg["from"] if msg["from"] else "Unknown Sender"

                    # Get content
                    content = self._get_email_content(msg)

                    # Create summary
                    summary = f"\nFrom: {sender}\nSubject: {subject}\nContent Summary: {content[:200]}...\n{separator}"
                    summaries.append(summary)
                except Exception as e:
                    summaries.append(f"\nError processing email: {str(e)}\n{separator}")

            mail.close()
            mail.logout()

            if not summaries:
                return "No emails found in the inbox."

            header = f"Latest {num_emails} emails from {self._email_service} account:"
            top_separator = "=" * 50
            bottom_separator = "=" * 50

            return f"{header}\n{top_separator}\n{''.join(summaries)}\n{bottom_separator}\nEnd of email summaries."

        except Exception as e:
            return f"Failed to read emails: {str(e)}"
