from django.shortcuts import render, redirect
from .models import User
from . import utils
from school_system_app.controllers import users, teachers, students, admin


def LoginView(request):
    """
    View function for handling user login.

    This view function handles the login process. It checks if the user is already
    authenticated and redirects them to the login page if necessary. If the user is
    not authenticated, it delegates the login process to the `users.user_login`
    function. If any exception occurs during the login process, an error message
    is displayed to the user.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - HttpResponse: The HTTP response containing the login page or an error message.
    """
    if 'messages' in request.session:
        data = request.session['messages'][0]
        del request.session['messages']
    else:
        data = None
    try:
        session_user = utils.is_authorized(request.user)
        if session_user is not None:
            response = redirect('user_login')
            response.delete_cookie('auth_token')
            return response
    
        response = users.user_login(request, data)
        return response
    except Exception as err:
        data = str(err)
        return utils.error_message(request, data, url_name='user_login')
           
def AdminPage(request):
    """
    View function for rendering the admin page.

    This view function renders the admin page. It checks if the current user is
    authorized to access the admin page using the `utils.is_authorized` function.
    If the user is not authorized, they are redirected to the login page.
    If the user is authorized, the admin page is rendered.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - HttpResponse: The HTTP response containing the admin page or a redirection
      to the login page if the user is not authorized.
    """
    
    if 'messages' in request.session:
        data = request.session['messages'][0]
        del request.session['messages']
    else:
        data = None
    session_user = utils.is_authorized(request.user)
    if session_user is None:
        data = "Please login to access this page."
        return utils.error_message(request, data, url_name='user_login')
        
    try:
        User.objects.get(id=session_user.id, is_superuser=True)
    except User.DoesNotExist:
        return redirect('permission_denied')
 
    return render(request, "admin_page.html", {'data': data})


def Register(request):
    """
    View function for rendering the registration page.

    This view function renders the registration page, allowing users to register
    for an account. The registration form is rendered using the "register.html"
    template.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - HttpResponse: The HTTP response containing the registration page.
    """
    return render(request, "register.html")


def StudentRegister(request):
    """
    View function for handling student registration.

    This view function handles the student registration process. It first checks
    if there are any messages stored in the session and retrieves them if present.
    Then, it delegates the registration process to the `students.student_registration`
    function. If any exception occurs during the registration process, an error
    message is displayed to the user.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - HttpResponse: The HTTP response containing the result of the registration
      process or an error message.
    """
    if 'messages' in request.session:
        data = request.session['messages'][0]
        del request.session['messages']
    else:
        data = None
    
    try:
        response = students.student_registration(request, data)
        return response
    except Exception as err:
        data = str(err)
        return utils.error_message(request, data, url_name='student_registration')


def TeacherRegister(request):
    """
    View function for handling teacher registration.

    This view function handles the teacher registration process. It first checks
    if there are any messages stored in the session and retrieves them if present.
    Then, it delegates the registration process to the `teachers.teacher_registration`
    function. If any exception occurs during the registration process, an error
    message is displayed to the user.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - HttpResponse: The HTTP response containing the result of the registration
      process or an error message.
    """
    if 'messages' in request.session:
        data = request.session['messages'][0]
        del request.session['messages']
    else:
        data = None

    try:
        response = teachers.teacher_registration(request, data)
        return response
    except Exception as err:
        data = str(err)
        return utils.error_message(request, data, url_name='teacher_registration')


def ViewAssignments(request):
    """
    View function for displaying assignments.

    This view function displays assignments to the user. It first checks if there
    are any messages stored in the session and retrieves them if present.
    Then, it checks if the user is authorized to access the page using the
    `utils.is_authorized` function. If the user is not authorized, they are
    redirected to the login page.
    If the user is authorized, the assignment data is retrieved using the
    `teachers.view_assignment` function.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - HttpResponse: The HTTP response containing the assignments or an error message.
    """
    if 'messages' in request.session:
        data = request.session['messages'][0]
        del request.session['messages']
    else:
        data = None

    try:
        session_user = utils.is_authorized(request.user)
        if session_user is None:
            data = "Please login to access this page."
            return utils.error_message(request, data, url_name='user_login')

        response = teachers.view_assignment(request, session_user, data)
        return response
    except Exception as err:
        data = str(err)
        return utils.error_message(request, data, url_name='view_assignment')


