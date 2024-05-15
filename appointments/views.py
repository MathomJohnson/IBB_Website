from django.shortcuts import render

def calendar(request):
    return render(request, 'appointments/index.html', {})
