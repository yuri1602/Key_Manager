
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.dateparse import parse_date
from django.utils import timezone
from django.http import HttpResponse
from .models import Key, KeyHistory
from django.http import JsonResponse
from django.contrib.auth import get_user_model


#v.1.1 Добавяне на търсачка за потребители по име (AJAX): Създаваме view, което ще връща списък с потребители според въведения текст.
User = get_user_model()

def search_users(request):
    query = request.GET.get('query', '')
    users = User.objects.filter(username__icontains=query).values('id', 'username', 'nfc_id')[:10]
    return JsonResponse({'users': list(users)})




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

#v.1.1 Логика за издаване на ключове: Модифицираме съществуващото view за издаване на ключа, за да обработва както баркод, така и търсене.
def issue_key(request):
    if request.method == 'POST':
        key_barcode = request.POST.get('key_barcode')
        user_barcode = request.POST.get('user_barcode')

        # Намиране на ключа
        key = get_object_or_404(Key, barcode=key_barcode)

        # Намиране на потребителя
        user = None
        if user_barcode:
            user = User.objects.filter(id=user_barcode).first()

        if not user:
            return render(request, 'keys/issue_key.html', {'error': 'User not found.'})

        if key.is_issued:
            return render(request, 'keys/issue_key.html', {'error': 'Key is already issued.'})

        # Издаване на ключа
        key.is_issued = True
        key.issued_to = user
        key.issued_at = timezone.now()
        key.save()

        # Запис в историята
        KeyHistory.objects.create(key=key, user=user, issued_at=key.issued_at)

        return render(request, 'keys/issue_key.html', {'success': 'Key issued successfully!'})

    return render(request, 'keys/issue_key.html')


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
