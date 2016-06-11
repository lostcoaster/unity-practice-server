import re
from datetime import datetime, timedelta
from django.utils import timezone
import pytz

from django.shortcuts import render
from django.http.request import HttpRequest
from django.http import JsonResponse, HttpResponse

from hubserver import settings
from shironeko.models import ShironekoGatcha
import mpld3

# Create your views here.


def upload_data(request):
    assert isinstance(request, HttpRequest)

    # upload gatcha results
    tz = pytz.timezone(settings.TIME_ZONE)
    if request.GET:
        counter = 0
        for url, star in zip(request.GET['url'].split(';'), request.GET['star']):
            info = re.match(
                r'(\d{2})(\d{2})-(\d{2})(\d{2})-(\d{2})-(\d{3}).jpg',
                url
            )
            info = [int(d) for d in info.groups()]
            info.insert(0, 2016)
            info[-1] *= 1000
            time = datetime(*info)
            time = tz.localize(time)
            star = int(star)

            if not 0 < star < 5:
                return JsonResponse({'success': False, 'msg': 'Invalid star {}'.format(request.GET['star'])})

            if not ShironekoGatcha.objects.filter(time=time).exists():
                ShironekoGatcha.objects.create(time=time, star=star)
                counter += 1

        return JsonResponse({'success': True, 'added': counter})


def browse(request):
    # setting
    list_interval = timedelta(hours=1)
    cluster_interval = timedelta(seconds=30)
    # select
    now = timezone.now()
    start = now - list_interval
    data = ShironekoGatcha.objects.filter(time__gte=start).order_by('time')
    x = []
    y = []
    if data.exists():
        t = []
        ss = 0
        for d in data:
            if t and d.time-t[-1] >= cluster_interval:
                x.append(t[len(t)//2])
                y.append(ss/len(t))
                t = []
                ss = 0
            t.append(d.time)
            ss += 1 if d.star >= 4 else 0
        else:
            # last record
            if t:
                x.append(t[len(t)//2])
                y.append(ss/len(t))
    else:
        x.append(now)
        y.append(0)

    import matplotlib.pyplot as pyp
    pyp.plot(x, y)
    fig_html = mpld3.fig_to_html(pyp.gcf())

    return render(request, 'view_result.html', context={'fig_html': fig_html})

