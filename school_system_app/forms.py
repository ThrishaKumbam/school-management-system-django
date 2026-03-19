from django import forms
from .models import Student, Teacher, Subject, Subject, Submission, \
                Assignment, Standard, TeacherStandard
from django.contrib.auth.models import User
from django.db.models import Q

# Forms
class UserForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter first name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter last name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter email'}))
 
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email']
 
class StudentForm(UserForm):
    
    gender = forms.ChoiceField(choices=Student.GENDER_CHOICES, required=False)
    standard = forms.ModelChoiceField(queryset=Standard.objects.all(), empty_label="Select Standard")
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter address', 'rows': 3}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter phone number'}))
 
    class Meta(UserForm.Meta):
        model = Student
        fields = UserForm.Meta.fields + ['standard', 'date_of_birth', 'gender', 'address', 'phone_number']
 
class TeacherForm(UserForm):
 
    gender = forms.ChoiceField(choices=Teacher.GENDER_CHOICES, required=False)
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), empty_label="Select Subject")
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter address', 'rows': 3}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter phone number'}))
 
    class Meta(UserForm.Meta):
        model = Teacher
        fields = UserForm.Meta.fields + ['subject', 'date_of_birth', 'gender', 'address', 'phone_number']
 
class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['standard', 'title', 'description', 'deadline']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }

    def set_teacher_obj(self, teacher_obj):
        teacher_standards = TeacherStandard.objects.filter(teacher=teacher_obj)
        standards = [teacher_standard.standard.pk for teacher_standard in teacher_standards]
        self.fields['standard'].queryset = Standard.objects.filter(pk__in=standards)

class AssignmentUpdateForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'deadline']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }

 
class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['assignment', 'file']    
 
    def __init__(self, student, *args, **kwargs):
        super(SubmissionForm, self).__init__(*args, **kwargs)
       
        student_obj = Student.objects.get(user_id=student)
        assignments = Assignment.objects.filter(standard_id=student_obj.standard).exclude(id__in=Submission.objects.filter(student=student_obj.user).values('assignment'))
        choices = [('', '--Select--')]
        choices.extend([(assignment.id, str(f"{assignment} - ({assignment.teacher.user_teacher.subject.name})")) for assignment in assignments])        
        self.fields['assignment'].choices = choices
 
        self.fields['file'].help_text = 'Only .txt files are accepted'

 
class SubmissionFilterFormForTeacher(forms.Form):
    FIELD_CHOICES = [
        ('', '-- Select Field Name --'),
        ('student_name', 'Student Name'),
        ('assignment_title', 'Assignment Title'),
        ('score', 'Score'),
        ('standard', 'Standard'),
    ]
    FILTER_CHOICES = [
        ('', '-- Select Filtering Option --'),
        ('exact', 'Exact'),
        ('range', 'Between'),
        ('lt', 'Less Than'),
        ('lte', 'Less Than or Equal To'),
        ('gt', 'Greater Than'),
        ('gte', 'Greater Than or Equal To'),
    ]
    field_name = forms.ChoiceField(choices=FIELD_CHOICES)
    filtering_option = forms.ChoiceField(choices=FILTER_CHOICES)
    filter_value = forms.CharField(max_length=255)
 
class SubmissionFilterFormForStudent(forms.Form):
    FIELD_CHOICES = [
        ('', '-- Select Field Name --'),
        ('subject__name', 'Subject Name'),
        ('score', 'Score'),
    ]
    FILTER_CHOICES = [
        ('', '-- Select Filtering Option --'),
        ('exact', 'Exact'),
        ('range', 'Between'),
        ('lt', 'Less Than'),
        ('lte', 'Less Than or Equal To'),
        ('gt', 'Greater Than'),
        ('gte', 'Greater Than or Equal To'),
    ]
    field_name = forms.ChoiceField(choices=FIELD_CHOICES)
    filtering_option = forms.ChoiceField(choices=FILTER_CHOICES)
    filter_value = forms.CharField(max_length=255)
 
class SortingForm(forms.Form):
    FIELD_CHOICES = [
        ('', '-- Select Field Name --'),
        ('id', 'Id'),
        ('score', 'Score'),
    ]
    ORDERING_CHOICE=[
        ('','--select asc or desc'),
        ('+','asc'),
        ('-','desc'),
    ]
    field_name = forms.ChoiceField(choices=FIELD_CHOICES, required=False, widget=forms.Select(attrs={'id': 'id_field_name'}))
    ordering = forms.ChoiceField(choices=ORDERING_CHOICE, required=False, widget=forms.Select(attrs={'id': 'id_ordering'}))
 
