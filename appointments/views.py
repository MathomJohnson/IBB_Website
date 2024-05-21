from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from .forms import NewAppointment
from .models import Appointment
from django.core.mail import send_mail
from django.conf import settings
import json
from .models import Meeting

def calendar(request):
    return render(request, 'appointments/index.html', {})



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
