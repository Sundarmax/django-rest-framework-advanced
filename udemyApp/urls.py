from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from rest_framework import routers
from core.views import *



router = routers.DefaultRouter()
router.register(r'customers',CustomerViewset, base_name="customer")
router.register(r'professions',ProfessionViewset)
router.register(r'data-sheets',DatasheetViewset)
router.register(r'documents',DocumentViewset)



urlpatterns = [
    path('api/',include(router.urls)),
    path('admin/', admin.site.urls),
    url(r'^api-auth/',include('rest_framework.urls'))
]
