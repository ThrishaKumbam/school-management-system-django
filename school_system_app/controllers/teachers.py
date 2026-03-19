"""
teacher related views
"""
from django.shortcuts import render, redirect, get_object_or_404
from school_system_app.forms import TeacherForm, AssignmentForm, SubmissionFilterFormForTeacher, \
    SortingForm, AdminFormForTeachers, SortingFormForAssignments, AssignmentsFilterFormForTeacher, \
        AssignmentUpdateForm
from school_system_app.models import Teacher, Assignment, Submission, User, TeacherStandard, \
        Standard
from school_system_app import utils
from datetime import datetime
from django.db.models import Q

# views
def teacher_registration(request, data):
    """View function for handling teacher registration."""
    if request.method == 'POST':
        teacher_form = TeacherForm(request.POST)
        if teacher_form.is_valid():
            if User.objects.filter(username = request.POST.get("username")).exists():
                data = "Username already exists."
                return utils.error_message(request, data, url_name='teacher_registration')
            
            user = User.objects.create_user(
                username=teacher_form.cleaned_data['username'],
                password=teacher_form.cleaned_data['password'],
                email=teacher_form.cleaned_data['email'],
                first_name=teacher_form.cleaned_data['first_name'],
                last_name=teacher_form.cleaned_data['last_name']
            )

            teacher = teacher_form.save(commit=False)
            teacher.user = user
            teacher.save()
            data = f"{teacher.user.username} registered successfully."
            return utils.success_message(request, data, url_name='user_login')
           
        else:
            data = list(teacher_form.errors.as_data().values())[0][0].message
            return utils.error_message(request, data, url_name='teacher_registration')
    else:
        teacher_form = TeacherForm()

    return render(request, "teacher_register.html", {'form': teacher_form, 'data': data})

def assignment_creation(request, session_user, data):
    """View function for creating assignments."""    
    teacher_obj = None
    admin_obj = None
    try:
        teacher_obj = Teacher.objects.get(user__id=session_user.id)
    except Teacher.DoesNotExist:
        try:
            admin_obj = User.objects.get(id=session_user.id, is_staff=True)
        except User.DoesNotExist:
            return redirect('permission_denied')
        
    if teacher_obj:
        if not TeacherStandard.objects.filter(teacher=session_user).exists():
            data = "You are not assigned to a standard, Please contact principal."
            response = utils.error_message(request, data, url_name='user_login')
            response.delete_cookie('auth_token')
            return response
        
        if request.method == 'POST':
            form = AssignmentForm(request.POST)
            form.set_teacher_obj(session_user)
            if form.is_valid():
                form.instance.teacher_id = session_user.id
                form.save()
                data = "Assignment Created Successfully"
                return utils.success_message(request, data, url_name='assignment_creation')
             
            else:
                data = list(form.errors.as_data().values())[0][0].message
                return utils.error_message(request, data, url_name='assignment_creation')
               
        else:
            form = AssignmentForm()
            form.set_teacher_obj(session_user)
    elif admin_obj:
        if request.method == 'POST':
            form = AdminFormForTeachers(request.POST)
            teach = request.POST.get("teacher")
            stand = request.POST.get("standard")
            user = User.objects.get(id=teach)
            standard = Standard.objects.get(id=stand)
            if TeacherStandard.objects.filter(teacher=user, standard=standard).exists():
                data = "Teacher is already assigned to that standard."
                return utils.error_message(request, data, url_name='assignment_creation')
                
            if form.is_valid():
                form.save()
                data = "Teacher successfully assigned to a standard."
                return utils.success_message(request, data, url_name='assignment_creation')
               
            else:
                data = list(form.errors.as_data().values())[0][0].message
                return utils.error_message(request, data, url_name='assignment_creation')
                
        else:
            form = AdminFormForTeachers()
    
    return render(request, 'assignment.html', {'form': form, "teacher_obj": teacher_obj, "admin_obj": admin_obj, 'data': data})

