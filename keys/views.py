from django.shortcuts import render, get_object_or_404, redirect
<<<<<<< HEAD
=======
from django.contrib.auth.models import User
>>>>>>> parent of 842cfad (Update views.py)
from django.db.models import Q
from django.utils.dateparse import parse_date
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from .models import Key, KeyHistory

<<<<<<< HEAD
# Получаваме правилния потребителски модел
User = get_user_model()

=======
>>>>>>> parent of 842cfad (Update views.py)
def view_reports(request):
    reports = KeyHistory.objects.all().order_by('-issued_at')

    user_id = request.GET.get('user_id', '')
    key_barcode = request.GET.get('key_barcode', '')
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    if user_id:
        reports = reports.filter(user__id=user_id)
    if key_barcode:
        reports = reports.filter(key__barcode__icontains=key_barcode)
    if start_date:
        reports = reports.filter(issued_at__date__gte=parse_date(start_date))
    if end_date:
        reports = reports.filter(issued_at__date__lte=parse_date(end_date))

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


def issue_key(request):
    if request.method == 'POST':
        barcode = request.POST.get('barcode')
        user_id = request.POST.get('user_id')

        key = get_object_or_404(Key, barcode=barcode)
        user = get_object_or_404(User, id=user_id)

        if key.is_issued:
            return HttpResponse("This key is already issued.")

        key.is_issued = True
        key.issued_to = user
        key.issued_at = timezone.now()
        key.save()

        KeyHistory.objects.create(key=key, user=user, issued_at=key.issued_at)

        return HttpResponse("Key issued successfully!")

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
