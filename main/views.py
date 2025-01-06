from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from models import User, ChatHistory
import bcrypt
import openai
import requests

# Create your views here.

openai.api_key = ''

user_data = ''



def process_course_catalog(file_path):
    if file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
    elif file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        raise ValueError("Unsupported file format. Use .xlsx or .csv")
    return df.to_dict(orient='records')

def score_extracurriculars(extracurriculars):
    prompt = f"""
    You are a college counselor evaluating a student's extracurricular activities. 
    Your task is to assign a score out of 350 based on the following criteria:
    - Leadership roles (e.g., club president, team captain): Up to 100 points
    - Impact (e.g., community service hours, awards, measurable achievements): Up to 100 points
    - Diversity and variety of activities (e.g., sports, arts, academic clubs): Up to 50 points
    - Consistency and commitment (e.g., years of participation, depth of involvement): Up to 50 points
    - Uniqueness or standout factor (e.g., rare or extraordinary achievements): Up to 50 points

    The extracurricular activities provided are:
    {extracurriculars}

    Return the score as in integer object and absolutely nothing else"""

    # Call OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use the appropriate model
        messages=[
            {"role": "system", "content": "You are an expert college admissions counselor."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )
    # Extract and return the response
    return response['choices'][0]['message']['content']


def signup(request):
    if not request.session.get('logged_in') or not request.session.get('username'):
        if request.method == "POST":
            email = request.POST.get('email')
            password = request.POST.get('password').encode("utf-8")
            full_name = request.POST.get('fullName')
            confirm_pass = request.POST.get('confirmPass').encode("utf-8")
            grade_level = request.POST.get('gradeLevel')
            schedules = request.POST.get('schedules')
            course_catalog = request.POST.get('courseCatalog')
            chosen_major = request.POST.get('chosenMajor')
            college_level = request.POST.get('collegeLevel')
            extracurr_awards = request.POST.get('extraCurrAwards')


            high_school_gpa_w = request.POST.get('highSchoolGPAW')
            high_school_gpa_uw = request.POST.get('highSchoolGPAUW')
            sat_reading = request.POST.get('satReading')
            sat_math = request.POST.get('satMath')
            act = request.POST.get('act')
            notes = request.POST.get('notes')
            sat = sat_reading+sat_math

            if sat/1600 > act/36:
                better = sat/1600
            else:
                better = act/36
            score = (high_school_gpa_w*100)+(better*150) + int(score_extracurriculars(extracurr_awards))

            inputs = [email, full_name, password, confirm_pass, grade_level, schedules, course_catalog, chosen_major, college_level, extracurr_awards, high_school_gpa_w, high_school_gpa_uw, sat_reading, sat_math, act, notes, score]



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
                messages.error(request, "An account with this email already exists.  If this is you, please log in.")    
                return redirect('signup') 
            
            if User.objects.filter(full_name=full_name).exists():
                messages.error(request, "An account with this username already exists.  Please pick another one.")
                return redirect('signup')
            
            else:
                course_catalog_json = process_course_catalog(course_catalog)
                user_data = {
                    "user_data": {
                        "email": email,
                        "full_name": full_name,
                        "grade_level": grade_level,
                        "schedules": schedules,
                        "chosen_major": chosen_major,
                        "college_level": college_level,
                        "extracurricular_awards": extracurr_awards,
                        "high_school_gpa": {
                            "weighted": high_school_gpa_w,
                            "unweighted": high_school_gpa_uw
                        },
                        "test_scores": {
                            "sat_reading": sat_reading,
                            "sat_math": sat_math,
                            "act": act
                        },
                        "notes": notes
                    },
                    "course_catalog": course_catalog_json
                }




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
                return redirect('dashboard')
    
    else:

        return redirect('dashboard')
    
    return render(request, 'auth/signup.html')

            

def login(request):
    if not request.session.get('logged_in') or not request.session.get('full_name'):
        if request.method == "POST":
            email = request.POST.get('email')
            password = request.POST.get('password').encode("utf8")
            inputs = [email, password]

            for inp in inputs:
                if inp == '':
                    messages.error(request, "Please input all the information.")
                    return redirect('login')

            

            if User.objects.filter(email=email).exists():
                saved_hashed_pass = User.objects.filter(email=email).get().password.encode("utf8")[2:-1]
                saved_salt = User.objects.filter(email=email).get().salt.encode("utf8")[2:-1]
                user  = User.objects.filter(email=email).get()
                request.session["email"] = user.email
                request.session['logged_in'] = True
            
                salted_password = bcrypt.hashpw(password, saved_salt)
                if salted_password == saved_hashed_pass:
                    return redirect('dashboard')
                else:
                    messages.error(request, "Your password is incorrect.")
                    return redirect('login')

            else:
                messages.error(request, "An account with this email does not exist. Please sign up.")
                return redirect('signup')

        else:
            if request.session.get('logged_in'):
                return redirect('login')

        return render(request, 'login.html')
    else:
        return redirect('dashboard')

def logout(request):
    if not request.session.get('logged_in') or not request.session.get('email'):
        return redirect('login')
    else:
        request.session["fullName"] = None
        request.session['logged_in'] = False
        return redirect('home')



def home(request):
        return render(request, 'home.html')


@csrf_exempt
def chat_tutor(request):
    
    if request.method == 'POST':

        user_message = request.POST.get('message')
        subject = request.POST.get('subject')

        message_schedule = [
        {
            "role": "system",
            "content": f'''
            You are a tutor in {subject}. answer all of the student's questions to the best of your ability with the most accurate information.
            ''' 
        }
        ]

        if not user_message or not subject:
            return JsonResponse({"error": "Both subject and message are required"}, status=400)
        
        prompt = f"Subject: {subject}\nUser Message: {user_message}\nResponse:"

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )

            chatgpt_response = response.choices[0].messages.content

            return JsonResponse({"response": chatgpt_response})
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)
    

