from django.urls import path, include

from . import views

urlpatterns = [
    path('a', views.index, name='index'),
    path('b', views.influx, name='influx'),
    # path('sb', include('django_sb_admin.urls')),

]