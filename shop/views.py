from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.mail import send_mail
from django.utils import timezone
from .models import Category_model,Product_model,Product_different_model

from .forms import SignupForm, LoginForm, OTPForm
from .models import OneTimePassword

User = get_user_model()


# -------------------------------
# Home Page
# -------------------------------
class Home(View):
    def get(self, request):
        b=Category_model.objects.all()
        v=Product_different_model.objects.all()
        return render(request, 'user/home.html',{'category':b,'product':v})



class Product(View):
    def get(self,request,i):
        b=Category_model.objects.get(id=i)
        return render(request,'user/productpage.html',{'category':b})
    
    
from django.shortcuts import get_object_or_404, render


class Get_product_details(View):
    def get(self, request, i):
        b = get_object_or_404(Product_model, id=i)
        c = Category_model.objects.all()
        return render(request, 'user/get_details.html', {
            'get': b,
            'category': c,
            
        })

    
    
class Get_product_details2(View):
    def get(self,request,i):
        b=Product_different_model.objects.get(id=i)
        c=Category_model.objects.all()
        return render(request,'user/get_details1.html',{'get':b,'category':c})

# -------------------------------
# Signup with OTP
# -------------------------------
class Signup(View):
    def get(self, request):
        form = SignupForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            otp = OneTimePassword.create_otp(user)

            send_mail(
                subject="Your Signup OTP - Ripi Foods",
                message=f"Hello {user.username}, your OTP is {otp.code}. It expires in 10 minutes.",
                from_email=None,
                recipient_list=[user.email],
                fail_silently=False,
            )

            request.session['pending_user_id'] = user.id
            messages.info(request, "We sent an OTP to your email. Please verify to activate your account.")
            return redirect('shop:verify-otp')

        messages.error(request, "Signup failed. Please correct the errors below.")
        return render(request, 'signup.html', {'form': form})


# -------------------------------
# Verify OTP
# -------------------------------
class VerifyOTP(View):
    def get(self, request):
        if 'pending_user_id' not in request.session:
            messages.warning(request, "No signup pending. Please register first.")
            return redirect('signup')
        form = OTPForm()
        return render(request, 'shop:verify_otp.html', {'form': form})

    def post(self, request):
        user_id = request.session.get('pending_user_id')
        if not user_id:
            messages.warning(request, "No signup pending. Please register first.")
            return redirect('shop:signup')

        form = OTPForm(request.POST)
        if not form.is_valid():
            return render(request, 'verify_otp.html', {'form': form})

        user = get_object_or_404(User, id=user_id)
        otp = user.otps.order_by('-created_at').first()

        if not otp or not otp.is_valid():
            messages.error(request, "OTP expired or invalid. Please resend.")
            return redirect('shop:verify-otp')

        if form.cleaned_data['code'] != otp.code:
            otp.attempts += 1
            otp.save(update_fields=['attempts'])
            messages.error(request, "Invalid OTP. Try again.")
            return render(request, 'verify_otp.html', {'form': form})

        otp.mark_used()
        user.is_active = True
        user.save(update_fields=["is_active"])
        login(request, user)
        request.session.pop('pending_user_id', None)

        messages.success(request, "Your account is verified and active. Welcome!")
        return redirect('shop:home')


# -------------------------------
# Resend OTP
# -------------------------------
class ResendOTP(View):
    COOLDOWN_SECONDS = 60
    MAX_RESENDS = 5

    def post(self, request):
        user_id = request.session.get('pending_user_id')
        if not user_id:
            messages.warning(request, "No signup pending.")
            return redirect('shop:signup')

        user = get_object_or_404(User, id=user_id)
        last = user.otps.order_by('-created_at').first()

        if last and (timezone.now() - last.last_sent_at).total_seconds() < self.COOLDOWN_SECONDS:
            messages.warning(request, "Please wait before requesting another OTP.")
            return redirect('shop:verify-otp')

        if last and last.resent_count >= self.MAX_RESENDS:
            messages.error(request, "Maximum OTP resend limit reached. Please start over.")
            return redirect('shop:signup')

        otp = OneTimePassword.create_otp(user)
        otp.resent_count = (last.resent_count + 1) if last else 0
        otp.save()

        send_mail(
            subject="Your new OTP - Ripi Foods",
            message=f"Your new OTP is {otp.code}. It expires in 10 minutes.",
            from_email=None,
            recipient_list=[user.email],
            fail_silently=False,
        )

        messages.success(request, "A new OTP has been sent.")
        return redirect('shop:verify-otp')


# -------------------------------
# Login & Logout
# -------------------------------
class Login(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if not user:
                messages.error(request, "Invalid username or password.")
                return redirect('shop:login')

            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            if user.is_superuser:
                return redirect('shop:admin-home')
            else:
                return redirect('shop:home')
        return render(request, 'login.html', {'form': form})


class Logout(View):
    def get(self, request):
        logout(request)
        messages.info(request, "You have been logged out.")
        return redirect('shop:login')


class Admin_home(View):
    def get(self, request):
        return render(request, 'admin/home.html')