@csrf_exempt
def chat_normal(request):
    user = User.objects.get(email=request.session["email"])
    normal_chat_history = NormalChatHistory.objects.get(user=user)
    schedule_chat_history_chat_history = SchedChatHistory.objects.get(user=user)
    message_schedule = [
        {
            "role": "system",
            "content": '''
            
            You are a college counselor with provided data, chat with students, and do your best to help them get into the college and major of their choice. 
            If they ask about scheduling or extracurriculars, tell them to visit the schedule planning page on the website. 
            If talk about doing basly in certain classes, or talk about needing help, urge them to visit the tutoring page on the website. 
            If they need help on their application essay, tell them to check the essay help page on the site.
            If they are currently applying to colleges, tell them to visit the application management page on the site.

            

            Here is some information about the student, including their previous school schedules, and preformance, their other extracurriculars, their test scores, thir major of choice, course catalog etc. Additionally, you will be provided with their previous chats with you.
            ''' + user_data + normal_chat_history + schedule_chat_history
        }
    ]
    if request.method == 'POST':

        user_message = request.POST.get('message')
        subject = request.POST.get('subject')

        if not user_message or not subject:
            return JsonResponse({"error": "Both subject and message are required"}, status=400)
        
        prompt = f"Subject: {subject}\nUser Message: {user_message}\nResponse:"

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )

            chatgpt_response = response.choices[0].messages.content

            return JsonResponse({"response": chatgpt_response})
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def chat_schedule(request):
    user = User.objects.get(email=request.session["email"])
    normal_chat_history = NormalChatHistory.objects.get(user=user)
    schedule_chat_history_chat_history = SchedChatHistory.objects.get(user=user)
    message_schedule = [
        {
            "role": "system",
            "content": '''
            
            You are a college counselor that specifically helps high school student plan and schedule their high school lives.  
            You are to suggest a high school course schedule of 6 classes, extracurriculars, competitions, and summer activities
            to best help students get accepted to their college of their choice.  Use the information about the student's previous
            performance and other data that will be supplied.

            Return the data in JSON format in a structure like this:

            {
            "message": "Encouraging message or advice to the student about their goals and plan.",
            "courses": [
                {"p1": "First course choice"},
                {"p2": "Second course choice"},
                {"p3": "Third course choice"},
                {"p4": "Fourth course choice"},
                {"p5": "Fifth course choice"},
                {"p6": "Sixth course choice"}
            ],
            "extracurriculars": [
                "List of suggested extracurricular activities"
            ],
            "competitions": [
                "List of suggested competitions to participate in"
            ],
            "summer_activities": [
                "List of suggested summer activities"
            ]
            }

            Here is some information about the student, including their previous school schedules, and preformance, their other extracurriculars, their test scores, thir major of choice, course catalog etc. Additionally, you will be provided with their previous chats with you.
            ''' + user_data + normal_chat_history + schedule_chat_history
        }
    ]

    if request.method == 'POST':

        user_message = request.POST.get('message')
        subject = request.POST.get('subject')

        if not user_message or not subject:
            return JsonResponse({"error": "Both subject and message are required"}, status=400)
        
        prompt = f"Subject: {subject}\nUser Message: {user_message}\nResponse:"

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )

            chatgpt_response = response.choices[0].messages.content

            return JsonResponse({"response": chatgpt_response})
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def chat_essay(request):
   
    if request.method == 'POST':

        user_message = request.POST.get('message')
        prompt = request.POST.get('prompt')

        

        if not user_message or not subject:
            return JsonResponse({"error": "Both subject and message are required"}, status=400)
        
        prompt = f"Subject: {subject}\nUser Message: {user_message}\nResponse:"

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )

            chatgpt_response = response.choices[0].messages.content

            return JsonResponse({"response": chatgpt_response})
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)


def dashboard(request):
    if not request.session.get('logged_in'):
        return redirect('/login')
    else:
        user = User.objects.get(full_name=request.session["fullName"])
        
        Context = {
            'fullName': user.full_name,
        }
        return render(request, 'dashboard.html', Context)

