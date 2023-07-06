from django.urls import include, path
from rest_framework.routers import SimpleRouter
from users.api.users import RegisterUserBaseAPI, UserBaseAPI

router = SimpleRouter()

router.register('', UserBaseAPI, basename='Users')

urlpatterns = [
    path('register/', RegisterUserBaseAPI.as_view()),
    path('', include(router.urls)),
]
