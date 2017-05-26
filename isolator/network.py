from django.http import JsonResponse, HttpResponse
import requests
import sys
import pdb
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
 
        #to check if dict is Null
        if network["IPAM"]["Config"].__len__() == 0:
            details["Subnet"] = "none" 
            details["Gateway"] = "none"
        else:
            ip_config = network["IPAM"]["Config"][0]

            details["Subnet"] = ip_config["Subnet"]
            details["Gateway"] = ip_config["Gateway"]

        table.append(details)
        #intializing to dict to None as scope if outside the for loop as well
        details = {}
    return table 

def network_info(request):
    if request.method == "GET":
        return JsonResponse(network_details(), safe=False)

def create_nw(content):
    response = requests.post("http://127.0.0.1:6000/networks/create", 
                            content, headers = HEADERS )   
    print(response.status_code) 
    return response.json()

def create_network(request):   
    if request.method == "POST":
        try:
            response = create_nw(request.body)
            print(response)
            if response.status_code != 200:
                return JsonResponse("Error : {}".format(response.values()[0]),safe=False)
        except ValueError:
	    return JsonResponse("Error : Improper JSON format provided" , safe=False)
        
        return JsonResponse("Success", safe=False)

           
