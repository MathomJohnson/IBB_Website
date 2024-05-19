from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import NewAppointment
from .models import Appointment

def calendar(request):
    return render(request, 'appointments/index.html', {})

def schedule(request):
    if request.method == "POST":
        form = NewAppointment(request.POST)

        if form.is_valid():
            n = form.cleaned_data["name"]
            e = form.cleaned_data["email"]
            a = Appointment(name=n, email=e)
            a.save()

        return HttpResponseRedirect("/appointments/")
    else:
        form = NewAppointment()
        return render(request, 'appointments/schedule.html', {"form": form})