def CreateAssignment(request):
    """
    View function for creating assignments.

    This view function handles the creation of assignments. It first checks if there
    are any messages stored in the session and retrieves them if present.
    Then, it delegates the assignment creation process to the appropriate function.
    If any exception occurs during the creation process, an error message is displayed
    to the user.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - HttpResponse: The HTTP response containing the result of the assignment creation
      process or an error message.
    """
    if 'messages' in request.session:
        data = request.session['messages'][0]
        del request.session['messages']
    else:
        data = None

    try:
        session_user = utils.is_authorized(request.user)
        if session_user is None:
            data = "Please login to access this page."
            return utils.error_message(request, data, url_name='user_login')

        response = teachers.assignment_creation(request, session_user, data)
        return response
    except Exception as err:
        data = str(err)
        return utils.error_message(request, data, url_name='assignment_creation')


def UpdateAssignment(request, id):
    """
    View function for updating an assignment.

    This view function handles the update of an existing assignment identified by the
    given ID. It first checks if there are any messages stored in the session and retrieves
    them if present.
    Then, it checks if the user is authorized to access the page using the
    `utils.is_authorized` function. If the user is not authorized, they are
    redirected to the login page.
    If the user is authorized, the assignment update process is delegated to the
    `teachers.update_assignment` function.

    Parameters:
    - request: The HTTP request object.
    - id: The ID of the assignment to be updated.

    Returns:
    - HttpResponse: The HTTP response containing the result of the assignment update
      process or an error message.

    """
    if 'messages' in request.session:
        data = request.session['messages'][0]
        del request.session['messages']
    else:
        data = None

    try:
        session_user = utils.is_authorized(request.user)
        if session_user is None:
            data = "Please login to access this page."
            return utils.error_message(request, data, url_name='user_login')

        response = teachers.update_assignment(request, session_user, data, id)
        return response
    except Exception as err:
        data = str(err)
        return utils.error_message(request, data, url_name='update_assignment')
        
    

def SubmitAssignment(request):
    """
    Handles assignment submission by student.
    """
    if 'messages' in request.session:
        data = request.session['messages'][0]
        del request.session['messages']
    else:
        data = None

    session_user = utils.is_authorized(request.user)
    if session_user is None:
        data = "Please login to access this page."
        return utils.error_message(request, data, url_name='user_login')
    
    try:
        response = students.assignment_submission(request, data, session_user)
        return response
    except Exception as err:
        data = str(err)
        return utils.error_message(request, data, url_name='assignment_submission') 


def ViewSubmittedAssignments(request):
    """
    View function for displaying submitted assignments.

    This view function displays the submitted assignments to the user.
    It first checks if there are any messages stored in the session and retrieves
    them if present.
    Then, it delegates the display of submitted assignments to the appropriate function.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - HttpResponse: The HTTP response containing the submitted assignments or an error message.
    """
    if 'messages' in request.session:
        data = request.session['messages'][0]
        del request.session['messages']
    else:
        data = None

    try:
        session_user = utils.is_authorized(request.user)
        if session_user is None:
            data = "Please login to access this page."
            return utils.error_message(request, data, url_name='user_login')
          
        response = teachers.list_submissions(request, session_user, data)
        return response
    except Exception as err:
        data = str(err)
        return utils.error_message(request, data, url_name='list_submissions')


def ViewSubmissions(request):
    """
    Handles retrieving of submissions done by a students.
    """
    if 'messages' in request.session:
        data = request.session['messages'][0]
        del request.session['messages']
    else:
        data = None

    session_user = utils.is_authorized(request.user)
    if session_user is None:
        data = "Please login to access this page."
        return utils.error_message(request, data, url_name='user_login')
            
    try:
        response = students.view_submits(request, data, session_user)
        return response
    except Exception as err:
        data = str(err)
        return utils.error_message(request, data, url_name='view_submits')


