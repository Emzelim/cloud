from django.urls import path, include
from django.conf.urls import url
# import django_sb_admin.views
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='sb_admin_dashboard'),
    path('charts/', views.charts, name='sb_admin_charts'),
    path('tables/', views.tables, name='sb_admin_tables'),
    path('forms/', views.forms, name='sb_admin_forms'),
    path('bootstrap-elements/', views.bootstrap_elements, name='sb_admin_bootstrap_elements'),
    path('bootstrap-grid/', views.bootstrap_grid, name='sb_admin_bootstrap_grid'),
    path('rtl-dashboard/', views.rtl_dashboard, name='sb_admin_rtl_dashboard'),
    path('blank/', views.blank, name='sb_admin_blank'),
    # -- Séparation
    path('', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('administration/', views.administration, name='administration'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('robot/<int:robot_id>/', views.robot, name='robot'),
]
