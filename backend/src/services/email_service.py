"""
Email service using SendGrid for transactional emails.
"""

import logging
from typing import Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from ..config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """
    Email service for sending transactional emails via SendGrid.

    Supports:
    - Email verification
    - Welcome emails
    - Password reset
    - Template-based emails with Jinja2
    """

    def __init__(self) -> None:
        """Initialize SendGrid client and template environment."""
        self.client = SendGridAPIClient(settings.sendgrid_api_key)
        self.from_email = settings.from_email
        self.from_name = settings.from_name

        # Initialize Jinja2 template environment
        # Templates will be in src/services/email_templates/
        try:
            self.template_env = Environment(
                loader=FileSystemLoader("src/services/email_templates"),
                autoescape=select_autoescape(["html", "xml"]),
            )
        except Exception as e:
            logger.warning(f"Failed to load email templates: {e}")
            self.template_env = None

    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
    ) -> bool:
        """
        Send an email via SendGrid.

        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML email body
            text_content: Plain text email body (optional)

        Returns:
            bool: True if sent successfully, False otherwise
        """
        try:
            message = Mail(
                from_email=(self.from_email, self.from_name),
                to_emails=to_email,
                subject=subject,
                html_content=html_content,
                plain_text_content=text_content or "",
            )

            response = self.client.send(message)

            if response.status_code in [200, 201, 202]:
                logger.info(f"Email sent successfully to {to_email}: {subject}")
                return True
            else:
                logger.error(
                    f"Failed to send email to {to_email}. "
                    f"Status: {response.status_code}, Body: {response.body}"
                )
                return False

        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error sending email to {to_email}: {error_msg}")
            # Log more details for debugging SendGrid issues
            if "400" in error_msg or "Bad Request" in error_msg:
                logger.error(
                    "SendGrid 400 Error - Common causes:\n"
                    "1. FROM_EMAIL not verified in SendGrid (Sender Authentication required)\n"
                    "2. Invalid email format\n"
                    "3. API key doesn't have mail.send permission\n"
                    f"FROM_EMAIL: {self.from_email}"
                )
            return False

    async def send_verification_email(
        self, to_email: str, verification_token: str, user_email: str
    ) -> bool:
        """
        Send email verification email with 6-digit code.

        Args:
            to_email: Recipient email
            verification_token: 6-digit verification code
            user_email: User's registered email

        Returns:
            bool: True if sent successfully
        """
        # Use the 6-digit code directly in the email
        html_content = self._get_verification_code_html(verification_token, user_email)

        subject = "Your Verification Code - Physical AI Learning Platform"

        result = await self.send_email(to_email, subject, html_content)
        
        # In development, log the code if email fails
        if not result:
            logger.warning(
                f"[DEV] Email failed - Verification code for {user_email}: {verification_token}"
            )
        
        return result

    @staticmethod
    def _get_verification_code_html(code: str, email: str) -> str:
        """HTML email template for verification code."""
        return f"""
        <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #2563eb; text-align: center;">Verify Your Email</h1>
                <p style="text-align: center;">Hello,</p>
                <p style="text-align: center;">Thank you for registering with Physical AI Learning Platform!</p>
                <p style="text-align: center;">Your verification code is:</p>
                <div style="background-color: #f3f4f6; border-radius: 8px; padding: 30px; margin: 30px 0; text-align: center;">
                    <span style="font-size: 42px; font-weight: bold; letter-spacing: 8px; color: #1f2937; font-family: 'Courier New', monospace;">
                        {code}
                    </span>
                </div>
                <p style="text-align: center; color: #6b7280;">
                    Enter this code in the verification form to complete your registration.
                </p>
                <p style="margin-top: 40px; color: #6b7280; font-size: 12px; text-align: center;">
                    This code will expire in 1 hour.<br>
                    If you didn't create an account, please ignore this email.
                </p>
            </body>
        </html>
        """

    async def send_welcome_email(self, to_email: str, user_name: str) -> bool:
        """
        Send welcome email after successful verification.

        Args:
            to_email: Recipient email
            user_name: User's name or email

        Returns:
            bool: True if sent successfully
        """
        if self.template_env:
            try:
                template = self.template_env.get_template("welcome.html")
                html_content = template.render(
                    user_name=user_name, platform_url=settings.frontend_url
                )
            except Exception as e:
                logger.warning(f"Failed to render welcome template: {e}")
                html_content = self._get_welcome_html_fallback(user_name)
        else:
            html_content = self._get_welcome_html_fallback(user_name)

        subject = "Welcome to Physical AI Learning Platform!"

        return await self.send_email(to_email, subject, html_content)

    async def send_password_reset_email(
        self, to_email: str, reset_token: str, user_email: str
    ) -> bool:
        """
        Send password reset email with token.

        Args:
            to_email: Recipient email
            reset_token: Password reset token
            user_email: User's email

        Returns:
            bool: True if sent successfully
        """
        reset_url = f"{settings.frontend_url}/reset-password?token={reset_token}"

        if self.template_env:
            try:
                template = self.template_env.get_template("password_reset.html")
                html_content = template.render(reset_url=reset_url, email=user_email)
            except Exception as e:
                logger.warning(f"Failed to render password reset template: {e}")
                html_content = self._get_password_reset_html_fallback(reset_url, user_email)
        else:
            html_content = self._get_password_reset_html_fallback(reset_url, user_email)

        subject = "Reset your password - Physical AI Learning Platform"

        return await self.send_email(to_email, subject, html_content)

    @staticmethod
    def _get_verification_html_fallback(verification_url: str, email: str) -> str:
        """Fallback HTML for verification email when template unavailable."""
        return f"""
        <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h1 style="color: #2563eb;">Verify Your Email</h1>
                <p>Hello,</p>
                <p>Thank you for registering with Physical AI Learning Platform!</p>
                <p>Please verify your email address ({email}) by clicking the link below:</p>
                <p style="margin: 30px 0;">
                    <a href="{verification_url}"
                       style="background-color: #2563eb; color: white; padding: 12px 24px;
                              text-decoration: none; border-radius: 4px; display: inline-block;">
                        Verify Email
                    </a>
                </p>
                <p>Or copy and paste this link into your browser:</p>
                <p style="word-break: break-all; color: #6b7280;">{verification_url}</p>
                <p style="margin-top: 40px; color: #6b7280; font-size: 12px;">
                    This link will expire in 24 hours.<br>
                    If you didn't create an account, please ignore this email.
                </p>
            </body>
        </html>
        """

    @staticmethod
    def _get_welcome_html_fallback(user_name: str) -> str:
        """Fallback HTML for welcome email."""
        return f"""
        <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h1 style="color: #2563eb;">Welcome to Physical AI!</h1>
                <p>Hello {user_name},</p>
                <p>Your email has been verified successfully!</p>
                <p>You're now ready to begin your journey in robotics and AI.</p>
                <p style="margin: 30px 0;">
                    <a href="{settings.frontend_url}/login"
                       style="background-color: #2563eb; color: white; padding: 12px 24px;
                              text-decoration: none; border-radius: 4px; display: inline-block;">
                        Get Started
                    </a>
                </p>
                <p>Happy learning!</p>
            </body>
        </html>
        """

    @staticmethod
    def _get_password_reset_html_fallback(reset_url: str, email: str) -> str:
        """Fallback HTML for password reset email."""
        return f"""
        <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <h1 style="color: #2563eb;">Reset Your Password</h1>
                <p>Hello,</p>
                <p>We received a request to reset the password for {email}.</p>
                <p>Click the link below to reset your password:</p>
                <p style="margin: 30px 0;">
                    <a href="{reset_url}"
                       style="background-color: #2563eb; color: white; padding: 12px 24px;
                              text-decoration: none; border-radius: 4px; display: inline-block;">
                        Reset Password
                    </a>
                </p>
                <p>Or copy and paste this link into your browser:</p>
                <p style="word-break: break-all; color: #6b7280;">{reset_url}</p>
                <p style="margin-top: 40px; color: #6b7280; font-size: 12px;">
                    This link will expire in 1 hour.<br>
                    If you didn't request a password reset, please ignore this email.
                </p>
            </body>
        </html>
        """


# Global email service instance
email_service = EmailService()
