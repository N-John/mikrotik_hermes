from django.urls import path
from . import views

urlpatterns = [
    path('',views.main),
    path('payment',views.payment_input),
    path('payment/input',views.payment_input),
    path('user',views.create_user),
    path('user/add',views.create_user),
    path('payment/history',views.payment_history),
    path('session',views.active_session),
    path('session/active',views.active_session),
    path('session/edit',views.session_edit),
    path('payment/verify',views.payment_input_FORM),
    path('verify',views.payment_input_FORM),



]
