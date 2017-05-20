from django.http import JsonResponse
import requests

def images_info(request):
    response = requests.get("http://127.0.0.1:6000/images/json")
    images_list = {}
    for i in response.json():
        images_list[i["RepoTags"][0].encode("utf-8")] = i["Id"].encode("utf-8")[7:19]

    return JsonResponse(images_list,safe=False)
