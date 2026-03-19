from rest_framework_simplejwt.tokens import RefreshToken
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime, timedelta
from django.shortcuts import redirect
from django.contrib import messages

def generate_tokens(user):
    token = RefreshToken.for_user(user)
    token['exp'] = datetime.utcnow() + timedelta(hours=1)
    return str(token)

def is_authorized(session_user):
    if session_user is None:
        return None
    return session_user

def success_message(request, data, url_name, id=None):
    data = data
    messages.success(request, data)
    if id:
        return redirect(url_name, id)
    return redirect(url_name)

def error_message(request, data, url_name, id=None):
    data = data
    messages.error(request, data)
    if id:
        return redirect(url_name, id)
    return redirect(url_name)

def paginate_items(request, items, items_per_page):
    paginator = Paginator(items, items_per_page)
    page = request.GET.get('page')
 
    try:
        paginated_items = paginator.page(page)
    except PageNotAnInteger:
        paginated_items = paginator.page(1)
    except EmptyPage:
        paginated_items = paginator.page(paginator.num_pages)
 
    return paginated_items