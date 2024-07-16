from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Question

# Create your views here.
def main_forum(request):
    questions = Question.objects.all()
    return render(request, "forum/forums.html", {
        'questions': questions,
    })

def submit_question(request):
    if request.method == "POST":
        title = request.POST.get("title").strip()
        content = request.POST.get("body").strip()
        author = request.user

        question = Question(title=title, body=content, author=author)
        question.save()

        return HttpResponseRedirect("/forum/")
