# users/email_utils.py
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


def send_registration_email(user, request):
    """
    Send an account activation email to newly registered users
    """
    # Generate activation token
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    # Build activation URL
    activation_url = request.build_absolute_uri(
        f'/activate/{uid}/{token}/'
    )

    subject = '🚀 Activate your Gold Cinema Account'
    
    # HTML email content
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: 'Segoe UI', Arial, sans-serif;
                background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
                margin: 0;
                padding: 20px;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
                overflow: hidden;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            }}
            .header {{
                background: linear-gradient(135deg, #ffd700, #ffed4e);
                padding: 40px 20px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                color: #1a1a2e;
                font-size: 32px;
            }}
            .content {{
                padding: 40px 30px;
                color: #333;
                text-align: center;
            }}
            .welcome-text {{
                font-size: 18px;
                line-height: 1.6;
                margin-bottom: 20px;
            }}
            .highlight {{
                color: #ffd700;
                font-weight: bold;
            }}
            .cta-button {{
                display: inline-block;
                background: linear-gradient(135deg, #4caf50, #45a049);
                color: white;
                padding: 15px 40px;
                text-decoration: none;
                border-radius: 30px;
                font-weight: bold;
                margin: 20px 0;
                box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
                font-size: 18px;
            }}
            .footer {{
                background: #1a1a2e;
                color: #fff;
                padding: 20px;
                text-align: center;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎬 Gold Cinema</h1>
            </div>
            <div class="content">
                <p class="welcome-text">
                    Hi <span class="highlight">{user.first_name or user.username}</span>,
                </p>
                <p class="welcome-text">
                    Almost there! To complete your registration, please verify your email address.
                </p>
                
                <a href="{activation_url}" class="cta-button">
                    Confirm Email Address
                </a>
                
                <p style="margin-top: 30px; color: #666; font-size: 14px;">
                    Or copy and paste this link into your browser:<br>
                    <a href="{activation_url}" style="color: #ffd700; word-break: break-all;">{activation_url}</a>
                </p>
                
                <p style="margin-top: 20px; color: #999; font-size: 13px;">
                    This link will expire in 24 hours. If you didn't sign up for Gold Cinema, you can safely ignore this email.
                </p>
            </div>
            <div class="footer">
                <p>© 2025 Gold Cinema. All Rights Reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Plain text version
    plain_message = f"""
    Hi {user.first_name or user.username},
    
    Almost there! To complete your registration, please verify your email address by clicking the link below:
    
    {activation_url}
    
    This link will expire in 24 hours.
    
    © 2025 Gold Cinema. All Rights Reserved.
    """
    
    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        email.attach_alternative(html_message, "text/html")
        email.send(fail_silently=False)
        return True
    except Exception as e:
        print(f"Error sending activation email: {e}")
        return False


def send_password_reset_email(user, request):
    """
    Send password reset email with token
    """
    # Generate password reset token
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    # Build reset URL
    reset_url = request.build_absolute_uri(
        f'/reset-password/{uid}/{token}/'
    )
    
    subject = '🔐 Password Reset Request - Gold Cinema'
    
    # HTML email content
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: 'Segoe UI', Arial, sans-serif;
                background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
                margin: 0;
                padding: 20px;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
                overflow: hidden;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            }}
            .header {{
                background: linear-gradient(135deg, #ff4d4d, #ff6b6b);
                padding: 40px 20px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                color: #fff;
                font-size: 32px;
            }}
            .content {{
                padding: 40px 30px;
                color: #333;
            }}
            .warning-box {{
                background: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 15px;
                margin: 20px 0;
                border-radius: 5px;
            }}
            .reset-button {{
                display: inline-block;
                background: linear-gradient(135deg, #ffd700, #ffed4e);
                color: #1a1a2e;
                padding: 15px 40px;
                text-decoration: none;
                border-radius: 30px;
                font-weight: bold;
                margin: 20px 0;
                box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
            }}
            .footer {{
                background: #1a1a2e;
                color: #fff;
                padding: 20px;
                text-align: center;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔐 Password Reset</h1>
            </div>
            <div class="content">
                <p>Hi <strong>{user.first_name or user.username}</strong>,</p>
                
                <p>
                    We received a request to reset your password for your Gold Cinema account.
                </p>
                
                <div class="warning-box">
                    <strong>⚠️ Important:</strong> If you didn't request this password reset, please ignore this email. 
                    Your password will remain unchanged.
                </div>
                
                <p>To reset your password, click the button below:</p>
                
                <p style="text-align: center;">
                    <a href="{reset_url}" class="reset-button">
                        Reset My Password
                    </a>
                </p>
                
                <p style="color: #666; font-size: 14px;">
                    Or copy and paste this link into your browser:<br>
                    <a href="{reset_url}" style="color: #ffd700; word-break: break-all;">{reset_url}</a>
                </p>
                
                <p style="margin-top: 30px; color: #666; font-size: 14px;">
                    <strong>This link will expire in 24 hours</strong> for security reasons.
                </p>
                
                <p style="color: #666; font-size: 14px;">
                    If you need help, contact us at 
                    <a href="mailto:info@goldcinema.com" style="color: #ffd700;">info@goldcinema.com</a>
                </p>
            </div>
            <div class="footer">
                <p>© 2025 Gold Cinema. All Rights Reserved.</p>
                <p>This is an automated email. Please do not reply.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Plain text version
    plain_message = f"""
    Hi {user.first_name or user.username},
    
    We received a request to reset your password for your Gold Cinema account.
    
    ⚠️ IMPORTANT: If you didn't request this password reset, please ignore this email.
    
    To reset your password, visit this link:
    {reset_url}
    
    This link will expire in 24 hours for security reasons.
    
    If you need help, contact us at info@goldcinema.com
    
    © 2025 Gold Cinema. All Rights Reserved.
    """
    
    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        email.attach_alternative(html_message, "text/html")
        email.send(fail_silently=False)
        return True
    except Exception as e:
        print(f"Error sending password reset email: {e}")
        return False


def send_booking_confirmation_email(user, booking):
    """
    Send booking confirmation email
    """
    subject = f'🎟️ Booking Confirmed: {booking.movie_name}'
    
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f4f4f4; padding: 20px; }}
            .container {{ max-width: 600px; margin: 0 auto; background: #fff; border-radius: 10px; overflow: hidden; box-shadow: 0 0 20px rgba(0,0,0,0.1); }}
            .header {{ background: #ffd700; padding: 30px; text-align: center; }}
            .content {{ padding: 30px; }}
            .ticket-info {{ background: #f9f9f9; padding: 20px; border-left: 4px solid #ffd700; margin: 20px 0; }}
            .footer {{ background: #333; color: #fff; padding: 20px; text-align: center; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Booking Confirmed! ✅</h1>
            </div>
            <div class="content">
                <p>Hi {user.first_name or user.username},</p>
                <p>Your ticket for <strong>{booking.movie_name}</strong> has been successfully booked.</p>
                
                <div class="ticket-info">
                    <p><strong>Ticket ID:</strong> {booking.ticket_number}</p>
                    <p><strong>Date:</strong> {booking.date}</p>
                    <p><strong>Time:</strong> {booking.time}</p>
                    <p><strong>Seats:</strong> {booking.seats}</p>
                </div>
                
                <p>You can download your ticket from your dashboard.</p>
            </div>
            <div class="footer">
                <p>© 2025 Gold Cinema. All Rights Reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    try:
        email = EmailMultiAlternatives(subject, "Booking Confirmed", settings.DEFAULT_FROM_EMAIL, [user.email])
        email.attach_alternative(html_message, "text/html")
        email.send(fail_silently=False)
        return True
    except Exception as e:
        print(f"Error sending booking email: {e}")
        return False


def send_booking_cancellation_email(user, booking):
    """
    Send booking cancellation email
    """
    subject = f'❌ Booking Cancelled: {booking.movie_name}'
    
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f4f4f4; padding: 20px; }}
            .container {{ max-width: 600px; margin: 0 auto; background: #fff; border-radius: 10px; overflow: hidden; }}
            .header {{ background: #ff4d4d; padding: 30px; text-align: center; color: white; }}
            .content {{ padding: 30px; }}
            .refund-info {{ background: #fff3cd; padding: 15px; border-radius: 5px; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Booking Cancelled</h1>
            </div>
            <div class="content">
                <p>Hi {user.first_name or user.username},</p>
                <p>Your booking for <strong>{booking.movie_name}</strong> has been cancelled as requested.</p>
                
                <div class="refund-info">
                    <strong>💰 Refund Status:</strong><br>
                    The amount has been refunded to your Gold Cinema account balance.
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    try:
        email = EmailMultiAlternatives(subject, "Booking Cancelled", settings.DEFAULT_FROM_EMAIL, [user.email])
        email.attach_alternative(html_message, "text/html")
        email.send(fail_silently=False)
        return True
    except Exception as e:
        print(f"Error sending cancellation email: {e}")
        return False


def send_account_deletion_email(user):
    """
    Send account deletion confirmation email
    """
    subject = '👋 Account Deleted - Gold Cinema'
    
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f4f4f4; padding: 20px; }}
            .container {{ max-width: 600px; margin: 0 auto; background: #fff; border-radius: 10px; overflow: hidden; }}
            .header {{ background: #333; padding: 30px; text-align: center; color: white; }}
            .content {{ padding: 30px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Account Deleted</h1>
            </div>
            <div class="content">
                <p>Hi {user.first_name or user.username},</p>
                <p>Your Gold Cinema account has been successfully deleted.</p>
                <p>We're sorry to see you go! If you change your mind, you can always create a new account.</p>
                <p>Thank you for being part of our community.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    try:
        email = EmailMultiAlternatives(subject, "Account Deleted", settings.DEFAULT_FROM_EMAIL, [user.email])
        email.attach_alternative(html_message, "text/html")
        email.send(fail_silently=False)
        return True
    except Exception as e:
        print(f"Error sending deletion email: {e}")
        return False
