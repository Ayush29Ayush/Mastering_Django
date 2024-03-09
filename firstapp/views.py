from django.shortcuts import render, HttpResponse


# Create your views here.
def index(request):
    # return HttpResponse("<h1>Hello, Ayush...</h1>")
    return render(request, 'firstapp/index.html')
