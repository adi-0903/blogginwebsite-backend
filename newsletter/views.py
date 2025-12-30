from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags

from .models import NewsletterSubscriber
from .serializers import NewsletterSubscribeSerializer, NewsletterSubscriberSerializer


class NewsletterSubscribeView(APIView):
    """Subscribe to newsletter"""
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = NewsletterSubscribeSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            # Check if already subscribed
            subscriber, created = NewsletterSubscriber.objects.get_or_create(
                email=email,
                defaults={'is_active': True}
            )
            
            if not created and subscriber.is_active:
                return Response(
                    {'message': 'This email is already subscribed'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Reactivate if was inactive
            if not subscriber.is_active:
                subscriber.is_active = True
                subscriber.save()
            
            # Set 24-day trial period
            subscriber.set_trial_period(24)
            
            # Send welcome email
            self.send_welcome_email(email)
            
            return Response(
                {
                    'message': 'Successfully subscribed to newsletter',
                    'subscriber': NewsletterSubscriberSerializer(subscriber).data
                },
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def send_welcome_email(self, email):
        """Send welcome email with trial info and upgrade button"""
        
        subject = '🎉 Welcome to Mind Matrix - Your 24-Day Free Trial Starts Now!'
        
        context = {
            'email': email,
            'trial_days': 24,
            'upgrade_url': f"{settings.FRONTEND_URL}/pricing",
            'app_name': 'Mind Matrix',
        }
        
        try:
            # Prepare HTML email
            html_message = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; background: #f9f9f9; border-radius: 10px; }}
                    .header {{ background: linear-gradient(135deg, #63ddbe 0%, #4cafd7 100%); color: white; padding: 30px 20px; border-radius: 10px 10px 0 0; text-align: center; }}
                    .header h1 {{ margin: 0; font-size: 28px; }}
                    .content {{ background: white; padding: 30px 20px; }}
                    .trial-badge {{ background: linear-gradient(135deg, #ffb147 0%, #ff5722 100%); color: white; padding: 15px; border-radius: 8px; text-align: center; margin: 20px 0; font-weight: bold; font-size: 18px; }}
                    .feature-list {{ margin: 20px 0; }}
                    .feature-list li {{ margin: 10px 0; padding-left: 25px; position: relative; }}
                    .feature-list li:before {{ content: "✓"; position: absolute; left: 0; color: #63ddbe; font-weight: bold; }}
                    .cta-button {{ display: inline-block; background: linear-gradient(135deg, #ffb147 0%, #ff5722 100%); color: white; padding: 15px 40px; border-radius: 8px; text-decoration: none; font-weight: bold; margin: 20px 0; text-align: center; }}
                    .footer {{ background: #f0f0f0; padding: 20px; text-align: center; font-size: 12px; color: #666; border-radius: 0 0 10px 10px; }}
                    .divider {{ height: 1px; background: #e0e0e0; margin: 20px 0; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>✦ Mind Matrix</h1>
                        <p>Stories that feel alive</p>
                    </div>
                    
                    <div class="content">
                        <h2 style="color: #333;">Welcome to Mind Matrix! 🎉</h2>
                        
                        <p>Hi there,</p>
                        
                        <p>Thank you for joining our creative community! We're thrilled to have you on board.</p>
                        
                        <div class="trial-badge">
                            🎁 {context['trial_days']}-Day Free Trial Active
                        </div>
                        
                        <p>Your free trial has been activated and you now have full access to all premium features:</p>
                        
                        <ul class="feature-list">
                            <li>Create unlimited journals and stories</li>
                            <li>Organize content with custom series</li>
                            <li>Access to our writer's toolkit</li>
                            <li>Motion and animation features</li>
                            <li>Community access and events</li>
                            <li>24-hour priority support</li>
                        </ul>
                        
                        <p><strong>Your trial expires in {context['trial_days']} days.</strong> After that, you can upgrade to continue enjoying Mind Matrix.</p>
                        
                        <div style="text-align: center;">
                            <a href="{context['upgrade_url']}" class="cta-button">Explore Upgrade Options</a>
                        </div>
                        
                        <div class="divider"></div>
                        
                        <h3>Get Started:</h3>
                        <ol>
                            <li>Log in to your Mind Matrix account</li>
                            <li>Start creating your first journal or story</li>
                            <li>Explore the toolkit and community features</li>
                            <li>Share your creations with our writing community</li>
                        </ol>
                        
                        <div class="divider"></div>
                        
                        <p><strong>Questions?</strong> Reply to this email or visit our help center. We're here to help you make the most of your creative journey.</p>
                        
                        <p>Happy writing! ✨</p>
                        
                        <p>The Mind Matrix Team</p>
                    </div>
                    
                    <div class="footer">
                        <p>© 2025 Mind Matrix. All rights reserved.</p>
                        <p>You received this email because you subscribed to the Mind Matrix newsletter.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Send email
            send_mail(
                subject=subject,
                message=strip_tags(html_message),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                html_message=html_message,
                fail_silently=False,
            )
            
            print(f"Welcome email sent to {email}")
            
        except Exception as e:
            print(f"Error sending email to {email}: {str(e)}")
