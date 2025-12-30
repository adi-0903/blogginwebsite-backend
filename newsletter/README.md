# Newsletter Subscription Feature

## Overview

The newsletter subscription feature allows users to subscribe to Mind Matrix's newsletter through the footer. Subscribers automatically receive:

1. **Welcome Email** - A beautiful HTML email with:
   - Welcome message
   - 24-day free trial activation
   - List of premium features included in the trial
   - Upgrade button linking to pricing page
   - Getting started guide

2. **Trial Tracking** - The system tracks:
   - Subscription date
   - Trial expiration date (24 days from subscription)
   - Trial status (active/expired)
   - Upgrade status

## Backend Setup

### 1. Database Migration

Run these commands to create the newsletter tables:

```bash
cd server
python manage.py makemigrations newsletter
python manage.py migrate
```

### 2. Email Configuration

Configure email in your `.env` file. Choose one of the following:

#### Option A: Gmail (Recommended for testing)
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@mindmatrix.com
```

**Note**: For Gmail, you need to:
1. Enable 2-Factor Authentication
2. Create an [App Password](https://support.google.com/accounts/answer/185833)
3. Use the app password instead of your regular password

#### Option B: SendGrid
```
EMAIL_BACKEND=sendgrid_backend.SendgridBackend
SENDGRID_API_KEY=your-sendgrid-api-key
DEFAULT_FROM_EMAIL=noreply@mindmatrix.com
```

#### Option C: Mailgun
```
EMAIL_BACKEND=django_mailgun.MailgunBackend
MAILGUN_ACCESS_KEY=your-mailgun-api-key
MAILGUN_SERVER_NAME=your-domain.mailgun.org
DEFAULT_FROM_EMAIL=noreply@mindmatrix.com
```

#### Option D: Development (Console - prints to terminal)
```
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=noreply@mindmatrix.com
```

### 3. Frontend URL Configuration

```
FRONTEND_URL=http://localhost:5173
```

This is used in the email upgrade button link.

### 4. Install Email Packages (if needed)

For SendGrid:
```bash
pip install sendgrid-django
```

For Mailgun:
```bash
pip install django-mailgun
```

### 5. API Endpoints

**Subscribe to Newsletter:**
- **URL**: `POST /api/newsletter/subscribe/`
- **Method**: POST
- **Auth**: Not required
- **Body**:
```json
{
  "email": "user@example.com"
}
```

**Response** (Success):
```json
{
  "message": "Successfully subscribed to newsletter",
  "subscriber": {
    "id": 1,
    "email": "user@example.com",
    "subscribed_at": "2025-12-25T10:30:00Z",
    "is_active": true,
    "trial_expires_at": "2026-01-18T10:30:00Z",
    "has_upgraded": false
  }
}
```

## Frontend Implementation

The newsletter subscription form is integrated in the Footer component and includes:

1. **Email Input** - Accepts user email address
2. **Subscribe Button** - Submits the form
3. **Success/Error Messages** - Provides user feedback
4. **Loading State** - Shows "Subscribing..." during submission

### Usage

The form automatically connects to the backend API:
- Sends POST request to `http://localhost:8000/api/newsletter/subscribe/`
- Handles success and error responses
- Displays appropriate messages to users

## Admin Interface

Access the Django admin panel to manage subscribers:

1. Navigate to `http://localhost:8000/admin/`
2. Go to "Newsletter" section
3. View all subscribers with:
   - Email address
   - Subscription date
   - Active status
   - Trial status
   - Upgrade status

## Email Template Customization

Edit the email template in `server/newsletter/views.py` in the `send_welcome_email()` method to customize:

- Subject line
- Email content
- Trial days duration
- Feature list
- Upgrade link
- Footer text

## Testing

### Test with Console Backend (Development)

1. Set `EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend` in .env
2. Subscribe using the frontend form
3. Check the Django server terminal output - the email content will be printed there

### Test with Gmail

1. Configure Gmail SMTP settings in .env
2. Use an App Password (not your regular password)
3. Subscribe and check the email inbox

## Database Schema

### NewsletterSubscriber Model

| Field | Type | Description |
|-------|------|-------------|
| id | BigAutoField | Primary key |
| email | EmailField | Unique email address |
| subscribed_at | DateTimeField | Subscription timestamp |
| is_active | BooleanField | Whether subscription is active |
| trial_expires_at | DateTimeField | When the 24-day trial expires |
| has_upgraded | BooleanField | Whether user has upgraded to paid plan |

## Features

- **Automatic Trial Setup**: 24-day trial automatically set on subscription
- **Beautiful Email**: HTML-formatted welcome email with gradient styling
- **Responsive Design**: Email looks good on all devices
- **Error Handling**: Graceful error messages for duplicate emails and failures
- **Admin Management**: Full admin interface for managing subscribers
- **Tracking**: Built-in fields to track trial and upgrade status

## Future Enhancements

Potential features to add:

1. Email Verification - Verify email before subscription
2. Unsubscribe Link - Allow users to unsubscribe from emails
3. Email Campaigns - Send periodic emails to active subscribers
4. Upgrade Notifications - Email users before trial expires
5. Analytics - Track email open rates and click rates
6. A/B Testing - Test different email templates
7. Drip Campaigns - Automated email sequences

## Support

For issues or questions about the newsletter feature, please refer to the backend logs or Django admin panel.
