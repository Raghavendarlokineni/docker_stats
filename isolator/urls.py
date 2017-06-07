from django.conf.urls import url

from . import views, images, containers, network

urlpatterns = [
              url(r'images', images.images_info),
              url(r'containers', containers.active_containers),
              url(r'network', network.network_info), 
              url(r'^$', views.index, name='index'),
              ]