class AssignmentsFilterFormForTeacher(forms.Form):
    FIELD_CHOICES = [
        ('', '-- Select Field Name --'),
        ('standard', 'Standard'),
        ('created_at', 'Created at'),
        ('deadline', 'Deadline'),
    ]
    FILTER_CHOICES = [
        ('', '-- Select Filtering Option --'),
        ('exact', 'Exact'),
        ('range', 'Between'),
        ('lt', 'Less Than'),
        ('lte', 'Less Than or Equal To'),
        ('gt', 'Greater Than'),
        ('gte', 'Greater Than or Equal To'),
    ]
    field_name = forms.ChoiceField(choices=FIELD_CHOICES)
    filtering_option = forms.ChoiceField(choices=FILTER_CHOICES)
    filter_value = forms.CharField(max_length=255)
 
class SortingFormForAssignments(forms.Form):
    FIELD_CHOICES = [
        ('', '-- Select Field Name --'),
        ('id', 'Id'),
        ('standard', 'Standard'),
    ]
    ORDERING_CHOICE=[
        ('','--select asc or desc'),
        ('+','asc'),
        ('-','desc'),
    ]
    field_name = forms.ChoiceField(choices=FIELD_CHOICES, required=False, widget=forms.Select(attrs={'id': 'id_field_name'}))
    ordering = forms.ChoiceField(choices=ORDERING_CHOICE, required=False, widget=forms.Select(attrs={'id': 'id_ordering'}))
 
class AdminFormForTeachers(forms.ModelForm):
    class Meta:
        model = TeacherStandard
        fields = ['teacher', 'standard']
 
    teacher = forms.ModelChoiceField(queryset=User.objects.filter(
        Q(id__in=Teacher.objects.values('user_id')) | Q(pk__in=Teacher.objects.values('user_id'))
    ))
    standard = forms.ModelChoiceField(queryset=Standard.objects.all())

class UForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter first name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter last name'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter email'}))
 
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']    

class SForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('', 'Select gender'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
 
    gender = forms.ChoiceField(choices=Student.GENDER_CHOICES, required=False)
    standard = forms.ModelChoiceField(queryset=Standard.objects.all(), empty_label="Select Standard")
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter address', 'rows': 3}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter phone number'}))
 
    class Meta(UserForm.Meta):
        model = Student
        fields = ['standard', 'date_of_birth', 'gender', 'address', 'phone_number']
 

class TForm(forms.ModelForm):
 
    gender = forms.ChoiceField(choices=Teacher.GENDER_CHOICES, required=False)
    subject = forms.ModelChoiceField(queryset=Subject.objects.all())
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter address', 'rows': 3}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter phone number'}))
 
    class Meta(UserForm.Meta):
        model = Teacher
        fields = ['subject', 'date_of_birth', 'gender', 'address', 'phone_number']

class FilteringStudentsFormForAdmin(forms.Form):
    FIELD_CHOICES = [
        ('', '-- Select Field Name --'),
        ('standard', 'Standard'),
        ('user__is_active', 'Status'),
    ]
    FILTER_CHOICES = [
        ('', '-- Select Filtering Option --'),
        ('exact', 'Exact'),
        ('range', 'Between'),
        ('lt', 'Less Than'),
        ('lte', 'Less Than or Equal To'),
        ('gt', 'Greater Than'),
        ('gte', 'Greater Than or Equal To'),
    ]
    field_name = forms.ChoiceField(choices=FIELD_CHOICES)
    filtering_option = forms.ChoiceField(choices=FILTER_CHOICES)
    filter_value = forms.CharField(max_length=255)

class FilteringTeachersFormForAdmin(forms.Form):
    FIELD_CHOICES = [
        ('', '-- Select Field Name --'),
        ('subject__name', 'Subject'),
        ('user__is_active', 'Status'),
    ]
    FILTER_CHOICES = [
        ('', '-- Select Filtering Option --'),
        ('exact', 'Exact'),
        
    ]
    field_name = forms.ChoiceField(choices=FIELD_CHOICES)
    filtering_option = forms.ChoiceField(choices=FILTER_CHOICES)
    filter_value = forms.CharField(max_length=255)
