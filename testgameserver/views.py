# Create your views here.
from django.http import HttpResponse
from django.template.loader import render_to_string


def update(request, **kwargs):

    pass


def view(request, **kwargs):
    return HttpResponse(render_to_string('testgameserverview.html'))


