from django.shortcuts import render
from django.utils import timezone
# Create your views here.


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Key, KeyHistory
from django.http import HttpResponse
from django.shortcuts import render
from .models import KeyHistory

def view_reports(request):
    # Получаване на всички записи за историята
    query = KeyHistory.objects.all().order_by('-issued_at')

    # Филтри от GET заявката
    key_name = request.GET.get('key_name', '')
    username = request.GET.get('username', '')

    # Прилагане на филтъра
    if key_name:
        query = query.filter(key__name__icontains=key_name)
    if username:
        query = query.filter(user__username__icontains=username)

    # Рендериране на шаблона
    return render(request, 'keys/reports.html', {
        'reports': query,
        'key_name': key_name,
        'username': username
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
