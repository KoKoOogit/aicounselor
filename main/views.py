from django.shortcuts import render, redirect
from django.contrib import messages
# from models import User, Chat_History
# import bcrypt

# Create your views here.


def signup(request):
    if not request.session.get('logged_in') or not request.session.get('username'):
        if request.method == "POST":
            email = request.POST.get('email')
            password = request.POST.get('password').encode("utf-8")
            full_name = request.POST.get('fullName')
            confirm_pass = request.POST.get('confirmPass').encode("utf-8")
            grade_level = request.POST.get('gradeLevel')
            schedules = request.POST.get('schedules')
            gpa = request.POST.get('gpa')
            course_catalog = request.POST.get('courseCatalog')
            chosen_major = request.POST.get('chosenMajor')
            college_level = request.POST.get('collegeLevel')
            extracurr_awards = request.POST.get('extraCurrAwards')
            inputs = [email, full_name, password, confirm_pass, grade_level, schedules,
                      course_catalog, chosen_major, college_level, extracurr_awards, gpa]

            if (password != confirm_pass):
                messages.error(request, "The passwords do not match!")
                return redirect('signup')

            for inp in inputs:
                if inp == '':
                    messages.error(request, "Please input all the information")
                    return redirect('signup')

            if password != '' and len(password) < 8:
                messages.error(request, "Your password must be at least")

            if "@" not in email:
                messages.error(request, "Please enter a valid email address.")

            if User.objects.filter(email=email).exists():
                messages.error(
                    request, "An account with this email already exists.  If this is you, please log in.")
                return redirect('signup')

            if User.objects.filter(full_name=full_name).exists():
                messages.error(
                    request, "An account with this username already exists.  Please pick another one.")
                return redirect('signup')

            else:
                salt = bcrypt.gensalt()
                user = User()
                user.email = email
                user.full_name = full_name
                user.password = bcrypt.hashpw(password, salt)
                user.salt = salt
                user.save()
                user.User.objects.get(full_name=full_name)
                context = {
                    'user': user
                }
                return redirect('login')

        else:
            if request.session.get('logged_in'):
                return redirect('/login')

    else:

        return redirect('dashboard')

    return render(request, 'main/signup.html',{})


def login(request):
    if not request.session.get('logged_in') or not request.session.get('full_name'):
        if request.method == "POST":
            full_name = request.POST.get('full_name')
            password = request.POST.get('password').encode("utf8")
            inputs = [full_name, password]

            for inp in inputs:
                if inp == '':
                    messages.error(
                        request, "Please input all the information.")
                    return redirect('login')

            if User.objects.filter(full_name=full_name).exists():
                saved_hashed_pass = User.objects.filter(
                    full_name=full_name).get().password.encode("utf8")[2:-1]
                saved_salt = User.objects.filter(
                    full_name=full_name).get().salt.encode("utf8")[2:-1]
                user = User.objects.filter(full_name=full_name).get()
                request.session["fullName"] = user.full_name
                request.session['logged_in'] = True

                salted_password = bcrypt.hashpw(password, saved_salt)
                if salted_password == saved_hashed_pass:
                    return redirect('dashboard')
                else:
                    messages.error(request, "Your password is incorrect.")
                    return redirect('login')

            else:
                messages.error(
                    request, "An account with this username does not exist. Please sign up.")
                return redirect('login')

        else:
            if request.session.get('logged_in'):
                return redirect('/login')

        return render(request, 'main/login.html')
    else:
        return redirect('dashboard')


def logout(request):
    if not request.session.get('logged_in') or not request.session.get('username'):
        return redirect('/login')
    else:
        request.session["fullName"] = None
        request.session['logged_in'] = False
        return redirect('/')


def home(request):
    return render(request, 'main/home.html',{})


def dashboard(request):
    if not request.session.get('logged_in'):
        return redirect('/login')
    else:
        user = User.objects.get(full_name=request.session["fullName"])

        Context = {
            'fullName': user.full_name,
        }
        return render(request, 'dashboard.html', Context)
