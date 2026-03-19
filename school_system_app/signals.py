from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.conf import settings
from .models import Teacher, Student, Assignment
from django.contrib.auth.models import User
from django.dispatch import receiver
 
# Signals
@receiver(post_save, sender=Teacher)
def teacher_register(sender, instance, created, **kwargs):
    if created:
        teacher_subject = 'Teacher Registration Successful'
        teacher_message = f'Hello {instance.user.first_name} {instance.user.last_name},\n\nThank you for registering!\n\nFrom: OSI Digital International School'
 
        principal_obj = User.objects.filter(is_superuser=True).first()
 
        principal_subject = 'New Teacher Registered'
        principal_message = f'Hello {principal_obj.first_name} {principal_obj.last_name},\n\nAssign a standard/standards to {instance.user.first_name} {instance.user.last_name}.\n\nFrom: OSI Digital International School'
 
        send_mail(teacher_subject, teacher_message, settings.EMAIL_HOST_USER, [instance.user.email])
        send_mail(principal_subject, principal_message, settings.EMAIL_HOST_USER, [principal_obj.email])

@receiver(post_save, sender=Student)
def student_register(sender, instance, created, **kwargs):
    if created:
        subject = 'Student Registration Successful'
        message = f'Hello {instance.user.username},\n\nThank you for registering!\n\nFrom: OSI Digital International School'
        from_email = settings.EMAIL_HOST_USER
        to_email = [instance.user.email]
        send_mail(subject, message, from_email, to_email)

# @receiver(post_save, sender=Assignment)
# def create_assignm(sender, instance, created, **kwargs):
#     if created:
#         students = Student.objects.filter(standard = instance.standard.id)
#         subject = 'New assignment added'
#         message = f'Hello Student,\n\nA new assignment is given by {instance.teacher.username}.\nDeadline: {instance.deadline}.\nFor more details reachout to the website.\n\nFrom: OSI Digital International School'
#         from_email = settings.EMAIL_HOST_USER
#         for student in students:
#             to_email = [student.user.email]
#             send_mail(subject, message, from_email, to_email)