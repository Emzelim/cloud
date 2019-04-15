from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import ArminRobot
from .utils import get_influxdb_client
import json
from revproxy.views import ProxyView


# Create your views here.
def index(request):
    """Start page with a documentation.
    """
    return render(request, 'page/index.html',
                  {"nav_active": "index"})


@staff_member_required
def administration(request):
    """Administration page
    """
    return render(request, 'page/administration.html',
                  {"nav_active": "administration"})


@login_required
def dashboard(request):
    """Dashboard pour selectionner les robots
    """
    armin_robots = ArminRobot.objects.all()
    users_armin = []
    current_user = request.user

    for armin_robot in armin_robots:
        if armin_robot.armin_of_user_id == current_user.id:
            users_armin.append(armin_robot)

    context = {
        "nav_active": "dashboard",
        "armin_robot": users_armin,
    }

    return render(request, 'page/dashboard.html', context)


@login_required
def robot(request, robot_id):
    """Information sur le robot
    """
    armin_robot = ArminRobot.objects.get(id=robot_id)
    current_user = request.user
    influxdb_client = get_influxdb_client()

    if armin_robot.armin_of_user_id == current_user.id:
        result = influxdb_client.query('select * '
                                       'from local_test7 '
                                       'where "Armin_ID" = '
                                       + str(armin_robot.serial_number) +
                                       ' order by time DESC '
                                       'limit 1;')
        result_r = result[('local_test7', None)]
        data_hmi = json.loads(json.dumps(list(result_r)[-1]))

        context = {
            "autorisation": True,
            "armin_robot": armin_robot,
            "i_HmiOpc_set_nbPartsToDo": data_hmi['plc:i_HmiOpc_set_nbPartsToDo'],
            "i_HmiOpc_get_nbPartsDone": data_hmi['plc:i_HmiOpc_get_nbPartsDone'],
            "current_time": data_hmi['time'],
            "data_hmi": json.dumps(data_hmi),
        }
    else:
        context = {
            "autorisation": False
        }

    return render(request, 'page/robot.html', context)


class GraphanaProxyView(ProxyView):
    upstream = 'http://localhost:8891/dashboard/'

    def get_proxy_request_headers(self, request):
        headers = super(GraphanaProxyView, self).get_proxy_request_headers(request)
        headers['X-WEBAUTH-USER'] = request.user.username
        return headers