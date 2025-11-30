"""Email template rendering utilities.

This module provides utilities for rendering email templates using Jinja2.
Templates are stored in src/services/email_templates/ directory.
"""

from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Get the email templates directory path
TEMPLATES_DIR = Path(__file__).parent.parent / "services" / "email_templates"

# Create Jinja2 environment for template rendering
template_env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    autoescape=select_autoescape(["html", "xml"]),
    trim_blocks=True,
    lstrip_blocks=True,
)


def render_verification_email(verification_url: str, user_email: str) -> str:
    """Render the email verification HTML template.

    Args:
        verification_url: Full URL for email verification
        user_email: User's email address

    Returns:
        Rendered HTML email content
    """
    template = template_env.get_template("verification.html")
    return template.render(verification_url=verification_url, email=user_email)


def render_welcome_email(user_email: str, login_url: str) -> str:
    """Render the welcome email HTML template.

    Args:
        user_email: User's email address
        login_url: URL to login page

    Returns:
        Rendered HTML email content
    """
    template = template_env.get_template("welcome.html")
    return template.render(email=user_email, login_url=login_url)


def render_password_reset_email(reset_url: str, user_email: str) -> str:
    """Render the password reset HTML template.

    Args:
        reset_url: Full URL for password reset
        user_email: User's email address

    Returns:
        Rendered HTML email content
    """
    template = template_env.get_template("password_reset.html")
    return template.render(reset_url=reset_url, email=user_email)
