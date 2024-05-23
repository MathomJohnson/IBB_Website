from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from .forms import NewAppointment
from .models import Appointment
from django.core.mail import send_mail
from django.conf import settings
import json
from .models import Meeting
import os
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth


# Load environment variables from .env file
load_dotenv()

def calendar(request):
    if request.user.is_authenticated:
        user_email = request.user.email
    else:
        user_email = ''
    return render(request, 'appointments/index.html', {
        "user_email":user_email
    })



#@csrf_exempt  # Only use this for development, for production use proper CSRF handling
def add_event(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data['occasion']
            time = data['start_time']
            year = data['year']
            month = data['month']
            day = data['day']
            
            event = Meeting(mentor=name, time=time, year=year, month=month, day=day)
            event.save()
            print("===================")
            print(event.id)
            return JsonResponse({'status': 'success'}, status=201)
        except (KeyError, TypeError, ValueError) as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


def get_events(request):
    if request.method == 'GET':
        year = request.GET.get('year')
        month = request.GET.get('month')
        day = request.GET.get('day')
        
        events = Meeting.objects.all()
        if year and month and day:
            events = events.filter(year=year, month=month, day=day)
        
        event_list = list(events.values())
        
        return JsonResponse({'status': 'success', 'events': event_list}, status=200)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
    

def delete_event(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        print("--------------------------------------------")
        print(event_id)
        try:
            event = Meeting.objects.get(id=event_id)
            event.delete()
            return JsonResponse({'success': True})
        except Meeting.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Event does not exist.'})
    return JsonResponse({'success': False, 'error': 'Invalid request.'})


def setup_meeting(request):
    if request.method == "POST":
        user_email = request.POST.get("user_email").strip()
        topic = request.POST.get("topic").strip()
        mentor = request.POST.get("mentor").strip()
        event_id = request.POST.get("event-id")
        club_email = os.getenv('EMAIL_HOST_USER')
        #Email code here
        send_mail(
            'Meeting on ',
            'content',
            club_email,
            [user_email],
        )

        event = Meeting.objects.get(id=event_id)
        event.delete()

        return HttpResponseRedirect("/calendar/")
    

def zoom_callback(request):
    code = request.GET.get('code')
    if not code:
        return HttpResponse("Error: No code parameter found in the callback.", status=400)

    # Exchange the authorization code for an access token
    token_url = 'https://zoom.us/oauth/token'
    client_id = ''
    client_secret = ''
    redirect_uri = 'http://localhost:8000/calendar/zoom/'

    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri
    }

    # Use HTTPBasicAuth to encode the client ID and secret
    auth = HTTPBasicAuth(client_id, client_secret)

    response = requests.post(token_url, data=payload, auth=auth)

    # Debugging: Print the response content to see if there's an error message
    print("Response status code:", response.status_code)
    print("Response content:", response.content)

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get('access_token')
        refresh_token = token_data.get('refresh_token')
        return HttpResponse(f"Access token: {access_token}<br>Refresh token: {refresh_token}")
    else:
        return HttpResponse(f"Error fetching token: {response.content}", status=response.status_code)



def schedule(request):
    if request.method == "POST":
        form = NewAppointment(request.POST)

        if form.is_valid():
            n = form.cleaned_data["name"]
            e = form.cleaned_data["email"]
            a = Appointment(name=n, email=e)
            a.save()

            send_mail(
                'django success',
                'Hello ' + n + '! you are cool.',
                'mathomjohnson57@gmail.com',
                [e],
            )

        return HttpResponseRedirect("/appointments/")
    else:
        form = NewAppointment()
        return render(request, 'appointments/schedule.html', {"form": form})
