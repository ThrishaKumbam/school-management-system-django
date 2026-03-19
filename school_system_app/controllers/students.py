"""
student related views
""" 
from django.shortcuts import render, redirect, get_object_or_404
from school_system_app.forms import StudentForm, SubmissionForm, SortingForm, \
    SubmissionFilterFormForStudent
from school_system_app.models import Student, Assignment, Submission, User
from django.utils import timezone
from school_system_app import utils
from django.db.models import Q
 
 
def student_registration(request, data):
    """View function for handling student registration."""
    if request.method == 'POST':
        student_form = StudentForm(request.POST)
        if student_form.is_valid():
            if User.objects.filter(username = request.POST.get("username")).exists():
                data = "Username already exists."
                return utils.error_message(request, data, url_name='student_registration')
               
            user = User.objects.create_user(
                username=student_form.cleaned_data['username'],
                password=student_form.cleaned_data['password'],
                email=student_form.cleaned_data['email'],
                first_name=student_form.cleaned_data['first_name'],
                last_name=student_form.cleaned_data['last_name']
            )
 
            student = student_form.save(commit=False)
            student.user = user
            student.save()
            data = f"{student.user.username} registered successfully."
            return utils.success_message(request, data, url_name='user_login')
       
        else:
            data = list(student_form.errors.as_data().values())[0][0].message
            return utils.error_message(request, data, url_name='student_registration')
           
    else:
        form = StudentForm()
 
    return render(request, "student_register.html", {'form': form, 'data': data})

 
def assignment_submission(request, data, session_user):
    """View function for handling assignment submission."""
    student_obj = None
    admin_obj = None
    try:
        student_obj = Student.objects.get(user__id=session_user.id)
    except Student.DoesNotExist:
        try:
            admin_obj = User.objects.get(id=session_user.id, is_staff=True)
        except User.DoesNotExist:
            return redirect('permission_denied')
 
    if student_obj:
        if request.method == 'POST':
            form = SubmissionForm(session_user, request.POST, request.FILES)
            if request.FILES['file'].content_type != 'text/plain':
                data = "Only .txt files are supported"
                return utils.error_message(request, data, url_name='assignment_submission')
           
            if data == None:
                if form.is_valid():
                    assignment = Assignment.objects.get(pk =request.POST.get("assignment"))
                    if assignment.deadline < timezone.now().date():
                        data = "Deadline date has already passed."
                        return utils.error_message(request, data, url_name='assignment_submission')
                       
                    submission = form.save(commit=False)
                    submission.student_id = session_user.id
                    submission.save()
                    data = "Assignment Submitted Successfully"
                    return utils.success_message(request, data, url_name='assignment_submission')
                   
                else:
                    data = list(form.errors.as_data().values())[0][0].message
                    return utils.error_message(request, data, url_name='assignment_submission')
       
        else:
            form = SubmissionForm(session_user)
    elif admin_obj:
        return redirect('view_submits')
 
    return render(request, 'submission.html', {'form': form, "student_obj":student_obj, "data":data})

 
def view_submits(request, data, session_user):
    """View function for displaying submitted assignments."""
    student_obj = None
    admin_obj = None
    try:
        student_obj = Student.objects.get(user__id=session_user.id)
    except Student.DoesNotExist:
        try:
            admin_obj = User.objects.get(id=session_user.id, is_staff=True)
        except User.DoesNotExist:
            return redirect('permission_denied')
 
    if student_obj:
        submissions = Submission.objects.filter(student_id = session_user.id)
        student_obj = Student.objects.get(user__id=session_user.id)
    elif admin_obj:
        submissions = Submission.objects.all()
 
    search_value = request.GET.get('query')
    if search_value=="":
        submissions = submissions.all()
    if search_value:
        submissions = submissions.filter(assignment__title__contains = search_value)
 
    form = SubmissionFilterFormForStudent(request.POST or None)
    if form.is_valid() and not any(field_value=="" for field_value in form.cleaned_data.values() if field_value):
        filter_field = form.cleaned_data.get('field_name')
        filtering_option = form.cleaned_data.get('filtering_option')
        filter_value = form.cleaned_data.get('filter_value')
 
        lookup_mapping = {
            'subject__name': 'subject__name__',
            'score': 'score__',
        }
 
        if filter_field == 'score':
            if filtering_option=="range":
                try:
                    start_range, end_range = map(float, filter_value.split('-'))
                except:
                    data = "Format should be, %d-%d"
                    return utils.error_message(request, data, url_name='view_submits')
                   
                q_objects = Q(score__gte=start_range, score__lte=end_range)
                submissions = submissions.filter(q_objects)
 
            elif filter_value.lower() == 'none':
                submissions = submissions.filter(score__isnull=True)
            else:
                lookup_key = lookup_mapping[filter_field] + filtering_option if filtering_option else lookup_mapping[filter_field]
                q_objects = Q(**{lookup_key: filter_value})
                submissions = submissions.filter(q_objects)
        elif filter_field=="subject__name":
            lookup_key = lookup_mapping[filter_field] + filtering_option if filtering_option else lookup_mapping[filter_field]
            lookup_key = "assignment__teacher__user_teacher__" + lookup_key
            q_objects = Q(**{lookup_key: filter_value})
 
            submissions = submissions.filter(q_objects)
 
    form2 = SortingForm(request.POST or None)
    if form2.is_valid():
        sort_field = form2.cleaned_data.get('field_name')
        sort_order = form2.cleaned_data.get('ordering')
   
        if sort_order=="+":
            submissions = submissions.order_by(sort_field)
        elif sort_order=="-":
            submissions = submissions.order_by(f"{sort_order}{sort_field}")
 
    return render(request, 'view_submits.html', {
                                    "submissions": submissions,
                                    "student_obj": student_obj,
                                    "admin_obj": admin_obj,
                                    "form":form,
                                    'form2':form2,
                                    'data': data
                                })
   
 
def student_file_retrieve(request, data, session_user, submission_id):
    """View function for retrieving a file related to a student submission."""
    student_obj = None
    try:
        student_obj = Student.objects.get(user__id=session_user.id)
        try:
            Submission.objects.get(id=submission_id, student_id=session_user.id)
        except Submission.DoesNotExist:
            return redirect('permission_denied')
    except Student.DoesNotExist:
        try:
            User.objects.get(id=session_user.id, is_staff=True)
        except User.DoesNotExist:
            return redirect('permission_denied')
   
    submission_obj = get_object_or_404(Submission, id=submission_id)
    with open(submission_obj.file.path, 'r', encoding='utf-8') as file:
        file_content = file.read()
    context = {
        'submission_obj': submission_obj,
        'file_content': file_content
    }
    if student_obj:
        context["student_obj"] = student_obj
 
    context['data'] = data
    return render(request, 'view_file.html', context)
   
 