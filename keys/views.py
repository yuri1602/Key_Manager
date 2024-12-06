
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.dateparse import parse_date
from django.utils import timezone
from django.http import HttpResponse
from .models import Key, KeyHistory
from django.contrib import messages

def view_reports(request):
    # Всички записи за историята
    reports = KeyHistory.objects.all().order_by('-issued_at')

    # Получаване на данни от GET параметрите
    user_id = request.GET.get('user_id', '')
    key_barcode = request.GET.get('key_barcode', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    # Прилагане на филтри
    if user_id:
        reports = reports.filter(user__id=user_id)
    if key_barcode:
        reports = reports.filter(key__barcode__icontains=key_barcode)
    if start_date:
        reports = reports.filter(issued_at__date__gte=parse_date(start_date))
    if end_date:
        reports = reports.filter(issued_at__date__lte=parse_date(end_date))

    # Подаване на параметри и резултати към шаблона
    return render(request, 'keys/reports.html', {
        'reports': reports,
        'users': User.objects.all(),
        'user_id': user_id,
        'key_barcode': key_barcode,
        'start_date': start_date,
        'end_date': end_date,
    })


def main_page(request):
    return render(request, 'keys/main_page.html')


def create_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if not username or not password:
            messages.error(request, "Username and password are required.")
            return redirect('create_user')

        # Създаване на нов потребител
        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            messages.success(request, "User created successfully!")
            return redirect('main_page')
        except Exception as e:
            messages.error(request, f"Error creating user: {e}")
            return redirect('create_user')

    return render(request, 'keys/create_user.html')

def issue_key(request):
    if request.method == 'POST':
        print("POST Data:", request.POST)  # Печата всички изпратени данни

        # Извличане на данни от POST
        user_id = request.POST.get('user')  # Получаване на ID на потребителя
        barcode = request.POST.get('barcode')  # Получаване на баркода на ключа
        print("User ID:", user_id)  # Печата ID-то на потребителя
        print("Barcode:", barcode)  # Печата баркода

        # Проверка дали са предоставени всички необходими данни
        if not user_id or not barcode:
            return HttpResponse("User ID or barcode not provided.", status=400)

        # Проверка дали съществуват ключът и потребителят
        user = get_object_or_404(User, id=user_id)
        key = get_object_or_404(Key, barcode=barcode)

        # Проверка дали ключът вече е издаден
        if key.is_issued:
            return HttpResponse("This key is already issued.", status=400)

        # Издаване на ключа
        key.is_issued = True
        key.issued_to = user
        key.issued_at = timezone.now()
        key.save()

        # Създаване на запис в историята
        KeyHistory.objects.create(key=key, user=user, issued_at=key.issued_at)

        return HttpResponse("Key issued successfully!")

    # Обработка на GET заявка (показване на формуляра)
    users = User.objects.all()
    return render(request, 'keys/issue_key.html', {'users': users})


def return_key(request):
    if request.method == 'POST':
        barcode = request.POST.get('barcode')

        key = get_object_or_404(Key, barcode=barcode)

        if not key.is_issued:
            return HttpResponse("This key is not issued.")

        key_history = KeyHistory.objects.filter(key=key, returned_at__isnull=True).first()
        key_history.returned_at = timezone.now()
        key_history.save()

        key.is_issued = False
        key.issued_to = None
        key.issued_at = None
        key.save()

        return HttpResponse("Key returned successfully!")

    return render(request, 'keys/return_key.html')
