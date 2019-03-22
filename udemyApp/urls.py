from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from core.views import *



router = routers.DefaultRouter()
router.register(r'customers',CustomerViewset, base_name="customer")
router.register(r'professions',ProfessionViewset)
router.register(r'data-sheets',DatasheetViewset)
router.register(r'documents',DocumentViewset)



urlpatterns = [
    path('api/',include(router.urls)),
    path('admin/', admin.site.urls),
    url('api-token-auth/',obtain_auth_token),
    url('api-auth/',include('rest_framework.urls'))
]
