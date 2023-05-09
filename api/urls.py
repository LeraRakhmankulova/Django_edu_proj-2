from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import SimpleRouter

from api.views import main_view, TimeslotModelViewSet, TagsViewSet

router = SimpleRouter()
router.register("timeslots", TimeslotModelViewSet, basename='timeslots')
router.register("tags", TagsViewSet, basename='tags')

urlpatterns = [
    path("", main_view),
    path("token/", obtain_auth_token),
    *router.urls
]