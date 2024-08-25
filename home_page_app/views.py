from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date
from django.core.exceptions import ValidationError
from django.middleware.csrf import get_token
from django.http import HttpResponse, JsonResponse
from home_page_app.models import User
from home_page_app.models import Contact
from search_app.models import Reservation

def render_index(request):
    return render(request, 'home_page_app/index.html')

def render_registermodal(request):
    return render(request, 'home_page_app/register_modal.html')

def render_loginmodal(request):
    return render(request, 'home_page_app/login_modal.html')

def render_contactform(request):
    return render(request, 'home_page_app/contact_form.html')

def render_liability(request):
    return render(request, 'home_page_app/liability.html')

def render_careers(request):
    return render(request, 'home_page_app/careers.html')

def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Use authenticate to verify if a user with this email and password exists
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            request.session['logged_in'] = True
            csrf_token = get_token(request)

            print("CSRF TOKEN:", csrf_token)
            print(request.session.items())
            print("Session Key:", request.session.session_key)

            return JsonResponse({'exists': True, 'correctPassword': True ,'csrfToken': csrf_token})
        else:
            try:
                User.objects.get(email=email)
                return JsonResponse({'exists': True, 'correctPassword': False})
            except User.DoesNotExist:
                return JsonResponse({'exists': False})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def logout_user(request):
    if request.method == 'POST':
        logout(request)
        request.session['logged_in'] = False
        return JsonResponse({'logged_out': True})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def register_user(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        license = request.POST.get('license')


        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return JsonResponse({'exists': True, 'success': False})

        user = User.objects.create_user(firstName=firstname, lastName=lastname, email=email, password=password, driverLicense=license)

        if user is not None:
            login(request, user)
            request.session['logged_in'] = True
            csrf_token = get_token(request)

            print(request.session.items())
            print("Session Key:", request.session.session_key)

            return JsonResponse({'exists': False, 'success': True, 'csrfToken': csrf_token})
        else:
            try:
                User.objects.get(email=email)
                return JsonResponse({'exists': True, 'success': False})
            except User.DoesNotExist:
                return JsonResponse({'exists': False})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
def render_account_page(request):
    user = request.user
    user_email = user.email
    reservations = Reservation.objects.filter(check_out_data__isnull=True)

    context = {
        'user': user,
        'reservations': reservations
    }
    return render(request, 'home_page_app/account_page.html', context)


def submit_contact_form(request):
    if request.method == 'POST':
        # Extract form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Create a new Contact instance and save it
        contact = Contact(name=name, email=email, message=message)
        contact.save()

        html_content = "<p style='color:green'>Form submitted successfully!</p>"
        return HttpResponse(html_content)

    return render(request, 'contact_app/contact_form.html')


@login_required
def update_personal_data(request):
    if request.method == 'POST':
        user = request.user
        user.firstName = request.POST.get('firstName', user.firstName)
        user.lastName = request.POST.get('lastName', '')
        user.driverLicense = request.POST.get('driverLicense', '')
        user.address = request.POST.get('address', '')
        user.city = request.POST.get('city', '')
        user.state = request.POST.get('state', '')

        date_of_birth_str = request.POST.get('dateofbirth', '')
        try:
            user.dateofbirth = parse_date(date_of_birth_str)
        except ValidationError:
            return HttpResponse('error: Invalid date format for date of birth. It must be in YYYY-MM-DD format. status=400')

        # Save the updated user object
        user.save()

        success_message = "Account Successfully Updated!"
        return HttpResponse(success_message)

    return HttpResponse('error: Invalid request method (Status: 400)')


@login_required
def delete_account(request):
    if request.method == 'DELETE':
        user = request.user
        user.delete()
        return HttpResponse('Account deleted successfully!')
    else:
        return JsonResponse('error: Invalid request method. status=400')