def StudentFileRetrieve(request, submission_id):
    """
    View function for retrieving a file related to a submission.

    This view function handles the retrieval of a file related to a submission
    identified by the given submission ID. It first checks if there are any messages
    stored in the session and retrieves them if present.
    Then, it checks if the user is authorized to access the page using the
    `utils.is_authorized` function. If the user is not authorized, they are
    redirected to the login page.
    If the user is authorized, the file retrieval process is delegated to the
    `students.student_file_retrieve` function.

    Parameters:
    - request: The HTTP request object.
    - submission_id: The ID of the submission for which the file is to be retrieved.

    Returns:
    - HttpResponse: The HTTP response containing the retrieved file or an error message.
    """
    if 'messages' in request.session:
        data = request.session['messages'][0]
        del request.session['messages']
    else:
        data = None

    session_user = utils.is_authorized(request.user)
    if session_user is None:
        data = "Please login to access this page."
        return utils.error_message(request, data, url_name='user_login')
           
    try:
        response = students.student_file_retrieve(request, data, session_user, submission_id)
        return response
    except Exception as err:
        data = str(err)
        return utils.error_message(request, data, url_name='view_submits')


def TeacherFileRetrieve(request, submission_id):
    """
    View function for retrieving a file related to a submission.

    This view function handles the retrieval of a file related to a submission
    identified by the given submission ID. It first checks if there are any messages
    stored in the session and retrieves them if present.
    Then, it checks if the user is authorized to access the page using the
    `utils.is_authorized` function. If the user is not authorized, they are
    redirected to the login page.
    If the user is authorized, the file retrieval process is delegated to the
    `teachers.teacher_file_retrieve` function.

    Parameters:
    - request: The HTTP request object.
    - submission_id: The ID of the submission for which the file is to be retrieved.

    Returns:
    - HttpResponse: The HTTP response containing the retrieved file or an error message.
    """
    if 'messages' in request.session:
        data = request.session['messages'][0]
        del request.session['messages']
    else:
        data = None

    try:
        session_user = utils.is_authorized(request.user)
        if session_user is None:
            data = "Please login to access this page."
            return utils.error_message(request, data, url_name='user_login')
        
        response = teachers.teacher_file_retrieve(request, session_user, data, submission_id)
        return response
    except Exception as err:
        data = str(err)
        return utils.error_message(request, data, url_name='list_submissions')
        

def ScoreUpdate(request, submission_id):
    """
    View function for updating the score of a submission.

    This view function handles the update of the score for a submission identified
    by the given submission ID. It first checks if there are any messages stored in
    the session and retrieves them if present.
    Then, it checks if the user is authorized to access the page using the
    `utils.is_authorized` function. If the user is not authorized, they are
    redirected to the login page.
    If the user is authorized, the score update process is delegated to the
    appropriate function.

    Parameters:
    - request: The HTTP request object.
    - submission_id: The ID of the submission for which the score is to be updated.

    Returns:
    - HttpResponse: The HTTP response containing the result of the score update
      process or an error message.
    """
    if 'messages' in request.session:
        data = request.session['messages'][0]
        del request.session['messages']
    else:
        data = None
 
    try:
        session_user = utils.is_authorized(request.user)
        if session_user is None:
            data = "Please login to access this page."
            return utils.error_message(request, data, url_name='user_login')
            
        response = teachers.score_update(request, session_user, data, submission_id)
        return response 
    except Exception as err:
        data = str(err)
        return utils.error_message(request, data, url_name='list_submissions')
 

def ProfileView(request):
    """
    """
    if 'messages' in request.session:
        data = request.session['messages'][0]
        del request.session['messages']
    else:
        data = None

    try:
        session_user = utils.is_authorized(request.user)
        if session_user is None:
            data = "Please login to access this page."
            return utils.error_message(request, data, url_name='user_login')

        response = users.my_profile(request, session_user, data)
        return response
    except Exception as err:
        data = str(err)
        return utils.error_message(request, data, url_name='my_profile')


def logoutView(request):
    """
    """
    try:
        session_user = utils.is_authorized(request.user)
        if session_user is None:
            data = "Please login to access this page."
            return utils.error_message(request, data, url_name='user_login')

        response = redirect('user_login')
        response.delete_cookie('auth_token')
        return response
    except Exception as err:
        data = str(err)
        return utils.error_message(request, data, url_name='user_login')


def PermissionDenied(request):
    return render(request, 'permission_denied.html')


# Admin views
def student_list(request):
    """
    Handles listing all students for admin.
    """
    if 'messages' in request.session:
        data = request.session['messages'][0]
        del request.session['messages']
    else:
        data = None

    try:
        session_user = utils.is_authorized(request.user)
        if session_user is None:
            data = "Please login to access this page."
            return utils.error_message(request, data, url_name='user_login')
    
        response = admin.StudentsList(request, data, session_user)
        return response
    
    except Exception as err:
        data = str(err)
        return utils.error_message(request, data, url_name='student_list')
        
    
 
