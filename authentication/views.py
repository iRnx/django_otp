import base64
from io import BytesIO
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.contrib import auth
import qrcode
from django.db.models import Q
from .models import UserProfile, User
from .utils import criar_qr_code


def teste(request):
    totp_device = TOTPDevice.objects.filter(user=request.user, confirmed=True).first()
   
    if not totp_device is None:
        return render(request, 'teste.html', {'totp_device': totp_device, 'confirmed': True})
    else:
        return render(request, 'teste.html', {'totp_device': totp_device})


def home(request):
    return render(request, 'home.html')


@login_required
def activate_2fa(request):
    # # Parei aqui

    if TOTPDevice.objects.filter(user=request.user, confirmed=True).exists():
        print('1aqui')
        return render(request, 'partials/_gostaria_de_desativar.html')
    
    if not TOTPDevice.objects.filter(user=request.user, confirmed=False).exists():
        totp_device = TOTPDevice.objects.create(user=request.user, confirmed=False)
    
    totp_device = TOTPDevice.objects.filter(user=request.user).first()

    qr_code_data = criar_qr_code(totp_device.config_url)

    if request.method == 'POST':
        code = request.POST.get('code')
        if totp_device.verify_token(code):
            totp_device.confirmed = True
            totp_device.save()
            return render(request, 'partials/_conta_ativada.html')
        else:
            return HttpResponse('codigo invalido')

    return render(request, 'activate_2fa.html', {'qr_code_data': qr_code_data})


def login(request):

    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':

        username = request.POST.get('username')
        senha = request.POST.get('senha')
        
        user = auth.authenticate(request, username=username, password=senha)
        auth.login(request, user)

        user_device = TOTPDevice.objects.filter(user=request.user, confirmed=True).exists()

        if user_device:
            return redirect(reverse('verify_2fa'))
        

        return render(request, 'home.html')
        

@login_required
def deactivate_2fa(request):
    TOTPDevice.objects.filter(user=request.user).delete()
    return redirect(reverse('home'))


@login_required
def verify_2fa(request):
    user = request.user
    totp_device = TOTPDevice.objects.filter(user=user).first()
    
    if request.method == 'POST':
        code = request.POST.get('code')
        if totp_device.verify_token(code):
            totp_device.confirmed = True
            totp_device.save()
            return redirect(reverse('home'))
        else:
            return HttpResponse('codigo invalido')
    
    return render(request, 'verify_2fa.html')


# def logout(request):
#     auth.logout(request)
#     return redirect('index')