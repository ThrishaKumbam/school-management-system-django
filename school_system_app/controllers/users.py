"""
users related views
"""
from django.shortcuts import render, redirect
from school_system_app.models import Student, Teacher, User
from school_system_app import utils
from django.contrib.auth import authenticate

# views
def user_login(request, data):
    """View function for handling user login."""
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user_obj = User.objects.get(username=username)
            if user_obj and user_obj.is_active == False:
                data = f'{user_obj.first_name} {user_obj.last_name} is in inactivate state'
                return utils.error_message(request, data, url_name='user_login')            
        except User.DoesNotExist:
            data = f'Invalid Username'
            return utils.error_message(request, data, url_name='user_login')
        
        user = authenticate(request, username=username, password=password)
        if user:
            access_token = utils.generate_tokens(user)
            teacher = Teacher.objects.filter(user__id=user.id).first()
            student = Student.objects.filter(user__id=user.id).first()
            if teacher :
                response = redirect('assignment_creation')
            elif student:
                response = redirect('assignment_submission')
            else:
                # response = redirect('/admin/')
                response = redirect('admin_page')
            response.set_cookie('auth_token', access_token, httponly=True)
            return response
        else:
            data = "Invalid Password."
            return utils.error_message(request, data, url_name='user_login')
    return render(request, "login.html", {'data': data})

def my_profile(request, session_user, data):
    """View function for viewing user profile."""
    teacher_obj = None
    student_obj = None
    admin_obj = None
    try:
        teacher_obj = Teacher.objects.get(user__id=session_user.id)
    except Teacher.DoesNotExist:
        try:
            student_obj = Student.objects.get(user__id = session_user.id)
        except Student.DoesNotExist:
            try:
                admin_obj = User.objects.get(id = session_user.id, is_superuser=True)
            except:
                return redirect('permission_denied')
    
    teacher_1 = None
    teacher_2 = None
    student_1 = None
    student_2 = None
    admin_1 =None
    if teacher_obj:
        teacher_1 = User.objects.get(id=session_user.id)
        teacher_2 = Teacher.objects.get(user=session_user.id)
    elif student_obj:
        student_1 = User.objects.get(id=session_user.id)
        student_2 = Student.objects.get(user=session_user.id)
    elif admin_obj:
        admin_1 = User.objects.get(id = session_user.id)
    
    context = {
        "teacher_1":teacher_1,
        "teacher_2":teacher_2,
        "student_1":student_1,
        "student_2":student_2,
        "admin_1":admin_1,
        'teacher_obj': teacher_obj,
        'student_obj': student_obj,
        "admin_obj":admin_obj,
        'data': data
    }

    return render(request, 'profiles.html', context)