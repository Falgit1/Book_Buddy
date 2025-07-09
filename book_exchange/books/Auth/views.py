from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import PhoneVerification
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .utils import generate_and_send_otp
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from BookStore.models import Book
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('landing_page')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    return render(request, 'login.html')


def forgot_password(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        try:
            phone_verification = PhoneVerification.objects.get(phone_number=phone_number)
            otp = generate_and_send_otp(phone_number)
            phone_verification.otp = otp
            phone_verification.save()

            return redirect('verify_reset_password_otp', phone_number=phone_number)
        except PhoneVerification.DoesNotExist:
            messages.error(request, 'No account is associated with this phone number.')

    return render(request, 'forgot_password.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            phone_number = form.cleaned_data.get('phone_number')

            if PhoneVerification.objects.filter(phone_number=phone_number, is_verified=True).exists():
                form.add_error('phone_number', 'Phone number already exists and is verified.')
            else:
                otp = generate_and_send_otp(phone_number)
                phone_verification, created = PhoneVerification.objects.get_or_create(phone_number=phone_number)
                if created or not phone_verification.is_verified:
                    phone_verification.otp = otp
                    phone_verification.is_verified = False
                    phone_verification.username = username
                    phone_verification.password = make_password(password)
                    phone_verification.save()
                return redirect(reverse('verify_otp') + f'?phone_number={phone_number}')

    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def verify_otp(request):
    phone_number = request.GET.get('phone_number').strip()
    if phone_number and not phone_number.startswith('+'):
        phone_number = '+' + phone_number

    if request.method == 'POST':
        otp = request.POST.get('otp')
        try:
            phone_verification = PhoneVerification.objects.get(phone_number=phone_number, otp=otp)
            if phone_verification:
                phone_verification.is_verified = True
                phone_verification.save()

                username = phone_verification.username
                password = phone_verification.password

                if User.objects.filter(username=username).exists():
                    user = User.objects.get(username=username)
                    user.set_password(password)
                    user.save()
                else:
                    user = User.objects.create_user(username=username, password=password)
                    user.save()

                login(request, user)
                return redirect('landing_page')
            else:
                messages.error(request, 'Invalid OTP.')
        except PhoneVerification.DoesNotExist:
            return render(request, 'verify_otp.html', {'error': 'Invalid OTP', 'phone_number': phone_number})

    return render(request, 'verify_otp.html', {'phone_number': phone_number})


@login_required
def landing_page(request):
    user = request.user
    books_sorted = Book.objects.filter(is_sold=False)

    try:
        phone_verification = PhoneVerification.objects.get(username=user.username)
        context = {
            'books':books_sorted,
            'username': user.username,
            'phone_number': phone_verification.phone_number,
            'book_list_url': 'book_list',
            'sell_book_url': 'sell_book',
        }
    except PhoneVerification.DoesNotExist:
        context = {
            'books': books_sorted,
            'username': user.username,
            'phone_number': 'Phone number not found',
            'book_list_url': 'book_list',
            'sell_book_url': 'sell_book',
        }

    return render(request, 'landing_page.html', context)


def verify_reset_password_otp(request, phone_number):
    if request.method == 'POST':
        otp = request.POST.get('otp')

        try:
            phone_verification = PhoneVerification.objects.get(phone_number=phone_number, otp=otp)
            if phone_verification:
                return redirect('reset_password', phone_number=phone_number)
            else:
                messages.error(request, 'Invalid OTP.')
        except PhoneVerification.DoesNotExist:
            messages.error(request, 'Phone number not found.')

    return render(request, 'verify_reset_password_otp.html')


def reset_password(request, phone_number):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        try:
            phone_verification = PhoneVerification.objects.get(phone_number=phone_number)
            user = User.objects.get(username=phone_verification.username)
            user.set_password(make_password(new_password))
            user.save()

            messages.success(request, 'Password has been reset.')
            return redirect('login')
        except (PhoneVerification.DoesNotExist, User.DoesNotExist):
            messages.error(request, 'User not found.')

    return render(request, 'reset_password.html')


def logout_view(request):
    logout(request)
    return redirect('login')
