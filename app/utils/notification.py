import requests
import os
from django.core.mail import send_mail
from django.utils import timezone
from app.models.notification import MessageLog


def get_token():
    login_url = "https://notify.eskiz.uz/api/auth/login"
    login_payload = {
        "email":os.getenv("ESKIZ_USER_EMAIL"),
        'password': os.getenv('ESKIZ_USER_PASSWoRD')
    }
    login_response = requests.post(login_url, json=login_payload)
    login_data = login_response.json()
    token = login_data.get('data', {}).get('token')
    
    return token


def send_sms(recipient, message):
    one_day_ago = timezone.now() - timezone.timedelta(days=1)
    sms_count = MessageLog.objects.filter(
        recipient=recipient,
        message_type=MessageLog.SMS,
        sent_at__gte=one_day_ago
    ).count()

    if sms_count >= 5:
        print("SMS limit reached for today.")
        return
    
    token=get_token()
    sms_url = "https://notify.eskiz.uz/api/message/sms/send"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    from_sms = '4546'
    sms_payload = {
        'mobile_phone': recipient,
        'message': message,
        'from': from_sms
    }
    
    try:
        sms_response = requests.post(sms_url, headers=headers, json=sms_payload)
        sms_response.raise_for_status() 
        sms_data = sms_response.json()
        return MessageLog.objects.create(
                    send_by=from_sms,
                    recipient=recipient,
                    message_type=MessageLog.SMS,
                    content=message
                )
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while sending SMS: {e}")


def send_email(self, recipient, message, subject):
    one_day_ago = timezone.now() - timezone.timedelta(days=1)
    email_count = MessageLog.objects.filter(
        recipient=recipient,
        message_type=MessageLog.EMAIL,
        sent_at__gte=one_day_ago
    ).count()

    if email_count >= 5:
        raise Exception("Email limit reached for today.")

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=os.getenv('EMAIL_HOST_USER'),
            recipient_list=[recipient],
            fail_silently=False
        )
        MessageLog.objects.create(
            send_by=os.getenv('EMAIL_HOST_USER'),
            recipient=recipient,
            message_type=MessageLog.EMAIL,
            content=message
        )
    except Exception as e:
        raise Exception(f"An error occurred while sending the email: {e}")