from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import requests

@require_http_methods(["GET"])
def images_info(request):
    response = requests.get("http://127.0.0.1:6000/images/json")
    table = []
    images_list = {}
    for image in response.json():
        try:
            images_list["RepoTag"] = image["RepoTags"][0].encode("utf-8") 
        except TypeError:
            images_list["RepoTag"] = '{}:none'.format( 
                         image["RepoDigests"][0].encode("utf-8").split("@")[0])

        images_list["Id"] = image["Id"].encode("utf-8")[7:19]
        table.append(images_list)
        images_list = {}

    return JsonResponse(table,safe=False)
