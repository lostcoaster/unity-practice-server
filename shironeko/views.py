import re
from datetime import datetime, timedelta

from django.shortcuts import render
from django.http.request import HttpRequest
from django.http import JsonResponse, HttpResponse
from shironeko.models import ShironekoGatcha
import mpld3

# Create your views here.


def upload_data(request):
    assert isinstance(request, HttpRequest)

    # upload gatcha results
    if request.GET['type'] == 'shironeko_gatcha':
        info = re.match(
            r'http://image\.shironeko\.gatyaken\.com/drop/drop345/(\d{2})(\d{2})-(\d{2})(\d{2})-(\d{2})-(\d{3}).jpg',
            request.GET['url']
        )
        info = [int(d) for d in info.groups()]
        info.insert(0, 2016)
        info[-1] *= 1000
        time = datetime(*info)
        star = int(request.GET['star'])

        if not 0 < star < 5:
            return JsonResponse({'success': False, 'msg': 'Invalid star {}'.format(request.GET['star'])})

        if ShironekoGatcha.objects.filter(time=time).exists():
            return JsonResponse({'success': True, 'added': 0})
        else:
            ShironekoGatcha.objects.create(time=time, star=star)
            return JsonResponse({'success': True, 'added': 1})


def browse(request):
    # select
    now = datetime.now()
    start = now - timedelta(hours=1)
    data = ShironekoGatcha.objects.filter(time__gte=start)
    x = []
    y = []
    if data.exists():
        raise NotImplementedError
    else:
        x.append(now)
        y.append(0)

    import matplotlib.pyplot as pyp
    pyp.plot(x, y)
    fig_html = mpld3.fig_to_html(pyp.gcf())

    return render(request, 'view_result.html', context={'fig_html': fig_html})

