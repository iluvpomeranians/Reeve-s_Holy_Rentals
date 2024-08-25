import json
import uuid
import re
import random
from datetime import datetime, timedelta
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from bs4 import BeautifulSoup
from .models import Car, Reservation


def browse(request):
    if request.method == 'GET':
        # Retrieve search parameters from the form submission
        make = request.GET.get('make', '').strip().lower()
        model = request.GET.get('model', '').strip().lower()
        year = request.GET.get('year', '').strip().lower()
        rental_price = request.GET.get('rental_price', '').strip().lower()
        color = request.GET.get('color', '').strip().lower()
        location = request.GET.get('location', '').strip().lower()

        # Filter cars queryset based on search parameters
        cars = Car.objects.all()
        if make:
            cars = cars.filter(make__icontains=make)
        if model:
            cars = cars.filter(model__icontains=model)
        if year:
            cars = cars.filter(year__icontains=year)
        if rental_price:
            cars = cars.filter(rental_price__icontains=rental_price)
        if color:
            cars = cars.filter(color__icontains=color)
        if location:
            cars = cars.filter(location__icontains=location)

        is_search_or_htmx = any([make, model, year, rental_price, color, location]) or 'HX-Request' in request.headers

        if is_search_or_htmx:
            # For searches or HTMX requests, return only the car list part
            return render(request, 'search_app/car_list.html', {'cars': cars})
        else:
            # For initial page loads, render the entire page
            return render(request, 'search_app/browse.html', {'cars': cars})

def search_by_field(request):
    if request.method == 'GET':
        make = request.GET.get('make', '').strip().lower()
        model = request.GET.get('model', '').strip().lower()
        year = request.GET.get('year', '').strip().lower()
        rental_price = request.GET.get('rental_price', '').strip().lower()
        color = request.GET.get('color', '').strip().lower()

        cars = Car.objects.all()
        if make:
            cars = cars.filter(make__icontains=make)
        if model:
            cars = cars.filter(model__icontains=model)
        if year:
            cars = cars.filter(year__icontains=year)
        if rental_price:
            cars = cars.filter(rental_price__icontains=rental_price)
        if color:
            cars = cars.filter(color__icontains=color)

        is_search_or_htmx = any([make, model, year, rental_price, color]) and 'HX-Request' in request.headers

        if is_search_or_htmx :
            # For searches or HTMX requests, return only the car list part
            return render(request, 'search_app/quick_search.html', {'cars': cars})
        else:
            # Clear the search results if no search parameters are provided
            cars = Car.objects.none()
            return render(request, 'search_app/quick_search.html', {'cars': cars})


def quick_search(request):
    search_results = None
    if request.method == 'POST':
        search_term = request.POST.get('search', '')
        if search_term:
            search_results = Car.objects.filter(make__icontains=search_term)
            search_results = search_results[:15]
        else:
            search_results = Car.objects.none()

    return render(request, 'search_app/quick_search.html', {'search_results': search_results})

def render_reservation_page(request):
    # Retrieve query parameters, or use defaults if not provided
    if not request.user.is_authenticated:
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return JsonResponse({'login_required': True})
        else:  # If not AJAX, render the login modal template
            return render(request, 'home_page_app/login_modal.html')

    car_make = request.GET.get('make', 'DefaultMake')
    car_model = request.GET.get('model', 'DefaultModel')
    car_year = request.GET.get('year', 'DefaultYear')
    car_color = request.GET.get('color', 'DefaultColor')
    car_price = request.GET.get('price', 'DefaultPrice')
    car_image = request.GET.get('image', 'DefaultImage')

    car_id = f"{car_make}-{car_model}-{car_year}-{car_color}-{car_price}"
    context = {
        'car_id': car_id,
        'car_image_url': car_image,
    }

    return render(request, 'search_app/make_reservation.html', context)


def confirm_reservervation(request):
    if request.method == 'POST':
        car_id = request.POST.get('car_id', '')
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')
        customer_name = request.POST.get('customer_name', '')
        customer_email = request.POST.get('customer_email', '')
        driver_license = request.POST.get('driver_license', '')

        if car_id and start_date and end_date:
            reservation = Reservation(car_id=car_id, start_date=start_date, end_date=end_date)
            reservation.customer_name = customer_name
            reservation.customer_email = customer_email
            reservation.driver_license = driver_license
            reservation.save()

            return render(request, 'search_app/reservation_success.html', {'reservation': reservation})
        else:
            return render(request, 'search_app/reservation_error.html')
    else:
        return render(request, 'search_app/make_reservation.html')

