# by biswajit paloi
from django.contrib import messages 
from django.http import HttpResponseRedirect

def check_user_able_to_see_flight_app_page(c_t1,c_t2 =None,c_t3 =None):
	def decorator(function):
		def wrapper(request, *args, **kwargs):
			# print("flight."+c_t)
			if c_t2 is not None:
				if c_t3 is not None:
					if request.user.has_perm("flight."+c_t1) and request.user.has_perm("flight."+c_t2) and request.user.has_perm("flight."+c_t3):
						return function(request, *args, **kwargs)
					messages.error(request, f"You don't have Permission for this page")
					return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
				else:
					if request.user.has_perm("flight."+c_t1) and request.user.has_perm("flight."+c_t2):
						return function(request, *args, **kwargs)
					messages.error(request, f"You don't have Permission for this page")
					return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
			else:
				if request.user.has_perm("flight."+c_t1):
					return function(request, *args, **kwargs)
				messages.error(request, f"You don't have Permission for this page")
				return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

		return wrapper

	return decorator