from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    delated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        if self.pk is not None:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def delete(self):
        self.delated_at = timezone.now()
        super().save()

class Standard(BaseModel):
    standard = models.IntegerField()  

    class Meta:
        db_table = "standard"  
 
    def __str__(self):
        return str(self.standard)


class Student(BaseModel):
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE, null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_student')
    date_of_birth = models.DateField(null=True)
    GENDER_CHOICES = (
        ('', 'Select gender'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    address = models.TextField(null=True)
    phone_number_validator = RegexValidator(
        regex=r'^[0-9]{10}$',
        message='Phone number must be exactly 10 digits.',
        code='invalid_phone_number'
    )

    phone_number = models.CharField(
        max_length=20,
        null=True,
        validators=[phone_number_validator]
    )

    class Meta:
        db_table = "student"

    def __str__(self):
        return self.user.username
    
class Subject(BaseModel):
    name = models.CharField(max_length=150, unique=True)
    
    class Meta:
        db_table = "subject"

    def __str__(self):
        return self.name
    
class Teacher(BaseModel):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=False)
    date_of_birth = models.DateField(null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_teacher')
    GENDER_CHOICES = (
        ('', 'Select gender'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    address = models.TextField(null=True)
    phone_number_validator = RegexValidator(
        regex=r'^[0-9]{10}$',
        message='Phone number must be exactly 10 digits and non-aphabetic.',
        code='invalid_phone_number'
    )

    phone_number = models.CharField(
        max_length=20,
        null=True,
        validators=[phone_number_validator]
    )
    
    class Meta:
        db_table = "teacher"

    def __str__(self):
        return self.user.username

class StandardSubject(BaseModel):
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE, null=False)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=False)
    
    class Meta:
        db_table = "standard_subject"

    def __str__(self):
        return str(self.standard.standard) + '__' + self.subject.name
    
class TeacherStandard(BaseModel):
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = "teacherstandard"

    def __str__(self):
        return self.teacher.username + '__standard-' + str(self.standard.standard)
    
class Assignment(BaseModel):
    title = models.CharField(max_length=150)
    description = models.TextField(null=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    deadline = models.DateField(null=False)
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "assignment"

    def __str__(self):
        return self.title
    
class Submission(BaseModel):
    student = models.ForeignKey(User, on_delete = models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete = models.CASCADE)
    file = models.FileField(upload_to='file_uploads/', validators=[FileExtensionValidator(allowed_extensions=['txt'])])
    score = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    
    class Meta:
        db_table = "submission"

    def __str__(self):
        return self.student.username+ '_' +self.assignment.title
