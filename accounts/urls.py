from django.contrib import admin
from django.urls import path, include
from accounts import views
from pages import views as pages_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('becomeSeller/', views.becomeSeller, name='becomeSeller'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:id>', pages_views.view_profile, name='view_profile'),
    path('profile/services/', include('pages.urls')),
    path('profile/edit/', views.edit_profile, name='editProfile'),
    path('profile/orders/', pages_views.yourOrders, name='yourOrders'),
    path('profile/orders/download/<int:id>/', views.download, name='download'),
    path('profile/ordersRec/', pages_views.orders_rec, name='orders_rec'),
    path('profile/ordersRec/complete/<int:id>/', pages_views.complete_order, name='complete_order'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