def view_assignment(request, session_user, data):
    """View function for displaying assignments."""
    teacher_obj = None
    admin_obj = None
    try:
        teacher_obj = Teacher.objects.get(user__id=session_user.id)
    except Teacher.DoesNotExist:
        try:
            admin_obj = User.objects.get(id=session_user.id, is_staff=True)
        except User.DoesNotExist:
            return redirect('permission_denied')
    if teacher_obj:
        assignments = Assignment.objects.filter(teacher_id=session_user.id)
    elif admin_obj:
        assignments = Assignment.objects.all()
 
    form = AssignmentsFilterFormForTeacher(request.POST or None)

    search_value = request.GET.get('query')
    if search_value:
        assignments = assignments.filter(title__contains = search_value)
    if search_value=="":
        assignments = assignments.all()


    if form.is_valid() and not any(field_value=="" for field_value in form.cleaned_data.values() if field_value):
        filter_field = form.cleaned_data.get('field_name')
        filtering_option = form.cleaned_data.get('filtering_option')
        filter_value = form.cleaned_data.get('filter_value')
 
        lookup_mapping = {
            'standard': 'standard__',
            'deadline': 'deadline__',
            'created_at': 'created_at__'
        }
 
        if filter_field == 'standard':
            if filtering_option=="range":
                try:
                    start_range, end_range = map(int, filter_value.split('-'))
                except:
                    data = "Format should be, %d-%d"
                    return utils.error_message(request, data, url_name='view_assignments')
                    
                q_objects = Q(standard__gte=start_range, standard__lte=end_range)
                assignments = assignments.filter(q_objects)
            else:
                try:
                    lookup_key = lookup_mapping[filter_field] + filtering_option if filtering_option else lookup_mapping[filter_field]
                    q_objects = Q(**{lookup_key : filter_value})
                    assignments = assignments.filter(q_objects)
                except:
                    data = "Format should be, %d"
                    return utils.error_message(request, data, url_name='view_assignments')
 
        elif filter_field=="deadline" or filter_field=="created_at": 
            if filter_field=="deadline" and filtering_option == "exact":
                try:
                    exact_date = datetime.strptime(filter_value, '%Y-%m-%d').date()
                except:
                    data = "Format should be, YYYY-MM-DD"
                    return utils.error_message(request, data, url_name='view_assignments')
                    
                lookup_key = lookup_mapping[filter_field] + filtering_option if filtering_option else lookup_mapping[filter_field]
                q_objects = Q(**{lookup_key: exact_date})
                assignments = assignments.filter(q_objects)

            elif filter_field=="created_at" and filtering_option=="exact":
                try:
                    exact_date = datetime.strptime(filter_value, '%Y-%m-%d').date()
                    exact_datetime_start = datetime.combine(exact_date, datetime.min.time())
                    exact_datetime_end = datetime.combine(exact_date, datetime.max.time())
                except:
                    data = "Format should be, YYYY-MM-DD"
                    return utils.error_message(request, data, url_name='view_assignments')
                    
                lookup_key = lookup_mapping[filter_field]
                q_objects = Q(**{lookup_key + "gte": exact_datetime_start, lookup_key + "lte": exact_datetime_end})
                assignments = assignments.filter(q_objects)
           
            elif filtering_option == "range":
                try:
                    start_date_str, end_date_str = filter_value.split('&')
                    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                except:
                    data = "Format should be, YYYY-MM-DD&YYYY-MM-DD"
                    return utils.error_message(request, data, url_name='view_assignments')
 
                lookup_key = lookup_mapping[filter_field] + filtering_option if filtering_option else lookup_mapping[filter_field]
                q_objects = Q(**{lookup_key : (start_date, end_date)})
 
                assignments = assignments.filter(q_objects)
    
    form2 = SortingFormForAssignments(request.POST or None)
    if form2.is_valid():
        sort_field = form2.cleaned_data.get('field_name')
        sort_order = form2.cleaned_data.get('ordering')

        if sort_field and sort_field:
            if sort_order=="+":
                assignments = assignments.order_by(sort_field)
            elif sort_order=="-":
                assignments = assignments.order_by(f"{sort_order}{sort_field}")
        else:
            assignments = assignments.order_by()

    return render(request, 'view_assignments.html', {
                                "assignments": assignments, 
                                "teacher_obj":teacher_obj, 
                                "admin_obj":admin_obj, 
                                "form":form, 
                                "form2":form2,
                                "data": data
                            })

def update_assignment(request, session_user, data, id):
    """View function for updating an assignment."""
    try:
        teacher_obj = Teacher.objects.get(user__id=session_user.id)
    except User.DoesNotExist:
        return redirect('permission_denied')

    assignment = get_object_or_404(Assignment, id=id)
    if request.method == 'POST':
        form = AssignmentUpdateForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            data = f"{assignment.title} updated successfully."
            return utils.success_message(request, data, url_name='view_assignments')
            
        else:
            data = list(form.errors.as_data().values())[0][0].message
            return utils.error_message(request, data, url_name='update_assignment', id=id)
            # messages.error(request, data)
            # return redirect('update_assignment', assignment_id=assignment_id)
    else:
        form = AssignmentUpdateForm(instance=assignment)

    return render(request, 'update_assignment.html', {'form': form, 'teacher_obj': teacher_obj, 'data': data})

