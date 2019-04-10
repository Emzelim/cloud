from django.shortcuts import render
from django.http import HttpResponse
from .utils import *



# def index(request):
#     return HttpResponse("<iframe "
#                         "src='http://localhost:3000/d/DtriK_rmz/host-overview?orgId=1&from=1551701230731&to=155170215"
#                         "0968&var-host=TPad-Mesut-debian&panelId=10&fullscreen' width='1300' height='1000' frameborder='0'>"
#                         "</iframe>")

def index(request):
    return render(request, '../../template/my_template.html')

def influx(request):
    # influxdb_client = InfluxDBClient(host='influxdb', port=8086, database='telegraf')
    influxdb_client = get_influxdb_client()
    # influxdb_client.create_database('wtf')
    # result = influxdb_client.query('select mean(/plc:i_*/) from local_test3;')
    result = influxdb_client.query('select "plc:i_HmiOpc_set_nbPartsToDo" from local_test3;')
    string = result[0]
    return HttpResponse("show plc:i_HmiOpc_set_nbPartsToDo value : {}".format(result))