from django.shortcuts import render , redirect
from django.contrib.auth import authenticate , login , logout , update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm , UserChangeForm , PasswordChangeForm
from django.contrib import messages
from . forms import SignUpForm , EditProfileForm , ChangedPassword

# Create your views here.
def home(request):
    return render(request,'authenticate/home.html',{})

def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,('You have been Logged in !'))
            return redirect('home')
        else:
            messages.success(request,('Error Logging In - Please try again !'))
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html',{})

def logout_user(request):
    logout(request)
    messages.success(request,('You Have Been Logged Out!'))
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST) # set our form as usercreation form and pass in whatever they posted
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(request,username=username,password=password)
            login(request,user)
            messages.success(request,('You have been Registered !'))
            return redirect('home')
    else:
        form = SignUpForm()
    context = {'form' : form}
    return render(request,'authenticate/register.html',context)


def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST,instance=request.user) # set our form as usercreation form and pass in whatever they posted
        if form.is_valid():
            form.save()
            messages.success(request,('You Have Edited Your Profile!'))
            return redirect('home')
    else:
        form = EditProfileForm(instance=request.user) #instance = passes the user info which is in database
    context = {'form' : form}

    return render(request,'authenticate/edit_profile.html',context)


def change_password(request):
    if request.method == 'POST':
        form = ChangedPassword(data=request.POST,user=request.user) # set our form as usercreation form and pass in whatever they posted
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            messages.success(request,('You Have Edited Your Password!'))
            return redirect('home')
    else:
        form = ChangedPassword(user=request.user) #instance = passes the user info which is in database
    context = {'form' : form}

    return render(request,'authenticate/change_password.html',context)





