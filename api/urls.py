from django.urls import include, path
from django.contrib import admin
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()

router.register(r'persons', PersonsViewSet, basename="person")
router.register(r'vehicles', VehiclesViewSet, basename="vehicle")
router.register(r'officers', OfficersViewSet, basename="office")
router.register(r'tickets', TicketsViewSet, basename="ticket")
router.register(r'generate_inform', GenerateInformViewSet, basename="generate_inform")

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

# Customization of Django Admin site
admin.site.site_title = "Traffic Tickets System"
admin.site.site_header = "Traffic Tickets System"
admin.site.index_title = "System administration"
