from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include

from files.views import loginPage,logoutUser,registerUser

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/',include('files.urls')),
    path('login/',loginPage,name='login'),
    path('logout/',logoutUser,name='logout'),
    path('register/',registerUser,name='register'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
