from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import requests
import json

HEADERS = {"Content-Type" : "application/json", "Accept" : "application/json"}

def network_details():
    response = requests.get("http://127.0.0.1:6000/networks")
    #table = [[Name, Id, Driver, Subnet, Gateway]]
    table = []
    details = {}
    for network in response.json():
        details["Name"] = network["Name"].encode("utf-8")
        details["Id"] = network["Id"].encode("utf-8")[:12]
        details["Driver"] = network["Driver"].encode("utf-8")
        
        ipconfig = network["IPAM"]["Config"]

        if ipconfig.__len__() == 0:
            ipconfig = [{}]
      
        #set subnet and gateway to none if not present, there are cases
        #when only one of them is avilable
        ipconfig[0].setdefault("Subnet", "none")
        ipconfig[0].setdefault("Gateway", "none")
        
        details["Subnet"] = ipconfig[0]["Subnet"] 
        details["Gateway"] = ipconfig[0]["Gateway"]

        table.append(details)
        #intializing to dict to None as scope is outside the for loop as well
        details = {}
    return table 

def create_nw(content):
    response = requests.post("http://127.0.0.1:6000/networks/create", 
                            content, headers = HEADERS )   
    return response.json()

@require_http_methods(["GET", "POST"])
def network_info(request):
    if request.method == "GET":
        return JsonResponse(network_details(), safe=False)
    elif request.method == "POST":
        try:
            response = create_nw(request.body)
            #explicitly looking for Warning or message to know the status
            if "Warning" in response:
                return JsonResponse("Success, Network created with ID: {}".
                                   format(response['Id'].encode('utf-8')[:12]),safe=False)
 	    elif "message" in response:
                return JsonResponse("Error : {}".
                                   format(response.values()[0]),safe=False)
        except ValueError:
	    return JsonResponse("Error : Improper JSON format provided", safe=False)

           
