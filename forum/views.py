from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from .models import Question, Comment

# Create your views here.
def main_forum(request):
    questions = Question.objects.all()
    questions = questions.order_by('-created_at')
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
    
def get_comments(request):
    if request.method == "GET":
        question_id = request.GET.get('question_id')
        question = Question.objects.get(id=question_id)
        comments = Comment.objects.filter(question=question)
        comments_data = list(comments.values('id', 'author__is_staff', 'author__username', 'body', 'created_at'))
        for c in comments_data:
            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(c)
        return JsonResponse({'status': 'success', 'comments': comments_data}, status=200)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
