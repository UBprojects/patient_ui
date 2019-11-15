"""patient_ui URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include

from patient_ui.views import app as app_view
from patient_ui.views import auth as auth_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', auth_view.index, name='home'),
    url(r'^auth/logout/$', auth_view.logout, name='logout'),
    url(r'^auth/login/$', auth_view.login, name='login'),
    url(r'^auth/forgot-password/$', auth_view.forgot_password, name='forgot_password'),
    url(r'^dashboard/$', app_view.dashboard, name='dashboard'),
    url(r'^my-profile/$', auth_view.my_profile, name='my_profile'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler500 = 'patient_ui.views.auth.error500'
handler502 = 'patient_ui.views.auth.error502'
handler503 = 'patient_ui.views.auth.error503'
handler504 = 'patient_ui.views.auth.error504'
