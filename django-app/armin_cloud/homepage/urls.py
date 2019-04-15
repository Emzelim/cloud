from django.urls import path, include
from django.conf.urls import url
# import django_sb_admin.views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('administration/', views.administration, name='administration'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('robot/<int:robot_id>/', views.robot, name='robot'),
    url(r'^grafana/(?P<path>.*)$', views.GraphanaProxyView.as_view(), name='graphana-dashboards'),
]
