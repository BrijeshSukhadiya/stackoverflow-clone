from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Answer

@receiver(post_save, sender=Answer)
def notify_question_author_on_answer(sender, instance, created, **kwargs):
    if created:
        question = instance.question
        author_email = question.author.email
        if author_email:
            send_mail(
                subject='New Answer to Your Question',
                message=f'Hi {question.author.username},\n\n'
                        f'Your question "{question.title}" just got a new answer:\n\n'
                        f'"{instance.body}"\n\n'
                        f'Visit the site to view it.',
                from_email=None,
                recipient_list=[author_email],
                fail_silently=True
            )
