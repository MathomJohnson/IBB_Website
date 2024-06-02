from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from .forms import NewAppointment
from django.core.mail import send_mail
from django.conf import settings
import json
from .models import Meeting, GoogleToken
import os
from dotenv import load_dotenv
import requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build


# Load environment variables from .env file
load_dotenv()

def calendar(request):
    if request.user.is_authenticated:
        user_email = request.user.email
    else:
        user_email = ''
    return render(request, 'appointments/index.html', {
        "user_email":user_email,
        "client_id":os.getenv("ZOOM_CLIENT_ID"),
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



def google_login(request):
    flow = Flow.from_client_config(
        client_config={
            "web": {
                "client_id": "",
                "client_secret": "",
                "redirect_uris": ["http://localhost:8000/calendar/oauth2callback"],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=['https://www.googleapis.com/auth/calendar'],
    )
    flow.redirect_uri = "http://localhost:8000/calendar/oauth2callback"

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
    )

    request.session['state'] = state
    return HttpResponseRedirect(authorization_url)

def oauth2callback(request):
    #state = request.session['state']

    flow = Flow.from_client_config(
        client_config={
            "web": {
                "client_id": "",
                "client_secret": "",
                "redirect_uris": ["http://localhost:8000/calendar/oauth2callback"],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
            }
        },
        scopes=['https://www.googleapis.com/auth/calendar'],
        #state=state,
    )
    flow.redirect_uri = "http://localhost:8000/calendar/oauth2callback"


    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials

    print("--------------------------------")
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print(credentials.token)
    print(credentials.refresh_token)
    print(credentials.token_uri)
    print(credentials.expiry)

    return HttpResponseRedirect("/")

def setup_google_meet(request):
    if request.method == "POST":
        user_email = request.POST.get("user_email").strip()
        topic = request.POST.get("topic").strip()
        mentor = request.POST.get("mentor").strip()
        event_id = request.POST.get("event-id")
        club_email = os.getenv('EMAIL_HOST_USER')

        event = Meeting.objects.get(id=event_id)
        event.delete()
    # print("#################################")
    # print(os.getenv("GOOGLE_ACCESS_TOKEN"))
    # new_access_token = refresh_access_token(os.getenv("GOOGLE_REFRESH_TOKEN"))
    # print(new_access_token)
    # print("####################################")
    token = GoogleToken.objects.get(id=1)
    credentials = Credentials(
        token=token.access_token,
        refresh_token=token.refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id="",
        client_secret="",
        #scopes=token_data.scopes.split(",")
    )

    service = build('calendar', 'v3', credentials=credentials)

    event = {
        'summary': 'Mathomsssssss',
        'description': 'A meeting with your mentor',
        'start': {
            'dateTime': '2024-06-07T16:20:00-05:00',
            'timeZone': 'America/Chicago',
        },
        'end': {
            'dateTime': '2024-06-07T16:50:00-05:00',
            'timeZone': 'America/Chicago',
        },
        'conferenceData': {
            'createRequest': {
                'requestId': 'some-random-string'
            }
        },
        'attendees': [
            {'email': 'mgjohnson8@wisc.edu'},
            {'email': 'mathomjohnson57@gmail.com'},
        ],
    }

    event = service.events().insert(
        calendarId='internationalbadgerbonds@gmail.com',
        body=event,
        conferenceDataVersion=1,
    ).execute()

    # Send email to mentee with the meeting link
    meeting_link = event['hangoutLink']
    print("meeting link: " + meeting_link)
    return HttpResponseRedirect("/")


def refresh_access_token(refresh_token):
    client_id = ""
    client_secret = ""
    token_uri = "https://oauth2.googleapis.com/token"

    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
    }

    response = requests.post(token_uri, data=data)

    if response.status_code == 200:
        tokens = response.json()
        new_access_token = tokens['access_token']
        return new_access_token
    else:
        raise Exception("Failed to refresh access token: " + response.text)





def setup_meeting(request):
    if request.method == "POST":
        user_email = request.POST.get("user_email").strip()
        topic = request.POST.get("topic").strip()
        mentor = request.POST.get("mentor").strip()
        event_id = request.POST.get("event-id")
        club_email = os.getenv('EMAIL_HOST_USER')

        event = Meeting.objects.get(id=event_id)
        event.delete()

        #####################
        try:
            access_token = os.getenv("ZOOM_ACCESS_TOKEN")
            refresh_token = os.getenv("ZOOM_REFRESH_TOKEN")


            token_url = 'https://zoom.us/oauth/token'
            payload = {
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
                'client_id': "2ffE_XoiQomWyzT8rOGoA",
                'client_secret': "72BV5V6aWwB5YKh2U2owwsPK38U1qNL4"
            }

            response = requests.post(token_url, data=payload)
            response_data = response.json()

            if response.status_code == 200:
                new_access_token = response_data['access_token']
                #token_data.refresh_token = response_data['refresh_token']
                print("******************************")
                print(new_access_token)
            else:
                raise Exception("Failed to refresh token: " + response_data.get('error', 'Unknown error'))
        except Exception as e:
            raise Exception("Error refreshing token: " + str(e))
        #####################

        create_meeting_url = 'https://api.zoom.us/v2/users/internationalbadgerbonds@gmail.com/meetings'
    
        headers = {
            'Authorization': f'Bearer {new_access_token}',
            'Content-Type': 'application/json'
        }
        meeting_details = {
            "topic": "My Meeting",
            "type": 2,
            "start_time": "2024-06-23T10:00:00Z",  # Replace with actual start time
            "duration": 60,
            "timezone": "UTC",
            "password": "123456",
            "agenda": "Discuss project updates",
            "settings": {
                "host_video": True,
                "participant_video": False,
                "join_before_host": True,
                "mute_upon_entry": False,
                "watermark": False,
                "use_pmi": False,
                "approval_type": 2,
                "audio": "both",
                "auto_recording": "cloud",
            }
        }

        response = requests.post(create_meeting_url, headers=headers, data=json.dumps(meeting_details))

        if response.status_code == 201:
            meeting_info = response.json()
            print(meeting_info)
            return HttpResponseRedirect('/calendar/')
        else:
            return HttpResponse(f"Failed to create meeting: {response.content}", status=response.status_code)

        #####################


        #Email code here
        # send_mail(
        #     'Meeting on ',
        #     'content',
        #     club_email,
        #     [user_email],
        # )

        
    

# def zoom_callback(request):
#     code = request.GET.get('code')
#     if not code:
#         return HttpResponse("Error: No code parameter found in the callback.", status=400)

#     # Exchange the authorization code for an access token
#     token_url = 'https://zoom.us/oauth/token'
#     client_id = ''
#     client_secret = ''
#     redirect_uri = 'http://localhost:8000/calendar/zoom/'

#     payload = {
#         'grant_type': 'authorization_code',
#         'code': code,
#         'redirect_uri': redirect_uri
#     }

#     # Use HTTPBasicAuth to encode the client ID and secret
#     auth = HTTPBasicAuth(client_id, client_secret)

#     response = requests.post(token_url, data=payload, auth=auth)

#     # Debugging: Print the response content to see if there's an error message
#     print("Response status code:", response.status_code)
#     print("Response content:", response.content)

#     if response.status_code == 200:
#         token_data = response.json()
#         access_token = token_data.get('access_token')
#         refresh_token = token_data.get('refresh_token')
#         return HttpResponse(f"Access token: {access_token}<br>Refresh token: {refresh_token}")
#     else:
#         return HttpResponse(f"Error fetching token: {response.content}", status=response.status_code)


# def mentor_zoom_auth(request):
#     authorization_url = 'https://zoom.us/oauth/authorize?client_id=2ffE_XoiQomWyzT8rOGoA&response_type=code&redirect_uri=http://localhost:8000/calendar/&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fcalendar%2F'
#     return HttpResponseRedirect(authorization_url)

