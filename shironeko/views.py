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
    if 't' in request.GET:
        list_interval = timedelta(minutes=int(request.GET['t']))
    else:
        list_interval = timedelta(hours=1)
    cluster_interval = timedelta(seconds=30)
    # select
    now = timezone.now()
    tz = timezone.get_current_timezone()
    start = now - list_interval
    data = ShironekoGatcha.objects.filter(time__gte=start).order_by('time')
    x = []
    y = []
    c = []
    if data.exists():
        t = []
        ss = 0
        for d in data:
            if t and d.time-t[-1] >= cluster_interval:
                x.append(t[len(t)//2].astimezone(tz).replace(tzinfo=None))  # ugly workaround as matplotlib sucks
                y.append(ss/len(t))
                c.append(len(t))
                t = []
                ss = 0
            t.append(d.time)
            ss += 1 if d.star >= 4 else 0
        else:
            # last record
            if t:
                x.append(t[len(t)//2].astimezone(tz).replace(tzinfo=None))
                y.append(ss/len(t))
                c.append(len(t))
    else:
        x.extend([start, now])
        y.extend([0, 0])
        c.extend([0, 0])

    # labels
    labels = []
    for i, vx in enumerate(x):
        labels.append('{}-{:.2%} ({})'.format(vx.strftime('%H:%M'), y[i], c[i]))
    s = [20*vc*2 for vc in c]
    import matplotlib.pyplot as pyp
    pyp.switch_backend('Agg')
    fig = pyp.figure(figsize=(12, 7.5))
    fig.gca().plot(x, y)
    points = fig.gca().scatter(x, y, s=s, c='cyan')
    tooltip = mpld3.plugins.PointLabelTooltip(points, labels)
    mpld3.plugins.connect(fig, tooltip)
    fig_html = mpld3.fig_to_html(fig)
    pyp.close(fig)

    return render(request, 'view_result.html', context={'fig_html': fig_html})