def reservation_err(request):
    return render(request, 'search_app/reservation_error.html')

def reservation_success(request):

    reservation_details = request.session.get('reservation', {})

    new_reservation = Reservation(
        car_id=reservation_details.get('car_id', ''),
        start_date=reservation_details.get('start_date', ''),
        end_date=reservation_details.get('end_date', ''),
        customer_name=reservation_details.get('customer_name', ''),
        customer_email=reservation_details.get('customer_email', ''),
        driver_license=reservation_details.get('driver_license', ''),
        deposit_paid=True,
        rental_agreement_signed_date=datetime.now().date(),
        rental_agreement_signed=True,
        email_sent=True,
    )

    new_reservation.save()

    #Send Booking Confirmation Email
    message_content = render_to_string('search_app/booking_confirmation_email.html', {
        'car_id': new_reservation.car_id,
        'start_date': datetime.strptime(reservation_details.get('start_date', ''), '%Y-%m-%d').date(),  # Format dates as strings
        'end_date': datetime.strptime(reservation_details.get('end_date', ''), '%Y-%m-%d').date(),
        'customer_name': new_reservation.customer_name,
        'driver_license': new_reservation.driver_license,
    })

    plain_message = strip_tags(message_content)

    send_mail(
        subject='Booking Confirmation',
        message=plain_message,
        from_email='david.martinez@spaceconcordia.com',
        recipient_list=[new_reservation.customer_email],
        fail_silently=False,
        html_message=message_content,
    )

    return render(request, 'search_app/reservation_success.html', {'reservation': reservation_details})


@login_required
def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    if request.method == 'POST':
        car_id = request.POST.get('car_id')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        reservation.car_id = car_id
        reservation.start_date = start_date
        reservation.end_date = end_date

        reservation.save()

        return  HttpResponse('Reservation updated successfully')
    else:
        return  HttpResponse('Error: Failed update!')


@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'DELETE':
        reservation.delete()
        return HttpResponse('Reservation deleted successfully')
    else:
        return HttpResponse('Error: Method not allowed, status=405')

def check_availability(request):
    if request.method == 'GET':
        car_id = request.GET.get('car_id', '')
        start_date = request.GET.get('start_date', '')
        end_date = request.GET.get('end_date', '')
        print(car_id, start_date, end_date)

        # Convert start and end dates from string to date objects
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:  # If there's an error in date conversion
            return HttpResponse('Please Choose Dates')

        if end_date < start_date:
            return HttpResponse('End date must be later than start date')

        if car_id and start_date and end_date:
            reservations = Reservation.objects.filter(car_id=car_id)
            for reservation in reservations:
                if start_date <= reservation.start_date <= end_date or start_date <= reservation.end_date <= end_date:
                    return HttpResponse('Not available. Choose another date')
            rental_span = end_date - start_date
            price_per_day = float(car_id.split("-")[-1])
            if rental_span.days == 0:
                total_cost = 1 * price_per_day
            else:
                total_cost = rental_span.days * price_per_day
            return HttpResponse(f'Available! Total rental cost: ${total_cost:.2f}')
        else:
            return HttpResponse('Error: Missing required parameters!')
    else:
        return HttpResponse('Error: Method not allowed', status=405)

def rental_agreement(request):
    return render(request, 'search_app/rental_agreement.html')


#@login_required
def render_booking_payment_info(request):

    car_id = request.GET.get('car_id', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    customer_name = request.GET.get('customer_name', '')
    customer_email = request.GET.get('customer_email', '')
    driver_license = request.GET.get('driver_license', '')

    additional_info = {
        'start_date': start_date,
        'end_date': end_date,
        'customer_name': customer_name,
        'customer_email': customer_email,
        'driver_license': driver_license,
    }

    request.session['reservation'] = {
        'car_id': car_id,
        'start_date': start_date,
        'end_date': end_date,
        'customer_name': customer_name,
        'customer_email': customer_email,
        'driver_license': driver_license,
    }

    host = request.get_host()
    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '500.00',
        'item_name': 'Deposit for Car Rental: ' + car_id + "\n" + json.dumps(additional_info),
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        "notify_url": "https://possible-dogfish-tight.ngrok-free.app/paypal/",
        'return_url': f'http://{host}/reservation_success/',
    }

    print(request.build_absolute_uri(reverse('paypal-ipn')))

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
    context = {
        'paypal_payment': paypal_payment,
        'paypal_business_email': settings.PAYPAL_RECEIVER_EMAIL,
    }


    return render(request, 'search_app/booking_payment_info.html', context)


