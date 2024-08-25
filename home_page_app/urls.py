from django.urls import path
from search_app.views import edit_reservation, cancel_reservation
from .views import render_index, render_loginmodal, render_registermodal
from .views import render_contactform, submit_contact_form, render_account_page
from .views import login_user, logout_user, register_user, render_liability
from .views import update_personal_data, delete_account, render_careers

urlpatterns = [
    path('', render_index, name='index'),
    path('login_modal/', render_loginmodal, name='login_modal'),
    path('register_modal/', render_registermodal, name='register_modal'),
    path('contact/', render_contactform, name='contact_form'),
    path('liability/', render_liability, name='liability'),
    path('careers/', render_careers, name='careers'),
    path('submit_contact_form/', submit_contact_form, name='submit_contact_form'),
    path('login/', login_user, name='login'),
    path('register_user/', register_user, name='register_user'),
    path('logout/', logout_user, name='logout'),
    path('account_page/', render_account_page, name='account_page'),
    path('update_personal_data/', update_personal_data, name='update_personal_data'),
    path('delete_account/', delete_account, name='delete_account'),
    path('edit_reservation/<int:reservation_id>/', edit_reservation, name='edit_reservation'),
    path('cancel_reservation/<int:reservation_id>/', cancel_reservation, name='cancel_reservation')
]
