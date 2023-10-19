import base64
from io import BytesIO
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django_otp.plugins.otp_totp.models import TOTPDevice
# from django_otp.plugins.otp_totp.views import TOTPView
import qrcode
from django.contrib import auth
from .models import UserProfile, User


def home(request):
    totp_device = TOTPDevice.objects.filter(user=request.user).first()
    if totp_device is None:
        print(totp_device, '444444')
    
    return render(request, 'home.html', {'totp_device': totp_device})


@login_required
def activate_2fa(request):

    if TOTPDevice.objects.filter(user=request.user).exists():
        return redirect(reverse('home'))
    
    totp_device = TOTPDevice.objects.create(user=request.user)

    qr_code_img = qrcode.make(totp_device.config_url)
    buffer = BytesIO()
    qr_code_img.save(buffer)
    buffer.seek(0)
    encoded_img = base64.b64encode(buffer.read()).decode()
    qr_code_data = f'data:image/png;base64,{encoded_img}'
    
    return render(request, 'activate_2fa.html', {'qr_code_data': qr_code_data})


def login(request):

    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':

        username = request.POST.get('username')
        senha = request.POST.get('senha')
        
        user = auth.authenticate(request, username=username, password=senha)
        auth.login(request, user)

        user_device = TOTPDevice.objects.filter(user=request.user).exists()

        if user_device:
            return redirect(reverse('verify_2fa'))
        else:
            user = auth.authenticate(request, username=username, password=senha)
            auth.login(request, user)

            return redirect(reverse('home'))
        
        # if user is not None:
        #     auth.login(request, user)
        #     return HttpResponse('ESTA LOGADO NA HOME')


@login_required
def deactivate_2fa(request):
    TOTPDevice.objects.filter(user=request.user).delete()
    return redirect(reverse('home'))


@login_required
def verify_2fa(request):
    user = request.user
    totp_device = TOTPDevice.objects.get(user=user)
    # totp_device = get_object_or_404(TOTPDevice, user=user)
    
    if request.method == 'POST':
        code = request.POST.get('code')
        if totp_device.verify_token(code):
            # O código inserido é válido
            return redirect(reverse('home'))
        else:
            return HttpResponse('codigo invalido')
    
    return render(request, 'verify_2fa.html')


# def logout(request):
#     auth.logout(request)
#     return redirect('index')