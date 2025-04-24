from dataclasses import dataclass
from typing import List, Optional

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from pydantic import EmailStr


@dataclass
class EmailData:
    email_to: List[EmailStr]
    fullname: Optional[str] = None
    task_id: Optional[int] = None
    task_title: Optional[str] = None
    company_name: Optional[str] = None
    password: Optional[str] = None

    def _send_email(self, subject: str, html_content: str):
        email = EmailMessage(
            subject=subject,
            body=html_content,
            from_email="demo@example.com",
            to=self.email_to,
        )
        # Send the email
        email.content_subtype = "html"  # Set the content type to HTML
        email.send(fail_silently=False)

    def send_task_assigned_email(self) -> None:
        """
        Send an email to the assignee.
        """
        subject = "Task Assigned"
        html_content = render_to_string("task_assigned_email.html", {"task_id": self.task_id,
                                                                     "task_title": self.task_title})
        self._send_email(subject, html_content)

    def send_create_staff_email(self) -> None:
        """
        Send an email to the staff.
        """
        subject = "Welcome to eTaskify!"
        html_content = render_to_string("staff_created_email.html", {"fullname": self.fullname,
                                                                     "company_name": self.company_name,
                                                                     "password": self.password})
        self._send_email(subject, html_content)
