from django.shortcuts import render
from django.http.request import HttpRequest
# Create your views here.


def upload_data(request):
    assert isinstance(request, HttpRequest)

    # upload gatcha results
    if request.GET['type'] == 'shironeko_gatcha':

