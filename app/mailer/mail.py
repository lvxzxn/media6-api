# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from typing import Any, Dict
from datetime import datetime
from pathlib import Path

import resend
from jinja2 import Template
from resend.exceptions import ResendError

from app.core.config import settings

BASE_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = BASE_DIR / "templates"

class MailService:
    def __init__(self) -> None:
        if not settings.resend_api_key:
            raise RuntimeError("resend_api_key não configurada")

        resend.api_key = settings.resend_api_key

        self.from_email = settings.from_email
        self.from_name = settings.from_name

    def _format_contact_info(self, contact: str) -> Dict[str, str]:
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        contact = contact.strip()

        if re.fullmatch(email_regex, contact):
            return {
                "contact_type": "E-mail",
                "contact_display": contact,
                "contact_link": f"mailto:{contact}",
            }

        phone_numbers_only = re.sub(r"\D", "", contact)

        return {
            "contact_type": "WhatsApp",
            "contact_display": contact,
            "contact_link": f"https://wa.me/55{phone_numbers_only}",
        }

    def send_email(self, *, to_email: str, subject: str, html_template: str, context: Dict[str, Any]) -> bool:
        try:
            html_content = Template(html_template).render(**context)

            email_data = {
                "from": f"{self.from_name} <{self.from_email}>",
                "to": [to_email],
                "subject": subject,
                "html": html_content,
            }

            resend.Emails.send(email_data)
            return True

        except ResendError as e:
            return False

        except Exception as e:
            return False


    def send_email_from_file(self, *, to_email: str, subject: str, template_path: Path, context: Dict[str, Any]) -> bool:
        try:
            if not template_path.exists():
                raise FileNotFoundError(template_path)

            html_template = template_path.read_text(encoding="utf-8")

            return self.send_email(
                to_email=to_email,
                subject=subject,
                html_template=html_template,
                context=context,
            )

        except FileNotFoundError:
            return False

        except Exception as e:
            return False

    def send_proposal(
        self,
        *,
        to_email: str,
        user_name: str,
        user_contact: str,
        user_message: str,
    ) -> bool:
        contact_info = self._format_contact_info(user_contact)

        context = {
            "user_name": user_name,
            "user_contact": user_contact,
            "user_message": user_message,
            "contact_type": contact_info["contact_type"],
            "contact_display": contact_info["contact_display"],
            "contact_link": contact_info["contact_link"],
            "email_date": datetime.now().strftime("%d/%m/%Y às %H:%M"),
        }

        template_path = TEMPLATE_DIR / "email_admin_notification.html"

        return self.send_email_from_file(
            to_email=to_email,
            subject=f"Nova mensagem - {user_name}",
            template_path=template_path,
            context=context,
        )
