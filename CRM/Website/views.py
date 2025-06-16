from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from .forms import *
from .models import Record
from .utils import generate_verification_code, send_verification_email
from django.contrib.auth.models import User
from django.core.cache import cache

# Create your views here.
def home(request):
    records=Record.objects.all()
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            records=Record.objects.all()
            # Set session data
            messages.success(request, 'There you GOOO!! . You are now logged in')
            return render(request, 'home.html',{'records':records})
        else:    
            messages.error(request, '!!Holy Cow!! Wrong credentials.')
            return render(request, 'home.html')

    return render(request, 'home.html', {'records':records})


def all_records(request):
    records=Record.objects.all()
    return render(request, 'all_records.html', {'records':records})




def logout_user(request):
    if request.user.is_authenticated:
        # # Clear all session data
        # request.session.flush()
        # # Delete the session cookie
        # if 'sessionid' in request.COOKIES:
        #     response = render(request, 'home.html')
        #     response.delete_cookie('sessionid')
        #     logout(request)
        #     messages.success(request, 'Bye Bye, You are logged out')
        #     return response
        logout(request)
        messages.success(request, 'Bye Bye, You are logged out')
        return render(request, 'home.html')
    return render(request,"home.html")



def verify_email_step(request):
    """First step of registration: Email verification"""
    email_form = EmailVerificationForm()
    otp_form = OTPVerificationForm()
    
    if request.method == 'POST':
        if 'email' in request.POST:
            # First step: Send OTP
            email_form = EmailVerificationForm(request.POST)
            if email_form.is_valid():
                email = email_form.cleaned_data['email']
                # Check if email already exists
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'This email is already registered.')
                    return render(request, 'verify_email_step.html', {
                        'email_form': email_form,
                        'otp_form': otp_form,
                        'otp_sent': False
                    })
                
                # Generate and send OTP
                verification_code = generate_verification_code()
                if send_verification_email(email, verification_code):
                    # Store email and OTP in session
                    request.session['pending_email'] = email
                    request.session['verification_code'] = verification_code
                    # messages.success(request, 'Verification code sent to your email.')
                    return render(request, 'verify_email_step.html', {
                        'email_form': email_form,
                        'otp_form': otp_form,
                        'otp_sent': True,
                        'email': email
                    })
                else:
                    messages.error(request, 'Failed to send verification code. Please try again.')
        else:
            # Second step: Verify OTP
            otp_form = OTPVerificationForm(request.POST)
            if otp_form.is_valid():
                entered_otp = otp_form.cleaned_data['otp']
                stored_otp = request.session.get('verification_code')
                email = request.session.get('pending_email')
                
                if entered_otp == stored_otp:
                    # OTP is correct, proceed to registration form
                    request.session['email_verified'] = True
                    return redirect('register')
                else:
                    messages.error(request, 'Invalid verification code. Please try again.')
    
    return render(request, 'verify_email_step.html', {
        'email_form': email_form,
        'otp_form': otp_form,
        'otp_sent': False
    })

def register_user(request):
    """Second step of registration: User details and password"""
    # Check if email is verified
    if not request.session.get('email_verified'):
        messages.error(request, 'Please verify your email first.')
        return redirect('verify_email_step')
    
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Set the email from the verified email
            form.instance.email = request.session.get('pending_email')
            user = form.save()
            
            # Clear session data
            request.session.pop('pending_email', None)
            request.session.pop('verification_code', None)
            request.session.pop('email_verified', None)
            
            # Log the user in
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    
    return render(request, 'register.html', {'form': form})

def add_record(request):
	# form = Addrecords(request.POST or None)
	# if request.user.is_authenticated:
	# 	if request.method == "POST":
	# 		if form.is_valid():
	# 			form.save()
	# 			messages.success(request, "Record Added...")
	# 			return redirect('home')
	# 	return render(request, 'addrecord.html', {'form':form})
	# else:
	# 	messages.success(request, "You Must Be Logged In...")
	# 	return redirect('home')
    form = Addrecords(request.POST, request.FILES)
    if request.user.is_authenticated:
        if request.method == "POST": 
            if form.is_valid():
                form.save()
                messages.success(request, "Record Added...")
                return redirect('home')
            else:
                messages.error(request, "Please correct the errors below.")
        else:
            form = Addrecords()
        return render(request, 'addrecord.html', {'form': form})
    else:
        messages.error(request, "You Must Be Logged In...")
        return redirect('home')	

def customer_record(request, pk):
    if request.user.is_authenticated:
        # Get the search ID from query parameters
        search_id = request.GET.get('pk')
        if search_id:
            try:
                customer_record = Record.objects.get(id=search_id)
                messages.success(request, "✅ User Found ✅")
                return render(request, 'record.html', {'customer_record': customer_record})
            except Record.DoesNotExist:
                messages.error(request, "❌ !!No User found!! ❌")
                return redirect('home')
        else:
            # If no search ID, use the pk from URL
            try:
                customer_record = Record.objects.get(id=pk)
                return render(request, 'record.html', {'customer_record': customer_record})
            except Record.DoesNotExist:
                messages.error(request, "❌ !!No User found!! ❌")
                return redirect('home')
    else:
        messages.error(request, "You Must Be Logged In...")
        return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated:
        try:
            record = Record.objects.get(id=pk)
            record.delete()
            messages.success(request, "Record Deleted...")
            return redirect('home')
        except Record.DoesNotExist:
            messages.error(request, "Record not found...")
            return redirect('home')
    else:
        messages.error(request, "You Must Be Logged In To Do That...")
        return redirect('home')
    

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        if request.method == "POST":
            form = Addrecords(request.POST, request.FILES, instance=current_record)
            if form.is_valid():
                form.save()
                messages.success(request, "Record Has Been Updated!")
                return redirect('home')
            else:
                messages.error(request, "Please correct the errors below.")
        else:
            form = Addrecords(instance=current_record)
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.error(request, "You Must Be Logged In...")
        return redirect('home')

def search_user(request, pk=None):
    if not request.user.is_authenticated:
        messages.error(request, "You Must Be Logged In...")
        return redirect('home')
    
    # If pk is provided in URL, redirect directly to record
    if pk is not None:
        try:
            record = Record.objects.get(id=pk)
            return redirect('record', pk=record.id)
        except Record.DoesNotExist:
            messages.error(request, "Record not found.")
            return redirect('home')
            
    return redirect('home')
    
                     