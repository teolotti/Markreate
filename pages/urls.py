from django.contrib import admin
from django.urls import path, include
from pages import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.yourServices, name='yourServices'),
    path('<int:id>/', views.service, name='service'),
    path('<int:id>/order/', views.order, name='order'),
    path('create/', views.create_service, name='create_service'),
    path('edit/<int:id>/', views.edit_service, name='edit_service'),
    path('delete/<int:id>/', views.delete_service, name='delete_service'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
