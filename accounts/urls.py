from django.contrib import admin
from django.urls import path, include
from accounts import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('becomeSeller/', views.becomeSeller, name='becomeSeller'),
    path('profile/', views.profile, name='profile'),
    path('profile/services/', include('pages.urls')),
    path('profile/edit/', views.edit_profile, name='editProfile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
