from django.http import JsonResponse
import requests
import sys, pdb

def network_details():
    response = requests.get("http://127.0.0.1:6000/networks")
    #table = [[Name, Id, Driver, Subnet, Gateway]]
    table = []
    details = {}
    for network in response.json():
        details["Name"] = network["Name"].encode("utf-8")
        details["Id"] = network["Id"].encode("utf-8")[:12]
        details["Driver"] = network["Driver"].encode("utf-8")
        
        if network["IPAM"]["Config"].__len__() == 0:

            details["Subnet"] = "none" 
            details["Gateway"] = "none"
        else:
            details["Subnet"] = network["IPAM"]["Config"][0]["Subnet"]
            details["Gateway"] = network["IPAM"]["Config"][0]["Gateway"]
        #pdb.Pdb(stdout=sys.__stdout__).set_trace()
        #pdb.set_trace()
        table.append(details)
        details = {}
    return table 

#def create_network():
    
def network_info(request):
    if request.method == "GET":
        return JsonResponse(network_details(), safe=False)
   
    elif request.method == "POST":
        print("REQUEST POST" ,request.POST)
        return (request.POST.get("network-info", False))
        #create_network()

#
#def network_id(request, network):
#    if request.method == "GET":
           
