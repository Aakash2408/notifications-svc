"""User service module for notifications-svc."""

from dataclasses import dataclass
from typing import Optional

from .email_client import send_email
from .sms_client import send_sms

@dataclass
class User:
    id: str
    name: str
    email: str
    preferences: Optional[dict] = None

def send_welcome_notification(user: User) -> dict:
    """Send welcome notification to a new user via email and SMS."""
    results = {}

    # Send welcome email
    results["email"] = send_email(
        to=user.email,
        subject="Welcome to the platform!",
        body=f"Hi {user.name}, welcome aboard! Your account is ready.",
    )

    # Send welcome SMS using phone number
    results["sms"] = send_sms(
        to=user.phone_number,
        message=f"Welcome {user.name}! Your account is now active. Reply HELP for support.",
    )

    return results

def create_user_profile(
    user_id: str,
    name: str,
    email: str,
    preferences: Optional[dict] = None,
) -> User:
    """Create a new user profile with contact details."""
    user = User(
        id=user_id,
        name=name,
        email=email,
        preferences=preferences or {},
    )

    # Send welcome notification on profile creation
    send_welcome_notification(user)

    return user

def notify_user(user: User, message: str, channels: list[str] = None) -> dict:
    """Send a notification to user on specified channels."""
    channels = channels or ["email", "sms"]
    results = {}

    if "email" in channels:
        results["email"] = send_email(
            to=user.email,
            subject="New Notification",
            body=message,
        )

    if "sms" in channels:
        results["sms"] = send_sms(
            to=user.phone_number,
            message=message,
        )

    return results