def student_update(request, id):
    """
    Handles updating student information by admin.
    """
    if 'messages' in request.session:
        data = request.session['messages'][0]
        del request.session['messages']
    else:
        data = None

    try:
        session_user = utils.is_authorized(request.user)
        if session_user is None:
            data = "Please login to access this page."
            return utils.error_message(request, data, url_name='user_login')
    
        response = admin.StudentUpdate(request, data, session_user, id)
        return response
    except Exception as err:
        data = str(err)
        return utils.error_message(request, data, url_name='student_update')
        
    
 
def student_activate(request, id):
    """
    Handles activating a student by admin.
    """
    try:
        session_user = utils.is_authorized(request.user)
        if session_user is None:
            data = "Please login to access this page."
            return utils.error_message(request, data, url_name='user_login')
        
        response = admin.StudentActivate(session_user, id)
        return response
    except Exception as err:
        data = str(err)
        return utils.error_message(request, data, url_name='student_list')
    
        
def student_deactivate(request, id):
    """
    Handles deactivating a student by admin.
    """
    try:
        session_user = utils.is_authorized(request.user)
        if session_user is None:
            data = "Please login to access this page."
            return utils.error_message(request, data, url_name='user_login')
        
        response = admin.StudentDeactivate(session_user, id)
        return response
    except Exception as err:
        data = str(err)
        return utils.error_message(request, data, url_name='student_list')
   
 
def teacher_list(request):
    """
    Handles listing all students for admin.
    """
    if 'messages' in request.session:
        data = request.session['messages'][0]
        del request.session['messages']
    else:
        data = None

    try:
        session_user = utils.is_authorized(request.user)
        if session_user is None:
            data = "Please login to access this page."
            return utils.error_message(request, data, url_name='user_login')
        
        response = admin.TeacherList(request, data, session_user)
        return response
    
    except Exception as err:
        data = str(err)
        return utils.error_message(request, data, url_name='teacher_list')
 

def admin_update(request, id):
    """
    Handles updating Admin information.
    """
    if 'messages' in request.session:
        data = request.session['messages'][0]
        del request.session['messages']
    else:
        data = None

    try:
        session_user = utils.is_authorized(request.user)
        if session_user is None:
            data = "Please login to access this page."
            return utils.error_message(request, data, url_name='user_login')
        
        response = admin.AdminUpdate(request, data, session_user, id)
        return response
    except Exception as err:
        data = str(err)
        return utils.error_message(request, data, url_name='admin_update')


def teacher_update(request, id):
    """
    Handles updating teacher information by admin.
    """
    if 'messages' in request.session:
        data = request.session['messages'][0]
        del request.session['messages']
    else:
        data = None

    try:
        session_user = utils.is_authorized(request.user)
        if session_user is None:
            data = "Please login to access this page."
            return utils.error_message(request, data, url_name='user_login')
        
        response = admin.TeacherUpdate(request, data, session_user, id)
        return response
    except Exception as err:
        data = str(err)
        return utils.error_message(request, data, url_name='teacher_update')       
    
 
def teacher_activate(request, id):
    """
    Handles activating a teacher by admin.
    """
    try:
        session_user = utils.is_authorized(request.user)
        if session_user is None:
            data = "Please login to access this page."
            return utils.error_message(request, data, url_name='user_login')
        
        response = admin.TeacherActivate(session_user, id)
        return response
    except Exception as err:
        data = str(err)
        return utils.error_message(request, data, url_name='teacher_list')       
    
 
def teacher_deactivate(request, id):
    """
    Handles deactivating a teacher by admin.
    """
    try:
        session_user = utils.is_authorized(request.user)
        if session_user is None:
            data = "Please login to access this page."
            return utils.error_message(request, data, url_name='user_login')
        
        response = admin.TeacherDeactivate(session_user, id)
        return response
    except Exception as err:
        data = str(err)
        return utils.error_message(request, data, url_name='teacher_list')
        

def play_video(request):
    """
    Handles playing introduction video.
    """
    return render(request, 'intro_video.html')
