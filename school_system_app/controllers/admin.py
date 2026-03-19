"""
admin related views
"""
from django.shortcuts import render, redirect, get_object_or_404
from school_system_app.forms import TForm, UForm, SForm, FilteringStudentsFormForAdmin, \
        FilteringTeachersFormForAdmin, SortingFormForAssignments
from school_system_app.models import Student, Teacher, User
from school_system_app import utils
from django.db.models import Q
 
 
def StudentsList(request, data, session_user):
    """
    View function for rendering a list of students.
    """
    try:
        admin_obj = User.objects.get(id=session_user.id, is_superuser=True)
    except User.DoesNotExist:
        return redirect('permission_denied')
   
    students = Student.objects.all()
    search_value = request.GET.get('query')
 
    if search_value=="":
        students = students.all()
    if search_value:
        students = students.filter(user__username__contains = search_value)
 
   
    form = FilteringStudentsFormForAdmin(request.POST or None)
    if form.is_valid() and not any(field_value=="" for field_value in form.cleaned_data.values() if field_value):
        filter_field = form.cleaned_data.get('field_name')
        filtering_option = form.cleaned_data.get('filtering_option')
        filter_value = form.cleaned_data.get('filter_value')
 
        lookup_mapping = {
            'standard': 'standard__',
            'user__is_active': 'user__is_active__',
        }
 
        if filter_field == 'standard':
            if filtering_option=='range':
                try:
                    start_range, end_range = map(int, filter_value.split('-'))
                except:
                    data = "Format should be, %d-%d"
                    return utils.error_message(request, data, url_name='student_list')
                   
                q_objects = Q(standard__gte=start_range, standard__lte=end_range)
                students = students.filter(q_objects)
            else:
                lookup_key = lookup_mapping[filter_field] + filtering_option if filtering_option else lookup_mapping[filter_field]
                q_objects = Q(**{lookup_key: filter_value})
                students = students.filter(q_objects)
        elif filter_field=="user__is_active":
            if filter_value.lower()=='active':
                filter_value = 1
            elif filter_value.lower()=='deactive':
                filter_value = 0
            else:
                data = "Value should be: Active/Deactive"
                return utils.error_message(request, data, url_name='student_list')
               
            lookup_key = lookup_mapping[filter_field] + filtering_option if filtering_option else lookup_mapping[filter_field]
            q_objects = Q(**{lookup_key: filter_value})
            students = students.filter(q_objects)
 
    form2 = SortingFormForAssignments(request.POST or None)
    if form2.is_valid():
        sort_field = form2.cleaned_data.get('field_name')
        sort_order = form2.cleaned_data.get('ordering')
   
        if sort_order=="+":
            students = students.order_by(sort_field)
        elif sort_order=="-":
            students = students.order_by(f"{sort_order}{sort_field}")
 
    return render(request, 'student_list.html', {'students': students, 'form': form, 'form2':form2, 'data': data})
 
 
def StudentUpdate(request, data, session_user, id):
    """View function for updating student information."""
    try:
        admin_obj = User.objects.get(id=session_user.id, is_superuser=True)
    except User.DoesNotExist:
        return redirect('permission_denied')
   
    student = get_object_or_404(Student, user__id=id)
 
    if request.method == 'POST':
        form1 = UForm(request.POST, instance=student.user)
        if form1.is_valid():
            form2 = SForm(request.POST, instance=student)
            if form2.is_valid():
                form2.save()
                form1.save()
                data = f"{student.user.first_name} {student.user.last_name} details updated successfully"
                return utils.success_message(request, data, url_name='student_list')
               
            else:
                data = list(form2.errors.as_data().values())[0][0].message
                return utils.error_message(request, data, url_name='student_update', id=id)
               
        else:
            data = list(form1.errors.as_data().values())[0][0].message
            return utils.error_message(request, data, url_name='student_update', id=id)
           
    else:
        form1 = UForm(instance=student.user)
        form2 = SForm(instance=student)
 
    return render(request, 'student_update.html', {'form1':form1, 'form2': form2, 'student': student, 'data': data})
 
 
def StudentActivate(session_user, id):
    """Function for activating a student."""
    try:
        User.objects.get(id=session_user.id, is_superuser=True)
    except User.DoesNotExist:
        return redirect('permission_denied')
   
    student_user = get_object_or_404(User, id=id)
    student_user.is_active = True
    student_user.save()
    return redirect('student_list')
 
 
def StudentDeactivate(session_user, id):
    """Function for deactivating a student."""
    try:
        User.objects.get(id=session_user.id, is_superuser=True)
    except User.DoesNotExist:
        return redirect('permission_denied')
   
    student_user = get_object_or_404(User, id=id)
    student_user.is_active = False
    student_user.save()
    return redirect('student_list')
 
 