def render_final_payment_info(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    car_id = reservation.car_id
    start_date = reservation.start_date.strftime('%Y-%m-%d')
    end_date = reservation.end_date.strftime('%Y-%m-%d')
    price_match = re.search(r'-(\d+\.\d+)$', car_id)
    if price_match:
        daily_price = float(price_match.group(1))
    else:
        # Set a default price or handle the error as appropriate.
        daily_price = 0.00

    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
    duration = (end_date_obj - start_date_obj).days
    if duration == 0:  # If rental is for the same day, count as one day.
        duration = 1

    full_payment = daily_price * duration

    request.session[f'checkout_data_{reservation_id}'] = {
        "engine": request.POST.get('engine'),
        "transmission": request.POST.get('transmission'),
        "body": request.POST.get('body'),
        "interior": request.POST.get('interior'),
        "lights": request.POST.get('lights'),
        "tires": request.POST.get('tires'),
        "gas_level_half": request.POST.get('gas_level_half'),
        "car_rating": request.POST.get('car_rating'),
        "service_rating": request.POST.get('service_rating'),
        "send_email": True,
    }

    host = request.get_host()
    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': full_payment,
        'total_price': full_payment,
        'item_name': f'Final Payment for Car Rental: {car_id}, Dates: {start_date} to {end_date}',
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        "notify_url": "https://possible-dogfish-tight.ngrok-free.app/paypal/",
        'return_url': f'http://{host}/checkout/{reservation_id}/',
    }

    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
    context = {
        'paypal_payment': paypal_payment,
        'paypal_business_email': settings.PAYPAL_RECEIVER_EMAIL,
        'reservation_id': reservation_id,
    }

    return render(request, 'search_app/final_payment_info.html', context)

