from django.urls import path,include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('blog',viewset=views.BlogViewset)

app_name = 'api'

urlpatterns = [
    path('',views.index,name='index'),
    path('api/',include(router.urls)),
]