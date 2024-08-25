from django.urls import path, include
from paypal.standard.ipn.views import ipn
from .views import search_by_field, quick_search, browse
from .views import confirm_reservervation, render_reservation_page, reservation_err, reservation_success
from .views import check_availability, rental_agreement
from .views import render_booking_payment_info, render_final_payment_info, checkin, checkout, save_checkout
from .views import compare


urlpatterns = [
    path('search_by_field/', search_by_field, name='search_by_field'),
    path('quick_search/', quick_search, name='quick_search'),
    path('compare/', compare, name='compare'),
    path('render_reservation_page/', render_reservation_page, name='render_reservation_page'),
    path('confirm_reservation/', confirm_reservervation, name='confirm_reservation'),
    path('reservation_error/', reservation_err, name='reservation_error'),
    path('reservation_success/', reservation_success, name='reservation_success'),
    path('browse/', browse, name='browse'),
    path('check_availability/', check_availability, name='check_availability'),
    path('rental_agreement/', rental_agreement, name='rental_agreement'),
    path('render_booking_payment_info/', render_booking_payment_info, name='render_booking_payment_info'),
    path('render_final_payment_info/<int:reservation_id>/', render_final_payment_info, name='render_final_payment_info'),
    path('checkin/<int:reservation_id>/', checkin, name='checkin'),
    path('checkout/<int:reservation_id>/', checkout, name='checkout'),
    path('save_checkout/<int:reservation_id>/', save_checkout, name='save_checkout'),
    path('paypal/', include('paypal.standard.ipn.urls')),
]