@login_required
@require_POST
def checkin(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    check_in_date = timezone.localdate()
    check_in_data = {
        "reservation_id": reservation.id,
        "car_id": reservation.car_id,
        "start_date": reservation.start_date.isoformat(),
        "end_date": reservation.end_date.isoformat(),
        "check_out_date": check_in_date.isoformat(),
        "engine": request.POST.get('checkin-engine') == 'true',
        "transmission": request.POST.get('checkin-transmission') == 'true',
        "body": request.POST.get('checkin-car-body') == 'true',
        "interior": request.POST.get('checkin-interior') == 'true',
        "lights": request.POST.get('checkin-lights') == 'true',
        "tires": request.POST.get('checkin-tires') == 'true',
        "gas-level-half": request.POST.get('checkin-gas-level-half') == 'true',
    }

    reservation.check_in = check_in_date
    reservation.check_in_data = check_in_data
    print(reservation.check_in_data)

    reservation.save()
    return HttpResponse('Check-in successful!')

@login_required
def save_checkout(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    check_out_date = timezone.localdate()

    check_out_data = {
        "reservation_id": reservation.id,
        "car_id": reservation.car_id,
        "start_date": reservation.start_date.isoformat(),
        "end_date": reservation.end_date.isoformat(),
        "check_out_date": check_out_date.isoformat(),
        "engine": request.POST.get('engine') == 'true',
        "transmission": request.POST.get('transmission') == 'true',
        "body": request.POST.get('body') == 'true',
        "interior": request.POST.get('interior') == 'true',
        "lights": request.POST.get('lights') == 'true',
        "tires": request.POST.get('tires') == 'true',
        "gas_level_half": request.POST.get('gas_level_half') == 'true',
        "car_rating": request.POST.get('car_rating'),
        "service_rating": request.POST.get('service_rating'),
    }

    reservation.check_out = check_out_date
    reservation.check_out_data = check_out_data
    print(reservation.check_out_data)

    reservation.save()

    return HttpResponse('Check-out form saved! Please Confirm :)')

@login_required
def checkout(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    check_out_date = timezone.localdate()

    checkout_data_key = f'checkout_data_{reservation_id}'
    check_out_data = request.session.get(checkout_data_key, {})

    reservation.check_out = check_out_date
    reservation.check_out_data = check_out_data
    print(reservation.check_out_data)
    reservation.save()
    send_email = check_out_data.get('send_email', False)

    if send_email:
        check_out_data_cap = reservation.check_out_data

        table_content = '<table border="1" style="border-collapse: collapse;">'
        table_content += '<tr><th>Field</th><th>Value</th></tr>'

        for key, value in check_out_data_cap.items():
            table_content += f'<tr><td>{key}</td><td>{value}</td></tr>'

        table_content += '</table>'

        message_content = f"""
        <html>
        <head>
        <style>
            table, th, td {{
            border: 1px solid black;
            border-collapse: collapse;
            padding: 5px;
            text-align: left;
            }}
            th {{
            background-color: #f2f2f2;
            }}
        </style>
        </head>
        <body>
        <p>Dear {reservation.customer_name},</p>

        <p>Your checkout is confirmed for reservation #{reservation_id}.<br>
        Car ID: {reservation.car_id}<br>
        Checkout Date: {reservation.check_out}
        Your Safety Deposit of 500$ will be issued within 2-3 business days</p>

        <p>Checkout Details:</p>
        {table_content}

        <p>Thank you for choosing us.</p>

        <p>REEVE'S HOLY RENTALS</p>
        <pre>
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣀⠀⠀⠀⠀⠀
        ⠀⠀⠀⣰⣿⣿⣿⣿⣿⠿⠿⣿⣿⣿⣿⣿⣿⣧⢀⠀⠀⠀⠀
        ⠀⠀⣿⣿⣿⠋⠀⠀⠀⠀⠀⠙⠀⠙⣿⣿⣿⣷⢳⢀⠀⠀⠀
        ⠀⣠⣿⣿⣿⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⢀
        ⠀⣸⣿⣿⣿⠸⠀⠀⠀⠒⠒⠒⠐⠀⠀⢿⣿⣿⣿⣿⣿⠀⠀
        ⣴⣿⣿⣿⣿⡿⠀⠒⣋⣙⡒⢰⠀⠤⣖⠒⢾⣿⣿⣿⣧⠀⠀
        ⢺⣿⣿⣿⣿⢀⠀⠀⠉⠉⠉⠸⠀⡇⠉⠉⠀⢿⣿⣿⣿⣄⠀⠀
        ⠀⠙⣿⣿⣧⢻⠀⠀⠀⠀⠀⠠⠀⠰⠀⠀⠀⣸⠸⣿⣿⠿⠰⠀
        ⠀⠀⠀⠹⣿⣿⣿⣷⠀⡠⠙⣲⣔⣅⢡⣰⣷⣿⣿⣿⣧⠀⠀⠀
        ⠀⠀⠀⣼⣿⣿⣿⣿⠀⡿⠭⠭⠭⠭⢿⠀⣿⢻⣿⣿⠃⠀⠀⠀
        ⠀⠀⠀⠙⠛⣿⢻⠹⣿⠐⠙⠛⠟⠉⢀⣴⡟⢿⣿⡏⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⠀⡟⠀⠀⠻⣦⣤⣶⠾⠋⠀⠀⠁⡦⢄⢀⠀⠀⠀
        ⠀⠀⠀⡠⠁⡇⠑⢄⠀⠀⠀⠀⠀⠀⠔⠀⠀⠁⠀⠀⠀⠉⠁
        ⠀⠔⠊⠁⠀⠀⣇⠀⠀⠀⠑⡤⠤⢎⠁⠀⠀⡘⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⠀⠀⠀⢢⠠⠀⡠⢆⠀⠀⡠⠙⢄⠀⡸⠀⠀⠀⠀⠀⠀
        ⠀⠀⠀⡠⠁⡇⠑⢄⠀⠀⠀⠀⠀⠀⠔⠀⠀⠁⠀⠀⠀⠉⠁
                                    THANK YOU
        </pre>
        </body>
        </html>
        """

        send_mail(
            subject='Checkout Confirmation',
            message="Your checkout is confirmed. Please check the HTML version of this email for details.",  # Plain text fallback
            from_email='david.martinez@spaceconcordia.com',
            recipient_list=[reservation.customer_email],
            fail_silently=False,
            html_message=message_content
        )

        return redirect('account_page')
    else:
        return HttpResponse('Error, Paypal Payment Gateway Failed!')


def compare(request):
    # Extracting car details from the request
    car_make = request.GET.get('make', 'DefaultMake')
    car_model = request.GET.get('model', 'DefaultModel')
    car_year = request.GET.get('year', 'DefaultYear')
    car_color = request.GET.get('color', 'DefaultColor')
    car_price = float(request.GET.get('price', '10000'))  # Assuming a default price
    car_image = request.GET.get('image', 'DefaultImage')

    formatted_price = "{:.2f}".format(car_price)

    globe_car_prices = scrape_globe_car_prices()
    kayak_car_prices = scrape_kayak()
    matching_kayak_cars = [car for car in kayak_car_prices if car_make.lower() in car['model'].lower()]
    matching_globe_cars = [car for car in globe_car_prices if car_make.lower() in car['model'].lower()]


    # Creating a unique identifier for the car
    car_id = f"{car_make}-{car_model}-{car_year}-{car_color}-{formatted_price}"

    # Simulating competitor prices (for simplicity, random prices around the car_price)
    competitor_prices = {
        'Enterprise': round(car_price + random.uniform(0.10, 0.25) * car_price, 2),
        'Kayak': round(car_price + random.uniform(0.10, 0.36) * car_price, 2),
        'Expedia': round(car_price + random.uniform(0.08, 0.41) * car_price, 2)
    }

    # Finding the best price among the competitors
    best_price = min(list(competitor_prices.values()) + [car_price])

    cleaned_car_id = re.sub(r"-\d+(\.\d+)?$", "", car_id)

    context = {
        'car_id': cleaned_car_id,
        'car_image_url': car_image,
        'car_price': formatted_price,
        'competitor_prices': competitor_prices,
        'best_price': best_price,
        'best_offer': best_price == car_price,
        'matching_globe_cars': matching_globe_cars,
        'matching_kayak_cars': matching_kayak_cars,
    }


    return render(request, 'search_app/compare.html', context)

def scrape_globe_car_prices():
    url = 'https://www.globecar.com/en/vehicles/'
    headers = {'User-Agent': 'Your User-Agent'}

    # Make the request with a timeout of 5 seconds
    response = requests.get(url, headers=headers, timeout=5)
    soup = BeautifulSoup(response.text, 'html.parser')

    car_prices = []

    descriptions = soup.find_all('div', class_='description')
    for description in descriptions:

        model = description.find('h3').text.strip()
        price_info = description.find('p').text.strip()
        price_match = re.search(r'\$(\d+\.\d+)', price_info)
        if price_match:
            #price = price_match.group(1)
            price = float(price_match.group(1)) * 2.8
            car_prices.append({'model': model, 'price': f'{price:.2f}'})

    return car_prices


def scrape_kayak():
    # Calculate today's date and a week from today's date
    today = datetime.today() + timedelta(days=6)
    one_week_later = today + timedelta(days=7)

    # Format the dates as 'YYYY-MM-DD'
    start_date = today.strftime('%Y-%m-%d')
    end_date = one_week_later.strftime('%Y-%m-%d')

    # Construct the URL with the formatted dates
    url = f'https://www.ca.kayak.com/cars/Montreal,Quebec,Canada-c6966/{start_date}/{end_date}'
    # Make the request
    headers = {'User-Agent': 'Your User-Agent'}
    response = requests.get(url, headers=headers, timeout=5)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        car_listings = []

        car_results_list = soup.find('div', class_='CarResultsList')

        if car_results_list:
            car_divs = car_results_list.find_all('div', role='button')
            for car_div in car_divs:
                car_div_msey_list = car_div.find_all('div', class_='MseY-list')
                for car_div_msey in car_div_msey_list:
                    car_div_msey_title = car_div_msey.find('div', class_='js-title')
                    model = car_div_msey_title.text.strip()
                details_div = car_div.find('div', class_=lambda x: x and 'booking-details' in x)
                if (details_div):
                    price_div = details_div.find(lambda tag: tag.name == 'div' and tag.get('role') == 'button' and 'C$' in tag.text)
                    if price_div:
                        price_match = re.search(r'C\$\s*(\d+)', price_div.text.strip())
                        price = price_match.group(1) if price_match else 'Unknown Price'

                        car_listings.append({'model': model, 'price': price})
                    else:
                        price = 'Unknown Price'

        return car_listings
    else:
        print(f'Failed to retrieve data, status code: {response.status_code}')
        return []

def show_me_the_money(sender, **kwargs):

    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        print('IPN Received')

    return HttpResponse("OKAY")

valid_ipn_received.connect(show_me_the_money)