def list_submissions(request, session_user, data):
    """View function for listing submissions."""
    try:
        teacher_obj = Teacher.objects.get(user__id=session_user.id)
    except Teacher.DoesNotExist:
        return redirect('permission_denied')
    
    assignments = Assignment.objects.filter(teacher_id = session_user.id)
    assignment_ids = [assignment.id for assignment in assignments]
    submissions = Submission.objects.filter(assignment_id__in = assignment_ids)
    teacher_obj = Teacher.objects.get(user__id=session_user.id)

    form = SubmissionFilterFormForTeacher(request.POST or None)
    search_value = request.GET.get('query')

    if search_value=="":
        submissions = submissions.all()
    if search_value:
        submissions = submissions.filter(assignment__title__contains = search_value)

    if form.is_valid() and not any(field_value=="" for field_value in form.cleaned_data.values() if field_value):
        filter_field = form.cleaned_data.get('field_name')
        filtering_option = form.cleaned_data.get('filtering_option')
        filter_value = form.cleaned_data.get('filter_value')

        lookup_mapping = {
            'student_name': 'student__username__',
            'assignment_title': 'assignment__title__',
            'score': 'score__',
            'standard': 'assignment__standard__'
        }

        if filtering_option=="range":
            if filter_field=="score":
                try:
                    start_range, end_range = map(float, filter_value.split('-'))
                except:
                    data = "Format should be, %d-%d"
                    return utils.error_message(request, data, url_name='list_submissions')
                    
                q_objects = Q(score__gte=start_range, score__lte=end_range)
                submissions = submissions.filter(q_objects)
            elif filter_field=="standard":
                try:
                    start_range, end_range = map(int, filter_value.split('-'))
                except:
                    data = "Format should be, %d-%d"
                    return utils.error_message(request, data, url_name='list_submissions')
                    
                q_objects = Q(assignment__standard__gte=start_range, assignment__standard__lte=end_range)
                submissions = submissions.filter(q_objects)
            else:
                data = f"{filter_field} does not supports {filtering_option}filter."
                return utils.error_message(request, data, url_name='list_submissions')

        elif filter_field=="score" and filter_value.lower() == 'none':
            submissions = submissions.filter(score__isnull=True)
        else:
            lookup_key = lookup_mapping[filter_field] + filtering_option if filtering_option else lookup_mapping[filter_field]
            q_objects = Q(**{lookup_key: filter_value})
            submissions = submissions.filter(q_objects)
        
    form2 = SortingForm(request.POST or None)
    if form2.is_valid() and not any(field_name=="" for field_name in form2.cleaned_data.values() if field_name):
        sort_field = form2.cleaned_data.get('field_name')
        sort_order = form2.cleaned_data.get('ordering')
        if sort_order=="+":
            submissions = submissions.order_by(sort_field)
        elif sort_order=="-":
            submissions = submissions.order_by(f"{sort_order}{sort_field}")

    return render(request, 'list_submissions.html', {
                                        "submissions": submissions, 
                                        "teacher_obj":teacher_obj, 
                                        "form": form, 
                                        "form2":form2, 
                                        "data": data
                                    })

def teacher_file_retrieve(request, session_user, data, submission_id):
    """View function for retrieving a file related to a teacher submission."""
   
    try:
        teacher_obj = Teacher.objects.get(user__id=session_user.id)
    except Teacher.DoesNotExist:
        return redirect('permission_denied')
    
    submission_obj = Submission.objects.get(id=submission_id)
    with open(submission_obj.file.path, 'r', encoding='utf-8') as file:
        file_content = file.read()
    context = {
        "teacher_obj":teacher_obj,
        'submission_obj': submission_obj,
        'file_content': file_content
    }

    if request.method == 'POST':
        input_score = request.POST.get('score', '').replace('"', '').strip()
        input_score = float(input_score)
        if input_score:
            try:
                if 0 <= input_score <= 10:
                    submission_obj.score = input_score
                    submission_obj.save()
                    data = f'Score updated!'
                    return utils.success_message(request, data, url_name='list_submissions')  
                else:
                    data = f'Score must be between 0.0 and 10.0'
                    return utils.error_message(request, data, url_name='list_submissions')  
            except ValueError:
                data = 'Invalid score format. Please enter a valid number.'
                return utils.error_message(request, data, url_name='list_submissions')

    context['data'] = data
    return render(request, 'view_file_teacher.html', context)


def score_update(request, session_user, data, submission_id):
    """View function for updating the score of a submission."""
    try:
        teacher_obj = Teacher.objects.get(user__id=session_user.id)
    except Teacher.DoesNotExist:
        return redirect('permission_denied')
    
    submission_obj = Submission.objects.get(id=submission_id)
    with open(submission_obj.file.path, 'r', encoding='utf-8') as file:
        file_content = file.read()
    context = {
        "teacher_obj":teacher_obj,
        'submission_obj': submission_obj,
        'file_content': file_content
    }

    if request.method == 'POST':
        input_score = request.POST.get('new_score', '').replace('"', '').strip()
        input_score = float(input_score)
        try:
            if 0.0 <= input_score <= 10.0:
                submission_obj.score = input_score
                submission_obj.save()
                data = f'Score updated'
                return utils.success_message(request, data, url_name='list_submissions')
            else:
                data = f'Score must be between 0.0 and 10.0'
                return utils.error_message(request, data, url_name='list_submissions')  
        except ValueError:
            data = 'Invalid score format. Please enter a valid number.'
            return utils.error_message(request, data, url_name='list_submissions')

    context['data'] = data
    return render(request, 'score_update.html', context)
