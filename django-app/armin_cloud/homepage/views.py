from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import ArminRobot
from .utils import get_influxdb_client
import json


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
            "data_hmi": json.dumps(data_hmi),
        }
    else:
        context = {
            "autorisation": False
        }

    return render(request, 'page/robot.html', context)


# ---- SEPARATION

def old_dashboard(request):
    """Dashboard page.
    """
    return render(request, "django_sb_admin/sb_admin_dashboard.html",
                  {"nav_active":"old_dashboard"})


def charts(request):
    """Charts page.
    """
    return render(request, "django_sb_admin/sb_admin_charts.html",
                  {"nav_active":"charts"})


def tables(request):
    """Tables page.
    """
    return render(request, "django_sb_admin/sb_admin_tables.html",
                  {"nav_active":"tables"})


def forms(request):
    """Forms page.
    """
    return render(request, "django_sb_admin/sb_admin_forms.html",
                  {"nav_active":"forms"})


def bootstrap_elements(request):
    """Bootstrap elements page.
    """
    return render(request, "django_sb_admin/sb_admin_bootstrap_elements.html",
                  {"nav_active":"bootstrap_elements"})


def bootstrap_grid(request):
    """Bootstrap grid page.
    """
    return render(request, "django_sb_admin/sb_admin_bootstrap_grid.html",
                  {"nav_active":"bootstrap_grid"})


def dropdown(request):
    """Dropdown  page.
    """
    return render(request, "django_sb_admin/sb_admin_dropdown.html",
                  {"nav_active":"dropdown"})


def rtl_dashboard(request):
    """RTL Dashboard page.
    """
    return render(request, "django_sb_admin/sb_admin_rtl_dashboard.html",
                  {"nav_active":"rtl_dashboard"})


def blank(request):
    """Blank page.
    """
    return render(request, "django_sb_admin/sb_admin_blank.html",
                  {"nav_active":"blank"})