def TeacherList(request, data, session_user):
    """View function for rendering a list of teachers."""
    try:
        admin_obj = User.objects.get(id=session_user.id, is_superuser=True)
    except User.DoesNotExist:
        return redirect('permission_denied')
   
    teachers = Teacher.objects.all()
    search_value = request.GET.get('query')
    if search_value=="":
        teachers = teachers.all()
    if search_value:
        teachers = teachers.filter(user__username__contains = search_value)
 
    for_sorting_asc = request.GET.get('query_sort_asc')
    if for_sorting_asc=='asc':
        teachers = teachers.order_by('user_id')
 
    for_sorting_desc = request.GET.get('query_sort_desc')
    if for_sorting_desc=='desc':
        teachers = teachers.order_by('-user_id')
 
 
    form = FilteringTeachersFormForAdmin(request.POST or None)
    if form.is_valid() and not any(field_value=="" for field_value in form.cleaned_data.values() if field_value):
        filter_field = form.cleaned_data.get('field_name')
        filtering_option = form.cleaned_data.get('filtering_option')
        filter_value = form.cleaned_data.get('filter_value')
 
        lookup_mapping = {
            'subject__name': 'subject__name__',
            'user__is_active': 'user__is_active__',
        }
 
        if filter_field == 'subject__name':
            lookup_key = lookup_mapping[filter_field] + filtering_option if filtering_option else lookup_mapping[filter_field]
            q_objects = Q(**{lookup_key: filter_value})
            teachers = teachers.filter(q_objects)
        elif filter_field=="user__is_active":
            if filter_value.lower()=='active':
                filter_value = 1
            elif filter_value=='deactive':
                filter_value = 0
            else:
                data = "Value should be: Active/Deactive"
                return utils.error_message(request, data, url_name='teacher_list')
               
            lookup_key = lookup_mapping[filter_field] + filtering_option if filtering_option else lookup_mapping[filter_field]
            q_objects = Q(**{lookup_key: filter_value})
            teachers = teachers.filter(q_objects)
 
    return render(request, 'teacher_list.html', {'teachers': teachers, 'form': form, 'data': data})
 
 
def TeacherUpdate(request, data, session_user, id):
    """View function for updating teacher information."""
    try:
        admin_obj = User.objects.get(id=session_user.id, is_superuser=True)
    except User.DoesNotExist:
        return redirect('permission_denied')
   
    teacher = get_object_or_404(Teacher, user__id=id)
 
    if request.method == 'POST':
        form1 = UForm(request.POST, instance=teacher.user)
        if form1.is_valid():
            form2 = TForm(request.POST, instance = teacher)
            if form2.is_valid():
                form2.save()
                form1.save()
                data = f"{teacher.user.first_name} {teacher.user.last_name} details updated successfully"
                return utils.success_message(request, data, url_name='teacher_list')
               
            else:
                data = list(form2.errors.as_data().values())[0][0].message
                return utils.error_message(request, data, url_name='teacher_update', id=id)
               
        else:
            data = list(form1.errors.as_data().values())[0][0].message
            return utils.error_message(request, data, url_name='teacher_update', id=id)
           
    else:
        form1 = UForm(instance = teacher.user)
        form2 = TForm(instance = teacher)
   
    return render(request, 'teacher_update.html', {'form1':form1, 'form2': form2, 'teacher': teacher, 'data': data})
 
 
def TeacherActivate(session_user, id):
    """Function for activating a teacher."""
    try:
        User.objects.get(id=session_user.id, is_superuser=True)
    except User.DoesNotExist:
        return redirect('permission_denied')
   
    teacher_user = get_object_or_404(User, id=id)
    teacher_user.is_active = True
    teacher_user.save()
    return redirect('teacher_list')
 
 
def TeacherDeactivate(session_user, id):
    """Function for deactivating a teacher."""
    try:
        User.objects.get(id=session_user.id, is_superuser=True)
    except User.DoesNotExist:
        return redirect('permission_denied')
   
    teacher_user = get_object_or_404(User, id=id)
    teacher_user.is_active = False
    teacher_user.save()
    return redirect('teacher_list')
 
 
def AdminUpdate(request, data, session_user, id):
    """View function for updating administrator information."""
    try:
        admin_obj = User.objects.get(id=session_user.id, is_superuser=True)
    except User.DoesNotExist:
        return redirect('permission_denied')
   
    if request.method == 'POST':
        form = UForm(request.POST, instance=admin_obj)
        if form.is_valid():
            form.save()
            data = f"{admin_obj.first_name} {admin_obj.last_name} details updated successfully"
            return utils.success_message(request, data, url_name='my_profile')
           
        else:
            data = list(form.errors.as_data().values())[0][0].message
            return utils.error_message(request, data, url_name='my_profile', id=id)
           
    else:
        form = UForm(instance = admin_obj)
 
    return render(request, 'admin_update.html', {'form':form, 'admin_obj': admin_obj, 'data': data})
 