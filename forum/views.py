from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Question, Comment

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
    
def new_comment(request):
    if request.method == "POST":
        comment = request.POST.get("body")
        author = request.user
        question_id = request.POST.get("question")
        question = Question.objects.get(id=question_id)

        new_comment = Comment(question=question, author=author, body=comment)
        new_comment.save()

        return HttpResponseRedirect("/forum/")
