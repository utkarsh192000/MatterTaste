"""onlineTiffin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from tiffin.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home, name="home"),
    path('about', About, name="about"),
    path('signup', Signup_User, name="signup"),
    path('contact', Contact, name="contact"),
    path('admin_home', Admin_Home, name="admin_home"),
    path('add_food', Add_Food, name="add_food"),
    path('view_food', View_food, name="view_food"),
    path('view_user', view_user, name="view_user"),
    path('booking_order/<int:pid>', Booking_order, name="booking_order"),
    path('payment/<int:total>', payment, name="payment"),
    path('edit_food/<int:pid>', Edit_Food, name="edit_food"),
    path('delete_food/<int:pid>', delete_food, name="delete_food"),
    path('delete_user/<int:pid>', delete_user, name="delete_user"),
    path('delete_feedback/<int:pid>', delete_feedback, name="delete_feedback"),
    path('booking_detail/<int:pid>', Booking_detail, name="booking_detail"),
    path('user_booking_detail/<int:pid>', User_Booking_detail, name="user_booking_detail"),
    path('edit_status/<int:pid>', Edit_status, name="edit_status"),
    path('get_invoice/<int:book_id>', get2, name="get_invoice"),
    path('delete_booking/<int:pid>', delete_booking, name="delete_booking"),
    path('Cancel_booking/<int:pid>', Cancel_booking, name="Cancel_booking"),
    path('login_user', Login, name="login_user"),
    path('login_admin', Admin_Login, name="login_admin"),
    path('logout', Logout, name="logout"),
    path('view_booking', View_Booking, name="view_booking"),
    path('view_feedback', View_feedback, name="view_feedback"),
    path('send_feedback',Feedback, name="send_feedback"),
    path('change_password', Change_Password, name="change_password"),
    path('profile', profile, name="profile"),
    path('edit_profile', Edit_profile, name="edit_profile"),
    path('Admin_View_Booking', Admin_View_Booking, name="Admin_View_Booking"),
    path('order_invoice', Order_Invoice, name="order_invoice"),
    path('view_all_food', View_All_Food, name="view_all_food"),
    path('pending_View_Booking', pending_View_Booking, name="pending_View_Booking"),
    path('cancel_view_booking',Cancel_View_Booking, name="cancel_view_booking"),
    path('confirmed_View_Booking', Confirmed_View_Booking, name="confirmed_View_Booking"),
]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
