# Create your views here.
from django.http import HttpResponse


def home(request):
    return HttpResponse("You're at the home index.")
