from django.shortcuts import render, render_to_response
from django.http import JsonResponse
import requests
from prettytable import PrettyTable

def container_status(status):
 
    url = "http://127.0.0.1:6000/containers/json?all"

    if status == "all":
       url += "=1"
    elif status == "running":
       pass
    else: raise ValueError("status should be either 'all' or 'running'")

    return requests.get(url)

def active_containers(request):
   
    response = container_status("all")
    #table = [["Container Name", "Container ID", "Status", "IP ADDR"]]
    table = []
    status = {}
    for i in response.json():
        try:
            #fetching the network type as it is the only key available here
            network_details, = i["NetworkSettings"]["Networks"].values()
        except ValueError:
            pass
        status["Name"] = i["Names"][0].encode('utf-8').replace('/', '')
        status["Id"] = i['Id'].encode('utf-8')[:12]
        status["Status"] = i["State"]
        status["IP Addr"] = network_details["IPAddress"]
        
        table.append(status)
        status = {}
    
    #context = {"table" : table}
    #return render(request, "containers.html", context)    
    return JsonResponse(table, safe=False)
