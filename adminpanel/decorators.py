# by biswajit paloi
from django.contrib import messages 
from django.http import HttpResponseRedirect


def check_user_able_to_see_adminpanel_app_page(c_t1=None,c_t2=None,c_t3=None):
    def decorator(function):
        def wrapper(request, *args, **kwargs):
            error_message = f"You don't have permission to view this page."
            if ((c_t1 is not None) and (c_t2 is None) and (c_t3 is None)):
                if request.user.has_perm("adminpanel."+c_t1):
                    return function(request, *args, **kwargs)
                else:
                    messages.error(request, error_message)
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif ((c_t1 is None) and (c_t2 is not None) and (c_t3 is None)):
                if request.user.has_perm("adminpanel."+c_t2):
                    return function(request, *args, **kwargs)
                else:
                    messages.error(request, error_message)
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif ((c_t1 is not None) and (c_t2 is not None) and (c_t3 is None)):
                if request.user.has_perm("adminpanel."+c_t1) and request.user.has_perm("adminpanel."+c_t2):
                    return function(request, *args, **kwargs)
                else:
                    messages.error(request, error_message)
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif ((c_t1 is not None) and (c_t2 is not None) and (c_t3 is not None)):
                if request.user.has_perm("adminpanel."+c_t1) and request.user.has_perm("adminpanel."+c_t2) and request.user.has_perm("adminpanel."+c_t3):
                    return function(request, *args, **kwargs)
                else:
                    messages.error(request, error_message)
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif ((c_t1 is None) and (c_t2 is not None) and (c_t3 is not None)):
                if request.user.has_perm("adminpanel."+c_t2) and request.user.has_perm("adminpanel."+c_t3):
                    return function(request, *args, **kwargs)
                else:
                    messages.error(request, error_message)
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif ((c_t1 is not None) and (c_t2 is None) and (c_t3 is not None)):
                if request.user.has_perm("adminpanel."+c_t1) and request.user.has_perm("adminpanel."+c_t3):
                    return function(request, *args, **kwargs)
                else:
                    messages.error(request, error_message)
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                
                messages.error(request, error_message)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return wrapper
    return decorator



def check_user_able_to_see_auth_app_page(c_t1=None,c_t2=None,c_t3=None):
    def decorator(function):
        def wrapper(request, *args, **kwargs):
            error_message = f"You don't have permission to view this page."
            if ((c_t1 is not None) and (c_t2 is None) and (c_t3 is None)):
                if request.user.has_perm("auth."+c_t1):
                    return function(request, *args, **kwargs)
                else:
                    messages.error(request, error_message)
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif ((c_t1 is None) and (c_t2 is not None) and (c_t3 is None)):
                if request.user.has_perm("auth."+c_t2):
                    return function(request, *args, **kwargs)
                else:
                    messages.error(request, error_message)
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif ((c_t1 is not None) and (c_t2 is not None) and (c_t3 is None)):
                if request.user.has_perm("auth."+c_t1) and request.user.has_perm("auth."+c_t2):
                    return function(request, *args, **kwargs)
                else:
                    messages.error(request, error_message)
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif ((c_t1 is not None) and (c_t2 is not None) and (c_t3 is not None)):
                if request.user.has_perm("auth."+c_t1) and request.user.has_perm("auth."+c_t2) and request.user.has_perm("auth."+c_t3):
                    return function(request, *args, **kwargs)
                else:
                    messages.error(request, error_message)
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif ((c_t1 is None) and (c_t2 is not None) and (c_t3 is not None)):
                if request.user.has_perm("auth."+c_t2) and request.user.has_perm("auth."+c_t3):
                    return function(request, *args, **kwargs)
                else:
                    messages.error(request, error_message)
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif ((c_t1 is not None) and (c_t2 is None) and (c_t3 is not None)):
                if request.user.has_perm("auth."+c_t1) and request.user.has_perm("auth."+c_t3):
                    return function(request, *args, **kwargs)
                else:
                    messages.error(request, error_message)
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                
                messages.error(request, error_message)
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return wrapper
    return decorator