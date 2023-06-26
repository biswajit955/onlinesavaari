"""Online_Savaari URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework.authtoken import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views #import this

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')), # Google Login
    path('oauth/', include('social_django.urls', namespace='social')), # Facebook Login
    path('api-token-auth/', views.obtain_auth_token),
    path('', include("onlinesavaari.urls")),
    # path('wallet/', include("wallet.urls")),
    path('adminpanel/', include("adminpanel.urls")),
    path('flight/', include("flight.urls")),
    path('payment/', include("payment.urls")),
    path('api/', include("api.urls")),
    path('Hotel/', include("Hotel.urls")),
    path('insurance/', include("insurance.urls")),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='online_savaari/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="online_savaari/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='online_savaari/password_reset_complete.html'), name='password_reset_complete'),      

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)